from django.shortcuts import render
from .models import Book

# Simple view examples (not used in this task)

def index(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/index.html', {'books': books})
