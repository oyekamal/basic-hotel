"""
Views of the website
"""
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Hotels, Rooms, Reservation
from .exceptions import (
    RenderingHotels,
    UserNameNotAvailable,
    UserNameAlreadyExists,
    IncorrectCredentials,
)

# Create your views here.


def home(request):
    """
    Home Page of the website
    """
    all_location = (
        Hotels.objects.values_list("hotel_location", "id").distinct().order_by()
    )
    if request.method != "POST":
        data: dict = {"all_location": all_location}
        response = render(request, "index.html", data)
        return HttpResponse(response)

    try:
        hotels: list = Hotels.objects.all().get(
            id=int(float(request.POST["search_location"]))
        )
        room_reservations: list = []

        # for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all():
            if str(each_reservation.check_in_date) < str(request.POST["cin"]) and str(
                each_reservation.check_out_date
            ) < str(request.POST["cout"]):
                pass
            elif str(each_reservation.check_in_date) > str(request.POST["cin"]) and str(
                each_reservation.check_out_date
            ) > str(request.POST["cout"]):
                pass
            else:
                room_reservations.append(each_reservation.room.id)

        rooms: list = (
            Rooms.objects.all()
            .filter(hotel=hotels, max_capacity=int(request.POST["capacity"]))
            .exclude(id__in=room_reservations)
        )

        if len(rooms) == 0:
            messages.warning(
                request, "Sorry No Rooms Are Available on this time period"
            )
        data = {"rooms": rooms, "all_location": all_location, "flag": True}
        response = render(request, "index.html", data)
    except RenderingHotels as e_x:
        messages.error(request, e_x)
        response = render(request, "index.html", {"all_location": all_location})

    return HttpResponse(response)


def about_us(request):
    """
    About us page
    """
    return HttpResponse(render(request, "about.html"))


def contact(request):
    """
    Contact page
    """
    return HttpResponse(render(request, "contact.html"))




@login_required(login_url="/user")
def book_room_page(request):
    """
    Book page
    """
    room = Rooms.objects.all().get(id=int(request.GET["roomid"]))
    return HttpResponse(render(request, "user/book_room.html", {"room": room}))


@login_required(login_url="/user")
def book_room(request):
    """
    Booking of the room
    """
    if request.method != "POST":
        return HttpResponse("Access Denied")

    room_id = request.POST["room_id"]

    room = Rooms.objects.all().get(id=room_id)
    # for finding the reserved rooms on this time period for excluding from the query set
    for each_reservation in Reservation.objects.all().filter(room=room):
        if str(each_reservation.check_in_date) < str(request.POST["check_in"]) and str(
            each_reservation.check_out_date
        ) < str(request.POST["check_out"]):
            pass
        elif str(each_reservation.check_in_date) > str(
            request.POST["check_in"]
        ) and str(each_reservation.check_out_date) > str(request.POST["check_out"]):
            pass
        else:
            messages.warning(request, "Sorry This Room is unavailable for Booking")
            return redirect("HomePage")

    current_user = request.user

    reservation = Reservation()
    room_object = Rooms.objects.all().get(id=room_id)
    room_object.availability_status = "2"

    user_object = User.objects.all().get(username=current_user)

    reservation.guest = user_object
    reservation.room = room_object

    reservation.check_in_date = request.POST["check_in"]
    reservation.check_out_date = request.POST["check_out"]

    reservation.save()

    messages.success(request, "Congratulations! Booking Successfull")

    return redirect("HomePage")


def handler404(request):
    """
    404 Page
    """
    return render(request, "404.html", status=404)


@login_required(login_url="/user")
def user_bookings(request):
    """
    Book the room
    """
    if request.user.is_authenticated == False:
        return redirect("userloginpage")
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(
        render(request, "user/my_bookings.html", {"bookings": bookings})
    )


