from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from feed import serializers
from feed.models import Ad, Comment
from feed.pagination import ResultsSetPagination
from feed.permissions import IsAdminOrOwner


class AdModelView(ModelViewSet):
    """
    Класс представления объявлений
    """

    queryset = Ad.objects.all()
    serializer_class = serializers.AdSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    pagination_class = ResultsSetPagination

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAdminOrOwner]
        elif self.action == "list":
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_class(self):
        match self.action:
            case "create":
                return serializers.AdCreateSerializer
            case "update":
                return serializers.AdUpdateSerializer
            case _:
                return serializers.AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentModelView(ModelViewSet):
    """
    Класс представления комментариев для объявлений
    """

    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAdminOrOwner]
        elif self.action == "list":
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_class(self):
        return (
            serializers.CommentSerializer
            if self.action in ("list", "retrieve")
            else serializers.CommentCreateUpdateSerializer
        )

    def perform_create(self, serializer):
        ad = Ad.objects.get(id=self.kwargs.get("ad_id"))
        serializer.save(author=self.request.user, ad=ad)

    def perform_update(self, serializer):
        ad = Ad.objects.get(id=self.kwargs.get("ad_id"))
        serializer.save(ad=ad)
