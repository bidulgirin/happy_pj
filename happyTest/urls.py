from django.contrib import admin
from django.urls import path, include
from happyTest import views

urlpatterns = [
    path("", views.start, name="start"),
]