from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


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
    list_display = UserAdmin.list_display + ('get_role',)
    list_filter = UserAdmin.list_filter + ('profile__role',)
    
    def get_role(self, obj):
        """Display user role in admin list."""
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ('user', 'role', 'user_email', 'user_date_joined')
    list_filter = ('role', 'user__date_joined', 'user__is_active')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('user__username',)
    
    def user_email(self, obj):
        """Display user email in profile admin."""
        return obj.user.email
    user_email.short_description = 'Email'
    
    def user_date_joined(self, obj):
        """Display user join date in profile admin."""
        return obj.user.date_joined.strftime('%Y-%m-%d')
    user_date_joined.short_description = 'Date Joined'
    
    # Custom actions
    actions = ['make_admin', 'make_librarian', 'make_member']
    
    def make_admin(self, request, queryset):
        """Bulk action to set selected users as Admin."""
        count = queryset.update(role='Admin')
        self.message_user(request, f'{count} users updated to Admin role.')
    make_admin.short_description = 'Set selected users as Admin'
    
    def make_librarian(self, request, queryset):
        """Bulk action to set selected users as Librarian."""
        count = queryset.update(role='Librarian')
        self.message_user(request, f'{count} users updated to Librarian role.')
    make_librarian.short_description = 'Set selected users as Librarian'
    
    def make_member(self, request, queryset):
        """Bulk action to set selected users as Member."""
        count = queryset.update(role='Member')
        self.message_user(request, f'{count} users updated to Member role.')
    make_member.short_description = 'Set selected users as Member'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = 'Library Management System Admin'
admin.site.site_title = 'LMS Admin'
admin.site.index_title = 'Role-Based Access Control Administration'