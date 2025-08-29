
from .models import Book

from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
