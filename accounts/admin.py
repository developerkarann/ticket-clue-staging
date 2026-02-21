from django.contrib import admin
from .models import *

admin.site.register(Profile)
@admin.register(SearchSession)
class SearchSessionAdmin(admin.ModelAdmin):
    list_display = ('hexid', 'user', 'primaryContact', 'email', 'bookingId', 'pnr', 'isTicketed', 'payment_status', 'created_at')
    search_fields = ('hexid', 'primaryContact', 'email', 'bookingId', 'pnr')
    list_filter = ('isTicketed', 'payment_status', 'isLcc')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(Passenger)
admin.site.register(Meal)
admin.site.register(Seat)
admin.site.register(Baggage)
admin.site.register(Fare)
admin.site.register(OTP)

@admin.register(FlightLead)
class FlightLeadAdmin(admin.ModelAdmin):
    list_display = ('from_location', 'to_location', 'departure_date', 'return_date', 'email', 'phone', 'name')
    search_fields = ('from_location', 'to_location', 'email', 'phone', 'name')
    list_filter = ('departure_date', 'return_date')
    readonly_fields = ('created_at', 'updated_at')
