from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import Post


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            # Return form with error context for template
            return render(request, 'core/login.html', {
                'form': type('FormErrors', (), {'errors': True})(),
            })

    return render(request, 'core/login.html')


@require_POST
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been signed out successfully.')
    return redirect('login')


def _get_time_of_day():
    """Return greeting based on time of day."""
    hour = datetime.now().hour
    if hour < 12:
        return 'morning'
    elif hour < 17:
        return 'afternoon'
    else:
        return 'evening'


@login_required(login_url='login')
def dashboard_view(request):
    """Main dashboard page."""
    total_posts = Post.objects.count()
    total_users = User.objects.count()
    recent_posts = Post.objects.order_by('-created_at')[:5]

    context = {
        'total_posts': total_posts,
        'total_users': total_users,
        'recent_posts': recent_posts,
        'time_of_day': _get_time_of_day(),
    }
    return render(request, 'core/dashboard.html', context)


@login_required(login_url='login')
def home(request):
    """Posts listing page."""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/index.html', {'posts': posts})


@login_required(login_url='login')
def profile_view(request):
    """User profile page."""
    return render(request, 'core/profile.html')
