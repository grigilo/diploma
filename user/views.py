from user.serializers import UserSerializer, UserUpdateSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from auth.models import User


class UserModelViewSet(ModelViewSet):
    """
    Класс представления пользователей
    """

    queryset = User
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "update":
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user
