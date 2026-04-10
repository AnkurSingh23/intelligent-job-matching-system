from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from candidates.models import CandidateProfile
from jobs.models import Job
from .models import JobApplication
from accounts.decorators import candidate_required


@login_required
@candidate_required
def apply_to_job(request, job_id):
    candidate = request.candidate_profile
    job = get_object_or_404(Job, id=job_id)

    already_applied = JobApplication.objects.filter(candidate=candidate, job=job).exists()

    if not already_applied:
        JobApplication.objects.create(candidate=candidate, job=job)
        messages.success(request, "Job applied successfully.")
    else:
        messages.info(request, "You already applied to this job.")

    return redirect('applied_jobs')


@login_required
@candidate_required
def applied_jobs(request):
    candidate = request.candidate_profile
    applications = JobApplication.objects.filter(candidate=candidate).select_related('job')

    return render(request, 'applications/applied_jobs.html', {
        'applications': applications
    })