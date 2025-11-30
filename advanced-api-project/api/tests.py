from django.test import TestCase
from django.utils import timezone
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer

class SerializerTests(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book_data = {
            'title': 'Harry Potter',
            'publication_year': 1997,
            'author': self.author
        }
        self.book = Book.objects.create(**self.book_data)
    
    def test_book_serializer_valid_data(self):
        """Test BookSerializer with valid data"""
        serializer = BookSerializer(instance=self.book)
        self.assertEqual(serializer.data['title'], 'Harry Potter')
        self.assertEqual(serializer.data['publication_year'], 1997)
    
    def test_book_serializer_validation(self):
        """Test BookSerializer validation for future publication year"""
        future_year = timezone.now().year + 1
        invalid_data = self.book_data.copy()
        invalid_data['publication_year'] = future_year
        
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)
    
    def test_author_serializer_nested_books(self):
        """Test AuthorSerializer includes nested books"""
        # Create another book by the same author
        Book.objects.create(
            title='Harry Potter 2',
            publication_year=1998,
            author=self.author
        )
        
        serializer = AuthorSerializer(instance=self.author)
        self.assertEqual(serializer.data['name'], 'J.K. Rowling')
        self.assertEqual(len(serializer.data['books']), 2)
        self.assertEqual(serializer.data['books'][0]['title'], 'Harry Potter')