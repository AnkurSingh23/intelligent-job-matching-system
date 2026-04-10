from django.contrib import admin
from .models import Job, JobSkill
from applications.models import JobApplication


class JobSkillInline(admin.TabularInline):
	model = JobSkill
	extra = 1


class JobApplicationInline(admin.TabularInline):
	model = JobApplication
	extra = 0
	readonly_fields = ("candidate", "status", "applied_at")
	can_delete = False

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "company", "created_by", "job_type", "location", "applicant_count", "created_at")
	list_filter = ("job_type", "company", "created_at")
	search_fields = ("title", "company__name", "created_by__name", "location")
	inlines = [JobSkillInline, JobApplicationInline]

	def applicant_count(self, obj):
		return obj.jobapplication_set.count()

	applicant_count.short_description = "Applicants"


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
	list_display = ("job", "skill", "importance", "required_level")
	list_filter = ("importance", "required_level", "skill")
	search_fields = ("job__title", "skill__name")
