# from django.shortcuts import render, get_object_or_404
# from .models import Coach
# from .services import get_all_clients


# def coach_dashboard(request, coach_id):
#     coach = get_object_or_404(Coach, id=coach_id)
#     clients = get_all_clients(coach)

#     return render(request, "tracking/dashboard.html", {
#         "coach": coach,
#         "clients": clients,
#     })


from django.shortcuts import render, get_object_or_404
from .models import Person, WeeklyCheckin
from .services import get_all_downline_people
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

# @login_required
# def coach_dashboard(request, slug):
#     coach = get_object_or_404(Person, slug=slug, role="coach")

#     downline = get_all_downline_people(coach)
#     clients = [p for p in downline if p.role == "client"]
#     coaches = [p for p in downline if p.role == "coach"]

#     return render(request, "tracking/dashboard.html", {
#         "coach": coach,
#         "clients": clients,
#         "coaches": coaches,
#     })

from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def coach_dashboard(request, slug):
    coach = get_object_or_404(Person, slug=slug, role="coach")

    downline = get_all_downline_people(coach)

    # split roles
    clients = [p for p in downline if p.role == "client"]
    coaches = [p for p in downline if p.role == "coach"]

    # -----------------------
    # Search filter
    # -----------------------
    # search = request.GET.get("search", "")
    # if search:
    #     clients = [
    #         p for p in clients
    #         if search.lower() in p.name.lower()
    #         or search in p.mobile
    #     ]
    # -----------------------
# Search filter
# -----------------------
    search = request.GET.get("search", "")
    search_results = []

    if search:
        search_results = [
            p for p in downline
            if search.lower() in p.name.lower()
            or (p.mobile and search in p.mobile)
        ]


    # -----------------------
    # Today's check-ins
    # -----------------------
    today = timezone.now().date()
    todays_checkins = WeeklyCheckin.objects.filter(
        person__in=downline,
        date=today
    )

    # -----------------------
    # Birthday & Anniversary logic
    # -----------------------
# -----------------------
# Birthday & Anniversary logic
# -----------------------
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)

    all_people = clients + coaches

    today_birthdays = [
        p for p in all_people
        if p.date_of_birth and
        p.date_of_birth.day == today.day and
        p.date_of_birth.month == today.month
    ]

    tomorrow_birthdays = [
        p for p in all_people
        if p.date_of_birth and
        p.date_of_birth.day == tomorrow.day and
        p.date_of_birth.month == tomorrow.month
    ]

    today_anniversaries = [
        p for p in all_people
        if p.anniversary and
        p.anniversary.day == today.day and
        p.anniversary.month == today.month
    ]

    tomorrow_anniversaries = [
        p for p in all_people
        if p.anniversary and
        p.anniversary.day == tomorrow.day and
        p.anniversary.month == tomorrow.month
    ]


    # -----------------------
    # Leaderboard calculations
    # -----------------------
    top_loss = None
    top_gain = None
    top_weekly_loss = None
    top_weekly_gain = None

    loss_results = []
    gain_results = []
    weekly_loss_results = []
    weekly_gain_results = []

    one_week_ago = today - timedelta(days=7)

    for person in clients:
        checkins = person.checkins.order_by("date")

        if checkins.count() >= 2:
            first = checkins.first()
            last = checkins.last()

            # TOTAL
            if person.goal == "weight_loss":
                total_loss = first.weight - last.weight
                if total_loss > 0:
                    loss_results.append((person, total_loss))

            elif person.goal == "weight_gain":
                total_gain = last.weight - first.weight
                if total_gain > 0:
                    gain_results.append((person, total_gain))

            # WEEKLY
            last_week_checkin = checkins.filter(date__lte=one_week_ago).last()
            if last_week_checkin:
                if person.goal == "weight_loss":
                    weekly_loss = last_week_checkin.weight - last.weight
                    if weekly_loss > 0:
                        weekly_loss_results.append((person, weekly_loss))

                elif person.goal == "weight_gain":
                    weekly_gain = last.weight - last_week_checkin.weight
                    if weekly_gain > 0:
                        weekly_gain_results.append((person, weekly_gain))

    # Select top performers
    if loss_results:
        top_loss = sorted(loss_results, key=lambda x: x[1], reverse=True)[0]

    if gain_results:
        top_gain = sorted(gain_results, key=lambda x: x[1], reverse=True)[0]

    if weekly_loss_results:
        top_weekly_loss = sorted(weekly_loss_results, key=lambda x: x[1], reverse=True)[0]

    if weekly_gain_results:
        top_weekly_gain = sorted(weekly_gain_results, key=lambda x: x[1], reverse=True)[0]
   
    return render(request, "tracking/dashboard.html", {
        "coach": coach,
        "todays_checkins": todays_checkins,
        "top_loss": top_loss,
        "top_gain": top_gain,
        "top_weekly_loss": top_weekly_loss,
        "top_weekly_gain": top_weekly_gain,

        "search": search,
        "search_results": search_results,

        "today_birthdays": today_birthdays,
        "tomorrow_birthdays": tomorrow_birthdays,
        "today_anniversaries": today_anniversaries,
        "tomorrow_anniversaries": tomorrow_anniversaries,
    })

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Person

@login_required
def search_people(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        people = Person.objects.filter(
            name__icontains=query
        ) | Person.objects.filter(
            mobile__icontains=query
        )

        people = people.distinct()[:10]

        for p in people:
            results.append({
                "name": p.name,
                "slug": p.slug,
                "role": p.role,
                "mobile": p.mobile,
            })

    return JsonResponse(results, safe=False)





# @login_required
# def coach_dashboard(request, slug):
#     coach = get_object_or_404(Person, slug=slug, role="coach")

#     downline = get_all_downline_people(coach)

#     # split roles
#     clients = [p for p in downline if p.role == "client"]
#     coaches = [p for p in downline if p.role == "coach"]

#     # -----------------------
#     # Search filter
#     # -----------------------
#     search = request.GET.get("search", "")
#     if search:
#         clients = [
#             p for p in clients
#             if search.lower() in p.name.lower()
#             or search in p.mobile
#         ]

#     # -----------------------
#     # Today's check-ins
#     # -----------------------
#     today = timezone.now().date()
#     todays_checkins = WeeklyCheckin.objects.filter(
#         person__in=downline,
#         date=today
#     )

#     # -----------------------
#     # Leaderboard calculations
#     # -----------------------
#     top_loss = None
#     top_gain = None
#     top_weekly_loss = None
#     top_weekly_gain = None

#     loss_results = []
#     gain_results = []
#     weekly_loss_results = []
#     weekly_gain_results = []

#     one_week_ago = today - timedelta(days=7)

#     for person in clients:
#         checkins = person.checkins.order_by("date")

#         if checkins.count() >= 2:
#             first = checkins.first()
#             last = checkins.last()

#             total_change = last.weight - first.weight

#             # WEEKLY
#             last_week_checkin = checkins.filter(date__lte=one_week_ago).last()
#             weekly_change = None
#             if last_week_checkin:
#                 weekly_change = last.weight - last_week_checkin.weight

#             # ---------------- GOAL LOGIC ----------------
#             if person.goal == "weight_loss":
#                 total_loss = first.weight - last.weight
#                 if total_loss > 0:
#                     loss_results.append((person, total_loss))

#                 if weekly_change is not None:
#                     weekly_loss = last_week_checkin.weight - last.weight
#                     if weekly_loss > 0:
#                         weekly_loss_results.append((person, weekly_loss))

#             elif person.goal == "weight_gain":
#                 total_gain = last.weight - first.weight
#                 if total_gain > 0:
#                     gain_results.append((person, total_gain))

#                 if weekly_change is not None:
#                     weekly_gain = last.weight - last_week_checkin.weight
#                     if weekly_gain > 0:
#                         weekly_gain_results.append((person, weekly_gain))

#     # Select top performers
#     if loss_results:
#         top_loss = sorted(loss_results, key=lambda x: x[1], reverse=True)[0]

#     if gain_results:
#         top_gain = sorted(gain_results, key=lambda x: x[1], reverse=True)[0]

#     if weekly_loss_results:
#         top_weekly_loss = sorted(weekly_loss_results, key=lambda x: x[1], reverse=True)[0]

#     if weekly_gain_results:
#         top_weekly_gain = sorted(weekly_gain_results, key=lambda x: x[1], reverse=True)[0]

#     return render(request, "tracking/dashboard.html", {
#         "coach": coach,
#         "clients": clients,
#         "coaches": coaches,
#         "todays_checkins": todays_checkins,
#         "top_loss": top_loss,
#         "top_gain": top_gain,
#         "top_weekly_loss": top_weekly_loss,
#         "top_weekly_gain": top_weekly_gain,
#         "search": search,
#     })

# @login_required
# def coach_dashboard(request, slug):
#     coach = get_object_or_404(Person, slug=slug, role="coach")

#     downline = get_all_downline_people(coach)

#     # split roles
#     clients = [p for p in downline if p.role == "client"]
#     coaches = [p for p in downline if p.role == "coach"]

#     # -----------------------
#     # Search filter
#     # -----------------------
#     search = request.GET.get("search", "")
#     if search:
#         clients = [
#             p for p in clients
#             if search.lower() in p.name.lower()
#             or search in p.mobile
#         ]

#     # -----------------------
#     # Today's check-ins
#     # -----------------------
#     today = timezone.now().date()
#     todays_checkins = WeeklyCheckin.objects.filter(
#         person__in=downline,
#         date=today
#     )

#     # -----------------------
#     # Leaderboard calculations
#     # -----------------------
#     top_overall = None
#     top_weekly = None

#     overall_results = []
#     weekly_results = []

#     for person in clients:
#         checkins = person.checkins.order_by("date")

#         if checkins.count() >= 2:
#             first = checkins.first()
#             last = checkins.last()

#             overall_loss = first.weight - last.weight
#             overall_results.append((person, overall_loss))

#             # weekly loss
#             one_week_ago = today - timedelta(days=7)
#             last_week_checkin = checkins.filter(date__lte=one_week_ago).last()

#             if last_week_checkin:
#                 weekly_loss = last_week_checkin.weight - last.weight
#                 weekly_results.append((person, weekly_loss))

#     if overall_results:
#         top_overall = sorted(overall_results, key=lambda x: x[1], reverse=True)[0]

#     if weekly_results:
#         top_weekly = sorted(weekly_results, key=lambda x: x[1], reverse=True)[0]

#     return render(request, "tracking/dashboard.html", {
#         "coach": coach,
#         "clients": clients,
#         "coaches": coaches,
#         "todays_checkins": todays_checkins,
#         "top_overall": top_overall,
#         "top_weekly": top_weekly,
#         "search": search,
#     })

from .forms import WeeklyCheckinForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.http import HttpResponse

# from .models import Person
# from .forms import WeeklyCheckinForm

@login_required
def client_profile(request, slug):
    person = get_object_or_404(Person, slug=slug)
    checkins = person.checkins.order_by("-date")

    form = WeeklyCheckinForm()

    if request.method == "POST":
        form = WeeklyCheckinForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.person = person
            checkin.save()
            return redirect("client_profile", slug=person.slug)

    # ------------------------
    # Comparison logic
    # ------------------------
    latest = None
    previous = None
    change = None

    if checkins.count() >= 1:
        latest = checkins.first()

    if checkins.count() >= 2:
        previous = checkins[1]
        change = latest.weight - previous.weight

    # ------------------------
    # PDF export
    # ------------------------
  # PDF export
    # ------------------------
# PDF export
# ------------------------
    if request.GET.get("export") == "pdf":
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        elements = []
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph(f"<b>{person.name} Progress Report</b>", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 15))

        # Comparison
        if latest and previous:
            comp_text = (
                f"<b>Latest:</b> {latest.date} – {latest.weight} kg<br/>"
                f"<b>Previous:</b> {previous.date} – {previous.weight} kg<br/>"
                f"<b>Change:</b> {change:.1f} kg"
            )
            comp = Paragraph(comp_text, styles["Normal"])
            elements.append(comp)
            elements.append(Spacer(1, 15))

        # Table data
        data = [
            [
                "Date",
                "Wt",
                "Fat%",
                "FatKg",
                "Vis",
                "RMR",
                "BMI",
                "BMA",
                "SubFat",
                "Trunk",
                "Muscle",
                "Fluid%",
                "Excess",
            ]
        ]

        for c in checkins:
            data.append([
                str(c.date),
                c.weight,
                c.body_fat_percent,
                c.body_fat_mass,
                c.visceral_fat,
                c.rmr,
                c.bmi,
                c.bma,
                c.subcutaneous_fat,
                c.trunk_fat,
                c.muscle_mass,
                c.body_fluid_percent,
                c.excess_fluid,
            ])

        table = Table(data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ]))

        elements.append(table)

        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(
            buffer,
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{person.slug}.pdf"'
            },
        )



    return render(request, "tracking/client_profile.html", {
        "person": person,
        "checkins": checkins,
        "form": form,
        "latest": latest,
        "previous": previous,
        "change": change,
    })


# def client_profile(request, slug):
#     person = get_object_or_404(Person, slug=slug)
#     checkins = person.checkins.order_by("-date")

#     form = WeeklyCheckinForm()

#     if request.method == "POST":
#         form = WeeklyCheckinForm(request.POST)
#         if form.is_valid():
#             checkin = form.save(commit=False)
#             checkin.person = person
#             checkin.save()
#             return redirect("client_profile", slug=person.slug)

#     return render(request, "tracking/client_profile.html", {
#         "person": person,
#         "checkins": checkins,
#         "form": form,
#     })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm


# def add_client(request, slug):
#     coach = get_object_or_404(Person, slug=slug, role="coach")

#     form = PersonForm()

#     if request.method == "POST":
#         form = PersonForm(request.POST)
#         if form.is_valid():
#             client = form.save(commit=False)
#             client.sponsor = coach
#             client.role = "client"
#             client.save()
#             return redirect("coach_dashboard", slug=coach.slug)

#     return render(request, "tracking/add_client.html", {
#         "form": form,
#         "coach": coach,
#     })
def add_client(request, slug):
    coach = get_object_or_404(Person, slug=slug, role="coach")

    form = PersonForm()

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            client.sponsor = coach
            client.role = "client"
            client.save()
            return redirect("coach_dashboard", slug=coach.slug)

    return render(request, "tracking/add_client.html", {
        "form": form,
        "coach": coach,
    })


from django.shortcuts import redirect, get_object_or_404

def convert_to_coach(request, slug):
    person = get_object_or_404(Person, slug=slug)

    person.role = "coach"
    person.save()

    # Redirect to their new dashboard
    return redirect("coach_dashboard", slug=person.slug)



def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # find linked person
            person = Person.objects.get(user=user)
            return redirect("coach_dashboard", slug=person.slug)

    return render(request, "tracking/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# def celebration_view(request, slug):
#     person = get_object_or_404(Person, slug=slug)

#     checkins = person.checkins.order_by("date")

#     total_change = 0
#     if checkins.count() >= 2:
#         first = checkins.first()
#         last = checkins.last()
#         total_change = first.weight - last.weight

#     return render(request, "tracking/celebration.html", {
#         "person": person,
#         "total_change": total_change,
#     })

def celebration_view(request, slug):
    person = get_object_or_404(Person, slug=slug)

    checkins = person.checkins.order_by("date")

    total_change = 0
    goal_text = "Progress"

    if checkins.count() >= 2:
        first = checkins.first()
        last = checkins.last()

        # weight difference
        weight_diff = last.weight - first.weight

        if person.goal == "weight_loss":
            total_change = first.weight - last.weight
            goal_text = "Weight Lost"

        elif person.goal == "weight_gain":
            total_change = last.weight - first.weight
            goal_text = "Weight Gained"

        elif person.goal == "muscle_gain":
            total_change = abs(weight_diff)
            goal_text = "Muscle Progress"

        elif person.goal == "fat_loss":
            total_change = abs(weight_diff)
            goal_text = "Fat Loss Progress"

        else:
            total_change = abs(weight_diff)
            goal_text = "Progress"

    return render(request, "tracking/celebration.html", {
        "person": person,
        "total_change": round(total_change, 1),
        "goal_text": goal_text,
    })



from django.utils import timezone
from datetime import timedelta
def tv_leaderboard(request, slug):
    coach = get_object_or_404(Person, slug=slug, role="coach")
    downline = get_all_downline_people(coach)
    clients = [p for p in downline if p.role == "client"]

    today = timezone.now().date()
    one_week_ago = today - timedelta(days=7)

    total_loss = []
    total_gain = []
    weekly_loss = []
    weekly_gain = []

    for person in clients:
        checkins = person.checkins.order_by("date")

        if checkins.count() >= 2:
            first = checkins.first()
            last = checkins.last()

            # total
            if person.goal == "weight_loss":
                loss = first.weight - last.weight
                if loss > 0:
                    total_loss.append((person, loss))

            elif person.goal == "weight_gain":
                gain = last.weight - first.weight
                if gain > 0:
                    total_gain.append((person, gain))

            # weekly
            last_week = checkins.filter(date__lte=one_week_ago).last()
            if last_week:
                if person.goal == "weight_loss":
                    w_loss = last_week.weight - last.weight
                    if w_loss > 0:
                        weekly_loss.append((person, w_loss))

                elif person.goal == "weight_gain":
                    w_gain = last.weight - last_week.weight
                    if w_gain > 0:
                        weekly_gain.append((person, w_gain))

    context = {
        "coach": coach,
        "top_total_loss": sorted(total_loss, key=lambda x: x[1], reverse=True)[:3],
        "top_total_gain": sorted(total_gain, key=lambda x: x[1], reverse=True)[:3],
        "top_weekly_loss": sorted(weekly_loss, key=lambda x: x[1], reverse=True)[:3],
        "top_weekly_gain": sorted(weekly_gain, key=lambda x: x[1], reverse=True)[:3],
    }

    return render(request, "tracking/tv_leaderboard.html", context)

# def tv_leaderboard(request, slug):
#     coach = get_object_or_404(Person, slug=slug, role="coach")
#     downline = get_all_downline_people(coach)
#     clients = [p for p in downline if p.role == "client"]

#     today = timezone.now().date()
#     one_week_ago = today - timedelta(days=7)

#     loss_results = []
#     gain_results = []

#     for person in clients:
#         checkins = person.checkins.order_by("date")

#         if checkins.count() >= 2:
#             first = checkins.first()
#             last = checkins.last()

#             if person.goal == "weight_loss":
#                 loss = first.weight - last.weight
#                 if loss > 0:
#                     loss_results.append((person, loss))

#             elif person.goal == "weight_gain":
#                 gain = last.weight - first.weight
#                 if gain > 0:
#                     gain_results.append((person, gain))

#     # sort and take top 3
#     top_loss = sorted(loss_results, key=lambda x: x[1], reverse=True)[:3]
#     top_gain = sorted(gain_results, key=lambda x: x[1], reverse=True)[:3]

#     return render(request, "tracking/tv_leaderboard.html", {
#         "coach": coach,
#         "top_loss": top_loss,
#         "top_gain": top_gain,
#     })

# def tv_leaderboard(request, slug):
#     coach = get_object_or_404(Person, slug=slug, role="coach")
#     downline = get_all_downline_people(coach)
#     clients = [p for p in downline if p.role == "client"]

#     today = timezone.now().date()
#     one_week_ago = today - timedelta(days=7)

#     loss_results = []
#     gain_results = []
#     weekly_loss_results = []
#     weekly_gain_results = []

#     for person in clients:
#         checkins = person.checkins.order_by("date")

#         if checkins.count() >= 2:
#             first = checkins.first()
#             last = checkins.last()

#             # total change
#             total_change = last.weight - first.weight

#             # weekly
#             last_week_checkin = checkins.filter(date__lte=one_week_ago).last()

#             # LOSS clients
#             if person.goal == "weight_loss":
#                 total_loss = first.weight - last.weight
#                 if total_loss > 0:
#                     loss_results.append((person, total_loss))

#                 if last_week_checkin:
#                     weekly_loss = last_week_checkin.weight - last.weight
#                     if weekly_loss > 0:
#                         weekly_loss_results.append((person, weekly_loss))

#             # GAIN clients
#             elif person.goal == "weight_gain":
#                 total_gain = last.weight - first.weight
#                 if total_gain > 0:
#                     gain_results.append((person, total_gain))

#                 if last_week_checkin:
#                     weekly_gain = last.weight - last_week_checkin.weight
#                     if weekly_gain > 0:
#                         weekly_gain_results.append((person, weekly_gain))

#     def top(result_list):
#         if result_list:
#             return sorted(result_list, key=lambda x: x[1], reverse=True)[0]
#         return None

#     context = {
#         "coach": coach,
#         "top_loss": top(loss_results),
#         "top_gain": top(gain_results),
#         "top_weekly_loss": top(weekly_loss_results),
#         "top_weekly_gain": top(weekly_gain_results),
#     }

#     return render(request, "tracking/tv_leaderboard.html", context)
from django.views.decorators.http import require_POST

@login_required
@require_POST
def quick_checkin(request, slug):
    coach = get_object_or_404(Person, slug=slug, role="coach")

    person_slug = request.POST.get("person")
    weight = request.POST.get("weight")

    if person_slug and weight:
        person = get_object_or_404(Person, slug=person_slug)

        WeeklyCheckin.objects.create(
            person=person,
            date=timezone.now().date(),
            weight=weight
        )

    return redirect("coach_dashboard", slug=coach.slug)
