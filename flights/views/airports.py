import requests
from django.conf import settings
from django.db import connection
from django.db.models import Q, F
from django.db.models.functions import Greatest, Coalesce
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from flights.models import Airport


def _fetch_airports_from_api(query):
    """
    Optional: fetch airport list from an external API.
    Set AIRPORT_API_URL in .env (e.g. your API or a third-party airport API).
    Expects JSON array or object with key 'data'/'Response'/'airports'/'City'.
    Maps common field names (AirportCode/CityCode, AirportName/CityName, etc.) to our format.
    Returns list of dicts or None on failure/empty.
    """
    api_url = getattr(settings, 'AIRPORT_API_URL', None)
    if not api_url:
        return None
    param = getattr(settings, 'AIRPORT_API_QUERY_PARAM', 'q') or 'q'
    try:
        resp = requests.get(api_url, params={param: query}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None
    # Unwrap if response is { "data": [...], "Response": [...], "airports": [...], "City": [...] }
    if isinstance(data, dict):
        for key in ('data', 'Response', 'airports', 'Airports', 'City', 'Cities'):
            if isinstance(data.get(key), list):
                data = data[key]
                break
        else:
            data = []
    if not isinstance(data, list):
        return None
    out = []
    for item in (data or []):
        if not isinstance(item, dict):
            continue
        # Map common API field names to our response shape
        iata = (item.get('iata') or item.get('AirportCode') or item.get('CityCode') or item.get('code') or '').strip()
        name = (item.get('name') or item.get('AirportName') or item.get('CityName') or item.get('AirportName') or '').strip()
        city = (item.get('city') or item.get('CityName') or item.get('City') or '').strip()
        country = (item.get('country') or item.get('CountryName') or item.get('Country') or '').strip()
        if not iata and not name:
            continue
        out.append({
            'icao': item.get('icao') or item.get('ICAOCode') or None,
            'iata': iata or None,
            'name': name or None,
            'city': city or None,
            'state': (item.get('state') or item.get('State') or '').strip() or None,
            'country': country or None,
            'elevation': item.get('elevation'),
            'lat': str(item.get('lat')) if item.get('lat') is not None else None,
            'lon': str(item.get('lon')) if item.get('lon') is not None else None,
            'tz': item.get('tz') or item.get('timezone'),
            'similarity': 1.0,
        })
    return out if out else None


@csrf_exempt
def search_airports(request):
    """
    Search airports. If AIRPORT_API_URL is set, tries the external API first;
    otherwise (or on API failure) uses the database (PostgreSQL trigram or SQLite icontains).
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method. Only GET allowed.'}, status=400)
    
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'error': 'Query parameter "q" is required.'}, status=400)
    
    if len(query) < 2:
        return JsonResponse({'error': 'Query must be at least 2 characters long.'}, status=400)

    query_lower = query.lower()

    # Optional: try external airport API first
    api_results = _fetch_airports_from_api(query)
    if api_results is not None and len(api_results) > 0:
        return JsonResponse(api_results, safe=False)

    # Fallback: database
    try:
        if connection.vendor == 'postgresql':
            from django.contrib.postgres.search import TrigramSimilarity
            airports = Airport.objects.annotate(
                name_sim=Coalesce(TrigramSimilarity('name', query_lower), 0.0),
                city_sim=Coalesce(TrigramSimilarity('city', query_lower), 0.0),
                iata_sim=Coalesce(TrigramSimilarity('iata', query_lower), 0.0),
                country_sim=Coalesce(TrigramSimilarity('country', query_lower), 0.0),
                state_sim=Coalesce(TrigramSimilarity('state', query_lower), 0.0),
            ).annotate(
                combined_score=Greatest(
                    F('name_sim'), F('city_sim'), F('iata_sim'),
                    F('country_sim'), F('state_sim'),
                )
            ).filter(
                Q(combined_score__gt=0.15) | Q(iata__iexact=query_lower)
            ).order_by('-combined_score', 'name')[:20]
            airport_list = [_airport_to_dict(a, float(a.combined_score)) for a in airports]
        else:
            # SQLite / other: simple case-insensitive partial match
            q = Q(name__icontains=query_lower) | Q(city__icontains=query_lower) | Q(iata__icontains=query_lower)
            q |= Q(country__icontains=query_lower) | Q(state__icontains=query_lower)
            airports = Airport.objects.filter(q).order_by('name')[:20]
            airport_list = [_airport_to_dict(a, 1.0) for a in airports]

        return JsonResponse(airport_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'Server error processing request'}, status=500)


def _airport_to_dict(airport, similarity=1.0):
    return {
        'icao': airport.icao,
        'iata': airport.iata,
        'name': airport.name,
        'city': airport.city,
        'state': airport.state,
        'country': airport.country,
        'elevation': airport.elevation,
        'lat': str(airport.lat) if airport.lat is not None else None,
        'lon': str(airport.lon) if airport.lon is not None else None,
        'tz': airport.tz,
        'similarity': similarity,
    }