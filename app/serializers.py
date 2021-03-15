from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Room, Booking, ROOM_CLASSES


class RoomSerializer(ModelSerializer):
    price = SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "room_number", "room_class", "price")

    @staticmethod
    def get_price(obj):
        return ROOM_CLASSES[obj.room_class]


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rooms'] = RoomSerializer(instance.rooms.all(), many=True).data
        return rep
