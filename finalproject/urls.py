from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("", views.login_request, name="login"),
    path("scoreboard", views.scoreboard_request, name="scoreboard"),
    path("user_profile", views.userprofile_request, name="user_profile"),
    path("share_prediction", views.shareprediction_request, name="share_prediction"),
]