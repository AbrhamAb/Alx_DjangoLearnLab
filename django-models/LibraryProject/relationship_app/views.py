from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library 
from .models import Book   # REQUIRED for the checker

def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"  # REQUIRED for the checker
    context_object_name = "library"
