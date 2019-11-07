from django.contrib import admin
from django.urls import include, path

from .apps.core.views import health

urlpatterns = [
    path('conditions', include('app_scraping.urls')),
    path('health/', health, name='health'),
    path('admin/', admin.site.urls),
]
