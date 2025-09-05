# relationship_app/views.py
# Add these authentication views to your existing views.py file

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Book, Author, Librarian
from .models import Library

# Your existing views here (keep all your previous view functions)...

# Authentication Views

class CustomLoginView(LoginView):
    """
    Custom login view using Django's built-in LoginView
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('relationship_app:list_books')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in!')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    """
    Custom logout view using Django's built-in LogoutView
    """
    template_name = 'relationship_app/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

def register(request):
    """
    User registration view using Django's built-in UserCreationForm
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)  # Automatically log in the user after registration
            return redirect('relationship_app:list_books')  # Redirect to books list
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Enhanced existing views with authentication decorators

@login_required
def list_books_protected(request):
    """
    Protected version of list_books that requires authentication
    """
    books = Book.objects.all()
    
    if request.GET.get('format') == 'text':
        response_content = f"List of All Books (User: {request.user.username}):\n\n"
        for book in books:
            response_content += f"• {book.title} by {book.author.name}\n"
        return HttpResponse(response_content, content_type="text/plain")
    
    context = {
        'books': books,
        'user': request.user
    }
    return render(request, 'relationship_app/list_books.html', context)

# Keep all your existing views (list_books, LibraryDetailView, etc.) as they were...