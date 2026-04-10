from django.db import models
from accounts.models import User
from core.models import Skill
from djmoney.models.fields import MoneyField

# Create your models here.
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(max_length = 200)
    total_experience = models.PositiveIntegerField()
    resume = models.FileField(upload_to="resumes/")
    preferred_location = models.CharField(max_length = 50, null=True)
    expected_salary = MoneyField(
        max_digits = 14,
        decimal_places=2,
        default_currency = 'INR'
    )

    

    def __str__(self):
        return self.full_name
    
class CandidateSkill(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    Proficiency_choices = [
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert')
    ]
    proficiency_level = models.CharField(max_length=20, choices=Proficiency_choices,default = 'beginner')
    experience = models.PositiveIntegerField()

    class Meta:
        unique_together = ("candidate", "skill")
