from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bookings.models import Bookings
from django.views.decorators.csrf import csrf_exempt
from accounts.models import FlightLead
from django.http import JsonResponse


@login_required
def all_bookings(request):
    # Get all Bookings for the logged-in user
    user_bookings = Bookings.objects.filter(user=request.user).order_by('-id')  
    context = {
        'bookings': user_bookings
    }
    return render(request, 'accounts/bookings.html', context)

def booking_details(request, booking_id):
    context = {
        'booking_id': booking_id
    }
    return render(request, 'booking_details.html', context)

@csrf_exempt
def flight_lead_form(request):
    from datetime import datetime
    if request.method == 'POST':
        rt_departure = request.POST.get('rt_departure')
        rt_return = request.POST.get('rt_return')
        rt_from = request.POST.get('rt_from')
        rt_to = request.POST.get('rt_to')
        rt_email = request.POST.get('rt_email')
        rt_phone = request.POST.get('rt_phone')
        rt_name = request.POST.get('rt_name')

        ow_departure = request.POST.get('ow_departure')
        ow_from = request.POST.get('ow_from')
        ow_to = request.POST.get('ow_to')
        ow_email = request.POST.get('ow_email')
        ow_phone = request.POST.get('ow_phone')
        ow_name = request.POST.get('ow_name')

        mc1_from = request.POST.get('mc1_from')
        mc1_to = request.POST.get('mc1_to')
        mc1_departure = request.POST.get('mc1_departure')

        mc2_from = request.POST.get('mc2_from')
        mc2_to = request.POST.get('mc2_to')
        mc2_departure = request.POST.get('mc2_departure')

        mc_email = request.POST.get('mc_email')
        mc_phone = request.POST.get('mc_phone')
        mc_name = request.POST.get('mc_name')

        from_location = rt_from or ow_from or mc1_from 
        to_location = rt_to or ow_to or mc1_to
        departure_input = rt_departure or ow_departure or mc1_departure or mc2_departure
        email = rt_email or ow_email or mc_email
        phone = rt_phone or ow_phone or mc_phone
        name = rt_name or ow_name or mc_name

        if from_location and to_location and departure_input:
            # Convert departure date to a proper date object in YYYY-MM-DD format
            try:
                departure_date = datetime.strptime(departure_input, "%Y-%m-%d").date()
            except ValueError:
                try:
                    departure_date = datetime.strptime(departure_input, "%m/%d/%Y").date()
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid departure date format. It must be in YYYY-MM-DD format.'
                    }, status=400)

            # Convert return date if provided
            rt_return_date = None
            if rt_return:
                try:
                    rt_return_date = datetime.strptime(rt_return, "%Y-%m-%d").date()
                except ValueError:
                    try:
                        rt_return_date = datetime.strptime(rt_return, "%m/%d/%Y").date()
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid return date format. It must be in YYYY-MM-DD format.'
                        }, status=400)

            flight_lead = FlightLead(
                from_location=from_location,
                to_location=to_location,
                departure_date=departure_date,
                return_date=rt_return_date,
                multicity_from=mc2_from,
                multicity_to=mc2_to,
                email=email,
                phone=phone,
                name=name,
            )
            flight_lead.save()

    return JsonResponse({'success': True})