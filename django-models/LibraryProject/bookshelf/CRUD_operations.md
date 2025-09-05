# Django CRUD Operations Documentation

This document contains all the CRUD operations performed on the Book model using Django shell.

## Prerequisites
1. Django project is set up
2. App is created and added to INSTALLED_APPS
3. Book model is defined in models.py
4. Migrations are created and applied:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Opening Django Shell
```bash
python manage.py shell
```

---

## CREATE Operation

### Command
```python
# Import the model
from myapp.models import Book

# Create a new Book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

# Display the created book
print(f"Created book: {book}")
print(f"Book ID: {book.id}")
```

### Actual Output
```
Created book: 1984 by George Orwell (1949)
Book ID: 1
```

---

## RETRIEVE Operation

### Command
```python
# Retrieve the book by ID
book = Book.objects.get(id=1)

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Retrieve all books
all_books = Book.objects.all()
print(f"\nAll books in database: {len(all_books)}")
for book in all_books:
    print(f"- {book}")
```

### Actual Output
```
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949

All books in database: 1
- 1984 by George Orwell (1949)
```

---

## UPDATE Operation

### Command
```python
# Retrieve the book to update
book = Book.objects.get(id=1)

# Display current title
print(f"Current title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
updated_book = Book.objects.get(id=1)
print(f"Updated title: {updated_book.title}")
print(f"Complete book info: {updated_book}")
```

### Actual Output
```
Current title: 1984
Updated title: Nineteen Eighty-Four
Complete book info: Nineteen Eighty-Four by George Orwell (1949)
```

---

## DELETE Operation

### Command
```python
# Retrieve the book to delete
book = Book.objects.get(id=1)
print(f"Book to delete: {book}")

# Delete the book
book.delete()
print("Book deleted successfully")

# Confirm deletion by checking all books
all_books = Book.objects.all()
print(f"Total books after deletion: {len(all_books)}")

# Try to retrieve the deleted book
try:
    deleted_book = Book.objects.get(id=1)
    print(f"Found book: {deleted_book}")
except Book.DoesNotExist:
    print("Confirmed: Book with ID 1 no longer exists")
```

### Actual Output
```
Book to delete: Nineteen Eighty-Four by George Orwell (1949)
Book deleted successfully
Total books after deletion: 0
Confirmed: Book with ID 1 no longer exists
```

---

## Summary

All CRUD operations completed successfully:
- ✅ **CREATE**: Book instance created with title "1984"
- ✅ **RETRIEVE**: Book data retrieved and displayed
- ✅ **UPDATE**: Title updated from "1984" to "Nineteen Eighty-Four"  
- ✅ **DELETE**: Book instance deleted and deletion confirmed

## Key Django ORM Methods Used
- `Model()` - Constructor for creating instances
- `save()` - Saves object to database
- `objects.get()` - Retrieves single object
- `objects.all()` - Retrieves all objects
- `delete()` - Deletes object from database

## Next Steps
Consider exploring:
- QuerySet methods like `filter()`, `exclude()`
- Field lookups like `__contains`, `__gt`, `__lt`
- Relationships between models (ForeignKey, ManyToMany)
- Django admin interface for GUI-based CRUD operations