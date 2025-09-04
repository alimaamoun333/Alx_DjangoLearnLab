# relationship_app/query_samples.py

"""
Django ORM Query Samples demonstrating ForeignKey, ManyToMany, and OneToOne relationships

To run this script:
1. Make sure you're in your Django project directory
2. Run: python manage.py shell
3. In the shell, run: exec(open('relationship_app/query_samples.py').read())

Or create sample data first by running the setup_sample_data() function
"""

from relationship_app.models import Author, Book, Library, Librarian

def setup_sample_data():
    """
    Create sample data for testing queries
    Run this first to populate your database
    """
    print("Setting up sample data...")
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Agatha Christie")
    
    # Create books with ForeignKey relationships
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="Murder on the Orient Express", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Public Library")
    library2 = Library.objects.create(name="University Library")
    library3 = Library.objects.create(name="Community Library")
    
    # Create ManyToMany relationships (books in libraries)
    library1.books.add(book1, book2, book3)  # Central Library has Harry Potter books and 1984
    library2.books.add(book3, book4, book5)  # University Library has Orwell and Christie books
    library3.books.add(book1, book5)         # Community Library has one Harry Potter and one Christie
    
    # Create librarians with OneToOne relationships
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    librarian3 = Librarian.objects.create(name="Carol Williams", library=library3)
    
    print("Sample data created successfully!")
    print(f"Created {Author.objects.count()} authors")
    print(f"Created {Book.objects.count()} books")
    print(f"Created {Library.objects.count()} libraries")
    print(f"Created {Librarian.objects.count()} librarians")
    print("-" * 50)

# ... (rest of the functions - query_books_by_author, query_books_in_library, etc.)