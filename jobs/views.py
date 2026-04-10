from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db import transaction

from candidates.models import CandidateProfile
from companies.models import RecruiterProfile
from jobs.models import Job, JobSkill
from core.models import Skill
from applications.models import JobApplication
from .services.matching import get_top_jobs_for_candidate, get_top_candidates_for_job
from accounts.decorators import candidate_required, recruiter_required


def home(request):
    return render(request, "home.html")


def about_view(request):
    return render(request, "about.html")


about = about_view


def job_list(request):
    jobs = Job.objects.select_related("company", "created_by").order_by("-created_at")
    candidate = None
    candidate_skill_names = []
    match_scores = {}

    if request.user.is_authenticated:
        candidate = CandidateProfile.objects.filter(user=request.user).first()

    if candidate is not None:
        matched_jobs = get_top_jobs_for_candidate(candidate)
        jobs = [job for job, _score in matched_jobs]
        match_scores = {job.id: score for job, score in matched_jobs}
        candidate_skill_names = list(
            candidate.candidateskill_set.select_related("skill")
            .values_list("skill__name", flat=True)
        )

    job_ids = [job.id for job in jobs]
    required_skills_map = {}
    for job_skill in JobSkill.objects.filter(job_id__in=job_ids).select_related("skill"):
        required_skills_map.setdefault(job_skill.job_id, []).append(job_skill.skill.name)

    job_cards = [
        {
            "job": job,
            "score": match_scores.get(job.id),
            "required_skills": required_skills_map.get(job.id, []),
        }
        for job in jobs
    ]

    return render(request, "jobs/job_list.html", {
        "job_cards": job_cards,
        "candidate": candidate,
        "candidate_skill_names": candidate_skill_names,
    })


@login_required
@recruiter_required
def create_job(request):
    recruiter = request.recruiter_profile
    skills = Skill.objects.order_by("name")

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        job_type = (request.POST.get("job_type") or "full_time").strip()
        location = (request.POST.get("location") or "").strip()
        salary_min = request.POST.get("salary_min") or None
        salary_max = request.POST.get("salary_max") or None
        selected_skill_ids = request.POST.getlist("skill_ids")

        if not title or not description or not location:
            messages.error(request, "Title, description and location are required.")
            return render(request, "jobs/create_job.html", {"skills": skills})

        if not selected_skill_ids:
            messages.error(request, "Please select at least one required skill for the job.")
            return render(request, "jobs/create_job.html", {"skills": skills})

        with transaction.atomic():
            job = Job.objects.create(
                company=recruiter.company,
                created_by=recruiter,
                title=title,
                description=description,
                job_type=job_type,
                location=location,
                salary_min=salary_min,
                salary_max=salary_max,
            )

            for skill in Skill.objects.filter(id__in=selected_skill_ids):
                JobSkill.objects.create(
                    job=job,
                    skill=skill,
                    importance="preferred",
                    required_level="intermediate",
                )

        messages.success(request, "Job created successfully.")
        return redirect("recruiter_jobs")

    return render(request, "jobs/create_job.html", {"skills": skills})


@login_required
@recruiter_required
def recruiter_jobs(request):
    recruiter = request.recruiter_profile
    jobs = (
        Job.objects.filter(created_by=recruiter)
        .select_related("company")
        .order_by("-created_at")
        .annotate(applicant_count=Count("jobapplication"))
    )
    return render(request, "jobs/recruiter_jobs.html", {"jobs": jobs})


@login_required
@recruiter_required
def job_applicants(request, job_id):
    recruiter = request.recruiter_profile
    job = get_object_or_404(Job.objects.select_related("company", "created_by"), id=job_id)

    if job.created_by_id != recruiter.id:
        messages.error(request, "You can only view applicants for your own jobs.")
        return redirect("recruiter_jobs")

    applications = (
        JobApplication.objects.filter(job=job)
        .select_related("candidate", "candidate__user")
        .order_by("-applied_at")
    )

    return render(request, "jobs/job_applicants.html", {
        "job": job,
        "applications": applications,
    })


@login_required
@candidate_required
def candidate_matches(request, candidate_id):
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    requester_profile = request.candidate_profile

    if requester_profile.id != candidate.id:
        messages.error(request, "You can only view your own candidate matches.")
        return redirect("job_list")

    results = get_top_jobs_for_candidate(candidate)

    return render(request, "jobs/candidate_matches.html", {
        "candidate": candidate,
        "results": results
    })


@login_required
@recruiter_required
def job_matches(request, job_id):
    recruiter = request.recruiter_profile
    job = get_object_or_404(Job.objects.select_related("created_by"), id=job_id)

    if job.created_by_id != recruiter.id:
        messages.error(request, "You can only view top candidates for your own jobs.")
        return redirect("recruiter_jobs")

    results = get_top_candidates_for_job(job)

    return render(request, "jobs/job_matches.html", {
        "job": job,
        "results": results
    })