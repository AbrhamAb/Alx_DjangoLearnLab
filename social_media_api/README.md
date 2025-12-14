# Social Media API

A starter Django REST API for social media-style user accounts. It includes a custom user model with bio, profile pictures, follower relationships, token-based authentication, CRUD APIs for posts and comments, likes, and notifications.

## Features
- Custom `User` model extending `AbstractUser` with `bio`, `profile_picture`, and self-referential `followers`/`following` relationship.
- Token authentication via `rest_framework.authtoken` (tokens issued on register/login and retrievable via `/api/accounts/token/`).
- CRUD for posts and comments with author-only edits, pagination, and search/order support on posts.
- Likes on posts with per-user like state and counts.
- Notifications for follows, likes, and comments.
- SQLite by default; configurable via Django settings.

## Project Structure
- `social_media_api/` – Django project settings and URLs.
- `accounts/` – app containing the custom user model, serializers, and auth views.
- `posts/` – posts and comments models, serializers, viewsets, and routing.
- `notifications/` – notifications model, serializer, view, and routing.

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
Authentication base path: `/api/accounts/`

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
- `POST /follow/<user_id>/` – Follow another user (self-follow blocked).
- `POST /unfollow/<user_id>/` – Unfollow a user (self-unfollow blocked).

Content base path: `/api/`

- `GET /posts/` – List posts (paginated). Supports `search=<query>` on title/content and `ordering=created_at` (or `-created_at`, `updated_at`, `title`).
- `POST /posts/` – Create a post (auth required). `title`, `content`.
- `GET /posts/{id}/` – Retrieve a post.
- `PUT/PATCH /posts/{id}/` – Update a post (author only).
- `DELETE /posts/{id}/` – Delete a post (author only).
- `POST /posts/{id}/like/` – Like a post (idempotent if already liked).
- `POST /posts/{id}/unlike/` – Remove a like from a post.

- `GET /comments/` – List comments (paginated). Filter by `?post=<post_id>`.
- `POST /comments/` – Create a comment (auth required). `post`, `content`.
- `GET /comments/{id}/` – Retrieve a comment.
- `PUT/PATCH /comments/{id}/` – Update a comment (author only).
- `DELETE /comments/{id}/` – Delete a comment (author only).
- `GET /feed/` – Posts by users the caller follows, newest first.

Notifications base path: `/api/notifications/`
- `GET /` – List notifications for the authenticated user (unread first, newest first). Notifications are generated for new followers, likes on your posts, and comments on your posts.

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
- Default permissions require authentication; unauthenticated access is allowed only on register/login endpoints. Posts/comments lists are public but write operations require auth.
- Pagination uses page-number style with `page` query param (page size 10 by default).
