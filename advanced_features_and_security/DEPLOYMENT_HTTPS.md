HTTPS Deployment Guide (Nginx + Certbot)

This document provides example steps and configuration snippets for deploying the
Django project over HTTPS using Nginx and Certbot (Let's Encrypt). Adjust paths
and service names to match your environment.

Prerequisites
- A server with a public DNS name pointing to it.
- Root or sudo access on the server.
- `python` and your virtualenv with dependencies installed.
- Nginx installed (or another reverse proxy).

1) Obtain a TLS certificate with Certbot (recommended)

Install Certbot (example for Ubuntu):

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

Request and install certificates (Certbot will edit Nginx config automatically):

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow prompts and allow Certbot to update your Nginx configuration. Certbot
will also set up automatic renewal via a cron/systemd timer.

2) Example Nginx site configuration

Place this in `/etc/nginx/sites-available/libraryproject` and symlink to
`sites-enabled`.

```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect all HTTP traffic to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /path/to/your/project/static/;
    }
    location /media/ {
        alias /path/to/your/project/media/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Notes:
- Ensure `proxy_set_header X-Forwarded-Proto $scheme;` is set so Django can
  detect HTTPS when behind a proxy.
- When running Django via Gunicorn/uvicorn, point `proxy_pass` to the socket
  or upstream you configured.

3) Django settings behind a proxy

If your proxy terminates TLS (Nginx handles HTTPS), ensure Django knows it's
behind a secure proxy by setting in `settings.py` (not enabled by default):

```python
# In settings.py
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

4) Firewall / ports

Open ports 80 and 443 in your firewall (ufw example):

```bash
sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'
```

5) Testing
- Visit `https://yourdomain.com` and confirm the certificate is valid.
- Check `https://www.ssllabs.com/ssltest/` for a full grade and recommendations.

6) Renewal
- Certbot sets up automatic renewals. Test with:

```bash
sudo certbot renew --dry-run
```

7) Additional hardening
- Use modern TLS settings and disable old ciphers.
- Enable HSTS (we set HSTS in Django settings). Be cautious: HSTS is sticky.

This guide is an example; tailor it for your PaaS or hosting provider (some
providers handle TLS for you).
