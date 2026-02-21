
def airlines_list(request):
    from .models import Airline
    airline_list = Airline.objects.all().values('name', 'logo', 'slug')
    return {'airline_list': airline_list}
