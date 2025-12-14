from django.urls import path

from .views import LoginView, ProfileView, RegisterView, UserTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account-register'),
    path('login/', LoginView.as_view(), name='account-login'),
    path('profile/', ProfileView.as_view(), name='account-profile'),
    path('token/', UserTokenView.as_view(), name='account-token'),
]
