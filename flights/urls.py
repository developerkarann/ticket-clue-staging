from django.urls import path
from . import views

urlpatterns = [
    path('flight-detail', views.details.flight_detail, name='flight_detail_to_book'),
    path('search-airports/', views.airports.search_airports, name='search_airports'),
    path('search-flights', views.search.FlightSearchView.as_view(), name='search_flights'),
    path('fare-rule', views.details.get_fare_rule, name='fare_rule'),
    path('fare-quote', views.details.get_fare_quote, name='fare_quote'),
    path('fare-ssr', views.details.get_ssr, name='fare_ssr'),
]
