# views.py
from datetime import datetime
from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404
from .models import Airline, Blog, DirectFlight, RoundTripFlight, NonStopFlight, CityVacationPackage, FlightFrom, LastMinuteFlight, OneWayFlight, InternationalFlight, AirlineVacationPackage, HomeFaq
import logging
from django.http import Http404

logger = logging.getLogger(__name__)

def home_view(request):
    context = {
        "hideCurrency": True,
        "direct_flights": DirectFlight.objects.all(),
        "round_trip_flights": RoundTripFlight.objects.all(),
        "non_stop_flights": NonStopFlight.objects.all(),
        "city_vacation_packages": CityVacationPackage.objects.all(),
        "flight_from": FlightFrom.objects.all(),
        "last_minute_flights": LastMinuteFlight.objects.all(),
        "one_way_flights": OneWayFlight.objects.all(),
        "international_flights": InternationalFlight.objects.all(),
        "airline_vacation_packages": AirlineVacationPackage.objects.all(),
        "blogs": Blog.objects.all(),
        "home_faqs": HomeFaq.objects.all()
    }
    return render(request, 'index.html', context)

def flight_search(request):
    context = {
        "hideCurrency": True,
        "direct_flights": DirectFlight.objects.all(),
        "round_trip_flights": RoundTripFlight.objects.all(),
        "non_stop_flights": NonStopFlight.objects.all(),
        "city_vacation_packages": CityVacationPackage.objects.all(),
        "flight_from": FlightFrom.objects.all(),
        "last_minute_flights": LastMinuteFlight.objects.all(),
        "one_way_flights": OneWayFlight.objects.all(),
        "international_flights": InternationalFlight.objects.all(),
        "airline_vacation_packages": AirlineVacationPackage.objects.all(),
        "blogs": Blog.objects.all()
    }
    return render(request, 'campaignSearchForm.html', context)


def _airport_display(iata_code):
    """Return (city_or_name, display_label) for an IATA code. Uses Airport model if available."""
    if not iata_code:
        return ("", "")
    try:
        airport = Airport.objects.filter(iata__iexact=iata_code.strip()).first()
        if airport:
            city = (airport.city or airport.name or iata_code).strip()
            return (city, f"{city} ({iata_code.upper()})")
    except Exception:
        pass
    return (iata_code.upper(), iata_code.upper())


def search_flight_results(request):
    """Renders the flight search results / quote page at /flight/search-flight."""
    from_code = (request.GET.get("from") or "").strip().upper()[:10]
    to_code = (request.GET.get("to") or "").strip().upper()[:10]
    trip_type = "Round-Trip" if request.GET.get("return") else "One-Way"
    adults = request.GET.get("adults", "1")
    try:
        passenger_count = max(1, int(adults))
    except ValueError:
        passenger_count = 1

    from_city, from_label = _airport_display(from_code) if from_code else ("", "")
    to_city, to_label = _airport_display(to_code) if to_code else ("", "")

    if not from_code:
        from_city, from_label = "Delhi", "Delhi (DEL)"
        from_code = "DEL"
    if not to_code:
        to_city, to_label = "Pune", "Pune (PNQ)"
        to_code = "PNQ"

    from datetime import datetime, timedelta
    departure_param = request.GET.get("departure")
    return_param = request.GET.get("return")
    # Normalize dates for lead form (YYYY-MM-DD)
    default_dep = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    departure_iso = default_dep
    return_iso = ""
    if departure_param:
        try:
            dt = datetime.strptime(departure_param.strip(), "%d %b %Y")
            departure_iso = dt.strftime("%Y-%m-%d")
        except ValueError:
            departure_iso = departure_param or default_dep
    if return_param:
        try:
            dt = datetime.strptime(return_param.strip(), "%d %b %Y")
            return_iso = dt.strftime("%Y-%m-%d")
        except ValueError:
            return_iso = return_param

    try:
        dep_dt = datetime.strptime(departure_iso, "%Y-%m-%d")
        departure_display = dep_dt.strftime("%a, %b %d")
    except Exception:
        departure_display = departure_iso
    return_display = ""
    if return_iso:
        try:
            ret_dt = datetime.strptime(return_iso, "%Y-%m-%d")
            return_display = ret_dt.strftime("%a, %b %d")
        except Exception:
            return_display = return_iso

    context = {
        "from_code": from_code,
        "from_city": from_city or from_code,
        "from_label": from_label or f"{from_code}",
        "to_code": to_code,
        "to_city": to_city or to_code,
        "to_label": to_label or f"{to_code}",
        "trip_type": trip_type,
        "is_round_trip": trip_type == "Round-Trip",
        "is_one_way": trip_type == "One-Way",
        "passenger_count": passenger_count,
        "travel_class": request.GET.get("class") or "Economy",
        "fixed_price": 150,
        "departure_iso": departure_iso,
        "return_iso": return_iso,
        "departure_display": departure_display,
        "return_display": return_display,
    }
    return render(request, "flight_search_results.html", context)




def about_us(request):
    return render(request, 'static/about.html')

def contact_us(request):
    return render(request, 'static/contact.html')

def blog(request):
    return render(request, 'static/blog.html')

def faq(request):
    context = {
        "home_faqs": HomeFaq.objects.all()
    }
    return render(request, 'static/faq.html', context)

def privacy_policy(request):
    return render(request, 'static/privacy-policy.html')

def terms_conditions(request):
    return render(request, 'static/terms-conditions.html')

def disclaimer(request):
    return render(request, 'static/disclaimer.html')

def popular_airlines(request):
    return render(request, 'static/popular-airlines.html')

def popular_flight_route(request):
    return render(request, 'static/popular-flight-route.html')

def airline_web_checkin(request):
    return render(request, 'static/airline-web-checkin.html')

def baggage_policy(request):
    return render(request, 'static/baggage-policy.html')


# airlines
def usa_flights(request):
    context = {
        "metaTitle": "Book Cheap Domestic Flight USA | Local Flight Deals | Cheap Airfare",
        "metaDescription": "Find cheap domestic flights in the USA! Compare local flight deals & save on airfare. Book now with Ticket Clue for the best prices on your next trip!"
    }
    return render(request, 'static/usa-flights.html', context)

def canada_flights(request):
    context = {
        "metaTitle": "Book Cheap Domestic Flight Canada | Local Flight Deals | Cheap Airfare",
        "metaDescription": "Find cheap domestic flights in Canada! Compare local flight deals & save on airfare. Book now with Ticket Clue for the best prices on your next trip!"
    }
    return render(request, 'static/canada-flights.html', context)


def all_airlines(request):
    context = {
        "metaTitle": "Book Cheap Domestic Flights | Local Flight Deals | Cheap Airfare",
        "metaDescription": "Find cheap domestic flights! Compare local flight deals & save on airfare. Book now with Ticket Clue for the best prices on your next trip!"
    }
    return render(request, 'airlines/all_airlines.html', context)

def airline_detail_view(request, slug):
    slug = slug.replace('book-', '')
    slug = slug.replace('-flights', '')
    airline = get_object_or_404(Airline, slug=slug)

    return render(request, "airlines/airline_detail.html", {"airline": airline, 
    "metaTitle": airline.metaTitle, "metaDescription":airline.metaDescription})

def package_detail_view(request, slug):
    print(slug)
    flight_models = [
        DirectFlight, FlightFrom, CityVacationPackage, InternationalFlight,
        AirlineVacationPackage, LastMinuteFlight, OneWayFlight, RoundTripFlight, NonStopFlight
    ]
    direct_flight = None
    for model in flight_models:
        try:
            direct_flight = model.objects.get(slug=slug)
            break
        except model.DoesNotExist:
            continue
    if not direct_flight:
        raise Http404("No flight package found matching the given slug")
    return render(request, "airlines/package_detail.html", {"direct_flight": direct_flight,
    "metaTitle": direct_flight.metaTitle, "metaDescription":direct_flight.metaDescription})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, "static/blog-detail.html", {"blog": blog})


import requests
from flights.models import Airport

IPINFO_TOKEN = 'd3c75b011cf45a'

def get_client_ip(request):
    """Extracts the client's IP address from the request, considering proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def get_city_from_ip(ip):
    """Fetches city name from IP using ipinfo.io."""
    try:
        response = requests.get(f'https://ipinfo.io/{ip}?token={IPINFO_TOKEN}')
        data = response.json()
        return data.get('city', '').strip()
    except Exception:
        return None

def get_airport_code(city):
    """Maps city name to IATA airport code with flexible matching."""
    # Try exact city and country match first
    airport = Airport.objects.filter(city=city).first()
    
    if not airport:
        # Try partial matches in name, city or country
        from django.db.models import Q
        airport = Airport.objects.filter(
            Q(name__icontains=city) | 
            Q(city__icontains=city) | 
            Q(country__icontains=city) 
        ).first()
    
    return airport.iata if airport else 'DEL'  # Default to Delhi if no match


def air_search(request, destination):
    ip = get_client_ip(request)
    city = get_city_from_ip(ip) if ip else None
    print("ip")
    print(ip)
    print("city")
    print(city)
    
    # Determine airport code
    myAirport = get_airport_code(city) if city else 'DEL'
    print("myAirport")
    print(myAirport)
    
    # Build redirect URL
    url = (
        f"/flights/search-flights?from={myAirport}"
        f"&to={destination}&departure={datetime.now().strftime('%d %b %Y')}"
        "&class=Economy&adults=1&children=0&infants=0"
    )
    return redirect(url)