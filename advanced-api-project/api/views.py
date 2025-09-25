from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# ---------------------------
# BOOK CRUD API USING GENERIC VIEWS
# ---------------------------

class BookListView(generics.ListAPIView):
    """
    GET: List all books.
    - Unauthenticated users: read-only
    - Authenticated users: read-only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID.
    - Unauthenticated users: read-only
    - Authenticated users: read-only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    - Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    - Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book.
    - Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
