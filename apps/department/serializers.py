from rest_framework import serializers
from .models import DepartmentModel


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModel
        fields = ("id", "name")
