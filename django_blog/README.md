# django_blog

A starter Django blog project.

## Quickstart

```powershell
Set-Location 'C:\Users\mommy\Downloads\Alx_DjangoLearnLab\django_blog'
python -m venv .venv
.\.venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

## App registration
- `blog` app is added to `INSTALLED_APPS` in `django_blog/settings.py`.

## Model
- `blog.models.Post` with fields: `title`, `content`, `published_date`, `author (ForeignKey to User)`.

## Templates & static
- Templates in `templates/blog/` (`base.html`, `post_list.html`).
- Static CSS in `static/css/main.css`.

## URLs
- Root URL includes `blog.urls`; `post_list` displays posts ordered by `published_date`.

## Next steps
- Add authentication (signup/login), CRUD views for posts, comments, tagging, and search as the project grows.
