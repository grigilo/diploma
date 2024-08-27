from rest_framework import serializers

from auth.models import User
from auth.validators import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Класс для сериализации регистрации пользователя
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("email", "password")


class UserLoginSerializer(serializers.Serializer):
    """
    Класс для сериализации авторизации пользователя
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    @staticmethod
    def get_user(data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Пользователь с таким email не найден"
                )

            if user.check_password(password):
                data["user"] = user
                return user
            else:
                raise serializers.ValidationError("Неверный пароль")

        return data


class ResetPasswordSerializer(serializers.Serializer):
    """
    Класс для сериализации обновления пароля
    """

    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    @staticmethod
    def update_password(password: str, user: User) -> None:
        try:
            user = User.objects.get(id=user.pk)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")
        else:
            user.set_password(password)
            user.save()
