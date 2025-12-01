Advanced Features and Security - Custom User Model

This copy contains a custom user model implementation for the exercise.

To run:

```powershell
Set-Location 'C:\Users\mommy\Downloads\Alx_DjangoLearnLab\advanced_features_and_security'
python .\manage.py makemigrations accounts bookshelf relationship_app
python .\manage.py migrate
python .\manage.py createsuperuser
python .\manage.py runserver
```

Notes:
- `AUTH_USER_MODEL` is set to `accounts.CustomUser` in `LibraryProject/settings.py`.
- Media is configured to `media/` in project root. For production use configure a proper media storage.

Permissions & Groups:

- The `bookshelf.Book` model includes custom permissions: `can_view`, `can_create`, `can_edit`, and `can_delete`.
- Use the management command to create the groups and assign permissions:

```powershell
Set-Location 'C:\Users\mommy\Downloads\Alx_DjangoLearnLab\advanced_features_and_security'
python .\manage.py setup_groups
```

- The management command will create three groups: `Editors`, `Viewers`, and `Admins` and assign the permissions as follows:
	- `Editors`: `can_create`, `can_edit`, `can_view`
	- `Viewers`: `can_view`
	- `Admins`: `can_view`, `can_create`, `can_edit`, `can_delete`

- Example views in `LibraryProject/bookshelf/views.py` are protected with `@permission_required('bookshelf.can_edit', raise_exception=True)` etc. You can test by creating users, assigning them to groups via admin, and attempting the create/edit/delete views.
 
Security Best Practices Implemented:

- CSRF protection: all form templates include `{% csrf_token %}` and views use Django forms for input validation.
- Secure settings: `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `CSRF_COOKIE_SECURE`, and `SESSION_COOKIE_SECURE` are set in `LibraryProject/settings.py`.
- Content Security Policy (CSP): a simple middleware `LibraryProject/security.py` adds a conservative `Content-Security-Policy` header. For production consider `django-csp`.
- Input validation: `bookshelf/forms.py` provides `BookForm` using Django's `ModelForm` to validate user input and avoid raw SQL or string interpolation.

To test security settings locally (development):

```powershell
# For local development set the DJANGO_DEBUG env var to allow DEBUG behavior
setx DJANGO_DEBUG 1; # restart shell/session for effect
python .\manage.py runserver
```

Note: `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` expect HTTPS in production. For local testing you may need to adjust or use a development proxy that supports HTTPS.
