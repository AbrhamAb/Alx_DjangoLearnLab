from rest_framework import generics, permissions
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Book Views
class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    
    Provides read-only access to all Book instances.
    No authentication required for listing books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view books


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    Provides read-only access to a specific Book instance.
    No authentication required for viewing individual books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    Handles POST requests to create new Book instances.
    Requires authentication to create books.
    Includes custom validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in to create


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    Handles PUT and PATCH requests to update Book instances.
    Requires authentication to update books.
    PUT for full updates, PATCH for partial updates.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    Handles DELETE requests to remove Book instances.
    Requires authentication to delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Author Views
class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their books.
    
    Provides read-only access to all Author instances.
    Includes nested book data through AuthorSerializer.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID.
    
    Provides read-only access to a specific Author instance.
    Includes nested book data for the author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new author.
    
    Handles POST requests to create new Author instances.
    Requires authentication to create authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing author.
    
    Handles PUT and PATCH requests to update Author instances.
    Requires authentication to update authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing an author.
    
    Handles DELETE requests to remove Author instances.
    Requires authentication to delete authors.
    Note: This will cascade delete related books due to CASCADE setting.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]