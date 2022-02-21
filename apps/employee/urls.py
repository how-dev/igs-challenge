from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EmployeeLogin, EmployeeViewSet

router = DefaultRouter()
router.register("employee", EmployeeViewSet)

urlpatterns = [
    path("login/", EmployeeLogin.as_view()),
]

urlpatterns += router.urls
