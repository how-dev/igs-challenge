from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class EmployeePermissions(BasePermission):
    protected_allowed_methods = ("GET", "PATCH", "PUT", "DELETE", "POST")

    def has_permission(self, request, _):
        method = request.method
        user = request.user

        if isinstance(user, AnonymousUser):
            return False

        is_rh = user.department.name == "RH"
        is_allowed_method = method in self.protected_allowed_methods

        return is_rh and is_allowed_method
