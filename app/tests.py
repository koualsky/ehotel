from django.test import TestCase
from rest_framework import status
import json
import pytz
from datetime import datetime, timedelta
from .models import Room, Booking


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


# class BookingListTest(TestCase):


class BookingCreateTest(TestCase):
    def setUp(self):
        Room.objects.create(room_number=305, room_class="A")

    def test_booking_create_with_all_wrong_values(self):
        # Create
        data = json.dumps({
            "rooms": "",
            "first_name": "",
            "last_name": "",
            "reservation_from": "",
            "reservation_to": ""
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["rooms"][0], 'Expected a list of items but got type "str".')
        self.assertEqual(response.data["first_name"][0], 'This field may not be blank.')
        self.assertEqual(response.data["last_name"][0], 'This field may not be blank.')
        self.assertEqual(response.data["reservation_from"][0], 'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].')
        self.assertEqual(response.data["reservation_to"][0], 'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].')

        # Check database
        booking = Booking.objects.filter().exists()
        self.assertEqual(booking, False)

    def test_booking_create_with_all_right_values(self):
        # Create
        today = datetime(2021, 10, 7)
        tomorrow = datetime(2021, 10, 8)
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        response_id = response.data["id"]
        response_first_name = response.data["first_name"]
        response_last_name = response.data["last_name"]
        response_reservation_from = datetime.strptime(response.data["reservation_from"], '%Y-%m-%dT%H:%M:%S')
        response_reservation_to = datetime.strptime(response.data["reservation_to"], '%Y-%m-%dT%H:%M:%S')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_id, 1)
        self.assertEqual(response_first_name, "John")
        self.assertEqual(response_last_name, "Doe")
        self.assertEqual(response_reservation_from, today)
        self.assertEqual(response_reservation_to, tomorrow)

        # Check database
        from_database = Booking.objects.get(pk=1)
        self.assertEqual(from_database.id, 1)
        self.assertEqual(from_database.first_name, "John")
        self.assertEqual(from_database.last_name, "Doe")
        self.assertEqual(from_database.reservation_from, today)
        self.assertEqual(from_database.reservation_to, tomorrow)

    def test_booking_create_with_all_right_values_and_without_right_rooms(self):
        # Create
        today = datetime(2021, 10, 7)
        tomorrow = datetime(2021, 10, 8)
        data = json.dumps({
            "rooms": [],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['rooms'][0], 'This list may not be empty.')

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)

    def test_booking_create_with_all_right_values_and_without_right_reservation_from(self):
        # Create
        today = "2021-10-07"
        tomorrow = datetime(2021, 10, 8)
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today,
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)

    def test_booking_create_with_all_right_values_and_without_right_reservation_to(self):
        # Create
        today = datetime(2021, 10, 7)
        tomorrow = 'Monday'
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)

    def test_booking_create_booking_for_two_rooms(self):
        # Add second room
        Room.objects.create(room_number=306, room_class="B")

        # Create
        today = datetime(2021, 10, 7)
        tomorrow = datetime(2021, 10, 11)
        data = json.dumps({
            "rooms": [1, 2],
            "first_name": "Jimmy",
            "last_name": "Zoe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        response_id = response.data["id"]
        response_first_name = response.data["first_name"]
        response_last_name = response.data["last_name"]
        response_reservation_from = datetime.strptime(response.data["reservation_from"], '%Y-%m-%dT%H:%M:%S')
        response_reservation_to = datetime.strptime(response.data["reservation_to"], '%Y-%m-%dT%H:%M:%S')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_id, 1)
        self.assertEqual(response_first_name, "Jimmy")
        self.assertEqual(response_last_name, "Zoe")
        self.assertEqual(response_reservation_from, today)
        self.assertEqual(response_reservation_to, tomorrow)

        # Check database
        from_database = Booking.objects.get(pk=1)
        self.assertEqual(from_database.id, 1)
        self.assertEqual(from_database.first_name, "Jimmy")
        self.assertEqual(from_database.last_name, "Zoe")
        self.assertEqual(from_database.reservation_from, today)
        self.assertEqual(from_database.reservation_to, tomorrow)

    def test_booking_create_reservation_to_equal_to_reservation_from(self):
        # Create
        today = datetime(2021, 10, 7)
        tomorrow = datetime(2021, 10, 7)
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)

    def test_booking_create_reservation_to_before_reservation_from(self):
        # Create
        today = datetime(2021, 10, 7)
        tomorrow = datetime(2021, 10, 6)
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)

    def test_booking_create_with_empty_reservation_to(self):
        # Create
        today = datetime(2021, 10, 7)
        tomorrow = None
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today.isoformat(),
            "reservation_to": tomorrow
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)

    def test_booking_create_with_empty_reservation_from(self):
        # Create
        today = None
        tomorrow = datetime(2021, 10, 8)
        data = json.dumps({
            "rooms": [1],
            "first_name": "John",
            "last_name": "Doe",
            "reservation_from": today,
            "reservation_to": tomorrow.isoformat()
        })
        response = self.client.post("/api/booking/", data, content_type="application/json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check database
        from_database = Booking.objects.filter().exists()
        self.assertEqual(from_database, False)
