from django.urls import path
from . import views

urlpatterns = [
    path('get-booking-details/', views.booking.get_booking_details, name='get_booking_details'),
    path('itinerary/<int:step>/<str:session>', views.booking.booking_detail, name='step_booking_detail'),

    path('passenger-details', views.passengers.post_passenger_details, name='post_passenger_details'),
]
