from django.urls import path

from . import views


urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("password-reset/", views.password_reset, name="password_reset"),
]

