from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from .models import Room, Booking, ROOM_CLASSES


class RoomSerializer(ModelSerializer):
    price = SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "room_number", "room_class", "price")

    @staticmethod
    def get_price(obj):
        return ROOM_CLASSES[obj.room_class]

    @staticmethod
    def validate_room_number(room_number):
        if not (1 <= room_number <= 1000000):
            raise ValidationError("The room number must be an integer between 0 and 1 000 000.")
        return room_number


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rooms'] = RoomSerializer(instance.rooms.all(), many=True).data
        return rep

    def validate(self, data):
        reservation_from = data["reservation_from"]
        reservation_to = data["reservation_to"]
        if reservation_to <= reservation_from:
            raise ValidationError("The reservation_to field should be greater than reservation_from.")
        return data
