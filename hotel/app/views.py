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


def user_sign_up(request):
    """
    User Sign Up page
    """
    if request.method != "POST":
        return HttpResponse("Access Denied")

    user_name = request.POST["username"]

    password1 = request.POST["password1"]
    password2 = request.POST["password2"]

    if password1 != password2:
        messages.warning(request, "Password didn't matched")
        return redirect("userloginpage")

    try:
        if User.objects.all().get(username=user_name):
            messages.warning(request, "Username Not Available")
            return redirect("userloginpage")
    except:
        pass

    new_user = User.objects.create_user(username=user_name, password=password1)
    new_user.is_superuser = False
    new_user.is_staff = False
    new_user.save()
    messages.success(request, "Registration Successfull")
    return redirect("userloginpage")


def staff_sign_up(request):
    """
    Staff Sign up page
    """
    if request.method != "POST":
        return HttpResponse("Access Denied")

    user_name = request.POST["username"]

    password1 = request.POST["password1"]
    password2 = request.POST["password2"]

    if password1 != password2:
        messages.success(request, "Password didn't Matched")
        return redirect("staffloginpage")
    try:
        if User.objects.all().get(username=user_name):
            messages.warning(request, "Username Already Exist")
            return redirect("staffloginpage")
    except:
        pass

    new_user = User.objects.create_user(username=user_name, password=password1)
    new_user.is_superuser = False
    new_user.is_staff = True
    new_user.save()
    messages.success(request, " Staff Registration Successfull")
    return redirect("staffloginpage")


def user_log_sign_page(request):
    """
    User SignUp/ Login Page
    """
    if request.method != "POST":
        response = render(request, "user/user_login_signup.html")
        return HttpResponse(response)

    email = request.POST["email"]
    password = request.POST["pswd"]

    user = authenticate(username=email, password=password)
    try:
        if user.is_staff:
            messages.error(request, "Incorrect username or Password")
            return redirect("staffloginpage")
    except:
        pass

    if user is not None:
        login(request, user)
        messages.success(request, "successful logged in")
        print("Login successfull")
        return redirect("HomePage")

    messages.warning(request, "Incorrect username or password")
    return redirect("userloginpage")


def logoutuser(request):
    """
    Logout user
    """
    if request.method != "GET":
        print("logout unsuccessfull")
        return redirect("userloginpage")

    logout(request)
    messages.success(request, "Logged out successfully")
    print("Logged out successfully")
    return redirect("HomePage")


def staff_log_sign_page(request):
    """
    Staff login page
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user.is_staff:
            login(request, user)
            return redirect("staffpanel")

        else:
            messages.success(request, "Incorrect username or password")
            return redirect("staffloginpage")
    response = render(request, "staff/staff_login_signup.html")
    return HttpResponse(response)


@login_required(login_url="/staff")
def panel(request):
    """
    Staff Panel Page
    """
    if request.user.is_staff == False:
        return HttpResponse("Access Denied")

    rooms = Rooms.objects.all()
    total_rooms: int = len(rooms) if len(rooms) > 0 else 1
    available_rooms: int = len(Rooms.objects.all().filter(availability_status="1"))
    unavailable_rooms: int = len(Rooms.objects.all().filter(availability_status="2"))
    reserved: int = len(Reservation.objects.all())

    hotel = Hotels.objects.values_list("hotel_location", "id").distinct().order_by()

    response = render(
        request,
        "staff/staff_panel.html",
        {
            "location": hotel,
            "reserved": reserved,
            "rooms": rooms,
            "total_rooms": total_rooms,
            "available": available_rooms,
            "unavailable": unavailable_rooms,
        },
    )
    return HttpResponse(response)


@login_required(login_url="/staff")
def edit_room(request):
    """
    Update the room information
    """

    if request.user.is_staff == False:
        return HttpResponse("Access Denied")

    if request.method == "POST" and request.user.is_staff:
        print(request.POST)
        old_room = Rooms.objects.all().get(id=int(request.POST["roomid"]))
        hotel = Hotels.objects.all().get(id=int(request.POST["hotel"]))
        old_room.room_type = request.POST["roomtype"]
        old_room.max_capacity = int(request.POST["capacity"])
        old_room.room_price = int(request.POST["price"])
        old_room.room_size = int(request.POST["size"])
        old_room.hotel = hotel
        old_room.availability_status = request.POST["status"]
        old_room.room_number = int(request.POST["roomnumber"])

        old_room.save()
        messages.success(request, "Room Details Updated Successfully")
        return redirect("staffpanel")

    room_id = request.GET["roomid"]
    room = Rooms.objects.all().get(id=room_id)
    response = render(request, "staff/edit_room.html", {"room": room})
    return HttpResponse(response)


@login_required(login_url="/staff")
def add_new_room(request):
    """
    Add new room to the list
    """
    if request.user.is_staff == False:
        return HttpResponse("Access Denied")
    if request.method == "POST":
        total_rooms = len(Rooms.objects.all())
        new_room = Rooms()
        hotel = Hotels.objects.all().get(id=int(request.POST["hotel"]))
        print(f"id={hotel.id}")
        print(f"name={hotel.hotel_name}")

        new_room.room_number = total_rooms + 1
        new_room.room_type = request.POST["roomtype"]
        new_room.max_capacity = int(request.POST["capacity"])
        new_room.room_size = int(request.POST["size"])
        new_room.hotel = hotel
        new_room.availability_status = request.POST["status"]
        new_room.room_price = request.POST["price"]

        new_room.save()
        messages.success(request, "New Room Added Successfully")

    return redirect("staffpanel")


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


@login_required(login_url="/staff")
def view_room(request):
    """
    View Room
    """
    room_id = request.GET["roomid"]
    room = Rooms.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(
        render(
            request, "staff/view_room.html", {"room": room, "reservations": reservation}
        )
    )


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


@login_required(login_url="/staff")
def add_new_location(request):
    """
    Add new location to the list
    """
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST["new_owner"]
        location = request.POST["new_city"]
        state = request.POST["new_state"]
        country = request.POST["new_country"]

        hotels = Hotels.objects.all().filter(hotel_location=location, hotel_state=state)
        if hotels:
            messages.warning(request, "Sorry City at this Location already exist")
            return redirect("staffpanel")

        new_hotel = Hotels()
        new_hotel.hotel_owner = owner
        new_hotel.hotel_location = location
        new_hotel.hotel_state = state
        new_hotel.hotel_country = country
        new_hotel.save()
        messages.success(request, "New Location Has been Added Successfully")
        return redirect("staffpanel")

    return HttpResponse("Not Allowed")


@login_required(login_url="/staff")
def all_bookings(request):
    """
    Show all bookings
    Staff login required
    """
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(
        render(request, "staff/all_bookings.html", {"bookings": bookings})
    )
