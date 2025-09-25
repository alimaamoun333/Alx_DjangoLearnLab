from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .models import Book
from .serializers import BookSerializer

# ---------------------------
# BOOK CRUD API USING GENERIC VIEWS
# ---------------------------

class BookListView(generics.ListAPIView):
    """
    Handles GET requests to retrieve all Book instances.
    Open to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view


class BookDetailView(generics.RetrieveAPIView):
    """
    Handles GET requests to retrieve a single Book by its ID.
    Open to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Handles POST requests to create a new Book instance.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Example customization: could log creator or apply additional validation
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Handles PUT/PATCH requests to update an existing Book instance.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Custom behavior: log who updated the book
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Handles DELETE requests to remove a Book instance.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
