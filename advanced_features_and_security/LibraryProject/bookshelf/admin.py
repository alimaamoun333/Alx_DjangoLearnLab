from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


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


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )


# Register models explicitly
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
