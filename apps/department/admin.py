from django.contrib import admin

from .models import DepartmentModel


@admin.register(DepartmentModel)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "date_joined")
