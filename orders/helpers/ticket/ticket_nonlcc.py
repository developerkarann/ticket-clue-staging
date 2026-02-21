from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from accounts.models import SearchSession
from home.utils import UniversalAirAPI
import logging

logger = logging.getLogger(__name__)

@staticmethod
def ticket_request_non_lcc(session_id, request):
    """
    Formats the ticket request payload for Non-LCC flights.
    """
    try:
        if not session_id:
            return {"success": False, "error": "Missing 'session_id' parameter."}
        sessionObj = SearchSession.objects.get(hexid=session_id)
        if not sessionObj:
            return {"success": False, "error": "Invalid session ID."}

        # We assume 'pnr' is retrieved from the session or passed separately
        pnr = sessionObj.pnr

        ticket_payload = {
            "TraceId": sessionObj.traceId,
            "PNR": pnr,
            "BookingId": sessionObj.bookingId,
        }

        api = UniversalAirAPI()

        # Call the booking API
        ticket_response = api.ticket_flight(ticket_payload, request)
        print("Ticket Response:", ticket_response)

        # Extract relevant information from the response
        response_data = ticket_response.get('Response', {})
        error_code = response_data.get('Error', {}).get('ErrorCode', -1)

        if error_code != 0:
            error_message = response_data.get('Error', {}).get('ErrorMessage', '')
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
