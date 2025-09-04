from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the book title")
    author = models.CharField(max_length=100, help_text="Enter the author's name")
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(datetime.now().year)
        ],
        help_text="Enter the publication year"
    )
    
    # Optional: Add more fields for richer admin experience
    isbn = models.CharField(max_length=13, blank=True, null=True, help_text="13-digit ISBN")
    pages = models.PositiveIntegerField(blank=True, null=True, help_text="Number of pages")
    genre = models.CharField(max_length=50, blank=True, help_text="Book genre")
    is_available = models.BooleanField(default=True, help_text="Is the book available?")
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
    
    # Custom method that can be displayed in admin
    def is_recent(self):
        return self.publication_year >= 2000
    is_recent.boolean = True
    is_recent.short_description = 'Recent Publication'