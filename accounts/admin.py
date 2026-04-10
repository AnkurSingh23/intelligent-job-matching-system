from django.contrib import admin
from .models import User

admin.site.site_header = "My Job Playground Admin"
admin.site.site_title = "Job Playground Admin"
admin.site.index_title = "Platform Management"


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)