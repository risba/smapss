from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("", views.login_request, name="login"),
    path("user_profile", views.userprofile_request, name="user_profile"),
    path("scoreboard", views.scoreboard_request, name="scoreboard"),
    path("search_user", views.searchuser_request, name="search_user"),
    path("share_prediction", views.shareprediction_request, name="share_prediction"),
    path("share_feedback", views.sharefeedback_request, name="share_feedback"),

]