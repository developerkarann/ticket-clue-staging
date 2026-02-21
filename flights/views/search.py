
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from home.utils import UniversalAirAPI
from datetime import datetime


# Flight search view
@method_decorator(csrf_exempt, name='dispatch')
class FlightSearchView(View):
    template_name = 'flight-list.html'

    def get(self, request):
        context = {
            "hide_form": True
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Extract query parameters
        origin = request.POST.get('from')
        destination = request.POST.get('to')
        departure_date_str = request.POST.get('departure')
        return_date_str = request.POST.get('return', None)
        travel_class_str = request.POST.get('class', 'Economy')
        adults = request.POST.get('adults', 1)
        children = request.POST.get('children', 0)
        infants = request.POST.get('infants', 0)
        currency = request.POST.get('currency', 'INR')

        # Mapping for travel class types
        class_mapping = {
            "Economy": 1,
            "Premium Economy": 2,
            "Business": 3,
            "First Class": 4
        }
        travel_class = class_mapping.get(travel_class_str, 1)

         # Parse dates
        departure_date = datetime.strptime(departure_date_str, "%d %b %Y").strftime("%Y-%m-%d")
        return_date = None
        if return_date_str:
            return_date = datetime.strptime(return_date_str, "%d %b %Y").strftime("%Y-%m-%d")
        
        if not origin or not destination or not departure_date:
            return render(request, self.template_name, {"error": "Missing required parameters."})

        # Prepare the API request payload
        search_payload = {
            "AdultCount": int(adults or 1),
            "ChildCount": int(children or 0),
            "InfantCount": int(infants or 0),
            "JourneyType": 2 if return_date else 1,  # 1 for one-way, 2 for round trip
            "Sources": None,
            "PreferredAirlines": [],
            "PreferredCurrency": currency,
            "Segments": [
                {
                    "Origin": origin,
                    "Destination": destination,
                    "FlightCabinClass": travel_class,
                    "PreferredDepartureTime": departure_date
                }
            ]
        }

        print(search_payload)

        # Add return segment for round trip
        if return_date:
            search_payload['Segments'].append({
                "Origin": destination,
                "Destination": origin,
                "FlightCabinClass": travel_class,
                "PreferredDepartureTime": return_date
            })

        # Make the request to Travel Boutique API
        api = UniversalAirAPI()
        response = api.search_flights(search_payload, request)
        return JsonResponse({"result": response.get("Response", [])})
    
