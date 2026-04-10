from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_to_job, name='apply_job'),
    path('applied/', views.applied_jobs, name='applied_jobs'),
]