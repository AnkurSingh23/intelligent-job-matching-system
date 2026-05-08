from datetime import date

from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_initial_data(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    Skill = apps.get_model("core", "Skill")
    Company = apps.get_model("companies", "Company")
    RecruiterProfile = apps.get_model("companies", "RecruiterProfile")
    CandidateProfile = apps.get_model("candidates", "CandidateProfile")
    CandidateSkill = apps.get_model("candidates", "CandidateSkill")
    Job = apps.get_model("jobs", "Job")
    JobSkill = apps.get_model("jobs", "JobSkill")
    JobApplication = apps.get_model("applications", "JobApplication")

    skills = ["Python", "Django", "SQL", "JavaScript", "React", "AWS", "Docker", "Git"]
    skill_map = {}
    for skill_name in skills:
        skill, _ = Skill.objects.get_or_create(name=skill_name)
        skill_map[skill_name] = skill

    companies_data = [
        ("TechNova", "Bengaluru", "Product engineering company"),
        ("CloudBridge", "Hyderabad", "Cloud and DevOps consulting"),
        ("DataSpring", "Pune", "Analytics and data platform startup"),
    ]
    company_map = {}
    for name, city, description in companies_data:
        company, _ = Company.objects.update_or_create(
            name=name,
            defaults={
                "city": city,
                "description": description,
                "website": "",
                "contact_email": "",
                "contact_phone": "",
            },
        )
        company_map[name] = company

    recruiters_data = [
        ("recruiter1@demo.com", "Rahul HR", "TechNova"),
        ("recruiter2@demo.com", "Priya Talent", "CloudBridge"),
        ("recruiter3@demo.com", "Aman Hiring", "DataSpring"),
    ]
    recruiter_map = {}
    for email, name, company_name in recruiters_data:
        user, _ = User.objects.update_or_create(
            email=email,
            defaults={"is_active": True, "password": make_password("pass1234")},
        )
        user.password = make_password("pass1234")
        user.save(update_fields=["password"])

        recruiter, _ = RecruiterProfile.objects.update_or_create(
            user=user,
            defaults={
                "name": name,
                "company": company_map[company_name],
                "phone": "",
                "is_active": True,
            },
        )
        recruiter_map[email] = recruiter

    candidates_data = [
        ("alice@demo.com", "Alice Sharma", "Backend Django developer", 3, "Bengaluru", 700000),
        ("bob@demo.com", "Bob Mehta", "Full stack engineer", 2, "Remote", 600000),
        ("carol@demo.com", "Carol Nair", "Data analyst transitioning to backend", 1, "Pune", 500000),
        ("dan@demo.com", "Dan Verma", "DevOps and cloud enthusiast", 4, "Hyderabad", 900000),
    ]
    candidate_map = {}
    for email, full_name, bio, exp, location, salary in candidates_data:
        user, _ = User.objects.update_or_create(
            email=email,
            defaults={"is_active": True, "password": make_password("pass1234")},
        )
        user.password = make_password("pass1234")
        user.save(update_fields=["password"])

        candidate, _ = CandidateProfile.objects.update_or_create(
            user=user,
            defaults={
                "full_name": full_name,
                "bio": bio,
                "total_experience": exp,
                "preferred_location": location,
                "expected_salary": salary,
                "resume": "resumes/placeholder_resume.txt",
            },
        )
        candidate_map[email] = candidate

    candidate_skill_map = {
        "alice@demo.com": ["Python", "Django", "SQL", "Git"],
        "bob@demo.com": ["Python", "JavaScript", "React", "Git"],
        "carol@demo.com": ["SQL", "Python", "Git"],
        "dan@demo.com": ["AWS", "Docker", "Python", "Git"],
    }
    for email, names in candidate_skill_map.items():
        candidate = candidate_map[email]
        for skill_name in names:
            CandidateSkill.objects.update_or_create(
                candidate=candidate,
                skill=skill_map[skill_name],
                defaults={"proficiency_level": "intermediate", "experience": max(1, candidate.total_experience - 1)},
            )

    jobs_data = [
        (
            "recruiter1@demo.com",
            "Backend Django Developer",
            "Build APIs and backend systems for product modules.",
            "full_time",
            "Bengaluru",
            800000,
            1400000,
            date(2026, 12, 31),
            ["Python", "Django", "SQL", "Git"],
        ),
        (
            "recruiter2@demo.com",
            "Full Stack Developer",
            "Work on frontend and backend features for client projects.",
            "remote",
            "Remote",
            700000,
            1200000,
            date(2026, 11, 30),
            ["Python", "JavaScript", "React", "SQL"],
        ),
        (
            "recruiter3@demo.com",
            "Junior Data Engineer",
            "Support ETL pipelines and analytics workloads.",
            "full_time",
            "Pune",
            500000,
            900000,
            date(2026, 10, 31),
            ["Python", "SQL", "AWS", "Git"],
        ),
        (
            "recruiter2@demo.com",
            "DevOps Engineer",
            "Manage CI/CD, containerization, and cloud deployments.",
            "full_time",
            "Hyderabad",
            900000,
            1600000,
            date(2026, 12, 15),
            ["AWS", "Docker", "Git", "Python"],
        ),
    ]
    job_map = {}
    for recruiter_email, title, description, job_type, location, salary_min, salary_max, deadline, skill_list in jobs_data:
        recruiter = recruiter_map[recruiter_email]
        job, _ = Job.objects.update_or_create(
            company=recruiter.company,
            created_by=recruiter,
            title=title,
            defaults={
                "description": description,
                "job_type": job_type,
                "location": location,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "application_deadline": deadline,
                "is_active": True,
            },
        )
        job_map[title] = job

        for skill_name in skill_list:
            JobSkill.objects.update_or_create(
                job=job,
                skill=skill_map[skill_name],
                defaults={"importance": "preferred", "required_level": "intermediate"},
            )

    applications_data = [
        ("alice@demo.com", "Backend Django Developer", "applied"),
        ("bob@demo.com", "Full Stack Developer", "shortlisted"),
        ("carol@demo.com", "Junior Data Engineer", "applied"),
        ("dan@demo.com", "DevOps Engineer", "applied"),
    ]
    for candidate_email, job_title, status in applications_data:
        JobApplication.objects.update_or_create(
            candidate=candidate_map[candidate_email],
            job=job_map[job_title],
            defaults={
                "status": status,
                "reviewer_notes": "",
                "reviewed_at": None,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("accounts", "0001_initial"),
        ("companies", "0002_alter_company_options_alter_recruiterprofile_options_and_more"),
        ("candidates", "0002_alter_candidateprofile_options_and_more"),
        ("jobs", "0002_alter_job_options_alter_jobskill_options_and_more"),
        ("applications", "0002_alter_jobapplication_options_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_initial_data, migrations.RunPython.noop),
    ]
