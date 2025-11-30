from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework  # Fixed import
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for books with advanced filtering, searching, and ordering capabilities.
    
    Features:
    - Filtering: Filter by publication year, title, and author name with various lookups
    - Searching: Full-text search on title and author name fields
    - Ordering: Order by any book field with multiple ordering options
    - Pagination: Results are paginated for better performance
    
    Example Usage:
    - Filter: /api/books/?publication_year=2020&author__name=Tolkien
    - Search: /api/books/?search=Harry Potter
    - Order: /api/books/?ordering=title,-publication_year
    - Combine: /api/books/?publication_year__gt=2000&search=fantasy&ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filter backends configuration - use the imported module directly
    filter_backends = [
        rest_framework.DjangoFilterBackend,  # Use the imported module
        SearchFilter, 
        OrderingFilter
    ]
    
    # Django Filter configuration
    filterset_class = BookFilter
    
    # Search configuration - enables full-text search on specified fields
    search_fields = [
        'title',           # Search in book titles
        'author__name',    # Search in author names
    ]
    
    # Ordering configuration - specifies which fields can be used for ordering
    ordering_fields = [
        'id',
        'title', 
        'publication_year',
        'author__name',    # Order by author name
    ]
    
    # Default ordering when no ordering specified
    ordering = ['title']

    def get_queryset(self):
        """
        Customize queryset to handle additional filtering logic.
        
        This method can be extended to add custom filtering logic
        that's not covered by the standard filter backends.
        """
        queryset = super().get_queryset()
        
        # Example of custom filtering logic
        # You can add any custom queryset modifications here
        
        return queryset.select_related('author')  # Optimize database queries


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    Provides read-only access to a specific Book instance.
    No authentication required for viewing individual books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    Handles POST requests to create new Book instances.
    Requires authentication to create books.
    Includes custom validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    Handles PUT and PATCH requests to update Book instances.
    Requires authentication to update books.
    PUT for full updates, PATCH for partial updates.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    Handles DELETE requests to remove Book instances.
    Requires authentication to delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Enhanced Author List View with basic filtering and ordering
class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their books.
    
    Includes basic search and ordering capabilities.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID.
    
    Provides read-only access to a specific Author instance.
    Includes nested book data for the author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new author.
    
    Handles POST requests to create new Author instances.
    Requires authentication to create authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing author.
    
    Handles PUT and PATCH requests to update Author instances.
    Requires authentication to update authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing an author.
    
    Handles DELETE requests to remove Author instances.
    Requires authentication to delete authors.
    Note: This will cascade delete related books due to CASCADE setting.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]