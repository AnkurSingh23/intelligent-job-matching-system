from django.contrib import admin
from .models import CandidateProfile, CandidateSkill


class CandidateSkillInline(admin.TabularInline):
	model = CandidateSkill
	extra = 1


# Register your models here.
@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
	list_display = ("id", "full_name", "user", "total_experience", "preferred_location", "expected_salary")
	list_filter = ("preferred_location",)
	search_fields = ("full_name", "user__email", "preferred_location")
	inlines = [CandidateSkillInline]


@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
	list_display = ("candidate", "skill", "proficiency_level", "experience")
	list_filter = ("proficiency_level", "skill")
	search_fields = ("candidate__full_name", "candidate__user__email", "skill__name")
