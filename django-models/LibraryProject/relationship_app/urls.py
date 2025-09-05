# relationship_app/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books
from . import views

# Define the app name for namespacing URLs
app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs using Django's built-in views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Function-based view for listing all books
    path('books/', views.list_books, name='list_books'),
    
    # Protected version of books (requires login)
    path('books/protected/', views.list_books_protected, name='list_books_protected'),
    
    # Alternative simple function-based view
    path('books/simple/', views.list_books_simple, name='list_books_simple'),
    
    # Class-based view for library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Class-based view for listing all libraries
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Class-based view for book detail
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    
    # Function-based view for library books (alternative approach)
    path('library/<int:library_id>/books/', views.library_books, name='library_books'),
    
    # Function-based view for author books
    path('author/<str:author_name>/books/', views.author_books, name='author_books'),
    
    # Root URL for the app (redirects to books list)
    path('', views.list_books, name='home'),
]

app_name = 'rbac'  # Role-Based Access Control app namespace

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Role-specific views
    path('admin/', views.admin_view, name='admin_dashboard'),
    path('librarian/', views.librarian_view, name='librarian_dashboard'),
    path('member/', views.member_view, name='member_dashboard'),
    
    # Access control
    path('access-denied/', views.access_denied_view, name='access_denied'),
    
    # Authentication URLs (optional - you might have these in your main urls.py)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Alternative URL patterns if you prefer different naming conventions
# urlpatterns = [
#     path('', views.home_view, name='home'),
#     path('admin-panel/', views.admin_view, name='admin_view'),
#     path('librarian-panel/', views.librarian_view, name='librarian_view'),
#     path('member-panel/', views.member_view, name='member_view'),
#     path('forbidden/', views.access_denied_view, name='access_denied'),
# ]