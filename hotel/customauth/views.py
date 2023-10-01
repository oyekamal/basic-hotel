import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Hotels, Rooms, Reservation
from app.exceptions import (
    RenderingHotels,
    UserNameNotAvailable,
    UserNameAlreadyExists,
    IncorrectCredentials,
)

# Create your views here.
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

