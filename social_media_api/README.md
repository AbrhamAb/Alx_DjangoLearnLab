# Social Media API

A starter Django REST API for social media-style user accounts. It includes a custom user model with bio, profile pictures, follower relationships, and token-based authentication for registration, login, and profile management.

## Features
- Custom `User` model extending `AbstractUser` with `bio`, `profile_picture`, and self-referential `followers`/`following` relationship.
- Token authentication via `rest_framework.authtoken` (tokens issued on register/login and retrievable via `/api/accounts/token/`).
- Endpoints for register, login, and authenticated profile read/update.
- SQLite by default; configurable via Django settings.

## Project Structure
- `social_media_api/` – Django project settings and URLs.
- `accounts/` – app containing the custom user model, serializers, and auth views.

## Setup
1. (Optional) Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations (from the project root `social_media_api/`):
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
Base path: `/api/accounts/`

- `POST /register/` – Create a user and return `user` + `token`.
  ```json
  {
    "username": "alice",
    "email": "alice@example.com",
    "password": "supersecret",
    "bio": "Hello!"
  }
  ```
- `POST /login/` – Authenticate and return `user` + `token`.
  ```json
  { "username": "alice", "password": "supersecret" }
  ```
- `GET /profile/` – Return the authenticated user's profile.
- `PUT/PATCH /profile/` – Update email, bio, or profile picture.
- `GET /token/` – Return (or create) the calling user's token.

Include the token in requests that require authentication:
```
Authorization: Token <token>
```

## Custom User Fields
- `bio`: freeform text
- `profile_picture`: uploaded image (served at `/media/` during development)
- `followers`: many-to-many to `User` (asymmetric) with reverse `following`

## Running Tests
Add tests as features grow; currently none are provided for this scaffold.

## Notes
- Media files are stored under `media/` in development. Configure cloud/object storage for production.
- Default permissions require authentication; unauthenticated access is allowed only on register/login endpoints.
