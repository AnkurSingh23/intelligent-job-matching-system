from django.db import models
from django.core import validators
from django.core.validators import FileExtensionValidator
from accounts.models import User
from core.models import Skill
from djmoney.models.fields import MoneyField

# Create your models here.
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    bio = models.TextField()
    total_experience = models.PositiveIntegerField(validators=[validators.MinValueValidator(0)])
    resume = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(["txt", "pdf", "doc", "docx"])],
    )
    preferred_location = models.CharField(max_length=50, null=True, blank=True)
    expected_salary = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='INR'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["full_name"]),
        ]

    

    def __str__(self):
        return self.full_name
    
class CandidateSkill(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_choices = [
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert')
    ]
    proficiency_level = models.CharField(max_length=20, choices=proficiency_choices, default='beginner')
    experience = models.PositiveIntegerField()

    class Meta:
        unique_together = ("candidate", "skill")
        ordering = ["candidate", "skill"]
        indexes = [
            models.Index(fields=["candidate"]),
            models.Index(fields=["skill"]),
        ]
    
    def __str__(self):
        return f"{self.candidate.full_name} - {self.skill.name}"
