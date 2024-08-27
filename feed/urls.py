from django.urls import path
from feed.views import AdModelView, CommentModelView
from feed.const import DETAILS_OBJECT_METHODS, OBJECT_METHODS

urlpatterns = [
    path("ad", AdModelView.as_view(OBJECT_METHODS)),
    path("ad/<int:pk>", AdModelView.as_view(DETAILS_OBJECT_METHODS)),
    path("<int:ad_id>/comment", CommentModelView.as_view(OBJECT_METHODS)),
    path(
        "<int:ad_id>/comment/<int:pk>", CommentModelView.as_view(DETAILS_OBJECT_METHODS)
    ),
]
