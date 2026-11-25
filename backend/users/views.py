from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer


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