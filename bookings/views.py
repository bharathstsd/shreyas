from django.shortcuts import render, redirect
from .models import Appointment
from django.core.mail import send_mail
from datetime import time, datetime, date
from urllib.parse import quote
from .zoom import create_zoom_meeting
from django.conf import settings
from django.core.mail import EmailMessage
from ics import Calendar, Event
from datetime import timedelta



TIME_SLOTS = [
    time(10, 0),
    time(11, 0),
    time(12, 0),
    time(16, 0),
    time(17, 0),
    time(18, 0),
]

def book_consultation(request):
    form_data = request.GET.copy()
    selected_date = form_data.get("date")
    selected_time = form_data.get("time")

    booked_times = []

    if selected_date:
        booked_times = Appointment.objects.filter(
            date=selected_date
        ).values_list("time", flat=True)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        selected_date = request.POST.get("date")
        time_str = request.POST.get("time")

        if name and email and phone and selected_date and time_str:
            time_obj = datetime.strptime(time_str, "%H:%M").time()

            exists = Appointment.objects.filter(
                date=selected_date,
                time=time_obj
            ).exists()

            if exists:
                return render(request, "book.html", {
                    "error": "This time slot is already booked.",
                    "time_slots": TIME_SLOTS,
                    "booked_times": booked_times,
                    "today": date.today().isoformat(),
                    "form_data": request.POST,
                })

            zoom_link = create_zoom_meeting(
                topic=f"Consultation with {name}",
                start_time=f"{selected_date}T{time_str}:00"
            )

            Appointment.objects.create(
                name=name,
                email=email,
                phone=phone,
                date=selected_date,
                time=time_obj,
                zoom_link=zoom_link
            )

            # Calendar event
            start_dt = datetime.strptime(
                f"{selected_date} {time_str}", "%Y-%m-%d %H:%M"
            )
            end_dt = start_dt + timedelta(minutes=30)

            cal = Calendar()
            event = Event()
            event.name = "Shreyas Wellness Consultation"
            event.begin = start_dt
            event.end = end_dt
            event.description = f"Zoom link: {zoom_link}"
            cal.events.add(event)

            ics_content = str(cal)

            # Email with calendar
            email_msg = EmailMessage(
                "Consultation Booking Confirmed",
                f"Hi {name},\n\nYour consultation is confirmed.\n\nZoom: {zoom_link}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            email_msg.attach("consultation.ics", ics_content, "text/calendar")
            email_msg.send(fail_silently=True)

            # Admin email
            send_mail(
                "New Consultation Booked",
                f"{name} booked on {selected_date} at {time_str}",
                settings.DEFAULT_FROM_EMAIL,
                ["bharathtsd@gmail.com"],
                fail_silently=True,
            )

            return redirect(
                f"/book/success/?date={selected_date}&time={time_str}&zoom={zoom_link}"
            )

    return render(request, "book.html", {
        "time_slots": TIME_SLOTS,
        "booked_times": booked_times,
        "today": date.today().isoformat(),
        "form_data": form_data,
    })

# def book_consultation(request):
#     selected_date = request.GET.get("date")
#     booked_times = []

#     if selected_date:
#         booked_times = Appointment.objects.filter(
#             date=selected_date
#         ).values_list("time", flat=True)

#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         selected_date = request.POST.get("date")
#         time_str = request.POST.get("time")

#         if name and email and phone and selected_date and time_str:
#             time_obj = datetime.strptime(time_str, "%H:%M").time()

#             # Prevent double booking
#             exists = Appointment.objects.filter(
#                 date=selected_date,
#                 time=time_obj
#             ).exists()

#             if exists:
#                 return render(request, "book.html", {
#                     "error": "This time slot is already booked.",
#                     "time_slots": TIME_SLOTS,
#                     "booked_times": booked_times,
#                     "today": date.today().isoformat(),
#                     "form_data": request.POST,
#                 })

#             # Create Zoom meeting
#             zoom_link = create_zoom_meeting(
#                 topic=f"Consultation with {name}",
#                 start_time=f"{selected_date}T{time_str}:00"
#             )

#             # Save appointment
#             Appointment.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 date=selected_date,
#                 time=time_obj,
#                 zoom_link=zoom_link
#             )

#             # Email content
#             # Email subject
#             subject = "Consultation Booking Confirmed"

#             user_message = (
#                 f"Hi {name},\n\n"
#                 f"Your consultation is confirmed.\n\n"
#                 f"Date: {selected_date}\n"
#                 f"Time: {time_str}\n"
#                 f"Zoom Link: {zoom_link}\n\n"
#                 "Please join on time.\n"
#                 "- Shreyas Wellness"
#             )

#             # Create calendar event
#             start_dt = datetime.strptime(
#                 f"{selected_date} {time_str}", "%Y-%m-%d %H:%M"
#             )
#             end_dt = start_dt + timedelta(minutes=30)

#             cal = Calendar()
#             event = Event()
#             event.name = "Shreyas Wellness Consultation"
#             event.begin = start_dt
#             event.end = end_dt
#             event.description = f"Zoom link: {zoom_link}"
#             cal.events.add(event)

#             ics_content = str(cal)

#             # Send email with calendar invite
#             email_msg = EmailMessage(
#                 subject,
#                 user_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#             )

#             email_msg.attach(
#                 "consultation.ics",
#                 ics_content,
#                 "text/calendar"
#             )

#             email_msg.send(fail_silently=False)

#             admin_message = (
#                 "New consultation booked.\n\n"
#                 f"Name: {name}\n"
#                 f"Email: {email}\n"
#                 f"Phone: {phone}\n"
#                 f"Date: {selected_date}\n"
#                 f"Time: {time_str}\n"
#                 f"Zoom Link: {zoom_link}"
#             )

#             # Send emails
#             send_mail(
#                 subject,
#                 user_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False,
#             )

#             send_mail(
#                 "New Consultation Booked",
#                 admin_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 ["bharathtsd@gmail.com"],
#                 fail_silently=False,
#             )

#             # WhatsApp redirect
#             message = quote(
#                 f"Hi, my consultation is booked on {selected_date} at {time_str}."
#             )

#             # return redirect(
#             #     f"https://wa.me/919666615225?text={message}"
#             # )
#             # return redirect("booking_success")
#             return redirect(f"/book/success/?date={selected_date}&time={time_str}&zoom={zoom_link}")



#     return render(request, "book.html", {
#         "time_slots": TIME_SLOTS,
#         "booked_times": booked_times,
#         "today": date.today().isoformat(),
#         # "form_data": request.GET,
#         "form_data": request.POST or request.GET,

#     })


from datetime import datetime, timedelta


def booking_success(request):
    date_str = request.GET.get("date")
    time_str = request.GET.get("time")
    zoom = request.GET.get("zoom")

    calendar_link = ""

    if date_str and time_str:
        # combine date + time
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(minutes=30)

        start = start_dt.strftime("%Y%m%dT%H%M%S")
        end = end_dt.strftime("%Y%m%dT%H%M%S")

        calendar_link = (
            "https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text=Shreyas+Wellness+Consultation"
            f"&dates={start}/{end}"
            f"&details=Zoom+Link:+{zoom}"
        )

    return render(request, "booking_success.html", {
        "date": date_str,
        "time": time_str,
        "zoom": zoom,
        "calendar_link": calendar_link,
    })



# def book_consultation(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         date = request.POST.get("date")
#         # time_str = request.POST.get("time")
#         time_str = request.POST.get("time")
#         time_obj = datetime.strptime(time_str, "%H:%M").time()


#         if name and email and phone and date and time_str:
#             # Prevent double booking
#             exists = Appointment.objects.filter(
#                 date=date,
#                 time=time_obj
#             ).exists()

#             if exists:
#                 return render(request, "book.html", {
#                     "error": "This time slot is already booked.",
#                     "time_slots": TIME_SLOTS
#                 })

#             # Temporary Zoom placeholder
#             # zoom_link = "https://zoom.us/j/1234567890"
#             zoom_link = create_zoom_meeting(
#                 topic=f"Consultation with {name}",
#                 start_time=f"{date}T{time_str}:00"
#             )

#             appointment = Appointment.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 date=date,
#                 time=time_obj,
#                 zoom_link=zoom_link
#             )

#             # Send email to user
#             send_mail(
#                 "Your Consultation is Booked",
#                 f"Hi {name},\n\nYour consultation is confirmed.\n\n"
#                 f"Date: {date}\n"
#                 f"Time: {time_str}\n"
#                 f"Zoom Link: {zoom_link}\n\n"
#                 "See you soon!",
#                 "your@email.com",
#                 [email],
#                 fail_silently=False,
#             )

#             # WhatsApp redirect
#             message = quote(
#                 f"Hi, my consultation is booked on {date} at {time_str}."
#             )

#             return redirect(
#                 f"https://wa.me/919666615225?text={message}"
#             )

#     return render(request, "book.html", {
#         "time_slots": TIME_SLOTS
#     })
