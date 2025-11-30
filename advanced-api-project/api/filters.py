import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Custom filter set for Book model with advanced filtering options.
    
    Provides filtering capabilities for:
    - Exact match on publication_year
    - Range filtering on publication_year
    - Case-insensitive contains filtering on title and author name
    - Multiple choice filtering
    """
    
    # Exact year filter
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        help_text="Filter by exact publication year"
    )
    
    # Year range filters
    publication_year__gt = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gt',
        help_text="Filter by publication year greater than"
    )
    
    publication_year__lt = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lt',
        help_text="Filter by publication year less than"
    )
    
    publication_year__gte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Filter by publication year greater than or equal to"
    )
    
    publication_year__lte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Filter by publication year less than or equal to"
    )
    
    # Title filters with different lookups
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Filter by title (case-insensitive contains)"
    )
    
    title__exact = django_filters.CharFilter(
        field_name='title',
        lookup_expr='exact',
        help_text="Filter by exact title match"
    )
    
    title__startswith = django_filters.CharFilter(
        field_name='title',
        lookup_expr='istartswith',
        help_text="Filter by title starting with (case-insensitive)"
    )
    
    # Author name filters
    author__name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive contains)"
    )
    
    author__name__exact = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='exact',
        help_text="Filter by exact author name match"
    )

    class Meta:
        model = Book
        fields = {
            'publication_year': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'title': ['exact', 'icontains', 'istartswith'],
            'author__name': ['exact', 'icontains'],
        }