from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_list(request):
    # Query all books
    books = Book.objects.all()

    # Pass them to the template
    return render(request, 'bookshelf/book_list.html', {'books': books})
