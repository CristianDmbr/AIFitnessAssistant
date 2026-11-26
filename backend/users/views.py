from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import RegistrationSerializer
from .tokens import EmailVerificationToken


class RegistrationView(APIView):

    def post(self,request):
        serializer = RegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message" : "Registration Successfull Please verify email"},
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )


class VerificationView(APIView):
    
    def post(self, request):
        token = request.data.get("token")

        user_id = EmailVerificationToken.verify(token)

        if user_id is None:
            return Response(
                {"error" : "Invalid or expired verification code"},
                status = status.HTTP_400_BAD_REQUEST
            )
        else:
            User = get_user_model()

            try:
                user = get_object_or_404(User, pk = user_id)

                if user.is_email_verified:
                    return Response(
                        {"message" : "Email has already been verified"},
                        status = status.HTTP_200_OK
                    )
                else:
                    user.is_email_verified = True
                    user.is_active = True
                    user.save()

                    return Response(
                        {"message" : "Email verified successfully. Your account is now active. "},
                        status = status.HTTP_200_OK
                    )

            except User.DoesNotExist:
                return Response(
                    {
                        "error" : "User does not exist",
                        "username" : user.username,
                        "email" : user.email,
                        "user_pk" : user.pk
                    },
                    status = status.HTTP_404_NOT_FOUND
                )