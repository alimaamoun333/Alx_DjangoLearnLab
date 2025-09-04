# relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Book, Library, Author, Librarian

def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Returns a simple text list of book titles and their authors.
    """
    # Get all books from the database
    books = Book.objects.all()
    
    # For simple text output (without template)
    if request.GET.get('format') == 'text':
        response_content = "List of All Books:\n\n"
        for book in books:
            response_content += f"• {book.title} by {book.author.name}\n"
        return HttpResponse(response_content, content_type="text/plain")
    
    # For HTML template rendering
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)

def list_books_simple(request):
    """
    Alternative simple function-based view for listing books
    Returns plain text response
    """
    books = Book.objects.all()
    book_list = []
    
    for book in books:
        book_list.append(f"{book.title} by {book.author.name}")
    
    response_content = "\n".join(book_list)
    return HttpResponse(response_content, content_type="text/plain")

class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books available in that library.
    Utilizes Django's DetailView.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        """
        Add extra context data to the template
        """
        context = super().get_context_data(**kwargs)
        # The library object is automatically available as 'library'
        # We can add additional context if needed
        library = self.get_object()
        context['book_count'] = library.books.count()
        context['librarian'] = getattr(library, 'librarian', None)
        return context

class LibraryListView(ListView):
    """
    Class-based view that displays a list of all libraries.
    Alternative class-based view using ListView.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        """
        Optimize the queryset by prefetching related books
        """
        return Library.objects.prefetch_related('books__author')

class BookDetailView(DetailView):
    """
    Class-based view for displaying individual book details
    """
    model = Book
    template_name = 'relationship_app/book_detail.html'
    context_object_name = 'book'

def library_books(request, library_id):
    """
    Function-based view to display books in a specific library
    Alternative to the class-based approach
    """
    library = get_object_or_404(Library, pk=library_id)
    books = library.books.all()
    
    context = {
        'library': library,
        'books': books,
        'book_count': books.count()
    }
    return render(request, 'relationship_app/library_books.html', context)

def author_books(request, author_name):
    """
    Function-based view to display all books by a specific author
    """
    author = get_object_or_404(Author, name=author_name)
    books = author.books.all()
    
    context = {
        'author': author,
        'books': books,
        'book_count': books.count()
    }
    return render(request, 'relationship_app/author_books.html', context)