from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "time", "phone")
    list_filter = ("date",)
    search_fields = ("name", "phone", "email")
