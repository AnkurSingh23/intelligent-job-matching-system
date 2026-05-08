from django.contrib import admin
from .models import Job, JobSkill
from applications.models import JobApplication


class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 1


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    readonly_fields = ('applied_at',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'created_by', 'created_at', 'location')
    list_filter = ('job_type', 'location', 'created_at')
    search_fields = ('title', 'company__name', 'location')
    inlines = [JobSkillInline, JobApplicationInline]
    ordering = ('-created_at',)


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('job', 'skill', 'importance', 'required_level')
    list_filter = ('importance', 'required_level')
    search_fields = ('job__title', 'skill__name')
    ordering = ('-id',)
