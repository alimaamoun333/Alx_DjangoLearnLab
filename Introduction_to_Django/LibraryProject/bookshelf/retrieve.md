# Retrieve the book by ID (assuming ID is 1)
book = Book.objects.get(id=1)

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Alternative: Retrieve by title
# book = Book.objects.get(title="1984")

# Retrieve all books
all_books = Book.objects.all()
print(f"\nAll books in database: {len(all_books)}")
for book in all_books:
    print(f"- {book}")