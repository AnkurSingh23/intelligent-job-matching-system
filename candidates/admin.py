from django.contrib import admin
from .models import CandidateProfile, CandidateSkill


class CandidateSkillInline(admin.TabularInline):
    model = CandidateSkill
    extra = 1


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'total_experience', 'preferred_location')
    list_filter = ('total_experience', 'preferred_location')
    search_fields = ('full_name', 'user__email')
    inlines = [CandidateSkillInline]
    ordering = ('-id',)


@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'skill', 'proficiency_level', 'experience')
    list_filter = ('proficiency_level',)
    search_fields = ('candidate__full_name', 'skill__name')
    ordering = ('-id',)
