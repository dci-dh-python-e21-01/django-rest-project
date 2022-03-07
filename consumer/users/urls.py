from django.contrib import admin
from django.urls import path

from .views import index, remote_user_view, local_user_view, dogs_view, dogs_detail, add_dog, edit_dog, delete_dog, add_user


urlpatterns = [
    path("", index, name='idex'),
    path("<int:id>/", remote_user_view, name="remote_user_view"),
    path("local/<int:pk>/", local_user_view, name="local_user_view"),
    path("users/add/", add_user, name="add_user"),
    path("dogs/", dogs_view, name="dogs_view"),
    path('dogs/<int:id>/', dogs_detail, name="dog_detail"),
    path("dogs/add/", add_dog, name="add_dog"),
    path('dogs/<int:id>/edit/', edit_dog, name="edit_dog"),
    path('dogs/<int:id>/delete/', delete_dog, name="delete_dog"),
]
