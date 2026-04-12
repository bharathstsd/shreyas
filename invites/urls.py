from django.urls import path
from . import views

urlpatterns = [
    path('', views.invite_form, name='invite_form'),
    path('generate/', views.generate_invite, name='generate_invite'),
]
