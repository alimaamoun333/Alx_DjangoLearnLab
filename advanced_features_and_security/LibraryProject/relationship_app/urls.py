from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import list_books, LibraryDetailView
app_name = 'relationship_app'

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Role-specific views
    path('admin/', views.admin_view, name='admin_dashboard'),
    path('librarian/', views.librarian_view, name='librarian_dashboard'),
    path('member/', views.member_view, name='member_dashboard'),
    
    # Book management URLs
    path('books/', views.list_books, name='list_books'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    
    # Library detail view
    path('library/<int:library_id>/', views.library_detail, name='library_detail'),
    
    # Access control
    path('access-denied/', views.access_denied_view, name='access_denied'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]