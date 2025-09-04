# relationship_app/models.py

from django.db import models

class Author(models.Model):
    """
    Author model representing book authors
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Book(models.Model):
    """
    Book model with ForeignKey relationship to Author
    One author can have many books (One-to-Many relationship)
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'  # Allows reverse lookup: author.books.all()
    )
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']

class Library(models.Model):
    """
    Library model with ManyToMany relationship to Book
    One library can have many books, and one book can be in many libraries
    """
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book,
        related_name='libraries'  # Allows reverse lookup: book.libraries.all()
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Libraries"

class Librarian(models.Model):
    """
    Librarian model with OneToOne relationship to Library
    Each library has exactly one librarian, and each librarian manages one library
    """
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name='librarian'  # Allows reverse lookup: library.librarian
    )
    
    def __str__(self):
        return f"{self.name} - Librarian of {self.library.name}"
    
    class Meta:
        ordering = ['name']