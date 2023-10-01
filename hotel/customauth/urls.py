from customauth import views as auth_view
from django.urls import path

urlpatterns = [
    path("user", auth_view.user_log_sign_page, name="userloginpage"),
    path("user/login", auth_view.user_log_sign_page, name="userloginpage"),
    path("user/signup", auth_view.user_sign_up, name="usersignup"),
    path("staff/", auth_view.staff_log_sign_page, name="staffloginpage"),
    path("staff/login", auth_view.staff_log_sign_page, name="staffloginpage"),
    path("staff/signup", auth_view.staff_sign_up, name="staffsignup"),
    path("logout", auth_view.logoutuser, name="logout"),
]