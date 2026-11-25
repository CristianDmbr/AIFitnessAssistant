from django.core import signing


class EmailVerificationToken:

    SALT = "users.email-verification"

    @staticmethod
    def generate(user):
        return signing.dumps(
            {"user_id": user.pk},
            salt=EmailVerificationToken.SALT
        )

    @staticmethod
    def verify(token):
        try:
            data = signing.loads(
                token,
                salt=EmailVerificationToken.SALT,
                max_age=60 * 60 * 24
            )

            return data["user_id"]

        except signing.BadSignature:
            return None