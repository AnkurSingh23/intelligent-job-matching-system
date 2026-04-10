from django.contrib import admin
from .models import Company, RecruiterProfile


class RecruiterInline(admin.TabularInline):
	model = RecruiterProfile
	extra = 1


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "city", "recruiter_count")
	list_filter = ("city",)
	search_fields = ("name", "city")
	inlines = [RecruiterInline]

	def recruiter_count(self, obj):
		return obj.recruiterprofile_set.count()

	recruiter_count.short_description = "Recruiters"


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "user", "company")
	list_filter = ("company",)
	search_fields = ("name", "user__email", "company__name")
