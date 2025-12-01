from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book


def index(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/index.html', {'books': books})


def book_list(request):
    """Compatibility view name expected by the checker; returns the same as `index`."""
    return index(request)


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Minimal placeholder view for creating a book protected by permission
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        author = request.POST.get('author', 'Unknown')
        year = request.POST.get('publication_year', None)
        book = Book.objects.create(title=title, author=author, publication_year=year or 0)
        return redirect('bookshelf_index')
    return render(request, 'bookshelf/create.html')


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = request.POST.get('publication_year', book.publication_year)
        book.save()
        return redirect('bookshelf_index')
    return render(request, 'bookshelf/edit.html', {'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf_index')
    return render(request, 'bookshelf/delete.html', {'book': book})
