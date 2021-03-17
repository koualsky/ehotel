from django.db import models


ROOM_CLASSES = {"A": 200, "B": 150, "C": 100, "D": 50}


class Room(models.Model):
    room_number = models.PositiveIntegerField(unique=True)
    room_class = models.CharField(
        max_length=32,
        choices=[(key, key) for key, value in ROOM_CLASSES.items()],
        default="A",
    )

    def __str__(self):
        return str(self.room_number)


class Booking(models.Model):
    rooms = models.ManyToManyField(Room)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    reservation_from = models.DateTimeField()
    reservation_to = models.DateTimeField()

    def __str__(self):
        return str(
            "{} {} (from {} to {})".format(
                self.first_name,
                self.last_name,
                self.reservation_from,
                self.reservation_to,
            )
        )
