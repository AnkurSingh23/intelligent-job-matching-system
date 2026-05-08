from django.db import models
from companies.models import Company, RecruiterProfile
from core.models import Skill
# Create your models here.



class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_by = models.ForeignKey(RecruiterProfile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150, null=False)
    description = models.TextField()
    job_choice = [
        ('remote','Remote'),
        ('full_time','Full Time')
    ]
    job_type = models.CharField(max_length=20, choices=job_choice, default='full_time')
    location = models.CharField(max_length=100)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.salary_min is not None and self.salary_max is not None and self.salary_min > self.salary_max:
            raise ValidationError('Salary minimum cannot be greater than maximum.')
        if self.salary_min is not None and self.salary_min < 0:
            raise ValidationError('Salary minimum cannot be negative.')
        if self.salary_max is not None and self.salary_max < 0:
            raise ValidationError('Salary maximum cannot be negative.')

    def get_salary(self):
        salary_min = self.salary_min
        salary_max = self.salary_max
        if salary_min is not None and salary_max is not None:
            return f'Rs. {salary_min} - Rs. {salary_max}'
        if salary_max is not None:
            return f'upto Rs.{salary_max}'
        else:
            return f'No mention'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    IMPORTANCE_CHOICE = [
        ('nice_to_have','Nice To Have'),
        ('preferred','Preferred'),
        ('very_important','Very Important') 
    ]

    LEVEL_CHOICE = [
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert') 
    ]

    importance = models.CharField(max_length=15, choices=IMPORTANCE_CHOICE, default='preferred')
    required_level = models.CharField(max_length=20, choices=LEVEL_CHOICE, default='beginner')

    class Meta:
        unique_together = ('job','skill')
        ordering = ['job', 'skill']
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['skill']),
        ]

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"

