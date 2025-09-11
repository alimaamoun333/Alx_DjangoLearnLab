# Import the model
from myapp.models import Book

# Create a new Book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Alternative method using create()
# book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Display the created book
print(f"Created book: {book}")
print(f"Book ID: {book.id}")