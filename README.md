# Run
Local: http://127.0.0.1:8000/api/ \
Backend API on heroku: https://eeehotel.herokuapp.com/api/ \
Frontend app on heroku: https://eeehotel-frontend.herokuapp.com/ 

# API

### Room
List:\
GET `/api/room/`

Create:\
POST `/api/room/`\
body example:
```
{
    "room_number": "303",
    "room_class": "A"
}
```

Read:\
GET `/api/room/303/`

Update:\
PUT `/api/room/303/`\
body example:
```
{
    "room_number": "304",
    "room_class": "A"
}
```

Delete:\
DELETE `/api/room/304/`

### Booking
List:\
GET `/api/booking/`

Create:\
POST `/api/booking/`\
body example:
```
{
    "first_name": "Jimmy",
    "last_name": "James",
    "reservation_from": "2021-10-7T00:00",
    "reservation_to": "2021-10-14T00:00",
    "rooms": ["304", "305"]
}
```

Read:\
GET `/api/booking/303/`

Update:\
PUT `/api/booking/303/`\
body example:
```
{
    "first_name": "Jimmy2",
    "last_name": "James2",
    "reservation_from": "2021-10-8T00:00",
    "reservation_to": "2021-10-15T00:00",
    "rooms": ["306", "307"]
}
```

Delete:\
DELETE `/api/booking/{booking_id}/`

# Filter bookings (example)
This GET request:\
`/api/booking/?room_nuber=303&last_name=Lennon&reservation_from=2020-10-7&reservation_to=2020-10-14`

will return all bookings which contains: \
room number - 303\
Last name - Lennon\
Reservation date between Oct 7 2020 and Oct 14 2020.
