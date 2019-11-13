from django.contrib import admin
from django.urls import path

from .apps.core.views import HomePageView, health

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
]
