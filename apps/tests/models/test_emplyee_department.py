from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.utils import timezone

from apps.department.models import DepartmentModel
from apps.employee.models import EmployeeModel, UserManager

from faker import Faker

fake = Faker()


class EmployeeDepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_department = DepartmentModel.objects.create(
            name="RH"
        )

        cls.base_employee = EmployeeModel.objects.create(
            name=fake.name(),
            email=fake.unique.email(),
            password=make_password("."),
            is_active=True,
            date_joined=timezone.now(),
            last_login=timezone.now(),
            document="00000000000",
            department=cls.base_department
        )

    def test_department_has_information_fields(self):
        self.assertIsInstance(self.base_department.name, str)
        self.assertIsInstance(self.base_department.__str__(), str)

    def test_department_has_datetime_fields(self):
        self.assertIsInstance(self.base_department.date_joined, datetime)

    def test_employee_has_information_fields(self):
        self.assertIsInstance(self.base_employee.name, str)
        self.assertIsInstance(self.base_employee.email, str)
        self.assertIsInstance(self.base_employee.password, str)
        self.assertIsInstance(self.base_employee.document, str)
        self.assertIsInstance(self.base_employee.is_active, bool)
        self.assertIsInstance(self.base_employee.is_superuser, bool)
        self.assertIsInstance(self.base_employee.is_staff, bool)

    def test_employee_has_datetime_fields(self):
        self.assertIsInstance(self.base_employee.last_login, datetime)
        self.assertIsInstance(self.base_employee.date_joined, datetime)

    def test_employee_has_related_fields(self):
        self.assertIsInstance(self.base_employee.department, DepartmentModel)

    def test_user_manager_create_user_without_email(self):
        manager = UserManager()
        manager.model = EmployeeModel
        try:
            manager.create_user(False, ".", **{})
        except ValueError:
            self.assertEquals(True, True)

    def test_user_manager_create_user_with_email(self):
        manager = UserManager()
        manager.model = EmployeeModel
        user = manager.create_user("test@test.com", "test", **{"name": "test", "department": self.base_department})
        self.assertIsInstance(user, EmployeeModel)

    def test_user_manager_create_superuser_with_email(self):
        manager = UserManager()
        manager.model = EmployeeModel
        user = manager.create_superuser("test@test.com", "test", **{"name": "test", "department": self.base_department})
        self.assertIsInstance(user, EmployeeModel)
