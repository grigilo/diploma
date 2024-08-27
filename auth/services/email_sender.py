from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from auth.services.jwt import ConfirmationToken


class AuthenticationTemplate:
    """
    Класс шаблона подтверждения аккаунта по email
    """

    def __init__(self, email: str):
        self.email = email

    def get_message_context(self) -> EmailMultiAlternatives:
        message_text_for_employees, sender = (
            "Подтвердите email",
            settings.EMAIL_HOST_USER,
        )
        confirmation_token = ConfirmationToken().encode(email=self.email)
        account_confirmation_url = (
            f"{settings.BASE_URL}/auth/confirm_account/{confirmation_token}"
        )
        content_for_employees = (
            f"Для активации аккаунта пройдите по ссылке - {account_confirmation_url}"
        )

        message_context = EmailMultiAlternatives(
            message_text_for_employees, content_for_employees, sender, [self.email]
        )

        return message_context

    def send_message_to_email(self) -> None:
        message_context = self.get_message_context()
        message_context.send()
