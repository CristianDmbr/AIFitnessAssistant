from django.contrib import admin
from django.urls import path, include

from .views import RegistrationView, VerificationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name = "register"),
    path("verify-email/", VerificationView.as_view(), name = "verify-email"),
]