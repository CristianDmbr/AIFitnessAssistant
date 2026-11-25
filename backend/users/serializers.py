from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.db import transaction
from .tokens import EmailVerificationToken
from .emails import send_verification_email

User = get_user_model()

from .models import FitnessProfile

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email"]
    
    def validate_email(self,value):
        if User.objects.filter(email__iexact = value).exists():
            raise serializers.ValidationError(
                "This email is already registered"
            )
        
        return value.lower()
    
    def create(self,validated_data):
        user = User(
            username = validated_data["username"],
            email = validated_data["email"],
            is_email_verified = False,
            is_active = False
        )

        user.set_unusable_password()
        user.save()

        token = EmailVerificationToken.generate(user)

        transaction.on_commit(
            lambda: send_verification_email(user, token)
        )

        return user