from django.http import JsonResponse
from home.utils import UniversalAirAPI
from django.shortcuts import render, redirect
from bookings.models import SearchSession
import json
from django.http import JsonResponse

def get_booking_details(request):
    if request.method == 'POST':
        print(request.POST)
        booking_id = request.POST.get('bookingId')
        print(booking_id)
        if booking_id:
            api = UniversalAirAPI()
            booking_details = api.get_booking_details({"BookingId": booking_id}, request)
            return JsonResponse(booking_details)
        else:
            return JsonResponse({"error": "Missing required parameters."})
        

def booking_detail(request, step, session):
    context = {}
    search = SearchSession.objects.filter(hexid=session).first()
    trace_id = search.traceId
    result_index = search.resultIndex

    if trace_id:
        request.session['TraceId'] = trace_id

    context['TraceId'] = trace_id
    context['ResultIndex'] = result_index
    context['hex_session'] = session
    context['sessionData'] = search
    context['seats'] = json.dumps(search.seats)
    context['meals'] = json.dumps(search.meals)
    context['baggage'] = json.dumps(search.baggage)
    context['passengers'] = context['passengers'] = json.dumps(list(search.passengers.all().values( 'first_name', 'last_name', 'pax_type', 'id')))
    
    if search.expiry:
        context['session_expiry'] = search.expiry.isoformat()
    else:
        context['session_expiry'] = None

    if step == 1:
        context['current_step'] = 1
        if not trace_id or not result_index:
            print("trace id or resultIndex is not there!")
            return redirect("/")
    elif step == 2:
        if request.user.is_authenticated:
            pass
        elif not search.email or not search.primaryContact:
            return redirect("step_booking_detail",1,session)
        context['current_step'] = 2
    elif step == 3:
        context['current_step'] = 3

    return render(request, 'flight-detail.html', context)
