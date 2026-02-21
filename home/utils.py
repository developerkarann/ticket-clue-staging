import requests
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from requests.exceptions import RequestException
from ipware import get_client_ip

class UniversalAirAPI:
    def __init__(self):
        self.base_url = settings.UNIVERSAL_AIR_API_BASE_URL
        self.book_url = settings.UNIVERSAL_AIR_API_BOOK_URL

    def _handle_response(self, response):
        try:
            response.raise_for_status()

            # print('\n\n******************************************\n\n')
            # print(response.json())
            # print('\n\n******************************************\n\n')
            # Use logging here instead of print statements in production
            return response.json()
        except json.JSONDecodeError:
            print('\n\n******************************************\n\n')
            print(response.json())
            print('\n\n******************************************\n\n')
            return {"error": "Invalid response format from API"}
        except RequestException:
            print('\n\n******************************************\n\n')
            print(response.json())
            print('\n\n******************************************\n\n')
            return {"error": "Request failed"}

    def make_request(self, endpoint, payload, request, url=None):
        client_ip, _ = get_client_ip(request)
        if not client_ip:
            client_ip = "127.0.0.1"
        
        # Build the full URL based on whether a specific URL is passed.
        full_url = f"{(url or self.base_url)}{endpoint}"
        
        headers = {
            'Content-Type': 'application/json',
        }
        # Always retrieve the current token.
        payload['TokenId'] = TravelBoutiqueAuth.get_token()
        payload['EndUserIp'] = client_ip

        try:
            response = requests.post(full_url, headers=headers, json=payload)
            return self._handle_response(response)
        except RequestException as e:
            # Consider replacing print with a logging call
            print("Error making request:", e)
            return {"error": "Request failed"}

    def search_flights(self, search_params, request):
        return self.make_request('Search', search_params, request, url=self.base_url)

    def get_fare_rule(self, fare_rule_params, request):
        return self.make_request('FareRule', fare_rule_params, request, url=self.base_url)

    def get_fare_quote(self, fare_quote_params, request):
        return self.make_request('FareQuote', fare_quote_params, request, url=self.base_url)

    def get_ssr(self, ssr_params, request):
        return self.make_request('SSR', ssr_params, request, url=self.base_url)

    def book_flight(self, book_params, request):
        return self.make_request('Book', book_params, request, url=self.book_url)

    def ticket_flight(self, ticket_params, request):
        return self.make_request('Ticket', ticket_params, request, url=self.book_url)

    def get_booking_details(self, booking_details_params, request):
        return self.make_request('GetBookingDetails', booking_details_params, request, url=self.book_url)
    
    # Additional methods can be added as needed.

class TravelBoutiqueAuth:
    AUTH_URL = settings.UNIVERSAL_AIR_API_AUTH_URL

    @staticmethod
    def get_token():
        token_info = cache.get("tbo_token")
        print('\n\n******************************************\n\n')
        print(token_info)
        print('\n\n******************************************\n\n')
        now = datetime.now()

        if token_info:
            token = token_info.get("token")
            expiry = token_info.get("expiry")
            if token and expiry and now < expiry:
                return token

        # Request a new token if none exists or if it has expired
        try:
            payload = {
                "ClientId": settings.TRAVEL_BOUTIQUE_CLIENT_ID,
                "UserName": settings.TRAVEL_BOUTIQUE_USERNAME,
                "Password": settings.TRAVEL_BOUTIQUE_PASSWORD,
                # Ensure this IP address is correct for your deployment.
                "EndUserIp": "192.168.1.11"
            }
            # print('\n\n******************************************\n\n')
            # print(payload)
            # print('\n\n******************************************\n\n')
            response = requests.post(TravelBoutiqueAuth.AUTH_URL, json=payload, timeout=30)
            response.raise_for_status()
            # print('\n\n******************************************\n\n')
            # print(response.json())
            # print('\n\n******************************************\n\n')
            data = response.json()
            token = data.get("TokenId")
            if token:
                # Set the token to expire in 24 hours. Adjust if the API specifies a different expiry.
                expiry = now + timedelta(hours=24)
                cache.set("tbo_token_info", {"token": token, "expiry": expiry}, timeout=24 * 3600)
                return token
        except RequestException as e:
            print(f"Authentication failed: {e}")

        return None
