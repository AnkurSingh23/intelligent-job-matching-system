from django.db import models
from companies.models import Company, RecruiterProfile
from core.models import Skill
# Create your models here.



class Job(models.Model):
    company = models.ForeignKey(Company, on_delete = models.PROTECT)
    created_by = models.ForeignKey(RecruiterProfile, null = True, on_delete=models.SET_NULL)
    title = models.CharField(max_length = 30, null = False)
    description = models.TextField()
    job_choice = [
        ('remote','Remote'),
        ('full_time','Full_time')
    ]
    job_type = models.CharField(max_length = 20, choices = job_choice, default = 'full_time')
    location = models.CharField(max_length =100)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def get_salary(self):
        salary_min = self.salary_min
        salary_max = self.salary_max
        if salary_min and salary_max:
            return f'Rs. {salary_min} - Rs. {salary_max}'
        if salary_max:
            return f'upto Rs.{salary_max}'
        else:
            return f'No mention'

    def __str__(self):
        return self.title

class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete = models.CASCADE)
    IMPRTANCE_CHOICE = [
        ('nice_to_have','Nice To Have'),
        ('preferred','Preferred'),
        ('very_important','Very Important') 
    ]

    LEVEL_CHOICE = [
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert') 
    ]

    importance = models.CharField(max_length = 15, choices = IMPRTANCE_CHOICE, default = 'preferred')
    required_level = models.CharField(max_length = 20, choices = LEVEL_CHOICE, default = 'beginner')

    class Meta:
        unique_together = ('job','skill')

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"

