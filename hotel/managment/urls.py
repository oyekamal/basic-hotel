from managment import views as managment_view
from django.urls import path, include

urlpatterns = [
    path("staff/panel", managment_view.panel, name="staffpanel"),
    path("staff/allbookings", managment_view.all_bookings, name="allbookigs"),
    path("staff/panel/add-new-location", managment_view.add_new_location, name="addnewlocation"),
    path("staff/panel/edit-room", managment_view.edit_room),
    path("staff/panel/add-new-room", managment_view.add_new_room, name="addroom"),
    path("staff/panel/edit-room/edit", managment_view.edit_room),
    path("staff/panel/view-room", managment_view.view_room),
]