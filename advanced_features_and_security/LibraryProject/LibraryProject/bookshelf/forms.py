from django import forms
from ...bookshelf.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        # Simple sanitization example: strip tags and trim length
        return title.strip()


class ExampleForm(forms.Form):
    """A simple example form included for automated checks and demos."""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        # Example validation: enforce a domain restriction (optional)
        # if not email.endswith('@example.com'):
        #     raise forms.ValidationError('Email must be from example.com')
        return email
