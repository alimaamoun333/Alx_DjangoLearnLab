from django.contrib import admin

from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

# Register your models here.
