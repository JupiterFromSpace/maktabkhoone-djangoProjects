from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import RegisterView, TestEmailSend, ChangePasswordApiView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('test-email', TestEmailSend.as_view(), name='test-email'),
    path('change-password/', ChangePasswordApiView.as_view(), name='change-password'),
]
