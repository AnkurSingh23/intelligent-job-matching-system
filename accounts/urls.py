from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/candidate/", views.register_candidate_view, name="register_candidate"),
    path("register/recruiter/", views.register_recruiter_view, name="register_recruiter"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]