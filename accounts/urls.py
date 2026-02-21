from django.urls import path
from . import views

urlpatterns = [
    path('login', views.authentication.login , name='login'),
    path('signup', views.authentication.signup , name='register'),
    path('logout', views.authentication.logout , name='logout'),
    path('send-otp', views.authentication.send_otp , name='send_otp'),

    path('bookings/', views.booking.all_bookings, name='bookings'),
    path('bookings/<int:booking_id>/', views.booking.booking_details, name="single_booking_details"),
    path('flight_lead_form/', views.booking.flight_lead_form, name='flight_lead_form'),
]