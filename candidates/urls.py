from django.urls import path
from . import views

urlpatterns = [
    path("skills/", views.manage_candidate_skills, name="candidate_skills"),
]
