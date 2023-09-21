from django.urls import path
from . import views

urlpatterns = [
    path("1", views.bruh, name = "few"),
    path("2", views.bruh2, name = "few"),
    path("3", views.bruh3, name = "few")
]