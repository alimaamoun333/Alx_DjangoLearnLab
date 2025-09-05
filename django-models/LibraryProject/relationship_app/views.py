from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User


def user_has_role(role):
    """
    Helper function to create a test function for checking user roles.
    Returns a function that can be used with @user_passes_test decorator.
    """
    def check_role(user):
        if not user.is_authenticated:
            return False
        try:
            return user.profile.role == role
        except:
            return False
    return check_role


def is_admin(user):
    """Check if user has Admin role"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Admin'
    except:
        return False


def is_librarian(user):
    """Check if user has Librarian role"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Librarian'
    except:
        return False


def is_member(user):
    """Check if user has Member role"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == 'Member'
    except:
        return False


@login_required
@user_passes_test(is_admin, login_url='/access-denied/')
def admin_view(request):
    """
    Admin-only view that displays administrative content.
    Only users with 'Admin' role can access this view.
    """
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Admin Dashboard',
        'welcome_message': f'Welcome {request.user.username}! You have administrator privileges.',
    }
    return render(request, 'admin_view.html', context)


@login_required
@user_passes_test(is_librarian, login_url='/access-denied/')
def librarian_view(request):
    """
    Librarian-only view that displays librarian-specific content.
    Only users with 'Librarian' role can access this view.
    """
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Librarian Dashboard',
        'welcome_message': f'Welcome {request.user.username}! You have librarian access.',
    }
    return render(request, 'librarian_view.html', context)


@login_required
@user_passes_test(is_member, login_url='/access-denied/')
def member_view(request):
    """
    Member-only view that displays member-specific content.
    Only users with 'Member' role can access this view.
    """
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Member Dashboard',
        'welcome_message': f'Welcome {request.user.username}! You have member access.',
    }
    return render(request, 'member_view.html', context)


def access_denied_view(request):
    """
    View to display when user doesn't have permission to access a page.
    """
    context = {
        'message': 'You do not have permission to access this page.',
        'user_role': request.user.profile.role if request.user.is_authenticated and hasattr(request.user, 'profile') else 'Unknown'
    }
    return render(request, 'access_denied.html', context, status=403)


@login_required
def home_view(request):
    """
    Home view that shows different content based on user role.
    """
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'No Role'
    
    context = {
        'user': request.user,
        'role': user_role,
        'page_title': 'Dashboard Home',
    }
    return render(request, 'relationship_app/home.html', context)
    # pass