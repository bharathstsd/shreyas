# from django.shortcuts import render, redirect
# from .models import Coach, Program, Testimonial, Lead


# def home(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")

#         if name and email:
#             Lead.objects.create(name=name, email=email)
#             return redirect('/')

#     context = {
#         # "coach": Coach.objects.first(),
#         "coach": Coach.objects.filter(is_head_coach=True).first(),
#         "programs": Program.objects.all(),
#         # "testimonials": Testimonial.objects.all(),
#         "testimonials": Testimonial.objects.filter(show_on_homepage=True),
#         # "featured": Testimonial.objects.filter(is_featured=True).first(),
#         "featured": Testimonial.objects.filter(is_featured=True)[:5],

#     }
#     return render(request, "home.html", context)


# from django.shortcuts import render, redirect
# from .models import Coach, Program, Testimonial, Lead
# from urllib.parse import quote


# def home(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         goal = request.POST.get("goal")

#         if name and email:
#             Lead.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 goal=goal
#             )

#             # WhatsApp redirect message
#             message = quote(
#                 f"Hi, I’m {name}. I’m interested in a consultation for {goal}."
#             )

#             return redirect(f"https://wa.me/919666615225?text={message}")

#     context = {
#         "coach": Coach.objects.filter(is_head_coach=True).first(),
#         "programs": Program.objects.all(),
#         "testimonials": Testimonial.objects.filter(show_on_homepage=True),
#         "featured": Testimonial.objects.filter(is_featured=True)[:5],
#     }

#     return render(request, "home.html", context)



from django.shortcuts import render, redirect
from .models import Coach, Program, Testimonial, Lead
from urllib.parse import quote
import threading
from django.core.mail import send_mail
from django.conf import settings


def send_lead_email(name, email, phone, goal):
    try:
        # Admin email
        send_mail(
            subject="New Consultation Request",
            message=f"""
New lead received:

Name: {name}
Email: {email}
Phone: {phone}
Goal: {goal}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["bharathtsd@gmail.com"],
            fail_silently=True,
        )

        # User confirmation
        send_mail(
            subject="Your Consultation Request – Madhura Wellness",
            message=f"""
Hi {name},

Thank you for requesting a consultation with Madhura Wellness.

We have received your details and our coach will contact you shortly.

Your Goal: {goal}

Stay healthy,
Madhura Wellness Team
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

    except Exception as e:
        print("Email error:", e)


def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        goal = request.POST.get("goal")

        if name and email:
            Lead.objects.create(
                name=name,
                email=email,
                phone=phone,
                goal=goal
            )

            # background email
            threading.Thread(
                target=send_lead_email,
                args=(name, email, phone, goal),
                daemon=True
            ).start()

            # WhatsApp redirect
            message = quote(
                f"Hi, I’m {name}. I’m interested in a consultation for {goal}."
            )
            return redirect(f"https://wa.me/919666615225?text={message}")

    context = {
        "coach": Coach.objects.filter(is_head_coach=True).first(),
        "programs": Program.objects.all(),
        "testimonials": Testimonial.objects.filter(show_on_homepage=True),
        "featured": Testimonial.objects.filter(is_featured=True)[:5],
    }

    return render(request, "home.html", context)



def about(request):
    coach = Coach.objects.filter(is_head_coach=True).first()
    coaches = Coach.objects.all()

    context = {
        "coach": coach,
        "coaches": coaches,
    }
    return render(request, "about.html", context)

from django.shortcuts import render
from .models import Coach

def team(request):
    specialization = request.GET.get("specialization")

    if specialization:
        coaches = Coach.objects.filter(specialization=specialization)
    else:
        coaches = Coach.objects.all()

    # get unique specializations for filter bar
    specializations = (
        Coach.objects.values_list("specialization", flat=True)
        .distinct()
    )

    return render(request, "team.html", {
        "coaches": coaches,
        "specializations": specializations,
        "active_specialization": specialization,
    })


from django.shortcuts import render, get_object_or_404
from .models import Coach

def coach_detail(request, slug):
    coach = get_object_or_404(Coach, slug=slug)
    return render(request, "coach_detail.html", {
        "coach": coach
    })



from django.shortcuts import render, get_object_or_404
from .models import Transformation


def transformations_list(request):
    category = request.GET.get("category")

    if category:
        transformations = Transformation.objects.filter(category=category)
    else:
        transformations = Transformation.objects.all()

    context = {
        "transformations": transformations
    }
    return render(request, "list.html", context)


def transformation_detail(request, slug):
    transformation = get_object_or_404(Transformation, slug=slug)

    context = {
        "transformation": transformation
    }
    return render(request, "detail.html", context)

from django.shortcuts import render, get_object_or_404
from .models import GalleryStory


def gallery_list(request):
    category = request.GET.get("category")

    if category:
        stories = GalleryStory.objects.filter(category=category).order_by("-date")
    else:
        stories = GalleryStory.objects.all().order_by("-date")

    context = {
        "stories": stories
    }
    return render(request, "gallerylist.html", context)


def gallery_detail(request, slug):
    story = get_object_or_404(GalleryStory, slug=slug)

    context = {
        "story": story
    }
    return render(request, "gallerydetail.html", context)


# import calendar
# from datetime import date
# from collections import defaultdict
# from django.shortcuts import render
# from .models import CalendarMonth


# def calendar_page(request):
#     month_obj = CalendarMonth.objects.filter(is_active=True).first()

#     if not month_obj:
#         return render(request, "calendar.html", {"month": None})

#     year = month_obj.year
#     month = month_obj.month

#     # Get month calendar matrix
#     cal = calendar.Calendar(firstweekday=0)  # Monday start
#     month_days = cal.monthdatescalendar(year, month)

#     # Group events by date
#     events = month_obj.events.all()
#     event_dict = defaultdict(list)
#     for event in events:
#         event_dict[event.date].append(event)

#     context = {
#         "month": month_obj,
#         "month_days": month_days,
#         "event_dict": dict(event_dict),
#         "today": date.today(),
#     }

#     return render(request, "calendar.html", context)


import calendar
from datetime import date, datetime
from django.shortcuts import render
from .models import Event


# def calendar_page(request):
#     year = int(request.GET.get("year", date.today().year))
#     month = int(request.GET.get("month", date.today().month))

#     cal = calendar.Calendar(firstweekday=6)
#     month_days = cal.monthdatescalendar(year, month)

#     events = Event.objects.filter(date__year=year, date__month=month)

#     events_by_day = {}
#     for event in events:
#         day = event.date.day
#         events_by_day.setdefault(day, []).append(event)

#     context = {
#         "month_days": month_days,
#         "events_by_day": events_by_day,   # ← match template
#         "month": month,
#         "year": year,
#     }
#     return render(request, "calendar.html", context)


def calendar_page(request):
    # Get month & year from URL
    month = request.GET.get("month")
    year = request.GET.get("year")

    today = date.today()

    if month and year:
        month = int(month)
        year = int(year)
    else:
        month = today.month
        year = today.year

    # Build calendar
    # cal = calendar.Calendar(firstweekday=0)
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    month_days = cal.monthdayscalendar(year, month)

    # Get events
    events = Event.objects.filter(date__year=year, date__month=month)

    events_by_day = {}
    for event in events:
        day = event.date.day
        events_by_day.setdefault(day, []).append(event)

    # Previous & next month logic
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1

    context = {
        "month_days": month_days,
        "month": month,
        "year": year,
        "events_by_day": events_by_day,
        "month_name": calendar.month_name[month],
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year,
    }

    return render(request, "calendar.html", context)


# from django.shortcuts import render, redirect
# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django.conf import settings


# def contact(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         email = request.POST.get("email")
#         message = request.POST.get("message")

#         # Email to you (admin)
#         admin_subject = f"New Contact Form Submission from {name}"
#         admin_message = f"""
# Name: {name}
# Phone: {phone}
# Email: {email}

# Message:
# {message}
# """

#         send_mail(
#             admin_subject,
#             admin_message,
#             settings.DEFAULT_FROM_EMAIL,
#             [bharathtsd@gmail.com],  # your email
#         )

#         # Auto-reply to customer
#         customer_subject = "We received your message | Madhura Wellness"
#         customer_message = f"""
# Hi {name},

# Thank you for contacting Madhura Wellness.

# Our team will get in touch with you shortly.

# If your query is urgent, you can reach us directly:
# Phone: +91 92464 37143
# WhatsApp: https://wa.me/919246437143

# Warm regards,
# Madhura Wellness Team
# """

#         send_mail(
#             customer_subject,
#             customer_message,
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#         )

#         return redirect("/contact/?sent=1")

#     return render(request, "contact.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Email to admin
        admin_subject = f"New Contact Form Submission from {name}"
        admin_message = f"""
Name: {name}
Phone: {phone}
Email: {email}

Message:
{message}
"""

        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )

        # Auto-reply to customer
        if email:
            customer_subject = "We received your message | Madhura Wellness"
            customer_message = f"""
Hi {name},

Thank you for contacting Madhura Wellness.
Our team will get in touch with you shortly.

Phone: +91 92464 37143
WhatsApp: https://wa.me/919246437143

Madhura Wellness Team
"""

            send_mail(
                customer_subject,
                customer_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

        return redirect("/contact/?sent=1")

    return render(request, "contact.html")



# from .models import Program


def programs_list(request):
    programs = Program.objects.all()
    return render(request, "programs.html", {
        "programs": programs
    })


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    return render(request, "program_detail.html", {
        "program": program
    })
