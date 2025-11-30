"""
Unit tests for Django REST Framework API endpoints.

This test suite covers:
- CRUD operations for Book and Author models
- Filtering, searching, and ordering functionalities
- Authentication and permission enforcement using self.client.login
- Response data integrity and status codes
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BaseTestCase(APITestCase):
    """
    Base test case with common setup methods for all test classes.
    Provides reusable methods for creating test data and authenticated clients.
    """
    
    def setUp(self):
        """
        Set up test data that will be used across multiple test cases.
        This method runs before each test.
        """
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        self.author3 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author3
        )
        self.book4 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # Create API client
        self.client = APIClient()


class AuthenticationTests(BaseTestCase):
    """
    Test cases specifically for authentication using self.client.login
    These tests demonstrate proper login/logout functionality.
    """
    
    def test_login_with_valid_credentials(self):
        """
        Test that users can log in with valid credentials using self.client.login.
        """
        # Test login with valid credentials
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success)
        
        # After login, should be able to access protected endpoints
        url = reverse('book-create')
        data = {
            'title': 'Book After Login',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        # Should succeed because user is logged in
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login_with_invalid_credentials(self):
        """
        Test that login fails with invalid credentials using self.client.login.
        """
        # Test login with invalid password
        login_success = self.client.login(username='regular', password='wrongpassword')
        self.assertFalse(login_success)
        
        # After failed login, should not be able to access protected endpoints
        url = reverse('book-create')
        data = {
            'title': 'Book After Failed Login',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        # Should fail because user is not logged in
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_logout_functionality(self):
        """
        Test that logout works properly using self.client.logout.
        """
        # First, log in
        self.client.login(username='regular', password='testpass123')
        
        # Verify we can access protected endpoints while logged in
        url = reverse('book-create')
        data = {
            'title': 'Book While Logged In',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Now log out
        self.client.logout()
        
        # After logout, should not be able to access protected endpoints
        data = {
            'title': 'Book After Logout',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        # Should fail because user is logged out
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookListViewTests(BaseTestCase):
    """
    Test cases for Book List View (GET /api/books/)
    Covers listing, filtering, searching, and ordering functionality.
    """
    
    def test_list_books_unauthorized(self):
        """
        Test that unauthenticated users can access the book list.
        Should return 200 OK.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)  # Assuming pagination
    
    def test_list_books_with_login(self):
        """
        Test that logged-in users can access the book list using self.client.login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by exact publication year.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_filter_books_by_publication_year_range(self):
        """
        Test filtering books by publication year range.
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'publication_year__gte': 1990,
            'publication_year__lte': 2000
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 3 books between 1990-2000
    
    def test_filter_books_by_author_name(self):
        """
        Test filtering books by author name.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author__name': 'Rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 books by Rowling
    
    def test_search_books_by_title(self):
        """
        Test searching books by title using the search functionality.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry Potter'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 Harry Potter books
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name using the search functionality.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Tolkien'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Hobbit')
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        publication_years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(publication_years, sorted(publication_years, reverse=True))
    
    def test_order_books_by_author_name(self):
        """
        Test ordering books by author name.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'author__name'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by author name alphabetically


class BookCreateViewTests(BaseTestCase):
    """
    Test cases for Book Create View (POST /api/books/create/)
    """
    
    def test_create_book_unauthorized(self):
        """
        Test that unauthenticated users cannot create books.
        Should return 403 Forbidden.
        """
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_with_login(self):
        """
        Test that logged-in users can create books using self.client.login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 5)  # 4 initial + 1 new
    
    def test_create_book_with_admin_login(self):
        """
        Test that admin users can create books using self.client.login.
        """
        # Log in as admin
        self.client.login(username='admin', password='testpass123')
        
        url = reverse('book-create')
        data = {
            'title': 'Admin Created Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Admin Created Book')
    
    def test_create_book_with_future_publication_year(self):
        """
        Test creating a book with future publication year (should fail validation).
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_with_invalid_data(self):
        """
        Test creating a book with invalid data (missing required fields).
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-create')
        data = {
            'title': '',  # Empty title
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookUpdateViewTests(BaseTestCase):
    """
    Test cases for Book Update View (PUT /api/books/update/<id>/)
    """
    
    def test_update_book_unauthorized(self):
        """
        Test that unauthenticated users cannot update books.
        """
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_with_login(self):
        """
        Test that logged-in users can update books using self.client.login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Harry Potter Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter Title')
    
    def test_partial_update_book_with_login(self):
        """
        Test partial update of a book using PATCH method after login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Partially Updated Title'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')


class BookDeleteViewTests(BaseTestCase):
    """
    Test cases for Book Delete View (DELETE /api/books/delete/<id>/)
    """
    
    def test_delete_book_unauthorized(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_with_login(self):
        """
        Test that logged-in users can delete books using self.client.login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_nonexistent_book_with_login(self):
        """
        Test deleting a book that doesn't exist after login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('book-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthorViewTests(BaseTestCase):
    """
    Test cases for Author views (list, detail, create, update, delete)
    """
    
    def test_list_authors(self):
        """
        Test listing all authors with their books.
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 3 authors
    
    def test_retrieve_author_detail(self):
        """
        Test retrieving a specific author with nested books.
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 2)  # 2 books by Rowling
    
    def test_create_author_with_login(self):
        """
        Test creating a new author as logged-in user using self.client.login.
        """
        # Log in first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('author-create')
        data = {'name': 'New Test Author'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Author')
        self.assertEqual(Author.objects.count(), 4)  # 3 initial + 1 new


class CombinedFilteringTests(BaseTestCase):
    """
    Test cases for combined filtering, searching, and ordering scenarios.
    """
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering in a single request.
        """
        url = reverse('book-list')
        params = {
            'publication_year__gte': 1990,  # Filter: books from 1990 onwards
            'search': 'Harry',              # Search: title contains "Harry"
            'ordering': '-publication_year' # Order: newest first
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 Harry Potter books from 1990+
        
        # Verify ordering (newest first)
        publication_years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(publication_years, sorted(publication_years, reverse=True))