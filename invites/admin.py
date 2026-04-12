# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Invite

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "customer_phone",
        "coach_name",
        "event_date",
        "created_at",
    )
    search_fields = ("customer_name", "coach_name", "customer_phone")
