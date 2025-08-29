
from .models import Book

from django.contrib import admin


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display    = ('title', 'author', 'publication_year')
    list_filter     = ('publication_year',)
    search_fields   = ('title', 'author')
