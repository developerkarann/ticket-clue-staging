
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import SearchSession, Passenger

@csrf_exempt
def post_passenger_details(request):
    hexId = request.session.get('hex_session')
    if not hexId:
        return JsonResponse({"error": "Session ID not found."})

    if request.method == 'POST':
        # Retrieve the SearchSession by hexId
        try:
            search_session = SearchSession.objects.get(hexid=hexId)
        except SearchSession.DoesNotExist:
            return JsonResponse({"error": "Search session not found."})
        
        if request.user.is_authenticated:
            search_session.user = request.user
            search_session.save() 

        # Parse form data and extract passenger data
        data = request.POST.dict()
        passengers = {}

        # Organize data into a structured format for passengers
        for key, value in data.items():
            if key == 'primaryEmail':
                search_session.email = value
                search_session.save()
            if key == 'primaryContactNumber':
                search_session.primaryContact = value
                search_session.save()

            if key.startswith('passengers'):
                # Example: 'passengers[1-1][title]' -> '1-1', 'title'
                parts = key.split('[')
                index = parts[1].strip(']')
                field = parts[2].strip(']')
                if index not in passengers:
                    passengers[index] = {}
                passengers[index][field] = value
        search_session.passengers.clear()
        # Create and link each Passenger instance to the SearchSession
        for index, passenger_data in passengers.items():
            passenger = Passenger(
                first_name=passenger_data.get('firstName'),
                last_name=passenger_data.get('lastName'),
                title=passenger_data.get('title'),
                country_code=passenger_data.get('country_code'),
                city=passenger_data.get('city'),
                pax_type=int(passenger_data.get('paxType')),
                is_lead_pax = True if index == '1-1' else False,
                # gender=int(passenger_data.get('gender')) if passenger_data.get('gender') else None,
                date_of_birth=(
                    datetime.strptime(passenger_data['dateOfBirth'], '%Y-%m-%d').date()
                    if passenger_data.get('dateOfBirth') else None
                ),
                passport_no=passenger_data.get('passportNo'),
                passport_expiry=(
                    datetime.strptime(passenger_data['passportExpiry'], '%Y-%m-%d').date()
                    if passenger_data.get('passportExpiry') else None
                ),
                passport_issue=(
                    datetime.strptime(passenger_data['passportIssue'], '%Y-%m-%d').date()
                    if passenger_data.get('passportIssue') else None
                ),
                address_line1=passenger_data.get('addressLine1'),
            )
            passenger.save()
            search_session.passengers.add(passenger)

        return JsonResponse({
            "hexId": hexId,
            "message": "Passenger details saved successfully.",
            "passengers": list(passengers.keys())  
        })

    return JsonResponse({"error": "Invalid request method."})
