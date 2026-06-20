from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .serializers import RegisterSerializer, ChangePasswordSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user)
        return Response({
            'email': user.email,
            'access': str(token.access_token),
            'refresh': str(token),
        }, status=status.HTTP_201_CREATED)


class TestEmailSend(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        send_mail(
            'subject here',
            'Here is the subject',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

        return Response("email sent.")




class ChangePasswordApiView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.data.get('old_password')):
            return Response(
                {'old_password': 'رمز عبور قدیمی اشتباه است.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response(
            {'detail': 'رمز عبور با موفقیت تغییر کرد.'},
            status=status.HTTP_200_OK,
        )