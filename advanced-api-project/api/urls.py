from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),             # GET all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'), # GET single book
    path('books/create/', BookCreateView.as_view(), name='book-create'),   # POST new book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # PUT/PATCH update
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # DELETE
]
 # "books/update", "books/delete"