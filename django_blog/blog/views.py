from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Post
from .forms import RegistrationForm, ProfileForm


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'registration/logout.html'


def home(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})


def posts(request):
    posts_qs = Post.objects.order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts_qs})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})
