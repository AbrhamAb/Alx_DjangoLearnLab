from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('login/', views.login_placeholder, name='login'),
    path('register/', views.register_placeholder, name='register'),
]
