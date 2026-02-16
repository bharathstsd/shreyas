# from django.db import models


# class Coach(models.Model):
#     name = models.CharField(max_length=100)

#     mobile = models.CharField(
#         max_length=15,
#         unique=True,
#         help_text="Primary identifier for coach"
#     )

#     email = models.EmailField(blank=True)

#     parent_coach = models.ForeignKey(
#         "self",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="downline_coaches"
#     )

#     def __str__(self):
#         return f"{self.name} ({self.mobile})"



# class Client(models.Model):
#     name = models.CharField(max_length=100)

#     coach = models.ForeignKey(
#         Coach,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="clients"
#     )

#     mobile = models.CharField(max_length=15)
#     email = models.EmailField(blank=True)

#     start_date = models.DateField()
#     dob = models.DateField(null=True, blank=True)
#     anniversary = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.name} ({self.mobile})"


# class WeeklyCheckin(models.Model):
#     client = models.ForeignKey(
#         Client,
#         on_delete=models.CASCADE,
#         related_name="checkins"
#     )

#     checkin_date = models.DateField(auto_now_add=True)

#     # Core metrics
#     weight = models.FloatField(help_text="Kg")
#     body_fat_percent = models.FloatField(help_text="%")
#     body_fluid_percent = models.FloatField(help_text="%")
#     muscle_mass_percent = models.FloatField(help_text="%")

#     # Auto-calculated
#     fat_kg = models.FloatField(blank=True, null=True)
#     excess_body_fluid = models.FloatField(
#         blank=True,
#         null=True,
#         help_text="Water reduced per day (grams)"
#     )

#     notes = models.TextField(blank=True)

#     def save(self, *args, **kwargs):
#         # Auto-calculate fat in kg
#         if self.weight and self.body_fat_percent:
#             self.fat_kg = (self.weight * self.body_fat_percent) / 100

#         # Example calculation for excess fluid
#         # (You can change formula later)
#         if self.body_fluid_percent:
#             normal_fluid = 55  # assumed normal %
#             self.excess_body_fluid = max(
#                 0,
#                 (self.body_fluid_percent - normal_fluid) * 100
#             )

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.client.name} - {self.checkin_date}"


from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Person(models.Model):
    ROLE_CHOICES = [
        ("client", "Client"),
        ("coach", "Coach"),
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="client"
    )

    sponsor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="downline"
    )

    start_date = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    anniversary = models.DateField(null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female")],
        blank=True,
        null=True
    )

    height_cm = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    GOAL_CHOICES = [
        ("weight_loss", "Weight Loss"),
        ("weight_gain", "Weight Gain"),
        ("muscle_gain", "Muscle Gain"),
        ("fat_loss", "Fat Loss"),
        ("maintenance", "Maintenance"),
    ]

    goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES,
        blank=True,
        null=True
    )




    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.mobile}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.role})"


# class WeeklyCheckin(models.Model):
#     person = models.ForeignKey(
#         Person,
#         on_delete=models.CASCADE,
#         related_name="checkins",
#     )

#     date = models.DateField()

#     weight = models.FloatField(help_text="Weight in kg")
#     body_fat_percent = models.FloatField()
#     body_fluid_percent = models.FloatField()

#     # auto-calculated fields
#     fat_kg = models.FloatField(blank=True, null=True)
#     excess_fluid = models.FloatField(blank=True, null=True)

#     notes = models.TextField(blank=True)

#     def save(self, *args, **kwargs):
#         # Calculate fat in kg
#         self.fat_kg = (self.weight * self.body_fat_percent) / 100

#         # Example excess fluid logic
#         ideal_fluid = 55
#         self.excess_fluid = self.body_fluid_percent - ideal_fluid

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.person.name} - {self.date}"
class WeeklyCheckin(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="checkins",
    )

    date = models.DateField()

    # Core metrics
    weight = models.FloatField(help_text="Weight in kg")
    body_fat_percent = models.FloatField()

    # Calculated
    body_fat_mass = models.FloatField(blank=True, null=True)

    # Additional machine metrics
    visceral_fat = models.FloatField(blank=True, null=True)
    rmr = models.FloatField(blank=True, null=True, help_text="Resting Metabolic Rate")
    bmi = models.FloatField(blank=True, null=True)
    bma = models.FloatField(blank=True, null=True)
    subcutaneous_fat = models.FloatField(blank=True, null=True)
    trunk_fat = models.FloatField(blank=True, null=True)
    muscle_mass = models.FloatField(blank=True, null=True)

    # Fluid
    body_fluid_percent = models.FloatField(blank=True, null=True)
    excess_fluid = models.FloatField(blank=True, null=True)

    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Calculate body fat mass
        if self.weight and self.body_fat_percent:
            self.body_fat_mass = (self.weight * self.body_fat_percent) / 100

        # Example fluid logic
        if self.body_fluid_percent is not None:
            ideal_fluid = 55
            self.excess_fluid = self.body_fluid_percent - ideal_fluid

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person.name} - {self.date}"
