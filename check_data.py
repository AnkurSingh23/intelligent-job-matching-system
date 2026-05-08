import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_matching.settings')
django.setup()

from accounts.models import User
from candidates.models import CandidateProfile, CandidateSkill
from companies.models import Company, RecruiterProfile
from jobs.models import Job, JobSkill
from applications.models import JobApplication
from core.models import Skill

print("=" * 50)
print("CHECKING DATABASE RECORDS")
print("=" * 50)
print(f"Users: {User.objects.count()}")
print(f"Skills: {Skill.objects.count()}")
print(f"Companies: {Company.objects.count()}")
print(f"RecruiterProfiles: {RecruiterProfile.objects.count()}")
print(f"CandidateProfiles: {CandidateProfile.objects.count()}")
print(f"CandidateSkills: {CandidateSkill.objects.count()}")
print(f"Jobs: {Job.objects.count()}")
print(f"JobSkills: {JobSkill.objects.count()}")
print(f"JobApplications: {JobApplication.objects.count()}")
print("=" * 50)
