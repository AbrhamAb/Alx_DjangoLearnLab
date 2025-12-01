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
