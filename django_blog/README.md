# django_blog

This project is a starter Django blog with authentication (login, logout, registration, profile editing), a `Post` model, and static assets wired per the provided spec.

## Setup
1. Create/activate the virtual environment:
   ```powershell
   cd C:\Users\mommy\Downloads\Alx_DjangoLearnLab\django_blog
   .\.venv\Scripts\activate
   ```
2. Install dependencies (Django is already installed in the venv):
   ```powershell
   pip install -r requirements.txt  # or ensure Django 6.0 is installed
   ```
3. Apply migrations:
   ```powershell
   python manage.py migrate
   ```
4. Run the dev server:
   ```powershell
   python manage.py runserver
   ```

## Authentication
- Login: `/login/` (built-in `LoginView`, template `blog/templates/registration/login.html`)
- Logout: `/logout/` (built-in `LogoutView`, template `blog/templates/registration/logout.html`)
- Register: `/register/` (custom view using `RegistrationForm`)
- Profile: `/profile/` (login required, edits username/email/name)

## Static and Templates
- Base template: `blog/templates/blog/base.html` (links to `css/styles.css` and `js/scripts.js`).
- Static assets: `blog/static/css/styles.css`, `blog/static/js/scripts.js`.
- Additional templates: `blog/templates/blog/home.html`, `blog/templates/blog/post_list.html`, `blog/templates/blog/profile.html`, and registration templates under `blog/templates/registration/`.

## Models
- `Post` with `title`, `content`, `published_date` (`auto_now_add`), and `author` (`User` FK).

## Forms
- `RegistrationForm` (extends `UserCreationForm`, adds required email).
- `ProfileForm` (edits username, email, first/last name).

## URLs
- Root includes `blog.urls`; names: `home`, `posts`, `login`, `logout`, `register`, `profile`.
