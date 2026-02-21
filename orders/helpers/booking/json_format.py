class BookingJsonFormater:

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
            "Gender": data.gender or '',
            "AddressLine1": data.address_line1 or '',
            "CountryCode": data.country_code or '',
            # "CountryName": data.country_name or '',
            "ContactNo": contact_number or '',
            "Email": email or '',
            "Fare": {},
        }

        if data.date_of_birth is not None:
            passenger["DateOfBirth"] = data.date_of_birth.strftime('%Y-%m-%dT%H:%M:%S')

        # Add optional GST fields if they exist
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
                "Currency": str(fare.Currency) if fare.Currency else 'INR',
                "BaseFare": float(fare.BaseFare) if fare.BaseFare else 0.0,
                "Tax": float(fare.Tax) if fare.Tax else 0.0,
                "YQTax": float(fare.YQTax) if fare.YQTax else 0.0,
                "AdditionalTxnFeePub": float(fare.AdditionalTxnFeePub) if fare.AdditionalTxnFeePub else 0.0,
                "AdditionalTxnFeeOfrd": float(fare.AdditionalTxnFeeOfrd) if fare.AdditionalTxnFeeOfrd else 0.0,
                "OtherCharges": float(fare.OtherCharges) if fare.OtherCharges else 0.0,
                "Discount": float(fare.Discount) if fare.Discount else 0.0,
                "PublishedFare": float(fare.PublishedFare) if fare.PublishedFare else 0.0,
                "OfferedFare": float(fare.OfferedFare) if fare.OfferedFare else 0.0,
                "TdsOnCommission": float(fare.TdsOnCommission) if fare.TdsOnCommission else 0.0,
                "TdsOnPLB": float(fare.TdsOnPLB) if fare.TdsOnPLB else 0.0,
                "TdsOnIncentive": float(fare.TdsOnIncentive) if fare.TdsOnIncentive else 0.0,
                "ServiceFee": float(fare.ServiceFee) if fare.ServiceFee else 0.0,
            }

        return passenger

    @staticmethod
    def booking_request(trace_id, result_index, passengers, email, contact_number):
        bookRequest = {
            "TraceId": trace_id,
            "ResultIndex": result_index,
            "Passengers": []
        }

        for passenger in passengers:
            bookRequest["Passengers"].append(
                BookingJsonFormater.passenger_details(passenger, email, contact_number)
            )

        print("Booking Request:", bookRequest)
        return bookRequest

