import random
import os

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from apps.department.models import DepartmentModel
from apps.employee.models import EmployeeModel
from services.user_flow import CPFLogics


class Command(BaseCommand, CPFLogics):
    base_departments = ["RH", "Developer", "Tester", "Financing", "Marketing"]
    queryset = EmployeeModel.objects.all()

    def handle(self, *_, **__):
        if len(self.queryset) >= 500:
            return "This command can only be run once"
        fake = Faker()

        departments = [DepartmentModel.objects.get_or_create(name=department)[0] for department in self.base_departments]
        try:
            EmployeeModel.objects.create(
                name="IGS Tester",
                email="igs_tester@igs-software.com.br",
                password=make_password("1g5@t35t3r"),
                is_active=True,
                document=self.force_valid_cpf(),
                department=DepartmentModel.objects.get(name="RH"),
                is_staff=True,
                is_superuser=True
            )
        except:
            print("")

        print("> This command is creating 500 fake users.")
        print("")
        print("> Creating users...")
        print("> While users are being created, you can test the login endpoints with the following credentials:")
        print('{\n  "email": "igs_tester@igs-software.com.br", \n  "password": "1g5@t35t3r" \n}')
        print('> With this account, you can log into Django-Admin and access the authenticated routes from the employee/ endpoint')
        for _ in range(500):
            try:
                EmployeeModel.objects.create(
                    name=fake.name(),
                    email=fake.unique.email(),
                    password=make_password("."),
                    is_active=True,
                    document=self.force_valid_cpf(),
                    department=departments[random.randrange(0, len(departments))]
                )
            except Exception as e:
                print(e)
                continue

        print("500 fake users was created.")
