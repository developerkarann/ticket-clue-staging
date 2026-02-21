
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from accounts.models import SearchSession, Profile
from home.utils import UniversalAirAPI
from .json_format import BookingJsonFormater

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def book_flight_non_lcc(session_id, request):
    try:
        if not session_id:
            return {"success": False, "error": "Missing 'session_id' parameter."}
        sessionObj = SearchSession.objects.get(hexid=session_id)
        if not sessionObj:
            return {"success": False, "error": "Invalid session ID."}

        passengers = sessionObj.passengers.all()
        if not passengers.exists():
            return {"success": False, "error": "No passengers found in the session."}

        primaryEmail = sessionObj.email
        primary_contact = sessionObj.primaryContact
        if sessionObj.user:
            primaryEmail = sessionObj.user.email
            userProfile = Profile.objects.get(user=sessionObj.user)
            primary_contact = userProfile.mobile_no

        booking_payload = BookingJsonFormater.booking_request(
            sessionObj.traceId,
            sessionObj.resultIndex,
            passengers,
            primaryEmail,
            primary_contact
        )

        api = UniversalAirAPI()

        # Call the booking API
        booking_response = api.book_flight(booking_payload, request)
        print("Booking Response:", booking_response)

        # Extract relevant information from the response
        response_data = booking_response.get('Response', {})
        error_code = response_data.get('Error', {}).get('ErrorCode', -1)

        if error_code != 0:
            error_message = response_data.get('Error', {}).get('ErrorMessage', '')
            logger.error(f"Booking failed for session {session_id}: {error_message}")
            return {
                "success": False,
                "error_code": error_code,
                "error": error_message,
                "response": response_data
            }

        booking_details = response_data.get('Response', {})
        print("Booking Details fetched:", booking_details)
        booking_id = booking_details.get('BookingId', '')
        pnr = booking_details.get('PNR', '')

        if not booking_id or not pnr:
            logger.error(f"Booking failed for session {session_id}: Booking ID or PNR not found.")
            return {
                "success": False,
                "error_code": error_code,
                "error": "Booking ID or PNR not found in response.",
                "response": booking_details
            }

        # Use atomic transaction to ensure data integrity
        with transaction.atomic():
            sessionObj.bookingId = booking_id
            sessionObj.pnr = pnr
            sessionObj.booking_response = booking_details
            sessionObj.save()

        return {"success": True, "hex_session": sessionObj.hexid}

    except ObjectDoesNotExist as e:
        logger.error(f"Object does not exist: {e}")
        return {"success": False, "error": "Session or related data not found."}

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return {
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }
