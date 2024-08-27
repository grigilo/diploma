from rest_framework.permissions import BasePermission

from feed.models import Ad
from auth.models import USER_ROLE_CHOICES


class IsOwner(BasePermission):
    message = "Пользователь не является владельцем объявления."

    def has_permission(self, request, view):
        ad_id = view.kwargs.get("pk")

        return Ad.objects.filter(id=ad_id, author=request.user).exists()


class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == USER_ROLE_CHOICES[0][0]:
            return True

        return obj.author == request.user
