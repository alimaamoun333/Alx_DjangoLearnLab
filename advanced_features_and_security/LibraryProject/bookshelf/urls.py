from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/delete/<int:pk>/", views.delete_book, name="delete_book"),

    # ✅ ExampleForm route
    path("example-form/", views.example_form_view, name="example_form"),
]
