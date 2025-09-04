# relationship_app/urls.py

from django.urls import path
from . import views

# Define the app name for namespacing URLs
app_name = 'relationship_app'

urlpatterns = [
    # Function-based view for listing all books
    path('books/', views.list_books, name='list_books'),
    
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