from rest_framework.serializers import ModelSerializer
from .models import Room, Booking


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rooms'] = RoomSerializer(instance.rooms.all(), many=True).data
        return rep
