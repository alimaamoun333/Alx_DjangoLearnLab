# LibraryProject/urls.py (or your main project's urls.py)

from django.contrib import admin
from django.urls import path
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include relationship_app URLs
    path('', include('relationship_app.urls')),
    
    # Alternative: Include with a prefix
    # path('library/', include('relationship_app.urls')),
]

# Optional: Add debug toolbar for development
try:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
except ImportError:
    pass