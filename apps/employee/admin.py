from django.contrib import admin

from apps.employee.models import EmployeeModel
from django.contrib.auth.models import Group


@admin.register(EmployeeModel)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department", "is_active")
    ordering = ("id",)
    search_fields = ("name", "email", "department__name")
    readonly_fields = ("last_login", "date_joined")
    fields = ("name", "email", "password", "department", "is_staff", "is_superuser", "last_login", "date_joined")


admin.site.unregister(Group)
