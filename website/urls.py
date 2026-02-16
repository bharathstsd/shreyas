from django.urls import path
from .views import home, about, team, coach_detail, transformations_list, transformation_detail, gallery_list, gallery_detail, calendar_page, contact, programs_list, program_detail

urlpatterns = [
    path('', home, name='home'),
    path("about/", about, name="about"),
    path("team/", team, name="team"),
    path('team/<slug:slug>/', coach_detail, name='coach_detail'),
    path("transformations/", transformations_list, name="transformations_list"),
    path("transformations/<slug:slug>/", transformation_detail, name="transformation_detail"),
    path("gallery/", gallery_list, name="gallery"),
    path("gallery/<slug:slug>/", gallery_detail, name="gallery_detail"),
    path("calendar/", calendar_page, name="calendar"),
    path("contact/", contact, name="contact"),
    path("programs/", programs_list, name="programs"),
    path("programs/<slug:slug>/", program_detail, name="program_detail"),








]
