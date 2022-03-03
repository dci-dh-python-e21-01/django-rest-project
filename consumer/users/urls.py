from django.contrib import admin
from django.urls import path

from .views import index, remote_user_view, local_user_view


urlpatterns = [
    path("", index),
    path("<int:id>/", remote_user_view, name="remote_user_view"),
    path("local/<int:pk>/", local_user_view, name="local_user_view")
]
