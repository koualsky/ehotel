from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from .api import RoomViewSet, BookingViewSet


router = DefaultRouter()
router.register(r"room", RoomViewSet)
router.register(r"booking", BookingViewSet)


urlpatterns = [
    url(r"^api/", include(router.urls)),
]
