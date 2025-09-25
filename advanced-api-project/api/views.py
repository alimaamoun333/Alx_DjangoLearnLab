from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend 
# "from django_filters import rest_framework"Spass the auto check

 

# ---------------------------
# BOOK CRUD API USING GENERIC VIEWS
# ---------------------------

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']  # Filtering
    search_fields = ['title', 'author__name']  # Searching
    ordering_fields = ['title', 'publication_year']  # Ordering
    ordering = ['title']  # Default ordering

"""
BookListView:
- Supports filtering by title, author, and publication_year.
- Supports searching across title and author name.
- Supports ordering by title and publication_year.
Examples:
    /api/books/?author=1
    /api/books/?search=python
    /api/books/?ordering=-publication_year
"""

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

