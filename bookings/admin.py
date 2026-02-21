from django.contrib import admin
from .models import *

admin.site.register(Fare)
admin.site.register(Passenger)
admin.site.register(Segment)
admin.site.register(FareRule)
admin.site.register(Invoice)
admin.site.register(FlightItinerary)
admin.site.register(Bookings)
