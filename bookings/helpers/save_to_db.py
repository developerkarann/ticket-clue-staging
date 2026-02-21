
import datetime
from django.utils import timezone
from bookings.models import (
    Bookings,
    FlightItinerary,
    Fare,
    Passenger as BookingPassenger,
    Segment,
    FareRule,
    Invoice,
)

def save_flight_response_to_db(response_data: dict, searchSession, user=None) -> Bookings:
    """
    Parse the API response JSON and save it into the corresponding Django models.
    Returns the created/updated FlightApiResponse object.
    """
    # -------------------------
    # 1. Parse top-level fields
    # -------------------------
    response_status = response_data["Response"].get("ResponseStatus", 0)
    trace_id = response_data["Response"].get("TraceId", "")

    # -------------------------
    # 2. Flight Itinerary data
    # -------------------------
    itinerary_data = response_data["Response"].get("FlightItinerary", {})

    # (a) Create main Fare object
    fare_data = itinerary_data.get("Fare", {})
    fare_obj = Fare.objects.create(
        currency=fare_data.get("Currency", ""),
        base_fare=fare_data.get("BaseFare", 0),
        tax=fare_data.get("Tax", 0),
        yq_tax=fare_data.get("YQTax", 0),
        additional_txn_fee_ofrd=fare_data.get("AdditionalTxnFeeOfrd", 0),
        additional_txn_fee_pub=fare_data.get("AdditionalTxnFeePub", 0),
        pg_charge=fare_data.get("PGCharge", 0),
        other_charges=fare_data.get("OtherCharges", 0),
        discount=fare_data.get("Discount", 0),
        published_fare=fare_data.get("PublishedFare", 0),
        commission_earned=fare_data.get("CommissionEarned", 0),
        plb_earned=fare_data.get("PLBEarned", 0),
        incentive_earned=fare_data.get("IncentiveEarned", 0),
        offered_fare=fare_data.get("OfferedFare", 0),
        tds_on_commission=fare_data.get("TdsOnCommission", 0),
        tds_on_plb=fare_data.get("TdsOnPLB", 0),
        tds_on_incentive=fare_data.get("TdsOnIncentive", 0),
        service_fee=fare_data.get("ServiceFee", 0),
        total_baggage_charges=fare_data.get("TotalBaggageCharges", 0),
        total_meal_charges=fare_data.get("TotalMealCharges", 0),
        total_seat_charges=fare_data.get("TotalSeatCharges", 0),
        total_special_service_charges=fare_data.get("TotalSpecialServiceCharges", 0),
    )

    # (b) Create flight itinerary
    flight_itinerary = FlightItinerary.objects.create(
        agent_remarks=itinerary_data.get("AgentRemarks", ""),
        is_auto_reissuance_allowed=itinerary_data.get("IsAutoReissuanceAllowed", False),
        issuance_pcc=itinerary_data.get("IssuancePcc", ""),
        journey_type=itinerary_data.get("JourneyType", 0),
        search_combination_type=itinerary_data.get("SearchCombinationType", 0),
        trip_indicator=itinerary_data.get("TripIndicator", 0),
        booking_allowed_for_roamer=itinerary_data.get("BookingAllowedForRoamer", False),
        booking_id=itinerary_data.get("BookingId", 0),
        is_coupon_applicable=itinerary_data.get("IsCouponAppilcable", False),
        is_manual=itinerary_data.get("IsManual", False),
        pnr=itinerary_data.get("PNR", ""),
        is_domestic=itinerary_data.get("IsDomestic", False),
        result_fare_type=itinerary_data.get("ResultFareType", ""),
        source=itinerary_data.get("Source", 0),
        origin=itinerary_data.get("Origin", ""),
        destination=itinerary_data.get("Destination", ""),
        airline_code=itinerary_data.get("AirlineCode", ""),
        last_ticket_date=(
            itinerary_data.get("LastTicketDate", None)
            if itinerary_data.get("LastTicketDate", None)
            else None
        ),
        validating_airline_code=itinerary_data.get("ValidatingAirlineCode", ""),
        airline_remark=itinerary_data.get("AirlineRemark", ""),
        airline_toll_free_no=itinerary_data.get("AirlineTollFreeNo", ""),
        is_lcc=itinerary_data.get("IsLCC", False),
        non_refundable=itinerary_data.get("NonRefundable", False),
        fare_type=itinerary_data.get("FareType", ""),
        credit_note_no=itinerary_data.get("CreditNoteNo", None),
        fare=fare_obj,
        status=itinerary_data.get("Status", 0),
        invoice_amount=itinerary_data.get("InvoiceAmount", 0),
        invoice_no=itinerary_data.get("InvoiceNo", ""),
        invoice_status=itinerary_data.get("InvoiceStatus", 0),
        invoice_created_on=(
            itinerary_data.get("InvoiceCreatedOn", None)
            if itinerary_data.get("InvoiceCreatedOn", None)
            else None
        ),
        remarks=itinerary_data.get("Remarks", ""),
        is_web_check_in_allowed=itinerary_data.get("IsWebCheckInAllowed", False),
    )

    # (c) Passengers
    passenger_list = itinerary_data.get("Passenger", [])
    for p in passenger_list:
        p_fare_data = p.get("Fare", {})
        passenger_fare_obj = Fare.objects.create(
            currency=p_fare_data.get("Currency", ""),
            base_fare=p_fare_data.get("BaseFare", 0),
            tax=p_fare_data.get("Tax", 0),
            yq_tax=p_fare_data.get("YQTax", 0),
            additional_txn_fee_ofrd=p_fare_data.get("AdditionalTxnFeeOfrd", 0),
            additional_txn_fee_pub=p_fare_data.get("AdditionalTxnFeePub", 0),
            pg_charge=p_fare_data.get("PGCharge", 0),
            other_charges=p_fare_data.get("OtherCharges", 0),
            discount=p_fare_data.get("Discount", 0),
            published_fare=p_fare_data.get("PublishedFare", 0),
            commission_earned=p_fare_data.get("CommissionEarned", 0),
            plb_earned=p_fare_data.get("PLBEarned", 0),
            incentive_earned=p_fare_data.get("IncentiveEarned", 0),
            offered_fare=p_fare_data.get("OfferedFare", 0),
            tds_on_commission=p_fare_data.get("TdsOnCommission", 0),
            tds_on_plb=p_fare_data.get("TdsOnPLB", 0),
            tds_on_incentive=p_fare_data.get("TdsOnIncentive", 0),
            service_fee=p_fare_data.get("ServiceFee", 0),
            total_baggage_charges=p_fare_data.get("TotalBaggageCharges", 0),
            total_meal_charges=p_fare_data.get("TotalMealCharges", 0),
            total_seat_charges=p_fare_data.get("TotalSeatCharges", 0),
            total_special_service_charges=p_fare_data.get("TotalSpecialServiceCharges", 0),
        )

        dob_str = p.get("DateOfBirth", None)
        date_of_birth = timezone.now()
        if dob_str:
            try:
                # Example: "2000-01-12T00:00:00"
                date_of_birth = datetime.datetime.fromisoformat(dob_str.replace("Z", ""))
            except Exception:
                pass

        passenger_obj = BookingPassenger.objects.create(
            pax_id=p.get("PaxId", 0),
            title=p.get("Title", ""),
            first_name=p.get("FirstName", ""),
            last_name=p.get("LastName", ""),
            pax_type=p.get("PaxType", 0),
            date_of_birth=date_of_birth,
            gender=p.get("Gender", 0),
            is_lead_pax=p.get("IsLeadPax", False),
            contact_no=p.get("ContactNo", ""),
            email=p.get("Email", ""),
            address_line1=p.get("AddressLine1", ""),
            city=p.get("City", ""),
            country_code=p.get("CountryCode", ""),
            nationality=p.get("Nationality", ""),
            pan=p.get("PAN", ""),
            passport_no=p.get("PassportNo", ""),
            fare=passenger_fare_obj
        )
        # Add passenger to the flight itinerary
        flight_itinerary.passengers.add(passenger_obj)

    # (d) Segments
    segments_list = itinerary_data.get("Segments", [])
    for seg in segments_list:
        origin_obj = seg.get("Origin", {})
        origin_airport = origin_obj.get("Airport", {})
        destination_obj = seg.get("Destination", {})
        destination_airport = destination_obj.get("Airport", {})

        dep_time_str = origin_obj.get("DepTime", None)
        arr_time_str = destination_obj.get("ArrTime", None)

        dep_time = None
        arr_time = None
        try:
            dep_time = datetime.datetime.fromisoformat(dep_time_str)
        except:
            pass
        try:
            arr_time = datetime.datetime.fromisoformat(arr_time_str)
        except:
            pass

        airline_data = seg.get("Airline", {})

        segment_obj = Segment.objects.create(
            baggage=seg.get("Baggage"),
            cabin_baggage=seg.get("CabinBaggage"),
            cabin_class=seg.get("CabinClass", 0),
            trip_indicator=seg.get("TripIndicator", 0),
            segment_indicator=seg.get("SegmentIndicator", 0),
            airline_code=airline_data.get("AirlineCode", ""),
            airline_name=airline_data.get("AirlineName", ""),
            flight_number=airline_data.get("FlightNumber", ""),
            fare_class=airline_data.get("FareClass", ""),
            operating_carrier=airline_data.get("OperatingCarrier", ""),
            airline_pnr=seg.get("AirlinePNR", ""),
            origin_airport_code=origin_airport.get("AirportCode", ""),
            origin_airport_name=origin_airport.get("AirportName", ""),
            origin_terminal=origin_airport.get("Terminal", ""),
            origin_city_code=origin_airport.get("CityCode", ""),
            origin_city_name=origin_airport.get("CityName", ""),
            origin_country_code=origin_airport.get("CountryCode", ""),
            origin_country_name=origin_airport.get("CountryName", ""),
            dep_time=dep_time,
            dest_airport_code=destination_airport.get("AirportCode", ""),
            dest_airport_name=destination_airport.get("AirportName", ""),
            dest_terminal=destination_airport.get("Terminal", ""),
            dest_city_code=destination_airport.get("CityCode", ""),
            dest_city_name=destination_airport.get("CityName", ""),
            dest_country_code=destination_airport.get("CountryCode", ""),
            dest_country_name=destination_airport.get("CountryName", ""),
            arr_time=arr_time,
            duration=seg.get("Duration", 0),
            ground_time=seg.get("GroundTime", 0),
            mile=seg.get("Mile", 0),
            stop_over=seg.get("StopOver", False),
            craft=seg.get("Craft", ""),
            remark=seg.get("Remark", ""),
            flight_status=seg.get("FlightStatus", ""),
            status=seg.get("Status", ""),
        )
        flight_itinerary.segments.add(segment_obj)

    # (e) Fare Rules
    fare_rules_list = itinerary_data.get("FareRules", [])
    for fr in fare_rules_list:
        fare_rule_obj = FareRule.objects.create(
            origin=fr.get("Origin", ""),
            destination=fr.get("Destination", ""),
            airline=fr.get("Airline", ""),
            fare_basis_code=fr.get("FareBasisCode", ""),
            fare_rule_detail=fr.get("FareRuleDetail", ""),
        )
        flight_itinerary.fare_rules.add(fare_rule_obj)

    # (f) Invoices
    invoice_list = itinerary_data.get("Invoice", [])
    for inv in invoice_list:
        inv_obj = Invoice.objects.create(
            invoice_id=inv.get("InvoiceId", 0),
            invoice_no=inv.get("InvoiceNo", ""),
            invoice_amount=inv.get("InvoiceAmount", 0),
            invoice_status=inv.get("InvoiceStatus", 0),
            invoice_created_on=(
                inv.get("InvoiceCreatedOn", timezone.now())
            ),
            remarks=inv.get("Remarks", ""),
        )
        flight_itinerary.invoices.add(inv_obj)

    # Finally, create the main FlightApiResponse
    api_response_obj = Bookings.objects.create(
        user=user,
        search_session=searchSession,
        response_status=response_status,
        trace_id=trace_id,
        flight_itinerary=flight_itinerary
    )

    return api_response_obj

