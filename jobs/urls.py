from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about_view, name="about"),
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/create/", views.create_job, name="create_job"),
    path("jobs/my/", views.recruiter_jobs, name="recruiter_jobs"),
    path("jobs/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("candidate/<int:candidate_id>/matches/", views.candidate_matches, name="candidate_matches"),
    path("job/<int:job_id>/matches/", views.job_matches, name="job_matches"),
]