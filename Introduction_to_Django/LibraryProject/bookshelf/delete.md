# Retrieve the book to delete
book = Book.objects.get(id=1)
print(f"Book to delete: {book}")

# Delete the book
book.delete()
print("Book deleted successfully")

# Confirm deletion by checking all books
all_books = Book.objects.all()
print(f"Total books after deletion: {len(all_books)}")

# Try to retrieve the deleted book (will raise DoesNotExist exception)
try:
    deleted_book = Book.objects.get(id=1)
    print(f"Found book: {deleted_book}")
except Book.DoesNotExist:
    print("Confirmed: Book with ID 1 no longer exists")

# Alternative bulk delete
# Book.objects.filter(title="Nineteen Eighty-Four").delete()