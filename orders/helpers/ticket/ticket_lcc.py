
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from accounts.models import SearchSession
from home.utils import UniversalAirAPI
from accounts.models import Profile
from .json_format import TicketJsonFormater
from bookings.helpers import save_flight_response_to_db
import logging

logger = logging.getLogger(__name__)

def ticket_request_lcc(session_id, request):
    """
    Formats the ticket request payload for LCC flights.
    """
    try:
        if not session_id:
            print("Missing 'session_id' parameter.")
            return {"success": False, "error": "Missing 'session_id' parameter."}
        sessionObj = SearchSession.objects.get(hexid=session_id)
        if not sessionObj:
            print("Session not found.")
            return {"success": False, "error": "Invalid session ID."}

        passengers = sessionObj.passengers.all()
        if not passengers.exists():
            print("No passengers found in the session.")
            return {"success": False, "error": "No passengers found in the session."}

        primaryEmail = sessionObj.email
        primary_contact = sessionObj.primaryContact
        if sessionObj.user:
            primaryEmail = sessionObj.user.email
            userProfile = Profile.objects.get(user=sessionObj.user)
            primary_contact = userProfile.mobile_no

        booking_payload = TicketJsonFormater.ticket_request(
            sessionObj.traceId,
            sessionObj.resultIndex,
            passengers,
            primaryEmail,
            primary_contact
        )

        api = UniversalAirAPI()

        # Call the booking API
        ticket_response = api.ticket_flight(booking_payload, request)
        print("ticket lcc Response:", ticket_response)

        # Extract relevant information from the response
        response_data = ticket_response.get('Response', {})
        error_code = response_data.get('Error', {}).get('ErrorCode', -1)

        if error_code != 0:
            error_message = response_data.get('Error', {}).get('ErrorMessage', '')
            print("Error:", error_message)
            logger.error(f"Ticketing failed for session {session_id}: {error_message}")
            return {
                "success": False,
                "error_code": error_code,
                "error": error_message,
                "response": response_data
            }

        ticket_details = response_data.get('Response', {})
        print("Ticket Details fetched:", ticket_details)
        booking_id = ticket_details.get('BookingId', '')
        pnr = ticket_details.get('PNR', '')

        if not booking_id or not pnr:
            logger.error(f"Ticketing failed for session {session_id}: Ticket ID or PNR not found.")
            print("Ticketing failed for session {session_id}: Ticket ID or PNR not found.")
            return {
                "success": False,
                "error_code": error_code,
                "error": "Ticket ID or PNR not found in response.",
                "response": ticket_details
            }

        # Use atomic transaction to ensure data integrity
        with transaction.atomic():
            sessionObj.bookingId = booking_id
            sessionObj.pnr = pnr
            sessionObj.ticket_response = ticket_details
            sessionObj.isTicketed = True
            sessionObj.save()

            # fetch and save booking details
            booking_details = api.get_booking_details({"BookingId": booking_id}, request)
            print("Booking Details fetched:------", booking_details)
            print("\n\n\n\n\n")
            save_flight_response_to_db(booking_details, sessionObj, user=sessionObj.user)

        return {"success": True, "hex_session": sessionObj.hexid}

    except ObjectDoesNotExist as e:
        logger.error(f"Object does not exist: {e}")
        print("Object does not exist: {e}")
        return {"success": False, "error": "Session or related data not found."}

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        return {
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }
