from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from candidates.models import CandidateProfile
from companies.models import RecruiterProfile


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if RecruiterProfile.objects.filter(user=request.user).exists():
                return redirect("recruiter_jobs")
            if CandidateProfile.objects.filter(user=request.user).exists():
                return redirect("job_list")
            if request.user.is_staff:
                return redirect("/admin/")
            return redirect("job_list")

        return view_func(request, *args, **kwargs)

    return wrapper


def candidate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        candidate = CandidateProfile.objects.filter(user=request.user).first()
        if candidate is None:
            messages.error(request, "Only candidates can access this page.")
            return redirect("job_list")

        request.candidate_profile = candidate
        return view_func(request, *args, **kwargs)

    return wrapper


def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        recruiter = RecruiterProfile.objects.select_related("company").filter(user=request.user).first()
        if recruiter is None:
            messages.error(request, "Only recruiters can access this page.")
            return redirect("job_list")

        request.recruiter_profile = recruiter
        return view_func(request, *args, **kwargs)

    return wrapper