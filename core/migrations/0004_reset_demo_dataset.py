from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_demo_dataset(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    Skill = apps.get_model("core", "Skill")
    Company = apps.get_model("companies", "Company")
    RecruiterProfile = apps.get_model("companies", "RecruiterProfile")
    CandidateProfile = apps.get_model("candidates", "CandidateProfile")
    CandidateSkill = apps.get_model("candidates", "CandidateSkill")
    Job = apps.get_model("jobs", "Job")
    JobSkill = apps.get_model("jobs", "JobSkill")
    JobApplication = apps.get_model("applications", "JobApplication")

    JobApplication.objects.all().delete()
    JobSkill.objects.all().delete()
    Job.objects.all().delete()
    CandidateSkill.objects.all().delete()
    CandidateProfile.objects.all().delete()
    RecruiterProfile.objects.all().delete()
    Company.objects.all().delete()
    Skill.objects.all().delete()
    User.objects.filter(email__endswith="@demo.com").delete()

    skills = ["Python", "Django", "SQL", "JavaScript", "React", "AWS", "Docker", "Git"]
    skill_objs = {name: Skill.objects.create(name=name) for name in skills}

    companies_data = [
        ("Tata Consultancy Services", "Mumbai", "India's large IT services company"),
        ("Infosys Limited", "Bengaluru", "Indian tech consulting and software company"),
        ("Wipro Technologies", "Bengaluru", "Global IT, consulting and business process services"),
        ("HCL Technologies", "Noida", "Engineering and digital transformation company"),
        ("Tech Mahindra", "Pune", "Telecom and digital solutions company"),
    ]
    company_objs = []
    for name, city, description in companies_data:
        company_objs.append(
            Company.objects.create(name=name, city=city, description=description)
        )

    recruiter_data = [
        ("ashi.demo@demo.com", "Ashi", company_objs[0]),
        ("mohit.demo@demo.com", "Mohit", company_objs[0]),
        ("aman.demo@demo.com", "Aman", company_objs[1]),
        ("neha.demo@demo.com", "Neha", company_objs[1]),
        ("rahul.demo@demo.com", "Rahul", company_objs[2]),
        ("riya.demo@demo.com", "Riya", company_objs[3]),
        ("kunal.demo@demo.com", "Kunal", company_objs[4]),
        ("priya.demo@demo.com", "Priya", company_objs[4]),
    ]
    recruiter_objs = []
    for email, name, company in recruiter_data:
        user = User.objects.create(
            email=email,
            password=make_password("pass1234"),
            is_active=True,
        )
        recruiter_objs.append(
            RecruiterProfile.objects.create(user=user, name=name, company=company)
        )

    candidate_data = [
        ("ankur.demo@demo.com", "Ankur", "Python and Django developer", 3, "Delhi", 800000),
        ("gaurav.demo@demo.com", "Gaurav", "Frontend and React developer", 2, "Pune", 650000),
        ("yash.demo@demo.com", "Yash", "SQL and backend enthusiast", 1, "Bengaluru", 550000),
        ("harsh.demo@demo.com", "Harsh", "Cloud and DevOps learner", 4, "Noida", 900000),
        ("rohan.demo@demo.com", "Rohan", "Full stack engineer", 2, "Mumbai", 700000),
    ]
    candidate_objs = []
    for email, full_name, bio, experience, location, salary in candidate_data:
        user = User.objects.create(
            email=email,
            password=make_password("pass1234"),
            is_active=True,
        )
        candidate = CandidateProfile.objects.create(
            user=user,
            full_name=full_name,
            bio=bio,
            total_experience=experience,
            preferred_location=location,
            expected_salary=salary,
            resume=f"resumes/{full_name.lower()}_resume.txt",
        )
        candidate_objs.append(candidate)

    candidate_skill_map = {
        candidate_objs[0]: ["Python", "Django", "SQL", "Git"],
        candidate_objs[1]: ["JavaScript", "React", "Git", "SQL"],
        candidate_objs[2]: ["Python", "SQL", "Git"],
        candidate_objs[3]: ["AWS", "Docker", "Python", "Git"],
        candidate_objs[4]: ["Python", "JavaScript", "React", "Docker"],
    }
    for candidate, names in candidate_skill_map.items():
        for index, skill_name in enumerate(names, start=1):
            CandidateSkill.objects.create(
                candidate=candidate,
                skill=skill_objs[skill_name],
                proficiency_level="intermediate" if index <= 3 else "beginner",
                experience=max(1, candidate.total_experience - 1),
            )

    job_data = [
        (recruiter_objs[0], "Python Backend Developer", "Build Django APIs and backend modules.", "full_time", "Mumbai", 700000, 1200000, ["Python", "Django", "SQL", "Git"]),
        (recruiter_objs[1], "Django Engineer", "Work on REST APIs and admin dashboards.", "full_time", "Bengaluru", 750000, 1300000, ["Python", "Django", "Git", "SQL"]),
        (recruiter_objs[2], "React Developer", "Create modern frontend screens and components.", "remote", "Remote", 600000, 1100000, ["JavaScript", "React", "Git", "SQL"]),
        (recruiter_objs[3], "Data Analyst", "Analyse data and build reports for product teams.", "full_time", "Noida", 500000, 900000, ["SQL", "Python", "Git", "AWS"]),
        (recruiter_objs[4], "DevOps Engineer", "Handle CI/CD and cloud deployments.", "full_time", "Bengaluru", 900000, 1600000, ["AWS", "Docker", "Python", "Git"]),
        (recruiter_objs[5], "Support Engineer", "Support production systems and customer escalations.", "full_time", "Noida", 450000, 800000, ["Git", "SQL", "Python", "Docker"]),
        (recruiter_objs[6], "Software Tester", "Test web apps and report bugs.", "full_time", "Pune", 400000, 700000, ["Python", "SQL", "Git", "JavaScript"]),
        (recruiter_objs[7], "Full Stack Developer", "Work on backend and frontend features.", "remote", "Remote", 800000, 1400000, ["Python", "JavaScript", "React", "Git"]),
        (recruiter_objs[0], "Cloud Engineer", "Manage cloud infra and deployments.", "full_time", "Mumbai", 950000, 1700000, ["AWS", "Docker", "Git", "Python"]),
        (recruiter_objs[2], "Junior Python Developer", "Support backend features and bug fixes.", "full_time", "Bengaluru", 500000, 850000, ["Python", "Django", "SQL", "Git"]),
    ]
    job_objs = []
    for recruiter, title, description, job_type, location, salary_min, salary_max, skill_list in job_data:
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
        job_objs.append(job)
        for skill_name in skill_list:
            JobSkill.objects.create(
                job=job,
                skill=skill_objs[skill_name],
                importance="preferred",
                required_level="intermediate",
            )

    application_pairs = [
        (candidate_objs[0], job_objs[0]),
        (candidate_objs[0], job_objs[9]),
        (candidate_objs[1], job_objs[2]),
        (candidate_objs[1], job_objs[7]),
        (candidate_objs[2], job_objs[3]),
        (candidate_objs[2], job_objs[1]),
        (candidate_objs[3], job_objs[4]),
        (candidate_objs[3], job_objs[8]),
        (candidate_objs[4], job_objs[6]),
    ]
    for candidate, job in application_pairs:
        JobApplication.objects.create(candidate=candidate, job=job)

    admin_user = User.objects.create(
        email="admin@demo.com",
        password=make_password("admin1234"),
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    admin_user.save()


def unseed_demo_dataset(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_seed_initial_data"),
    ]

    operations = [
        migrations.RunPython(seed_demo_dataset, unseed_demo_dataset),
    ]
