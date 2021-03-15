from django.test import TestCase
from rest_framework import status
import json
from .models import Room


# class RoomListTest(TestCase):


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

    def test_room_create_right_room_number_with_right_room_class(self):
        # Create
        data = json.dumps({"room_number": 305, "room_class": "B"})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check database
        room = Room.objects.get(room_number=305)
        self.assertEqual(room.room_number, 305)
        self.assertEqual(room.room_class, "B")

    def test_room_create_right_room_number_with_wrong_room_class(self):
        # Create
        data = json.dumps({"room_number": 305, "room_class": "E"})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        room = Room.objects.filter().exists()
        self.assertEqual(room, False)

    def test_room_create_right_room_number_with_wrong_room_class_2(self):
        # Create
        data = json.dumps({"room_number": 305, "room_class": 2})
        response = self.client.post("/api/room/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        room = Room.objects.filter().exists()
        self.assertEqual(room, False)


class RoomUpdateTest(TestCase):
    def setUp(self):
        Room.objects.create(room_number=305, room_class="A")

    def test_room_update_init_data(self):
        existing = Room.objects.get(room_number=305)
        self.assertEqual(existing.pk, 1)
        self.assertEqual(existing.room_number, 305)
        self.assertEqual(existing.room_class, "A")

    def test_room_update_right_room_number_with_right_room_class(self):
        # Update existing room
        data = json.dumps({"room_number": 333, "room_class": "B"})
        response = self.client.put("/api/room/1/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check database
        room = Room.objects.get(pk=1)
        self.assertEqual(room.room_number, 333)
        self.assertEqual(room.room_class, "B")

    def test_room_update_right_room_number_with_wrong_room_class(self):
        # Update existing room
        data = json.dumps({"room_number": 333, "room_class": "E"})
        response = self.client.put("/api/room/1/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['room_class'][0], '"E" is not a valid choice.')

        # Check database
        room = Room.objects.get(pk=1)
        self.assertEqual(room.room_number, 305)
        self.assertEqual(room.room_class, "A")

    def test_room_update_wrong_room_number_with_right_room_class(self):
        # Update existing room
        data = json.dumps({"room_number": 0, "room_class": "D"})
        response = self.client.put("/api/room/1/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['room_number'][0], "The room number must be an integer between 0 and 1 000 000.")

        # Check database
        room = Room.objects.get(pk=1)
        self.assertEqual(room.room_number, 305)
        self.assertEqual(room.room_class, "A")


class RoomDeleteTest(TestCase):
    def setUp(self):
        Room.objects.create(room_number=305, room_class="A")

    def test_room_update_init_data(self):
        existing = Room.objects.get(room_number=305)
        self.assertEqual(existing.pk, 1)
        self.assertEqual(existing.room_number, 305)
        self.assertEqual(existing.room_class, "A")

    def test_room_delete_right_pk(self):
        # Delete room
        response = self.client.delete("/api/room/1/")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check database
        room = Room.objects.filter().exists()
        self.assertEqual(room, False)

    def test_room_delete_wrong_pk(self):
        # Delete room
        response = self.client.delete("/api/room/0/")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

        # Check database
        room = Room.objects.filter().exists()
        self.assertEqual(room, True)

    # def test_room_update_right_room_number_with_wrong_room_class(self):
    #     # Update existing room
    #     data = json.dumps({"room_number": 333, "room_class": "E"})
    #     response = self.client.put("/api/room/1/", data, content_type="application/json")
    #
    #     # Check response
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['room_class'][0], '"E" is not a valid choice.')
    #
    #     # Check database
    #     room = Room.objects.get(pk=1)
    #     self.assertEqual(room.room_number, 305)
    #     self.assertEqual(room.room_class, "A")
    #
    # def test_room_update_wrong_room_number_with_right_room_class(self):
    #     # Update existing room
    #     data = json.dumps({"room_number": 0, "room_class": "D"})
    #     response = self.client.put("/api/room/1/", data, content_type="application/json")
    #
    #     # Check response
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['room_number'][0], "The room number must be an integer between 0 and 1 000 000.")
    #
    #     # Check database
    #     room = Room.objects.get(pk=1)
    #     self.assertEqual(room.room_number, 305)
    #     self.assertEqual(room.room_class, "A")
