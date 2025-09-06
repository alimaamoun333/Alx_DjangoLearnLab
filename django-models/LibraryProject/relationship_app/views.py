from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Book, Author, UserProfile
from django.forms import ModelForm


class BookForm(ModelForm):
    """Form for creating and editing books"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'isbn', 'pages', 'cover', 'language']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }


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


# Permission-protected views for book operations
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """Add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been added successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Book',
        'action': 'Add',
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/add_book.html', context)


@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """Edit an existing book - requires can_change_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" has been updated successfully!')
            return redirect('relationship_app:list_books')
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
    return render(request, 'relationship_app/edit_book.html', context)


@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """Delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" has been deleted successfully!')
        return redirect('relationship_app:list_books')
    
    context = {
        'book': book,
        'page_title': f'Delete "{book.title}"',
        'user': request.user,
        'user_role': request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown',
    }
    return render(request, 'relationship_app/delete_book.html', context)


# Role-based views from previous implementation
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
    # Template: relationship_app/admin_view.html
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
    # Template: relationship_app/librarian_view.html
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
    # Template: relationship_app/member_view.html
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
    """Home view that shows different content based on user role"""
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'No Role'
    
    context = {
        'user': request.user,
        'role': user_role,
        'page_title': 'Dashboard Home',
    }
    return render(request, 'relationship_app/home.html', context)