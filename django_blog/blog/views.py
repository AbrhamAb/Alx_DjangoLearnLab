from django.shortcuts import render
from .models import Post


def home(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})


def posts(request):
    posts_qs = Post.objects.order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts_qs})


def login_placeholder(request):
    return render(request, 'blog/placeholder.html', {'title': 'Login coming soon'})


def register_placeholder(request):
    return render(request, 'blog/placeholder.html', {'title': 'Register coming soon'})
