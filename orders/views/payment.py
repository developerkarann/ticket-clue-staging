
import uuid
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from orders.models import PaymentTransaction
from accounts.models import SearchSession
from orders.helpers import book_flight_non_lcc,razorpay_client, ticket_request_lcc, ticket_request_non_lcc

@csrf_exempt
def make_payment(request):
    hexId = request.session.get('hex_session')
    if not hexId:
        return JsonResponse({"error": "Session ID not found."})

    if request.method == 'POST':
        try:
            amount = request.POST.get('amount')
            currency = request.POST.get('currency') or 'INR'
            amount_in_paise = int(float(amount) * 100)  # Convert to paise

            # Example for retrieving your session
            search_session = SearchSession.objects.get(hexid=hexId)

            # If the session is already ticketed or payment is done, stop here
            if search_session.isTicketed:
                return JsonResponse({'error': 'Ticket already booked.'})
            elif search_session.payment_status != 'success':
                if search_session.bookingId is None:
                    if not search_session.isLcc:
                        booking_response = book_flight_non_lcc(hexId, request)
                        if not booking_response.get('success', False):
                            return JsonResponse(booking_response, status=400)
                        
            

            if search_session.isLcc:
                result = ticket_request_lcc(hexId, request)
            else:
                result = ticket_request_non_lcc(hexId, request)



            # Create a Razorpay Order
            session_id = str(uuid.uuid4().hex[:12])
            order_data = {
                'amount': amount_in_paise,
                'currency': currency,
                'receipt': f'receipt_{session_id}',
                'payment_capture': '1',
            }

            order = razorpay_client.order.create(order_data)

            # Create PaymentTransaction record
            payment_transaction = PaymentTransaction.objects.create(
                search_session=search_session, 
                order_id=order['id'],
                amount=order['amount'],
                currency=order['currency'],
                status='created'
            )

            response_data = {
                'status': 'success',
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'session_id': session_id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    else:
        return HttpResponseBadRequest('Invalid request')
