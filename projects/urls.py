from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
]