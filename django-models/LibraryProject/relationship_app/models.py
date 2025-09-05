from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    """Author model for book authors"""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model with custom permissions for role-based access control"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    cover = models.CharField(max_length=20, choices=[
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
    ])
    language = models.CharField(max_length=30, default='English')
    
    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        ]
    
    def __str__(self):
        return self.title


class Library(models.Model):
    """Library model"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Librarian(models.Model):
    """Librarian model"""
    name = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    UserProfile model to extend Django's built-in User model with role-based access control.
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Member',
        help_text="Select the user's role for access control"
    )
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def is_admin(self):
        """Check if user has Admin role"""
        return self.role == 'Admin'
    
    def is_librarian(self):
        """Check if user has Librarian role"""
        return self.role == 'Librarian'
    
    def is_member(self):
        """Check if user has Member role"""
        return self.role == 'Member'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a UserProfile when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the UserProfile when User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Create profile if it doesn't exist (edge case handling)
        UserProfile.objects.create(user=instance)