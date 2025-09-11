# management/commands/assign_permissions.py
# Place this file in: relationship_app/management/commands/assign_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import UserProfile, Book


class Command(BaseCommand):
    help = 'Assign book permissions based on user roles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all permissions before assigning new ones',
        )

    def handle(self, *args, **options):
        # Get book permissions
        try:
            content_type = ContentType.objects.get_for_model(Book)
            can_add_book = Permission.objects.get(
                codename='can_add_book',
                content_type=content_type
            )
            can_change_book = Permission.objects.get(
                codename='can_change_book',
                content_type=content_type
            )
            can_delete_book = Permission.objects.get(
                codename='can_delete_book',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Book permissions not found. Please run migrations first.')
            )
            return

        # Create permission groups if they don't exist
        admin_group, created = Group.objects.get_or_create(name='Admins')
        librarian_group, created = Group.objects.get_or_create(name='Librarians')
        member_group, created = Group.objects.get_or_create(name='Members')

        # Assign permissions to groups
        admin_group.permissions.set([can_add_book, can_change_book, can_delete_book])
        librarian_group.permissions.set([can_add_book, can_change_book])
        member_group.permissions.clear()  # Members get no book permissions

        if options['reset']:
            self.stdout.write('Resetting all user permissions...')
            # Clear all book permissions from users
            for user in User.objects.all():
                user.user_permissions.remove(can_add_book, can_change_book, can_delete_book)
                user.groups.clear()

        # Assign permissions based on user roles
        profiles = UserProfile.objects.all()
        
        admin_count = 0
        librarian_count = 0
        member_count = 0

        for profile in profiles:
            user = profile.user
            
            if profile.role == 'Admin':
                # Grant all permissions to Admins
                user.user_permissions.add(can_add_book, can_change_book, can_delete_book)
                user.groups.add(admin_group)
                admin_count += 1
                self.stdout.write(f"✓ Admin permissions granted to {user.username}")
                
            elif profile.role == 'Librarian':
                # Grant add and change permissions to Librarians
                user.user_permissions.add(can_add_book, can_change_book)
                user.user_permissions.remove(can_delete_book)
                user.groups.add(librarian_group)
                librarian_count += 1
                self.stdout.write(f"✓ Librarian permissions granted to {user.username}")
                
            elif profile.role == 'Member':
                # Remove all book permissions from Members
                user.user_permissions.remove(can_add_book, can_change_book, can_delete_book)
                user.groups.add(member_group)
                member_count += 1
                self.stdout.write(f"✓ Member role assigned to {user.username} (no book permissions)")

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Permission assignment completed!'))
        self.stdout.write('=' * 50)
        self.stdout.write(f"Admins (full permissions): {admin_count}")
        self.stdout.write(f"Librarians (add/edit permissions): {librarian_count}")
        self.stdout.write(f"Members (no book permissions): {member_count}")
        self.stdout.write('=' * 50)
        
        # Display permission details
        self.stdout.write('')
        self.stdout.write('Permission Details:')
        self.stdout.write('- Admins: can_add_book, can_change_book, can_delete_book')
        self.stdout.write('- Librarians: can_add_book, can_change_book')
        self.stdout.write('- Members: view access only')


class Command2(BaseCommand):
    """Alternative command for creating test users with permissions"""
    help = 'Create test users with appropriate book permissions'

    def handle(self, *args, **options):
        # Test users with permissions
        test_users = [
            {
                'username': 'admin_user',
                'email': 'admin@library.com',
                'password': 'admin123',
                'role': 'Admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'permissions': ['can_add_book', 'can_change_book', 'can_delete_book']
            },
            {
                'username': 'librarian_user',
                'email': 'librarian@library.com',
                'password': 'librarian123',
                'role': 'Librarian',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'permissions': ['can_add_book', 'can_change_book']
            },
            {
                'username': 'member_user',
                'email': 'member@library.com',
                'password': 'member123',
                'role': 'Member',
                'first_name': 'John',
                'last_name': 'Doe',
                'permissions': []
            }
        ]

        content_type = ContentType.objects.get_for_model(Book)

        for user_data in test_users:
            # Create or get user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f"Created user: {user_data['username']}")
            else:
                self.stdout.write(f"User {user_data['username']} already exists")

            # Set role
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': user_data['role']}
            )
            profile.role = user_data['role']
            profile.save()

            # Assign permissions
            user.user_permissions.clear()
            for perm_code in user_data['permissions']:
                try:
                    permission = Permission.objects.get(
                        codename=perm_code,
                        content_type=content_type
                    )
                    user.user_permissions.add(permission)
                    self.stdout.write(f"  ✓ Granted {perm_code} to {user.username}")
                except Permission.DoesNotExist:
                    self.stdout.write(f"  ✗ Permission {perm_code} not found")

        self.stdout.write(self.style.SUCCESS('Test users with permissions created successfully!'))