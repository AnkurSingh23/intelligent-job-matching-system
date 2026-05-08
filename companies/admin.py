from django.contrib import admin
from .models import Company, RecruiterProfile


class RecruiterInline(admin.TabularInline):
    model = RecruiterProfile
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name', 'city')
    inlines = [RecruiterInline]
    ordering = ('name',)


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'company')
    list_filter = ('company',)
    search_fields = ('name', 'user__email', 'company__name')
    ordering = ('name',)
