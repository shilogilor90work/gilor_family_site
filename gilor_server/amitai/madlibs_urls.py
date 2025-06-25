# your_app_name/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MadlibsViewSet # Adjust 'your_app_name' to your actual app name

router = DefaultRouter()
router.register(r'madlibs', MadlibsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
