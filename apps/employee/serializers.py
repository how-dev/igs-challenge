from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import EmployeeModel
from ..department.models import DepartmentModel
from ..department.serializers import DepartmentSerializer


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = EmployeeModel
        fields = (
            "id",
            "name",
            "email",
            "document",
            "last_login",
            "date_joined",
            "is_staff",
            "is_superuser",
            "department",
            "password"
        )
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
            "is_staff": {"write_only": True},
            "password": {"required": True, "write_only": True}
        }

    def create(self, validated_data):
        department = validated_data["department"]
        password = validated_data["password"]
        password = make_password(password)
        department = DepartmentModel.objects.get_or_create(**department)[0]

        validated_data["department"] = department
        validated_data["password"] = password

        instance = EmployeeModel.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        if "department" in validated_data:
            department = validated_data["department"]
            department = DepartmentModel.objects.get_or_create(**department)[0]
            instance.department = department

        if "password" in validated_data:
            password = validated_data["password"]
            password = make_password(password)
            instance.password = password

        return instance
