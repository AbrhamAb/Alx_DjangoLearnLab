from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Post, Comment, Tag


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags",
        widget=TagWidget(attrs={"placeholder": "e.g. django, python"}),
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "tags": TagWidget(attrs={"placeholder": "e.g. django, python"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            existing = self.instance.tags.values_list("name", flat=True)
            self.fields["tags"].initial = ", ".join(existing)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        tag_names = self.cleaned_data.get("tags", "")
        tags = []
        for name in [t.strip() for t in tag_names.split(",") if t.strip()]:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        if commit:
            instance.tags.set(tags)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
