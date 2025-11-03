from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

Book.objects.all()
# Expected output: <QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>
