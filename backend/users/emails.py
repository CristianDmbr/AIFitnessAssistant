# Email related functions
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, token):

    verification_link = (
        f"http://localhost:5173/verify-email/?token={token}"
    )

    subject = "Verify your email address"

    message = f"""
    Hello {user.username},

    Thank you for registering!

    Please click the link below to verify your email address:

    {verification_link}

    This link expires in 24 hours.

    If you did not create this account, you can ignore this email.
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )