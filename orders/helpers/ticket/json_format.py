class TicketJsonFormater:

    @staticmethod
    def passenger_details(data, email, contact_number, gst_details=None):
        if data.title == 'Mr' and data.pax_type == 3:
            title = 'Mstr'
        else:
            title = data.title

        passenger = {
            "Title": title,
            "FirstName": data.first_name or '',
            "LastName": data.last_name or '',
            "PaxType": data.pax_type or '',
            "Gender": 1 if data.title == 'Mr' else 2,
            "AddressLine1": data.address_line1 or '',
            "CountryCode": data.country_code or '',
            "ContactNo": contact_number or '',
            "Email": email or '',
            "Fare": {},
        }

        if data.date_of_birth is not None:
            passenger["DateOfBirth"] = data.date_of_birth.strftime('%Y-%m-%dT%H:%M:%S')

        if data.city is not None:
            passenger["City"] = data.city

        if gst_details is not None:
            if gst_details.gst_company_address is not None:
                passenger["GSTCompanyAddress"] = gst_details.gst_company_address
            if gst_details.gst_company_contact_number is not None:
                passenger["GSTCompanyContactNumber"] = gst_details.gst_company_contact_number
            if gst_details.gst_company_name is not None:
                passenger["GSTCompanyName"] = gst_details.gst_company_name
            if gst_details.gst_number is not None:
                passenger["GSTNumber"] = gst_details.gst_number
            if gst_details.gst_company_email is not None:
                passenger["GSTCompanyEmail"] = gst_details.gst_company_email

        if data.is_lead_pax is not None:
            passenger["IsLeadPax"] = data.is_lead_pax

        # Passport details
        if data.passport_no is not None:
            passenger["PassportNo"] = data.passport_no
        if data.passport_expiry is not None:
            passenger["PassportExpiry"] = data.passport_expiry.strftime('%Y-%m-%dT%H:%M:%S')
        if data.passport_issue is not None:
            passenger["PassportIssueDate"] = data.passport_issue.strftime('%Y-%m-%dT%H:%M:%S')

        if data.fare is not None:
            fare = data.fare
            passenger["Fare"] = {
                "BaseFare": float(fare.BaseFare) if fare.BaseFare else 0.0,
                "Tax": float(fare.Tax) if fare.Tax else 0.0,
                "YQTax": float(fare.YQTax) if fare.YQTax else 0.0,
                "AdditionalTxnFeePub": float(fare.AdditionalTxnFeePub) if fare.AdditionalTxnFeePub else 0.0,
                "AdditionalTxnFeeOfrd": float(fare.AdditionalTxnFeeOfrd) if fare.AdditionalTxnFeeOfrd else 0.0,
                "OtherCharges": float(fare.OtherCharges) if fare.OtherCharges else 0.0
            }
        
        # if data.meal_preference is not None:
        #     meal = data.meal_preference
        #     passenger["MealDynamic"] = [
        #        {
        #             "AirlineCode": meal.AirlineCode,
        #             "FlightNumber": meal.FlightNumber,
        #             "WayType": meal.WayType,
        #             "Code": meal.Code,
        #             "Description": meal.Description,
        #             "AirlineDescription": meal.AirlineDescription,
        #             "Quantity": meal.Quantity,
        #             "Currency": meal.Currency,
        #             "Price": float(meal.Price) if meal.Price is not None else None,
        #             "Origin": meal.Origin,
        #             "Destination": meal.Destination,
        #         }
        #     ]

        if data.seat_preference is not None:
            seat = data.seat_preference
            passenger["SeatDynamic"] = [
                {
                    "AirlineCode": seat.AirlineCode,
                    "FlightNumber": seat.FlightNumber,
                    "CraftType": seat.CraftType,
                    "Origin": seat.Origin,
                    "Destination": seat.Destination,
                    "AvailablityType": seat.AvailablityType,
                    "Description": seat.Description,
                    "Code": seat.Code,
                    "RowNo": seat.RowNo,
                    "SeatNo": seat.SeatNo,
                    "SeatType": seat.SeatType,
                    "SeatWayType": seat.SeatWayType,
                    "Compartment": seat.Compartment,
                    "Deck": seat.Deck,
                    "Currency": seat.Currency,
                    "Price": float(seat.Price) if seat.Price is not None else None,
                }
            ]
        
        # if data.baggage_preference is not None:
        #     baggage = data.baggage_preference
        #     passenger["Baggage"] = [
        #        {
        #             "AirlineCode": baggage.AirlineCode,
        #             "FlightNumber": baggage.FlightNumber,
        #             "WayType": baggage.WayType,
        #             "Code": baggage.Code,
        #             "Description": baggage.Description,
        #             "Weight": baggage.Weight,
        #             "Currency": baggage.Currency,
        #             "Price": float(baggage.Price) if baggage.Price is not None else None,
        #             "Origin": baggage.Origin,
        #             "Destination": baggage.Destination
        #         }
        #     ]
        

        return passenger

    @staticmethod
    def ticket_request(trace_id, result_index, passengers, email, contact_number):
        ticketRequest = {
            "TraceId": trace_id,
            "ResultIndex": result_index,
            "Passengers": []
        }

        for passenger in passengers:
            ticketRequest["Passengers"].append(
                TicketJsonFormater.passenger_details(passenger, email, contact_number)
            )

        print("\n\n\nTicket lcc Request:", ticketRequest, "\n\n\n")
        return ticketRequest

