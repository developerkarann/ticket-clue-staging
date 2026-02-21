from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

# Define the resource for Airport
class AirportResource(resources.ModelResource):
    class Meta:
        model = Airport
        

# Register Airport with AirportAdmin using the decorator
@admin.register(Airport)
class AirportAdmin(ImportExportModelAdmin):
    resource_class = AirportResource
    list_display = ('name', 'iata', 'city', 'country', 'lat', 'lon')
    search_fields = ('name', 'iata', 'city', 'country')
