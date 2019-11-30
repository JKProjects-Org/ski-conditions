from django.contrib import admin
from django.urls import include, path

from .apps.core.views import health

urlpatterns = [
    path('conditions/', include(('ski_conditions.apps.app_scraping.urls', 'conditions'))),
    path('health/', health, name='health'),
    path('admin/', admin.site.urls),
]
