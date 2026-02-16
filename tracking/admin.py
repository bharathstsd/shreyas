# from django.contrib import admin
# from .models import Coach, Client, WeeklyCheckin


# @admin.register(Coach)
# class CoachAdmin(admin.ModelAdmin):
#     list_display = ("name", "mobile", "parent_coach")
#     search_fields = ("name", "mobile")


# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ("name", "mobile", "coach", "start_date")
#     search_fields = ("name", "mobile")
#     list_filter = ("coach",)


# @admin.register(WeeklyCheckin)
# class WeeklyCheckinAdmin(admin.ModelAdmin):
#     list_display = ("client", "checkin_date", "weight", "body_fat_percent")
#     list_filter = ("checkin_date", "client__coach")


from django.contrib import admin
from .models import Person, WeeklyCheckin


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "role", "sponsor", "start_date")
    search_fields = ("name", "mobile")
    list_filter = ("role",)


@admin.register(WeeklyCheckin)
class WeeklyCheckinAdmin(admin.ModelAdmin):
    list_display = ("person", "date", "weight", "body_fat_percent")
    list_filter = ("date",)
