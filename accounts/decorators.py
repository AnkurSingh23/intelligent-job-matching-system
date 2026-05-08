from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from candidates.models import CandidateProfile
from companies.models import RecruiterProfile


def get_dashboard_url_name(user):
    if user.is_staff:
        return "admin:index"
    if RecruiterProfile.objects.filter(user=user).exists():
        return "recruiter_jobs"
    if CandidateProfile.objects.filter(user=user).exists():
        return "job_list"
    return "home"


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(get_dashboard_url_name(request.user))

        return view_func(request, *args, **kwargs)

    return wrapper


def candidate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        candidate = CandidateProfile.objects.filter(user=request.user).first()
        if candidate is None:
            messages.error(request, "Only candidates can access this page.")
            return redirect(get_dashboard_url_name(request.user))

        request.candidate_profile = candidate
        return view_func(request, *args, **kwargs)

    return wrapper


def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        recruiter = RecruiterProfile.objects.select_related("company").filter(user=request.user).first()
        if recruiter is None:
            messages.error(request, "Only recruiters can access this page.")
            return redirect(get_dashboard_url_name(request.user))

        request.recruiter_profile = recruiter
        return view_func(request, *args, **kwargs)

    return wrapper