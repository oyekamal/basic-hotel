"""
Admin
"""
from django.contrib import admin
from .models import Hotels, Reservation, Rooms

# Register your models here.

admin.site.register(Hotels)
admin.site.register(Reservation)
admin.site.register(Rooms)
