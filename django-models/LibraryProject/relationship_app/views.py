from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Book, Author, UserProfile
from django.forms import ModelForm
from django import forms


class BookForm(ModelForm):
    """Form for creating and editing books"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'isbn', 'pages', 'cover', 'language']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Role constants for consistency
ROLES = {
    'ADMIN': 'Admin',
    'LIBRARIAN': 'Librarian',
    'MEMBER': 'Member'
}


def user_has_role(role):
    """
    Helper function to create a test function for checking user roles.
    Returns a function that can be used with @user_passes_test decorator.
    """
    def check_role(user):
        if not user.is_authenticated:
            return False
        try:
            return hasattr(user, 'profile') and user.profile.role == role
        except:
            return False
    return check_role


# Create role checkers using the factory function
is_admin = user_has_role(ROLES['ADMIN'])
is_librarian = user_has_role(ROLES['LIBRARIAN'])
is_member = user_has_role(ROLES['MEMBER'])


def has_book_permission(user, permission_type):
    """Check if user has specific book permission based on their role"""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    
    role = user.profile.role
    # Admin has all permissions
    if role == ROLES['ADMIN']:
        return True
    # Librarian has add/edit permissions but not delete
    elif role == ROLES['LIBRARIAN']:
        return permission_type in ['add', 'change']
    # Member has no permissions
    elif role == ROLES['MEMBER']:
        return False
    return False


# Book list view - accessible to all authenticated users
@login_required
def list_books(request):
    """Display list of all books"""
    books = Book.objects.all()
    context = {
        'books': books,
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/list_books.html', context)


# Role-protected views for book operations (using role-based checks instead of permissions)
@login_required
def add_book(request):
    """Add a new book - requires Admin or Librarian role"""
    if not has_book_permission(request.user, 'add'):
        return redirect('access_denied')
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been added successfully!')
            return redirect('list_books')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Book',
        'action': 'Add',
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/book_form.html', context)


@login_required
def edit_book(request, book_id):
    """Edit an existing book - requires Admin or Librarian role"""
    if not has_book_permission(request.user, 'change'):
        return redirect('access_denied')
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated successfully!')
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'page_title': f'Edit "{book.title}"',
        'action': 'Edit',
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/book_form.html', context)


@login_required
def delete_book(request, book_id):
    """Delete a book - requires Admin role only"""
    if not has_book_permission(request.user, 'delete'):
        return redirect('access_denied')
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" has been deleted successfully!')
        return redirect('list_books')
    
    context = {
        'book': book,
        'page_title': f'Delete "{book.title}"',
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/delete_book.html', context)


# Role-based dashboard views
@login_required
@user_passes_test(is_admin, login_url='/access-denied/')
def admin_view(request):
    """Admin-only view"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Admin Dashboard',
        'welcome_message': f'Welcome {request.user.username}! You have administrator privileges.',
    }
    return render(request, 'relationship_app/admin_view.html', context)


@login_required
@user_passes_test(is_librarian, login_url='/access-denied/')
def librarian_view(request):
    """Librarian-only view"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Librarian Dashboard',
        'welcome_message': f'Welcome {request.user.username}! You have librarian access.',
    }
    return render(request, 'relationship_app/librarian_view.html', context)


@login_required
@user_passes_test(is_member, login_url='/access-denied/')
def member_view(request):
    """Member-only view"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Member Dashboard',
        'welcome_message': f'Welcome {request.user.username}! You have member access.',
    }
    return render(request, 'relationship_app/member_view.html', context)


def access_denied_view(request):
    """View to display when user doesn't have permission"""
    context = {
        'message': 'You do not have permission to access this page.',
        'user_role': request.user.profile.role if request.user.is_authenticated and hasattr(request.user, 'profile') else 'Unknown'
    }
    return render(request, 'relationship_app/access_denied.html', context, status=403)


@login_required
def home_view(request):
    """Home view that redirects to appropriate dashboard based on role"""
    if not hasattr(request.user, 'profile'):
        return redirect('access_denied')
    
    role = request.user.profile.role
    if role == ROLES['ADMIN']:
        return redirect('admin_view')
    elif role == ROLES['LIBRARIAN']:
        return redirect('librarian_view')
    elif role == ROLES['MEMBER']:
        return redirect('member_view')
    else:
        return redirect('access_denied')


# Additional view for book details
@login_required
def book_detail(request, book_id):
    """View details of a specific book"""
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/book_detail.html', context)