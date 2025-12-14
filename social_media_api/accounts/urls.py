from django.urls import path

from .views import (
    FollowUserView,
    LoginView,
    ProfileView,
    RegisterView,
    UnfollowUserView,
    UserTokenView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account-register'),
    path('login/', LoginView.as_view(), name='account-login'),
    path('profile/', ProfileView.as_view(), name='account-profile'),
    path('token/', UserTokenView.as_view(), name='account-token'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='account-follow'),
    path('unfollow/<int:user_id>/',
         UnfollowUserView.as_view(), name='account-unfollow'),
]
