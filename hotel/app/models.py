"""
Database Models
"""
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Hotels(models.Model):
    """
    Hotels Info
    Hotel Name, Owner Name, Location, State Country
    """

    hotel_name = models.CharField(max_length=30, default="Naif")
    hotel_owner = models.CharField(max_length=20)
    hotel_location = models.CharField(max_length=50)
    hotel_state = models.CharField(max_length=50, default="Dubai")
    hotel_country = models.CharField(max_length=50, default="UAE")

    def __str__(self):
        return self.hotel_name


class Rooms(models.Model):
    """
    Rooms in the hotel
    Room Type
    Room Availability
    Maximum Capacity
    """

    AVAILABILITY: tuple = (
        ("1", "Available"),
        ("2", "Not Available"),
    )

    ROOM_TYPE: tuple = (
        ("1", "Suite"),
        ("2", "Penthouse"),
        ("3", "Quad Bedroom"),
    )

    room_type = models.CharField(max_length=50, choices=ROOM_TYPE)
    max_capacity = models.IntegerField()
    room_price = models.IntegerField()
    room_size = models.IntegerField()
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    availability_status = models.CharField(choices=AVAILABILITY, max_length=15)
    room_number = models.IntegerField()

    def __str__(self):
        return self.hotel.hotel_name


class Reservation(models.Model):
    """
    Reservation of the room
    """

    check_in_date = models.DateField(auto_now=False)
    check_out_date = models.DateField()
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)

    booking_id = models.CharField(max_length=100, default="null")

    def __str__(self):
        return self.guest.username
