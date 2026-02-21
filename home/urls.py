from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('search-flight', views.flight_search, name='flight_search'),
    path('flight/search-flight', views.search_flight_results, name='search_flight_results'),
    path('air_search/<str:destination>/', views.air_search, name='air_search'),
    
    # Static pages
    path('about', views.about_us, name='about_us'),
    path('contact', views.contact_us, name='contact_us'),
    path('blog', views.blog, name='blog'),
    path('blog/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('faq', views.faq, name='faq'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions', views.terms_conditions, name='terms_conditions'),
    path('disclaimer', views.disclaimer, name='disclaimer'),
    path('popular-airlines', views.popular_airlines, name='popular_airlines'),
    path('popular-flight-route', views.popular_flight_route, name='popular_flight_route'),
    path('airline-web-checkin', views.airline_web_checkin, name='airline_web_checkin'),
    path('baggage-policy', views.baggage_policy, name='baggage_policy'),
    path('usa-flights', views.usa_flights, name='usa_flights'),
    path('canada-flights', views.canada_flights, name='canada_flights'),

    #airlines
    path('airlines/', views.all_airlines, name='all_airlines'),
    path('airlines/<slug:slug>/', views.airline_detail_view, name='home_airlines'),
    # path('package/<slug:slug>/', views.package_detail_view, name='package_detail'),


    path('direct-flights/<slug:slug>/', views.package_detail_view, name='direct_flight_detail'),
    path('city-escapes/<slug:slug>/', views.package_detail_view, name='city_escapes_detail'),
    path('round-trip-flights/<slug:slug>/', views.package_detail_view, name='round_trip_flight_detail'),
    path('non-stop-flights/<slug:slug>/', views.package_detail_view, name='non_stop_flight_detail'),
    path('city-vacation-packages/<slug:slug>/', views.package_detail_view, name='city_vacation_package_detail'),
    path('international-flights/<slug:slug>/', views.package_detail_view, name='international_flight_detail'),
    path('airline-vacation-packages/<slug:slug>/', views.package_detail_view, name='airline_vacation_package_detail'),
    path('last-minute-flights/<slug:slug>/', views.package_detail_view, name='last_minute_flight_detail'),
    path('one-way-flights/<slug:slug>/', views.package_detail_view, name='one_way_flight_detail'),
    path('popular-departures/<slug:slug>/', views.package_detail_view, name='popular_departures_detail'),
    

]