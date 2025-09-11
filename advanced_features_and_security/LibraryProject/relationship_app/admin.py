from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import UserProfile, Book, Author, Library, Librarian
from django.utils.translation import gettext_lazy as _

class UserProfileInline(admin.StackedInline):
    """
    Inline admin interface for UserProfile within User admin.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('role',)


class CustomUserAdmin(UserAdmin):
    """
    Extended User admin with UserProfile inline.
    """
    inlines = (UserProfileInline,)
    
    # Add role information to the user list display
    list_display = UserAdmin.list_display + ('get_role', 'get_permissions')
    list_filter = UserAdmin.list_filter + ('profile__role',)
    
    def get_role(self, obj):
        """Display user role in admin list."""
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'
    
    def get_permissions(self, obj):
        """Display user permissions for books."""
        perms = []
        if obj.has_perm('relationship_app.can_add_book'):
            perms.append('Add')
        if obj.has_perm('relationship_app.can_change_book'):
            perms.append('Edit')
        if obj.has_perm('relationship_app.can_delete_book'):
            perms.append('Delete')
        return ', '.join(perms) if perms else 'None'
    get_permissions.short_description = 'Book Permissions'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ('user', 'role', 'user_email', 'user_date_joined', 'get_book_permissions')
    list_filter = ('role', 'user__date_joined', 'user__is_active')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('user__username',)
    actions = ['make_admin', 'make_librarian', 'make_member', 'grant_all_book_permissions', 'grant_librarian_permissions']

    def user_email(self, obj):
        """Display user email in profile admin."""
        return obj.user.email
    user_email.short_description = 'Email'
    
    def user_date_joined(self, obj):
        """Display user join date in profile admin."""
        return obj.user.date_joined.strftime('%Y-%m-%d')
    user_date_joined.short_description = 'Date Joined'
    
    def get_book_permissions(self, obj):
        """Display book permissions for the user."""
        user = obj.user
        perms = []
        if user.has_perm('relationship_app.can_add_book'):
            perms.append('Add')
        if user.has_perm('relationship_app.can_change_book'):
            perms.append('Edit')
        if user.has_perm('relationship_app.can_delete_book'):
            perms.append('Delete')
        return ', '.join(perms) if perms else 'None'
    get_book_permissions.short_description = 'Book Permissions'

    def make_admin(self, request, queryset):
        """Bulk action to set selected users as Admin."""
        count = queryset.update(role='Admin')
        for profile in queryset:
            user = profile.user
            perms = [
                Permission.objects.get(codename='can_add_book'),
                Permission.objects.get(codename='can_change_book'),
                Permission.objects.get(codename='can_delete_book')
            ]
            user.user_permissions.add(*perms)
        self.message_user(request, f'{count} users updated to Admin role with full permissions.')
    make_admin.short_description = 'Set selected users as Admin (with all book permissions)'

    def make_librarian(self, request, queryset):
        """Bulk action to set selected users as Librarian."""
        count = queryset.update(role='Librarian')
        # Grant add and change permissions to Librarians
        for profile in queryset:
            user = profile.user
            user.user_permissions.add(
                Permission.objects.get(codename='can_add_book'),
                Permission.objects.get(codename='can_change_book')
            )
            user.user_permissions.remove(Permission.objects.get(codename='can_delete_book'))
        self.message_user(request, f'{count} users updated to Librarian role with add/edit permissions.')
    make_librarian.short_description = 'Set selected users as Librarian (with add/edit permissions)'

    def make_member(self, request, queryset):
        """Bulk action to set selected users as Member."""
        count = queryset.update(role='Member')
        # Remove all book permissions from Members
        for profile in queryset:
            user = profile.user
            user.user_permissions.remove(Permission.objects.get(codename='can_add_book'))
            user.user_permissions.remove(Permission.objects.get(codename='can_change_book'))
            user.user_permissions.remove(Permission.objects.get(codename='can_delete_book'))
        self.message_user(request, f'{count} users updated to Member role (no book permissions).')
    make_member.short_description = 'Set selected users as Member (no book permissions)'

    def grant_all_book_permissions(self, request, queryset):
        """Grant all book permissions to selected users."""
        count = 0
        for profile in queryset:
            user = profile.user
            user.user_permissions.add(
                Permission.objects.get(codename='can_add_book'),
                Permission.objects.get(codename='can_change_book'),
                Permission.objects.get(codename='can_delete_book')
            )
            count += 1
        self.message_user(request, f'Granted all book permissions to {count} users.')
    grant_all_book_permissions.short_description = 'Grant all book permissions'

    def grant_librarian_permissions(self, request, queryset):
        """Grant librarian-level permissions (add and change)."""
        count = 0
        for profile in queryset:
            user = profile.user
            user.user_permissions.add(
                Permission.objects.get(codename='can_add_book'),
                Permission.objects.get(codename='can_change_book')
            )
            count += 1
        self.message_user(request, f'Granted librarian permissions to {count} users.')
    grant_librarian_permissions.short_description = 'Grant librarian permissions (add/edit books)'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin interface for Book model."""
    list_display = ('title', 'author', 'isbn', 'publication_date', 'pages', 'cover')
    list_filter = ('cover', 'language', 'publication_date', 'author')
    search_fields = ('title', 'author__name', 'isbn')
    ordering = ('title',)
    date_hierarchy = 'publication_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn')
        }),
        ('Publication Details', {
            'fields': ('publication_date', 'pages', 'cover', 'language')
        }),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model."""
    list_display = ('name', 'get_book_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_book_count(self, obj):
        """Display number of books by this author."""
        return obj.book_set.count()
    get_book_count.short_description = 'Number of Books'


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """Admin interface for Library model."""
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    ordering = ('name',)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    """Admin interface for Librarian model."""
    list_display = ('name', 'library')
    list_filter = ('library',)
    search_fields = ('name', 'library__name')
    ordering = ('name',)


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = 'Library Management System Admin'
admin.site.site_title = 'LMS Admin'
admin.site.index_title = 'Role-Based Access Control Administration'


# Create default permission groups
def create_permission_groups():
    """Create default permission groups for different roles."""
    try:
        # Admin Group - Full permissions
        admin_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            admin_perms = Permission.objects.filter(
                codename__in=['can_add_book', 'can_change_book', 'can_delete_book']
            )
            admin_group.permissions.set(admin_perms)
        
        # Librarian Group - Add and change permissions only
        librarian_group, created = Group.objects.get_or_create(name='Librarians')
        if created:
            librarian_perms = Permission.objects.filter(
                codename__in=['can_add_book', 'can_change_book']
            )
            librarian_group.permissions.set(librarian_perms)
        
        # Member Group - No special permissions
        member_group, created = Group.objects.get_or_create(name='Members')
        if created:
            # Members have no special permissions by default
            pass
            
    except Exception as e:
        print(f"Error creating permission groups: {e}")

# Call the function to create groups when admin module is loaded
create_permission_groups()