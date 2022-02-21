from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from services.person_token import BearerToken
from .filters import EmployeeFilter
from .models import EmployeeModel
from .permissions import EmployeePermissions
from .serializers import LoginSerializer, EmployeeSerializer
from services.user_flow import GenericErrors, ResetToken, CPFLogics
from django_filters import rest_framework as filters


class EmployeeLogin(APIView, GenericErrors):
    def post(self, request):
        data = request.data

        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = data["email"]
        password = data["password"]

        try:
            user = EmployeeModel.objects.get(email=email)
        except EmployeeModel.DoesNotExist:
            response = self.failure_result()
            return Response(**response)

        is_valid_password = check_password(password, user.password)

        if is_valid_password:
            user.last_login = timezone.now()
            user.save()
            data = EmployeeSerializer(user).data

            token = Token.objects.get_or_create(user=user)[0]
            reset_token = ResetToken(token_key=token.key, user=user, hour=1)
            token = reset_token.reset_token()
            data["token"] = token.key

            response = self.success_result(data)
            return Response(**response)
        else:
            response = self.failure_result()
            return Response(**response)


class EmployeeViewSet(ModelViewSet, CPFLogics):
    queryset = EmployeeModel.objects.filter(is_active=True).order_by("id")
    serializer_class = EmployeeSerializer
    authentication_classes = [BearerToken]
    permission_classes = [EmployeePermissions]
    throttle_classes = [UserRateThrottle]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter

    @method_decorator(cache_page(60, key_prefix="list_employee"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if "document" in request.data:
            cpf = request.data["document"]
            is_valid_cpf = self.validate_cpf(cpf)

            if not is_valid_cpf:
                return Response({"detail": "invalid brazilian document"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if "document" in request.data:
            cpf = request.data["document"]
            is_valid_cpf = self.validate_cpf(cpf)

            if not is_valid_cpf:
                return Response({"detail": "invalid brazilian document"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
