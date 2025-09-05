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

# Alternative bulk update method
# Book.objects.filter(id=1).update(title="Nineteen Eighty-Four")