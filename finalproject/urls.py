from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("", views.login_request, name="login"),
    path("scoreboard", views.scoreboard_request, name="scoreboard"),
    path("userprofile", views.userprofile_request, name="userprofile"),
]