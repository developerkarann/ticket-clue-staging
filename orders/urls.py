from django.urls import path
from . import views

urlpatterns = [
    path('make-booking-request', views.booking.book_flight, name='make_booking_request'),
    path('make-flight-payment', views.payment.make_payment, name='make_flight_payment'),
    path('razorpay/webhook/', views.webhook.razorpay_webhook, name='razorpay_webhook'),
]
