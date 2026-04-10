from django.db import migrations
from django.contrib.auth.hashers import make_password


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
    skill_objs = {name: Skill.objects.get_or_create(name=name)[0] for name in skills}

    companies_data = [
        ("TechNova", "Bengaluru", "Product engineering company"),
        ("CloudBridge", "Hyderabad", "Cloud and DevOps consulting"),
        ("DataSpring", "Pune", "Analytics and data platform startup"),
    ]
    company_objs = []
    for name, city, description in companies_data:
        company, _ = Company.objects.get_or_create(
            name=name,
            defaults={"city": city, "description": description},
        )
        company_objs.append(company)

    recruiters_data = [
        ("recruiter1@demo.com", "Rahul HR", company_objs[0]),
        ("recruiter2@demo.com", "Priya Talent", company_objs[1]),
        ("recruiter3@demo.com", "Aman Hiring", company_objs[2]),
    ]
    recruiter_objs = []
    for email, name, company in recruiters_data:
        user, _ = User.objects.get_or_create(email=email, defaults={"is_active": True})
        user.password = make_password("pass1234")
        user.is_active = True
        user.save(update_fields=["password", "is_active"])

        recruiter, _ = RecruiterProfile.objects.get_or_create(
            user=user,
            defaults={"name": name, "company": company},
        )
        recruiter.name = name
        recruiter.company = company
        recruiter.save(update_fields=["name", "company"])
        recruiter_objs.append(recruiter)

    candidates_data = [
        (
            "alice@demo.com",
            "Alice Sharma",
            "Backend Django developer",
            3,
            "Bengaluru",
            700000,
        ),
        (
            "bob@demo.com",
            "Bob Mehta",
            "Full stack engineer",
            2,
            "Remote",
            600000,
        ),
        (
            "carol@demo.com",
            "Carol Nair",
            "Data analyst transitioning to backend",
            1,
            "Pune",
            500000,
        ),
        (
            "dan@demo.com",
            "Dan Verma",
            "DevOps and cloud enthusiast",
            4,
            "Hyderabad",
            900000,
        ),
    ]
    candidate_objs = []
    for email, full_name, bio, exp, location, salary in candidates_data:
        user, _ = User.objects.get_or_create(email=email, defaults={"is_active": True})
        user.password = make_password("pass1234")
        user.is_active = True
        user.save(update_fields=["password", "is_active"])

        candidate, _ = CandidateProfile.objects.get_or_create(
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
        candidate.full_name = full_name
        candidate.bio = bio
        candidate.total_experience = exp
        candidate.preferred_location = location
        candidate.expected_salary = salary
        if not candidate.resume:
            candidate.resume = "resumes/placeholder_resume.txt"
        candidate.save(
            update_fields=[
                "full_name",
                "bio",
                "total_experience",
                "preferred_location",
                "expected_salary",
                "resume",
            ]
        )
        candidate_objs.append(candidate)

    candidate_skill_map = {
        candidate_objs[0]: ["Python", "Django", "SQL", "Git"],
        candidate_objs[1]: ["Python", "JavaScript", "React", "Git"],
        candidate_objs[2]: ["SQL", "Python", "Git"],
        candidate_objs[3]: ["AWS", "Docker", "Python", "Git"],
    }
    for candidate, names in candidate_skill_map.items():
        for skill_name in names:
            CandidateSkill.objects.get_or_create(
                candidate=candidate,
                skill=skill_objs[skill_name],
                defaults={"proficiency_level": "intermediate", "experience": max(1, candidate.total_experience - 1)},
            )

    jobs_data = [
        (
            recruiter_objs[0],
            "Backend Django Developer",
            "Build APIs and backend systems for product modules.",
            "full_time",
            "Bengaluru",
            800000,
            1400000,
            ["Python", "Django", "SQL", "Git"],
        ),
        (
            recruiter_objs[1],
            "Full Stack Developer",
            "Work on frontend and backend features for client projects.",
            "remote",
            "Remote",
            700000,
            1200000,
            ["Python", "JavaScript", "React", "SQL"],
        ),
        (
            recruiter_objs[2],
            "Junior Data Engineer",
            "Support ETL pipelines and analytics workloads.",
            "full_time",
            "Pune",
            500000,
            900000,
            ["Python", "SQL", "AWS", "Git"],
        ),
        (
            recruiter_objs[1],
            "DevOps Engineer",
            "Manage CI/CD, containerization, and cloud deployments.",
            "full_time",
            "Hyderabad",
            900000,
            1600000,
            ["AWS", "Docker", "Git", "Python"],
        ),
    ]

    job_objs = []
    for recruiter, title, description, job_type, location, salary_min, salary_max, skill_list in jobs_data:
        job, _ = Job.objects.get_or_create(
            company=recruiter.company,
            created_by=recruiter,
            title=title,
            defaults={
                "description": description,
                "job_type": job_type,
                "location": location,
                "salary_min": salary_min,
                "salary_max": salary_max,
            },
        )
        job.description = description
        job.job_type = job_type
        job.location = location
        job.salary_min = salary_min
        job.salary_max = salary_max
        job.save(update_fields=["description", "job_type", "location", "salary_min", "salary_max"])

        for skill_name in skill_list:
            JobSkill.objects.get_or_create(
                job=job,
                skill=skill_objs[skill_name],
                defaults={"importance": "preferred", "required_level": "intermediate"},
            )

        job_objs.append(job)

    JobApplication.objects.get_or_create(
        candidate=candidate_objs[0],
        job=job_objs[0],
        defaults={"status": "applied"},
    )
    JobApplication.objects.get_or_create(
        candidate=candidate_objs[1],
        job=job_objs[1],
        defaults={"status": "shortlisted"},
    )
    JobApplication.objects.get_or_create(
        candidate=candidate_objs[2],
        job=job_objs[2],
        defaults={"status": "applied"},
    )
    JobApplication.objects.get_or_create(
        candidate=candidate_objs[3],
        job=job_objs[3],
        defaults={"status": "applied"},
    )

    admin_user, _ = User.objects.get_or_create(
        email="admin@demo.com",
        defaults={"is_staff": True, "is_superuser": True, "is_active": True},
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.password = make_password("admin1234")
    admin_user.save(update_fields=["password", "is_staff", "is_superuser", "is_active"])


def unseed_initial_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_delete_candidateprofile"),
        ("applications", "0001_initial"),
        ("candidates", "0002_remove_candidateprofile_name_and_more"),
        ("companies", "0001_initial"),
        ("core", "0002_alter_skill_name"),
        ("jobs", "0002_job_created_at"),
    ]

    operations = [
        migrations.RunPython(seed_initial_data, unseed_initial_data),
    ]
