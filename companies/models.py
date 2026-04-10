from django.db import models
from accounts.models import User
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.name

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    company = models.ForeignKey(Company,on_delete= models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.company.name})"