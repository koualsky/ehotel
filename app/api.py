from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        # Change room_numbers to pk
        rooms_pk = []
        rooms_numbers = request.data['rooms']
        for room in rooms_numbers:
            try:
                room_pk = Room.objects.get(room_number=room).pk
            except Room.DoesNotExist as err:
                raise ValidationError("Room {} does not exist.".format(room))
            rooms_pk.append(room_pk)
        request.data['rooms'] = rooms_pk

        # Create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        # Change room_numbers to pk
        rooms_pk = []
        rooms_numbers = request.data['rooms']
        for room in rooms_numbers:
            try:
                room_pk = Room.objects.get(room_number=room).pk
            except Room.DoesNotExist as err:
                raise ValidationError("Room {} does not exist.".format(room))
            rooms_pk.append(room_pk)
        request.data['rooms'] = rooms_pk

        # Update
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

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
