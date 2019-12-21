from django.contrib import admin
from django.urls import include, path

from .apps.core.views import HomePageView, health

urlpatterns = [
    path('conditions/', include(('ski_conditions.apps.app_scraping.urls', 'conditions'))),
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
]
