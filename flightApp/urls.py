
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('flights/', include('flights.urls')),
    path('', include('bookings.urls')),
    path('orders/', include('orders.urls')),
    path('', include('home.urls')),
    
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns() + [
    re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False)),
]

# urlpatterns += [
#     re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False)),
# ]