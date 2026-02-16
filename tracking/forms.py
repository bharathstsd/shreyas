from django import forms
from .models import Person, WeeklyCheckin


# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = [
#             "name",
#             "mobile",
#             "email",
#             "gender",
#             "goal",
#             "photo",
#             "height_cm",
#             "start_date",
#             "date_of_birth",
#             "anniversary",
#         ]
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "mobile",
            "email",
            "gender",
            "goal",
            "photo",
            "start_date",
            "date_of_birth",
            "anniversary",
            "height_cm"
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "anniversary": forms.DateInput(attrs={"type": "date"}),
        }


# class WeeklyCheckinForm(forms.ModelForm):
#     class Meta:
#         model = WeeklyCheckin
#         fields = [
#             "date",
#             "weight",
#             "body_fat_percent",
#             "body_fluid_percent",
#             "notes",
#         ]
class WeeklyCheckinForm(forms.ModelForm):
    class Meta:
        model = WeeklyCheckin
        fields = [
            "date",
            "weight",
            "body_fat_percent",
            "visceral_fat",
            "rmr",
            "bmi",
            "bma",
            "subcutaneous_fat",
            "trunk_fat",
            "muscle_mass",
            "body_fluid_percent",
            "notes",
        ]
