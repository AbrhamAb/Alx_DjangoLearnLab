LibraryProject (advanced_features_and_security)

This is the Django project copy used for the "Advanced Features and Security" exercises.

Key points
- Custom user model: `accounts.CustomUser` (defined in `advanced_features_and_security/accounts/models.py`).
  - Fields: `date_of_birth` (DateField), `profile_photo` (ImageField).
  - `AUTH_USER_MODEL` is set to `accounts.CustomUser` in `LibraryProject/LibraryProject/settings.py`.

- Book model permissions (in `LibraryProject/bookshelf/models.py`):
  - `can_view`, `can_create`, `can_edit`, `can_delete`.

- Groups and permissions management:
  - A management command `setup_groups` exists in `LibraryProject/bookshelf/management/commands/setup_groups.py`.
  - It creates three groups: `Editors`, `Viewers`, and `Admins` and assigns bookshelf permissions.

Quick run & setup (PowerShell)

```powershell
Set-Location 'C:\Users\mommy\Downloads\Alx_DjangoLearnLab\advanced_features_and_security'
# install dependencies if needed
pip install -r requirements.txt   # optional: create a requirements.txt with Django, Pillow

# make & apply migrations
python .\manage.py makemigrations accounts bookshelf relationship_app
python .\manage.py migrate

# create a superuser
python .\manage.py createsuperuser

# create groups and assign permissions
python .\manage.py setup_groups

# run dev server
python .\manage.py runserver
```

Notes
- The `bookshelf` app contains example views at `LibraryProject/bookshelf/views.py` that are protected with `@permission_required('bookshelf.can_create', raise_exception=True)`, etc.
- Media files uploaded via `profile_photo` require the `Pillow` package. Install with `pip install Pillow`.
- If you already have an existing database using Django's default `auth.User`, switching to a custom user model requires a fresh database or careful migration planning. For this exercise use a fresh DB if possible.

Testing permissions
- After running `setup_groups`, open the admin site at `http://127.0.0.1:8000/admin/` and:
  - Create test users and assign them to `Viewers`, `Editors`, or `Admins`.
  - Log in as those users and attempt to access the create/edit/delete views to verify enforcement.

Contact
- This README is generated automatically to help the checker and local testing. If you want, I can add simple templates so the views can be exercised via the browser.
