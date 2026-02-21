"""
Load sample airport data so /flights/search-airports/?q=delhi (and similar) return results.
Run once: python manage.py load_sample_airports
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from flights.models import Airport


# Sample airports including Delhi and a few others for testing search
SAMPLE_AIRPORTS = [
    {
        "icao": "VIDP",
        "iata": "DEL",
        "name": "Indira Gandhi International Airport",
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "elevation": 777,
        "lat": Decimal("28.5665"),
        "lon": Decimal("77.1031"),
        "tz": "Asia/Kolkata",
    },
    {
        "icao": "VABB",
        "iata": "BOM",
        "name": "Chhatrapati Shivaji Maharaj International Airport",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "elevation": 39,
        "lat": Decimal("19.0896"),
        "lon": Decimal("72.8656"),
        "tz": "Asia/Kolkata",
    },
    {
        "icao": "VOCI",
        "iata": "COK",
        "name": "Cochin International Airport",
        "city": "Kochi",
        "state": "Kerala",
        "country": "India",
        "elevation": 30,
        "lat": Decimal("10.1520"),
        "lon": Decimal("76.4019"),
        "tz": "Asia/Kolkata",
    },
    {
        "icao": "EGLL",
        "iata": "LHR",
        "name": "London Heathrow Airport",
        "city": "London",
        "state": "",
        "country": "United Kingdom",
        "elevation": 83,
        "lat": Decimal("51.4700"),
        "lon": Decimal("-0.4543"),
        "tz": "Europe/London",
    },
    {
        "icao": "KJFK",
        "iata": "JFK",
        "name": "John F. Kennedy International Airport",
        "city": "New York",
        "state": "New York",
        "country": "United States",
        "elevation": 13,
        "lat": Decimal("40.6398"),
        "lon": Decimal("-73.7787"),
        "tz": "America/New_York",
    },
    {
        "icao": "OMDB",
        "iata": "DXB",
        "name": "Dubai International Airport",
        "city": "Dubai",
        "state": "",
        "country": "United Arab Emirates",
        "elevation": 62,
        "lat": Decimal("25.2532"),
        "lon": Decimal("55.3657"),
        "tz": "Asia/Dubai",
    },
]


class Command(BaseCommand):
    help = "Load sample airports (Delhi, Mumbai, etc.) so search-airports returns results."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove all existing airports before loading samples (optional).",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            n = Airport.objects.count()
            Airport.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {n} existing airport(s)."))

        created = 0
        for data in SAMPLE_AIRPORTS:
            _, was_created = Airport.objects.update_or_create(
                iata=data["iata"],
                defaults=data,
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(SAMPLE_AIRPORTS)} sample airports ({created} new). "
                "Try: http://127.0.0.1:8000/flights/search-airports/?q=delhi"
            )
        )
