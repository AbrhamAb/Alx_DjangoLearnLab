from rest_framework import generics, viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Book
from .serializers import BookSerializer

# Keep the existing ListAPIView but add permissions
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

# Update ViewSet with authentication and permissions
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    
    # Different permissions for different actions
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any authenticated user to view books
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only allow admin users to create, update, or delete books
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]