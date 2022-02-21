from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from apps.employee.models import EmployeeModel
from apps.department.serializers import DepartmentModel

fake = Faker()


class FinalUserEndpointTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.rh_department = DepartmentModel.objects.create(
            name="RH"
        )

        cls.rh_employee = EmployeeModel.objects.create(
            name=fake.name(),
            email="rh@igs-software.com.br",
            password=make_password("rh_test"),
            is_active=True,
            date_joined=timezone.now(),
            last_login=timezone.now(),
            document="00000000000",
            department=cls.rh_department
        )

        cls.no_rh_department = DepartmentModel.objects.create(
            name="Developer"
        )

        cls.no_rh_employee = EmployeeModel.objects.create(
            name=fake.name(),
            email="no_rh@igs-software.com.br",
            password=make_password("no_rh_test"),
            is_active=True,
            date_joined=timezone.now(),
            last_login=timezone.now(),
            document="00000000001",
            department=cls.no_rh_department
        )

        cls.rh_employee_token = Token.objects.get_or_create(user=cls.rh_employee)[0]
        cls.no_rh_employee_token = Token.objects.get_or_create(user=cls.no_rh_employee)[0]

        cls.endpoints = {
            "login": "/login/",
            "employee": "/employee/"
        }

    def test_cant_GET_employee_unauthenticated(self):
        response = self.client.get(self.endpoints["employee"])

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_POST_employee_unauthenticated(self):
        response = self.client.post(self.endpoints["employee"])

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_PATCH_employee_unauthenticated(self):
        response = self.client.patch(self.endpoints["employee"] + "1/")

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_PUT_employee_unauthenticated(self):
        response = self.client.put(self.endpoints["employee"] + "1/")

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_DELETE_employee_unauthenticated(self):
        response = self.client.get(self.endpoints["employee"] + "1/")

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_login_with_invalid_credentials(self):
        request = {
            "path": self.endpoints["login"],
            "data": {
                "email": "rh@igs-software.com.br",
                "password": "invalid"
            }
        }

        response = self.client.post(**request)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_login_with_valid_email_invalid_password(self):
        request = {
            "path": self.endpoints["login"],
            "data": {
                "email": "invalid_credentials@invalid.com",
                "password": "invalid"
            }
        }

        response = self.client.post(**request)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_login_with_valid_credentials(self):
        request = {
            "path": self.endpoints["login"],
            "data": {
                "email": "rh@igs-software.com.br",
                "password": "rh_test"
            }
        }

        response = self.client.post(**request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cant_GET_employee_with_invalid_token(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer invalid_token"
        }
        self.client.credentials(**headers)
        response = self.client.get(self.endpoints["employee"])

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_GET_employee_with_valid_token_but_no_rh_employee(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.no_rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.get(self.endpoints["employee"])

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_GET_employee_with_valid_token_and_is_rh_employee(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.get(self.endpoints["employee"])

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cant_POST_employee_with_invalid_token(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer invalid_token"
        }
        self.client.credentials(**headers)
        response = self.client.post(self.endpoints["employee"], format="json")

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_POST_employee_with_valid_token_but_no_rh_employee(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.no_rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.post(self.endpoints["employee"], format="json")

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_POST_employee_with_valid_token_and_is_rh_employee(self):
        request = {
            "path": self.endpoints["employee"],
            "data": {
                "name": "Test",
                "email": "test@test.com",
                "password": "bla",
                "document": "62208311361",
                "department": {
                    "name": "test"
                },
                "is_staff": True,
                "is_superuser": True
            }
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.post(**request, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_cant_POST_employee_with_valid_token_and_is_rh_employee_but_invalid_document(self):
        request = {
            "path": self.endpoints["employee"],
            "data": {
                "name": "Test",
                "email": "test@test.com",
                "password": "bla",
                "document": "12345678911",
                "department": {
                    "name": "test"
                },
                "is_staff": True,
                "is_superuser": True
            }
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.post(**request, format="json")

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_PATCH_employee_with_valid_token_and_is_rh_employee_but_invalid_document(self):
        request = {
            "path": self.endpoints["employee"] + f"{self.rh_employee.id}/",
            "data": {
                "document": "12345678911"
            }
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.patch(**request, format="json")

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_PATCH_employee_with_valid_token_and_is_rh_employee(self):
        request = {
            "path": self.endpoints["employee"] + f"{self.rh_employee.id}/",
            "data": {
                "document": "90078144191",
                "password": "test",
                "department": {
                    "name": "Developer"
                }
            }
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.patch(**request, format="json")

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_DELETE_employee_with_valid_token_and_is_rh_employee(self):
        request = {
            "path": self.endpoints["employee"] + f"{self.no_rh_employee.id}/",
        }
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.rh_employee_token}"
        }
        self.client.credentials(**headers)
        response = self.client.delete(**request, format="json")

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)



