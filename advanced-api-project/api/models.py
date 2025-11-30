from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField to store the author's full name
    """
    name = models.CharField(max_length=100, help_text="Full name of the author")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField for the book's title
    - publication_year: IntegerField for the year of publication
    - author: ForeignKey linking to the Author model (one-to-many relationship)
    
    Relationship:
    - One Author can have multiple Books (one-to-many)
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Author of the book"
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['title']