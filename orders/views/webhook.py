
import json
import razorpay
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from accounts.models import SearchSession
from orders.helpers import ticket_request_lcc, ticket_request_non_lcc, razorpay_client
from orders.models import PaymentTransaction

@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        try:
            payload = request.body.decode('utf-8')  # Decode bytes to string
            webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
            webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET

            # Double-check these are non-empty strings
            if not webhook_signature:
                return JsonResponse({'error': 'Missing Razorpay signature in headers.'}, status=400)
            if not webhook_secret:
                return JsonResponse({'error': 'Razorpay webhook secret not configured.'}, status=400)

            # Verify webhook signature
            razorpay_client.utility.verify_webhook_signature(
                payload,
                webhook_signature,
                webhook_secret
            )

            # Parse JSON
            event_json = json.loads(payload)
            event_type = event_json.get('event')
            payload_entity = event_json.get('payload', {}).get('payment', {}).get('entity', {})

            order_id = payload_entity.get('order_id')
            payment_id = payload_entity.get('id')
            status = payload_entity.get('status')

            payment_transaction = PaymentTransaction.objects.filter(order_id=order_id).first()
            if payment_transaction:
                payment_transaction.payment_id = payment_id
                payment_transaction.status = status
                payment_transaction.save()

                # If payment is captured, finalize booking, etc.
                if status == 'captured':
                    sessionId = payment_transaction.search_session
                    search_session = SearchSession.objects.get(hexid=sessionId)
                    search_session.payment_status = 'success'
                    search_session.save()

                    if search_session.isLcc:
                        result = ticket_request_lcc(sessionId, request)
                    else:
                        result = ticket_request_non_lcc(sessionId, request)

                    if result.get('success', False):
                        return JsonResponse({'status': 'ok'})
                    else:
                        return JsonResponse({'error': 'Ticketing failed.'}, status=400)

            # Return ok even if no matching transaction is found
            return JsonResponse({'status': 'ok'})

        except razorpay.errors.SignatureVerificationError:
            print("Invalid signature")
            return JsonResponse({'error': 'Invalid signature.'}, status=400)
        except Exception as e:
            print("Error processing webhook")
            print(e)
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return HttpResponseBadRequest('Invalid request')
    
    