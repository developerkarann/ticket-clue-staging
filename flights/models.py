from django.db import models
from django.db import connection
from django.conf import settings

# Use PostgreSQL-only search field when using PostgreSQL; otherwise a no-op field for SQLite
if 'postgresql' in (settings.DATABASES.get('default') or {}).get('ENGINE', ''):
    from django.contrib.postgres.search import SearchVectorField
    from django.contrib.postgres.indexes import GinIndex
    _search_vector_field = SearchVectorField(null=True, blank=True)
    _extra_indexes = [GinIndex(fields=['search_vector'])]
else:
    _search_vector_field = models.TextField(null=True, blank=True)
    _extra_indexes = []


class Airport(models.Model):
    icao = models.CharField(max_length=10, blank=True, null=True)
    iata = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    tz = models.CharField(max_length=50, blank=True, null=True)
    search_vector = _search_vector_field

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['iata']),
            models.Index(fields=['name']),
        ] + _extra_indexes

    def save(self, *args, **kwargs):
           # Update search vector on save
        super().save(*args, **kwargs)
        if connection.vendor == 'postgresql':
            from django.contrib.postgres.search import SearchVector
            Airport.objects.filter(pk=self.pk).update(
                search_vector=SearchVector('name', 'city', 'iata', 'country', 'state')
            )
