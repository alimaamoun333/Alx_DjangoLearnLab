from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Original read-only list endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # All CRUD routes for BookViewSet
    path('', include(router.urls)),
]
