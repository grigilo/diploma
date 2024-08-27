from django.urls import path
from user.views import UserModelViewSet
from feed.const import DETAILS_OBJECT_METHODS

urlpatterns = [
    path("me", UserModelViewSet.as_view(DETAILS_OBJECT_METHODS)),
    path("profile/<int:pk>", UserModelViewSet.as_view({"get": "retrieve"})),
]
