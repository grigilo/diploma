from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from auth import views

urlpatterns = [
    path("register", views.RegisterAccount.as_view()),
    path("confirm_account/<str:token>", views.ConfirmAccount.as_view()),
    path("reset_password", views.ResetPassword.as_view()),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
