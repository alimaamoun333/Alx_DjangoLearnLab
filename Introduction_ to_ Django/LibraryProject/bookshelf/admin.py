from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ['title', 'author', 'publication_year']
    
    # Add filters in the right sidebar
    list_filter = ['author', 'publication_year']
    
    # Add search functionality
    search_fields = ['title', 'author']
    
    # Add ordering
    ordering = ['title']
    
    # Number of items per page
    list_per_page = 25
    
    # Make certain fields clickable links to the edit page
    list_display_links = ['title']
    
    # Add date hierarchy (if you had date fields)
    # date_hierarchy = 'created_date'
    
    # Customize the form layout in the detail view
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
    )
    
    # Add actions dropdown
    actions = ['mark_as_classic']
    
    def mark_as_classic(self, request, queryset):
        """Custom admin action example"""
        # This is just an example - you'd need a 'is_classic' field in your model
        # queryset.update(is_classic=True)
        self.message_user(request, f"{queryset.count()} books marked as classics.")
    
    mark_as_classic.short_description = "Mark selected books as classics"

# Alternative registration method (commented out since we're using @admin.register)
# admin.site.register(Book, BookAdmin)