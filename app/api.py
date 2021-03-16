from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime

from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


class RoomViewSet(ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating and deleting rooms
    """

    # permission_classes = (IsAuthenticated,)
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class BookingViewSet(ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating and deleting bookings
    """

    # permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def list(self, request):
        if self.request.GET:
            room_number = self.request.GET.get('room_number')
            last_name = self.request.GET.get('last_name')
            reservation_from = self.request.GET.get('reservation_from')
            reservation_to = self.request.GET.get('reservation_to')
            q = dict()
            if room_number:
                q.update({'rooms__room_number': room_number})
            if last_name:
                q.update({'last_name': last_name})
            if reservation_from:
                try:
                    converted_date = datetime.strptime(reservation_from, '%Y-%m-%d')
                    q.update({'reservation_from__date__gte': converted_date})
                except ValueError as err:
                    raise ValidationError(err)
            if reservation_to:
                try:
                    converted_date = datetime.strptime(reservation_to, '%Y-%m-%d')
                    q.update({'reservation_to__date__lte': converted_date})
                except ValueError as err:
                    raise ValidationError(err)
            queryset = Booking.objects.filter(**q)
        else:
            queryset = Booking.objects.all()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)
