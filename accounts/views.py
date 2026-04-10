from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction

from candidates.models import CandidateProfile
from companies.models import RecruiterProfile, Company
from .decorators import unauthenticated_user


User = get_user_model()


@unauthenticated_user
def register_view(request):
    return render(request, "accounts/register_choice.html")


@unauthenticated_user
def register_candidate_view(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        password = (request.POST.get("password") or "").strip()
        full_name = (request.POST.get("full_name") or "").strip()
        bio = (request.POST.get("bio") or "").strip()
        total_experience = request.POST.get("total_experience") or 0
        preferred_location = (request.POST.get("preferred_location") or "").strip()

        if not email or not password or not full_name or not bio:
            messages.error(request, "Please fill all required fields.")
            return render(request, "accounts/register_candidate.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please log in.")
            return redirect("login")

        try:
            with transaction.atomic():
                user = User.objects.create_user(email=email, password=password)

                profile = CandidateProfile.objects.create(
                    user=user,
                    full_name=full_name,
                    bio=bio,
                    total_experience=total_experience,
                    preferred_location=preferred_location or None,
                    expected_salary=0,
                )
                profile.resume.save("placeholder_resume.txt", ContentFile("Resume not uploaded yet"), save=True)
        except IntegrityError:
            messages.error(request, "Email already registered. Please log in.")
            return redirect("login")

        login(request, user)

        messages.success(request, "Candidate account created. You are now logged in.")
        return redirect("job_list")

    return render(request, "accounts/register_candidate.html")


@unauthenticated_user
def register_recruiter_view(request):
    companies = Company.objects.order_by("name")

    if not companies.exists():
        messages.error(request, "No companies available. Ask admin to create a company first.")
        return redirect("login")

    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        password = (request.POST.get("password") or "").strip()
        recruiter_name = (request.POST.get("name") or "").strip()
        company_id = request.POST.get("company_id")

        if not email or not password or not recruiter_name or not company_id:
            messages.error(request, "Email, password, recruiter name and company are required.")
            return render(request, "accounts/register_recruiter.html", {"companies": companies})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please log in.")
            return redirect("login")

        company = Company.objects.filter(id=company_id).first()
        if company is None:
            messages.error(request, "Selected company does not exist. Contact admin.")
            return render(request, "accounts/register_recruiter.html", {"companies": companies})

        try:
            with transaction.atomic():
                user = User.objects.create_user(email=email, password=password)
                RecruiterProfile.objects.create(user=user, name=recruiter_name, company=company)
        except IntegrityError:
            messages.error(request, "Email already registered. Please log in.")
            return redirect("login")

        login(request, user)
        messages.success(request, "Recruiter account created. You are now logged in.")
        return redirect("recruiter_jobs")

    return render(request, "accounts/register_recruiter.html", {"companies": companies})


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        password = (request.POST.get("password") or "").strip()

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            if RecruiterProfile.objects.filter(user=user).exists():
                return redirect("recruiter_jobs")
            if CandidateProfile.objects.filter(user=user).exists():
                return redirect("job_list")
            if user.is_staff:
                return redirect("/admin/")
            return redirect("job_list")

        messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")