from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer serializes all fields of the Book model.
    
    Includes custom validation to ensure publication_year is not in the future.
    
    Fields:
    - id: Auto-generated primary key
    - title: Book title
    - publication_year: Year of publication with validation
    - author: Foreign key to Author model
    
    Validation:
    - publication_year cannot be greater than current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Validate that publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer serializes Author model with nested BookSerializer.
    
    Fields:
    - id: Auto-generated primary key
    - name: Author's name
    - books: Nested serialization of related Book objects
    
    Relationship Handling:
    - Uses BookSerializer to serialize all books by this author
    - The 'books' field is read-only and represents the one-to-many relationship
    """
    
    # Nested serializer for related books
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


class AuthorBookCreateSerializer(serializers.ModelSerializer):
    """
    Alternative serializer for creating authors with books in a single request.
    This demonstrates handling nested creation scenarios.
    """
    books = BookSerializer(many=True, required=False)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def create(self, validated_data):
        """
        Custom create method to handle nested book creation.
        """
        books_data = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        
        return author