from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'relationship_app'  # Role-Based Access Control app namespace

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Role-specific views
    path('admin/', views.admin_view, name='admin_dashboard'),
    path('librarian/', views.librarian_view, name='librarian_dashboard'),
    path('member/', views.member_view, name='member_dashboard'),
    
    # Access control
    path('access-denied/', views.access_denied_view, name='access_denied'),
    
    # Authentication URLs (optional - you might have these in your main urls.py)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Alternative URL patterns if you prefer different naming conventions
# urlpatterns = [
#     path('', views.home_view, name='home'),
#     path('admin-panel/', views.admin_view, name='admin_view'),
#     path('librarian-panel/', views.librarian_view, name='librarian_view'),
#     path('member-panel/', views.member_view, name='member_view'),
#     path('forbidden/', views.access_denied_view, name='access_denied'),
# ]