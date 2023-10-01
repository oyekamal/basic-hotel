from django.urls import path
from app import views
urlpatterns = [
    path("", views.home, name="HomePage"),
    path("about", views.about_us, name="aboutpage"),
    path("contact", views.contact, name="contact"),
    path("user/bookings", views.user_bookings, name="dashboard"),
    path("user/book-room", views.book_room_page, name="bookroompage"),
    path("user/book-room/book", views.book_room, name="bookroom"),
]
