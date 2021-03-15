from django.test import TestCase
from rest_framework import status
import json
from .models import Room


class RoomCreateTest(TestCase):
    def test_room_create_right_room_number_and_without_room_class(self):
        # Create
        data = json.dumps({"room_number": 305})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check database
        room = Room.objects.get(room_number=305)
        self.assertEqual(room.room_number, 305)
        self.assertEqual(room.room_class, "A")

    def test_room_create_right_room_number_and_with_D_room_class(self):
        # Create
        data = json.dumps({"room_number": 305, "room_class": "D"})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check database
        room = Room.objects.get(room_number=305)
        self.assertEqual(room.room_number, 305)
        self.assertEqual(room.room_class, "D")

    def test_room_create_wrong_room_number_minus1(self):
        # Create
        data = json.dumps({"room_number": -1})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        room = Room.objects.filter(room_number=-1).exists()
        self.assertEqual(room, False)

    def test_room_create_wrong_room_number_0(self):
        # Create
        data = json.dumps({"room_number": 0})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        room = Room.objects.filter(room_number=0).exists()
        self.assertEqual(room, False)

    def test_room_create_wrong_room_number_1000001(self):
        # Create
        data = json.dumps({"room_number": 1000001})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        room = Room.objects.filter(room_number=1000001).exists()
        self.assertEqual(room, False)

    def test_room_create_wrong_room_number_a_letter(self):
        # Create
        data = json.dumps({"room_number": 'a'})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["room_number"][0], "A valid integer is required.")

        # Check database
        room = Room.objects.filter().exists()
        self.assertEqual(room, False)

    def test_room_create_wrong_room_number_not_a_digit(self):
        # Create
        data = json.dumps({"room_number": '%%x'})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["room_number"][0], "A valid integer is required.")

        # Check database
        room = Room.objects.filter().exists()
        self.assertEqual(room, False)
