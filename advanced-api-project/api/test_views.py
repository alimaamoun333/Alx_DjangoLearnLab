from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Covers CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Authenticated client
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        # Create an Author
        self.author = Author.objects.create(name="Test Author")

        # Create some Books
        self.book1 = Book.objects.create(
            title="Book One",
            author=self.author,
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author=self.author,
            publication_year=2021
        )

        # Endpoints
        self.list_url = reverse("book-list")   # DRF router registered as book-list
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})

    def test_list_books(self):
        """Ensure we can retrieve the list of books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a book."""
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2022,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Ensure unauthenticated users cannot create books."""
        client = APIClient()  # No login
        data = {
            "title": "Unauthorized Book",
            "author": self.author.id,
            "publication_year": 2022,
        }
        response = client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book_detail(self):
        """Ensure we can retrieve a single book by ID."""
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book One")

    def test_update_book(self):
        """Ensure we can update a book."""
        data = {"title": "Updated Book One", "author": self.author.id, "publication_year": 2020}
        response = self.client.put(self.detail_url(self.book1.id), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_delete_book(self):
        """Ensure we can delete a book."""
        response = self.client.delete(self.detail_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_year(self):
        """Ensure filtering works for publication_year."""
        response = self.client.get(self.list_url, {"publication_year": 2021})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book Two")

    def test_search_books_by_title(self):
        """Ensure searching works for title."""
        response = self.client.get(self.list_url, {"search": "Book One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book One")

    def test_order_books_by_year(self):
        """Ensure ordering works for publication_year."""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Book Two")
