from django.contrib import admin
from .models import JobApplication

# Register your models here.
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
	list_display = ("id", "candidate", "job", "status", "applied_at")
	list_filter = ("status", "job__company")
	search_fields = ("candidate__full_name", "candidate__user__email", "job__title")
	date_hierarchy = "applied_at"
