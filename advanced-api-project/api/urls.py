from django.urls import path
from . import views

urlpatterns = [
    # Book URLs - Updated to match checker requirements
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),  # Fixed pattern
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),  # Fixed pattern
    
    # Author URLs - Also updated for consistency
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/update/<int:pk>/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/delete/<int:pk>/', views.AuthorDeleteView.as_view(), name='author-delete'),
]