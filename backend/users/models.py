from django.db import models

# AbstractUser Django's existing user functionality and it allows us to add additional fields.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_email_verified = models.BooleanField(default = False)