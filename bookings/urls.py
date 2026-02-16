from django.urls import path
from .views import book_consultation, booking_success

urlpatterns = [
    path("", book_consultation, name="book_consultation"),
    path("success/", booking_success, name="booking_success"),

]
