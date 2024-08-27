from django.db import transaction
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from auth import serializers as auth_serializer
from auth.models import User
from auth.services.email_sender import AuthenticationTemplate
from auth.services.jwt import ConfirmationToken, AccessToken


class RegisterAccount(generics.CreateAPIView):
    """
    Класс для регистрации пользователей
    """

    serializer_class = auth_serializer.UserRegisterSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)
        authentication_template = AuthenticationTemplate(
            email=serializer.validated_data.get("email")
        )
        authentication_template.send_message_to_email()


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """

    def get(self, request, token, *args, **kwargs):
        if not token:
            return JsonResponse(status=400, data={"message": "Нет токена"})

        confirmation_token_instance = ConfirmationToken()
        decoded_payload = confirmation_token_instance.decode(token)

        user_email = decoded_payload.get("email")
        user = User.objects.filter(email=user_email).first()

        if not user:
            return JsonResponse(status=404, data={"message": "Пользователь не найден"})

        user.is_active = True
        user.save()

        return JsonResponse(status=200, data={"message": "Аккаунт активирован"})


@extend_schema(
    request=inline_serializer(
        name="ResetPasswordSerializer",
        fields={
            "new_password": serializers.CharField(),
        },
    )
)
class ResetPassword(APIView):
    """
    Класс для обновления пароля
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = auth_serializer.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = request.data.get("new_password")
        serializer.update_password(new_password, self.request.user)

        return JsonResponse(
            {"message": "Пароль успешно обновлен"}, status=status.HTTP_200_OK
        )
