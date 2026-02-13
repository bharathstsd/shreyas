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
