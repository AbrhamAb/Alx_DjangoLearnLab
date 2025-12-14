# Deployment Guide (Production)

This project is production-ready with environment-driven settings, WhiteNoise for static files, and Gunicorn for WSGI. Below is a concise checklist for deploying to a Linux host (works for Render, Railway, Fly.io, DigitalOcean, Heroku-like stacks).

## 1) Environment Variables
Set these in your hosting dashboard or `.env` (never commit secrets):

- `DJANGO_SECRET_KEY` (required)
- `DJANGO_DEBUG` (set to `False` in prod)
- `DJANGO_ALLOWED_HOSTS` (comma-separated, e.g. `myapp.com,api.myapp.com`)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (comma-separated full origins, e.g. `https://myapp.com,https://api.myapp.com`)
- `DJANGO_SECURE_SSL_REDIRECT=True`
- `DJANGO_SESSION_COOKIE_SECURE=True`
- `DJANGO_CSRF_COOKIE_SECURE=True`
- `DJANGO_SECURE_HSTS_SECONDS=31536000`
- `DATABASE_URL` (if you switch to Postgres via dj-database-url; otherwise configure DATABASES manually)

## 2) Dependencies
Install with:
```bash
pip install -r requirements.txt
```
Key prod deps: `gunicorn` (WSGI), `whitenoise` (static files), `psycopg2-binary` (Postgres client).

## 3) Static Files
Collect static assets before starting the server:
```bash
python manage.py collectstatic --noinput
```
WhiteNoise is enabled in settings to serve `STATIC_ROOT=staticfiles`.

## 4) Database
For Postgres, provision a managed instance and expose `DATABASE_URL`. If using dj-database-url, configure `DATABASES['default']` from that URL. For SQLite, no change is needed (not recommended for production scale).

## 5) Gunicorn Command
From the project root (`social_media_api/`):
```bash
gunicorn social_media_api.wsgi:application --bind 0.0.0.0:8000 --workers 3
```
Behind Nginx/ingress, forward traffic to this port and terminate TLS at the proxy.

## 6) Nginx (reverse proxy example)
- Proxy `location /` to `http://127.0.0.1:8000`.
- Serve `/static/` from the `staticfiles/` directory if you prefer Nginx for static files.
- Redirect HTTP to HTTPS.

## 7) Media Files
For production, use object storage (e.g., AWS S3, GCS, or DigitalOcean Spaces). Configure `MEDIA_URL` and storage backend accordingly.

## 8) Health & Logging
- Enable probes on `/admin/login/` or a custom health endpoint if desired.
- Configure log forwarding (e.g., to CloudWatch, LogDNA, Papertrail). Django defaults to stdout/stderr via Gunicorn.

## 9) Post-deploy Steps
```bash
python manage.py migrate
python manage.py createsuperuser  # optional admin access
```

## 10) Final Checklist
- `DEBUG=False`
- Strong `DJANGO_SECRET_KEY` set
- `ALLOWED_HOSTS` populated
- HTTPS enforced via proxy + `DJANGO_SECURE_SSL_REDIRECT=True`
- Static collected and served via WhiteNoise or Nginx
- Database connected and migrated
- Monitoring/logging enabled
