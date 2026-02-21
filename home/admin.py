
from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class AirlinetResource(resources.ModelResource):
    class Meta:
        model = Airline
@admin.register(Airline)
class AirportAdmin(ImportExportModelAdmin):
    resource_class = AirlinetResource
    list_display = ('name', 'logo', 'slug', 'tagline', 'contact_info')
    search_fields = ('name', 'logo', 'slug', 'tagline', 'contact_info')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)

@admin.register(DirectFlight)
class DirectFlightAdmin(admin.ModelAdmin):
    list_display = ('title',  'price')
    search_fields = ('title',  'price')

@admin.register(FlightFrom)
class FlightFromAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(CityVacationPackage)
class CityVacationPackageAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(InternationalFlight)
class InternationalFlightAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(AirlineVacationPackage)
class AirlineVacationPackageAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(LastMinuteFlight)
class LastMinuteFlightAdmin(admin.ModelAdmin):      
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(OneWayFlight)
class OneWayFlightAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(RoundTripFlight)
class RoundTripFlightAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')

@admin.register(NonStopFlight)
class NonStopFlightAdmin(admin.ModelAdmin):
    list_display = ('title',  'rating', 'price')
    search_fields = ('title',  'rating', 'price')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'author')
    search_fields = ('title', 'author', 'category', 'tags')
    list_filter = ('published_date', 'category', 'tags')


@admin.register(HomeFaq)
class HomeFaqAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)


