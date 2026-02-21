
import json
import logging
from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import *

logger = logging.getLogger(__name__)

@csrf_exempt
def book_flight(request):
    """
    Handles flight booking by processing selected meals, baggage, and seats,
    associating them with the appropriate passengers, and assigning Fare objects
    to each passenger based on passenger type.
    """
    hexId = request.session.get('hex_session')
    if not hexId:
        return JsonResponse({"error": "Session ID not found."}, status=400)

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

    try:
        selected_seats = json.loads(request.POST.get('selectedSeats', '{}'))
        selected_baggage = json.loads(request.POST.get('selectedBaggage', '{}'))
        selected_meals = json.loads(request.POST.get('selectedMeals', '{}'))
        fare_breakdown = json.loads(request.POST.get('fare', '[]'))  # It's a list
        is_lcc = request.POST.get('isLcc', 'false').lower() == 'true'

        print(fare_breakdown)

        logger.debug("Selected Baggage: %s", selected_baggage)
        logger.debug("Selected Meals: %s", selected_meals)
        logger.debug("Selected Seats: %s", selected_seats)
        logger.debug("Fare Breakdown: %s", fare_breakdown)

        errors = []
        passenger_ids = set()

        # -------------------------------------------------
        # Helper function: Extract passenger IDs
        # -------------------------------------------------
        def extract_passenger_ids(data, category, nested=False):
            """
            Extracts passenger IDs from the provided data.
            Handles both flat and nested structures.
            """
            if nested:
                for outer_key, group in data.items():
                    if isinstance(group, dict):
                        for inner_key, entry in group.items():
                            if isinstance(entry, dict):
                                passenger_info = entry.get('passenger', {})
                                passenger_id = passenger_info.get('id')
                                if passenger_id is not None:
                                    passenger_ids.add(passenger_id)
                                else:
                                    msg = (f"Passenger ID missing in {category} "
                                           f"entry '{outer_key}.{inner_key}'.")
                                    errors.append(msg)
                                    logger.error(msg)
                    else:
                        msg = (f"Invalid structure in {category} "
                               f"entry '{outer_key}', expected a dictionary.")
                        errors.append(msg)
                        logger.error(msg)
            else:
                for key, entry in data.items():
                    if isinstance(entry, dict):
                        passenger_info = entry.get('passenger', {})
                        passenger_id = passenger_info.get('id')
                        if passenger_id is not None:
                            passenger_ids.add(passenger_id)
                        else:
                            msg = f"Passenger ID missing in {category} entry '{key}'."
                            errors.append(msg)
                            logger.error(msg)
                    else:
                        msg = (f"Invalid structure in {category} entry '{key}', "
                               f"expected a dictionary.")
                        errors.append(msg)
                        logger.error(msg)

        # -------------------------------------------------
        # Extract passenger IDs from input
        # -------------------------------------------------
        extract_passenger_ids(selected_meals, 'meal', nested=False)
        extract_passenger_ids(selected_baggage, 'baggage', nested=True)
        extract_passenger_ids(selected_seats, 'seat', nested=True)

        if not passenger_ids:
            return JsonResponse({'error': 'No passenger IDs found in the data.', 'details': errors}, status=400)

        # -------------------------------------------------
        # Fetch Passengers in bulk
        # -------------------------------------------------
        passengers = Passenger.objects.filter(id__in=passenger_ids)
        passenger_map = {p.id: p for p in passengers}

        missing_passengers = passenger_ids - passenger_map.keys()
        if missing_passengers:
            msg = f"Passengers with IDs {missing_passengers} not found."
            errors.append(msg)
            logger.error(msg)
            return JsonResponse({'error': 'Some passengers were not found.', 'details': errors}, status=404)

        # -------------------------------------------------
        # Begin transaction
        # -------------------------------------------------
        with transaction.atomic():
            # ---------------------------------------------
            # 1) Process Meals (flat structure)
            # ---------------------------------------------
            for meal_key, meal_data in selected_meals.items():
                passenger_info = meal_data.get('passenger', {})
                passenger_id = passenger_info.get('id')
                if passenger_id is None:
                    # Already logged
                    continue

                passenger = passenger_map.get(passenger_id)
                if not passenger:
                    # Already handled as missing
                    continue

                # Clear old meal prefs
                passenger.meal_preference = None

                try:
                    meal = Meal.objects.create(
                        AirlineCode=meal_data.get('airlineCode'),
                        FlightNumber=str(meal_data.get('flightNumber')),
                        WayType=meal_data.get('wayType'),
                        Code=meal_data.get('code'),
                        Description=meal_data.get('description'),
                        Quantity=meal_data.get('quantity'),
                        Currency=meal_data.get('currency'),
                        Price=meal_data.get('price'),
                        Origin=meal_data.get('origin'),
                        Destination=meal_data.get('destination'),
                        AirlineDescription=meal_data.get('description')
                    )
                    passenger.meal_preference =meal
                except Exception as e:
                    msg = f"Error creating meal entry '{meal_key}': {e}"
                    errors.append(msg)
                    logger.error(msg)

            # ---------------------------------------------
            # 2) Process Baggage (nested structure)
            # ---------------------------------------------
            for baggage_key, baggage_group in selected_baggage.items():
                if not isinstance(baggage_group, dict):
                    # Invalid structure already logged
                    continue

                for inner_key, baggage_data in baggage_group.items():
                    passenger_info = baggage_data.get('passenger', {})
                    passenger_id = passenger_info.get('id')
                    if passenger_id is None:
                        # Already logged
                        continue

                    passenger = passenger_map.get(passenger_id)
                    if not passenger:
                        # Already handled as missing
                        continue

                    # Clear old baggage prefs
                    passenger.baggage_preference = None

                    try:
                        baggage = Baggage.objects.create(
                            AirlineCode=baggage_data.get('AirlineCode'),
                            FlightNumber=str(baggage_data.get('FlightNumber')),
                            WayType=baggage_data.get('WayType'),
                            Code=baggage_data.get('Code'),
                            Description=baggage_data.get('Description'),
                            Weight=baggage_data.get('Weight'),
                            Currency=baggage_data.get('Currency'),
                            Price=baggage_data.get('Price'),
                            Origin=baggage_data.get('Origin'),
                            Destination=baggage_data.get('Destination')
                        )
                        passenger.baggage_preference =baggage
                    except Exception as e:
                        msg = (f"Error creating baggage entry "
                               f"'{baggage_key}.{inner_key}': {e}")
                        errors.append(msg)
                        logger.error(msg)

            # ---------------------------------------------
            # 3) Process Seats (nested structure)
            # ---------------------------------------------
            for seat_key, seat_group in selected_seats.items():
                if not isinstance(seat_group, dict):
                    # Invalid structure already logged
                    continue

                for inner_key, seat_data in seat_group.items():
                    passenger_info = seat_data.get('passenger', {})
                    passenger_id = passenger_info.get('id')
                    if passenger_id is None:
                        # Already logged
                        continue

                    passenger = passenger_map.get(passenger_id)
                    if not passenger:
                        # Already handled as missing
                        continue

                    # Clear old seat prefs
                    passenger.seat_preference = None

                    try:
                        seat = Seat.objects.create(
                            AirlineCode=seat_data.get('AirlineCode'),
                            FlightNumber=str(seat_data.get('FlightNumber')),
                            CraftType=seat_data.get('CraftType'),
                            Origin=seat_data.get('Origin'),
                            Destination=seat_data.get('Destination'),
                            AvailablityType=seat_data.get('AvailablityType'),
                            Description=seat_data.get('Description'),
                            Code=seat_data.get('Code'),
                            RowNo=str(seat_data.get('RowNo')),
                            SeatNo=seat_data.get('SeatNo') or seat_data.get('seatNumber'),
                            SeatType=seat_data.get('SeatType'),
                            SeatWayType=seat_data.get('SeatWayType'),
                            Compartment=seat_data.get('Compartment'),
                            Deck=seat_data.get('Deck'),
                            Currency=seat_data.get('Currency'),
                            Price=seat_data.get('Price')
                        )
                        passenger.seat_preference = seat
                    except Exception as e:
                        msg = f"Error creating seat entry '{seat_key}.{inner_key}': {e}"
                        errors.append(msg)
                        logger.error(msg)

            # ---------------------------------------------
            # 4) Assign Fare to Passengers
            # ---------------------------------------------
            # The fare_breakdown is a list of dicts, each containing:
            # {
            #   "Currency": "INR",
            #   "PassengerType": 1,   <--- matches pax_type in Passenger
            #   "PassengerCount": 2,
            #   "BaseFare": 10800,
            #   "Tax": 2256,
            #   ...
            # }
            #
            # We divide amounts by 'PassengerCount' to get per-passenger amounts.


            all_passengers = list(passenger_map.values())

            for fare_item in fare_breakdown:
                if not isinstance(fare_item, dict):
                    print(f"Skipping invalid fare_item: {fare_item}")
                    continue

                p_type = fare_item.get('PassengerType')  # e.g. 1, 2, 3
                p_count = fare_item.get('PassengerCount', 1) or 1

                # Filter passengers by this fare's passenger type
                matching_passengers = [
                    p for p in all_passengers
                    if p.pax_type == p_type
                ]

                # If mismatch between passenger_count in data vs actual count
                if len(matching_passengers) != p_count:
                    msg = (f"Warning: Fare item expects {p_count} passenger(s) "
                           f"of type {p_type}, but found {len(matching_passengers)}.")
                    logger.warning(msg)
                    # You can decide whether to treat this as an error or not.

                # Helper for dividing values
                def safe_div(key):
                    return Decimal(fare_item.get(key, 0)) / Decimal(p_count)

                # Create & assign a Fare object to each passenger of that type
                for passenger in matching_passengers:
                    try:
                        fare_obj = Fare.objects.create(
                            Currency=fare_item.get('Currency'),
                            BaseFare=safe_div('BaseFare'),
                            Tax=safe_div('Tax'),
                            YQTax=safe_div('YQTax'),
                            AdditionalTxnFeeOfrd=safe_div('AdditionalTxnFeeOfrd'),
                            AdditionalTxnFeePub=safe_div('AdditionalTxnFeePub'),
                            OtherCharges=safe_div('OtherCharges'),  # Adjust if needed
                            Discount=safe_div('Discount'),
                            PublishedFare=safe_div('PublishedFare'),
                            OfferedFare=safe_div('OfferedFare'),
                            TdsOnCommission=safe_div('TdsOnCommission'),
                            TdsOnPLB=safe_div('TdsOnPLB'),
                            TdsOnIncentive=safe_div('TdsOnIncentive'),
                            ServiceFee=safe_div('ServiceFee'),
                            transaction_fee=safe_div('transaction_fee'),
                            air_trans_fee=safe_div('air_trans_fee')
                        )
                        # Assign this fare to the passenger
                        passenger.fare = fare_obj
                        passenger.save()
                    except Exception as e:
                        msg = (f"Error creating Fare for passenger={passenger.id} "
                               f"(pax_type={p_type}): {e}")
                        errors.append(msg)
                        logger.error(msg)

            search_session = SearchSession.objects.get(hexid=hexId)
            search_session.isLcc = is_lcc
            search_session.save()
        # End of transaction

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------
        if errors:
            return JsonResponse({'status': 'partial_success', 'details': errors}, status=207)
        else:
            return JsonResponse({
                'status': 'success',
                "hex_session": hexId,
                'message': 'Data processed successfully'
            })

    except json.JSONDecodeError:
        logger.error("JSON decode error.")
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        logger.exception("Unexpected error occurred.")
        return JsonResponse(
            {'error': 'An unexpected error occurred while processing your request.'},
            status=500
        )
 