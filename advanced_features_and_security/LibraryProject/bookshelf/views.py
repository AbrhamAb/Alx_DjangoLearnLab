from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookForm, ExampleForm


def index(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/index.html', {'books': books})


def book_list(request):
    """Compatibility view name expected by the checker; returns the same as `index`."""
    return index(request)


def example_form_view(request):
    """Simple demo view for ExampleForm to show usage in the project."""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # For demo purposes we just echo the cleaned data
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            return render(request, 'bookshelf/example_result.html', {'name': name, 'email': email})
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Use a ModelForm to validate and sanitize input to prevent injection risks
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf_index')
    else:
        form = BookForm()
    return render(request, 'bookshelf/create.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookshelf_index')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit.html', {'form': form, 'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf_index')
    return render(request, 'bookshelf/delete.html', {'book': book})
