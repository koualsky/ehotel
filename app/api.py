from rest_framework.viewsets import ModelViewSet

from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
