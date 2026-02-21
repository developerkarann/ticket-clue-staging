
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from home.utils import UniversalAirAPI
import json
from django.shortcuts import redirect
from accounts.models import SearchSession

def flight_detail(request):
    trace_id = request.GET.get('TraceId')
    result_index = request.GET.get('ResultIndex')
    
    if not trace_id or not result_index:
        print(" no trace_id or result_index")
        return redirect("/")
    else:
        searchSession = SearchSession(traceId=trace_id, resultIndex=result_index)
        if request.user.is_authenticated:
            searchSession.user = request.user

        searchSession.save()
        request.session['hex_session'] = searchSession.hexid
        return redirect("step_booking_detail",1,searchSession.hexid)


@csrf_exempt
def get_ssr(request):
    trace_id = request.POST.get('TraceId')
    result_index = request.POST.get('ResultIndex')
    if not trace_id or not result_index:
        return JsonResponse({"error": "Invalid request."})

    api = UniversalAirAPI()
    ssr_response = api.get_ssr({"TraceId": trace_id, "ResultIndex": result_index},request)
    print(ssr_response)
    return JsonResponse(ssr_response)

@csrf_exempt
def get_fare_rule(request):
    trace_id = request.POST.get('TraceId')
    result_index = request.POST.get('ResultIndex')
    if not trace_id or not result_index:
        return JsonResponse({"error": "Invalid request."})

    api = UniversalAirAPI()
    fare_rule = api.get_fare_rule({"TraceId": trace_id, "ResultIndex": result_index},request)
    return JsonResponse(fare_rule)


@csrf_exempt
def get_fare_quote(request):
    trace_id = request.POST.get('TraceId')
    result_index = request.POST.get('ResultIndex')
    if not trace_id or not result_index:
        return JsonResponse({"error": "Invalid request."})

    api = UniversalAirAPI()
    fare_rule = api.get_fare_quote({"TraceId": trace_id, "ResultIndex": result_index}, request)
    
    context = {
        "fare_rule": json.dumps(fare_rule),
        "user": request.user
    }
    traveller_html = render_to_string('components/traveller-details.html', context)
    price_summary_html = render_to_string('components/price-summary.html', context)

    print(fare_rule)
    
    return JsonResponse({"travellerDetails": traveller_html,'priceSummary':price_summary_html, "fare_rule": fare_rule})
