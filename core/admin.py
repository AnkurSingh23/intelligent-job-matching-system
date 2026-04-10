from django.contrib import admin
from .models import Skill

# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)
	ordering = ("name",)
