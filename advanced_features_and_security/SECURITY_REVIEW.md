Security Review — HTTPS & Redirects

Overview
--------
This project has been configured to enforce HTTPS and related secure headers in
production (when `DEBUG=False`). The goal is to protect data in transit, reduce
risk of XSS/CSRF, and prevent clickjacking.

What was implemented
---------------------
- SECURE_SSL_REDIRECT: When `DEBUG=False`, all HTTP requests are redirected to HTTPS.
- SECURE_HSTS_SECONDS: Set to `31536000` (one year) when `DEBUG=False`.
- SECURE_HSTS_INCLUDE_SUBDOMAINS: Set to `True` when `DEBUG=False`.
- SECURE_HSTS_PRELOAD: Set to `True` when `DEBUG=False`.
- CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE: Ensures cookies are sent only
  over HTTPS.
- X_FRAME_OPTIONS: Set to `DENY` to prevent framing and clickjacking.
- SECURE_CONTENT_TYPE_NOSNIFF and SECURE_BROWSER_XSS_FILTER: Enabled to
  reduce MIME-sniffing and enable XSS protection.
- Content Security Policy: Added a minimal CSP via `LibraryProject/security.py`.
- Deployment guidance: `DEPLOYMENT_HTTPS.md` includes Nginx + Certbot example
  and notes about `SECURE_PROXY_SSL_HEADER`.

Testing performed / suggested
----------------------------
- Manual review of `settings.py` to ensure secure flags are present.
- After deploying with TLS, verify that:
  - HTTP requests return 301 redirects to HTTPS.
  - Responses include `Strict-Transport-Security` header with configured values.
  - Cookies have the `Secure` attribute set.
  - CSP header is present (adjust the policy as required by your asset origins).
- Use security scanners (Mozilla Observatory, SSL Labs) to check TLS and headers.

Potential improvements
----------------------
- Replace the simple CSP middleware with `django-csp` for richer policy support.
- Add automated tests verifying security headers are present in responses.
- Ensure `SECURE_HSTS_SECONDS` is enabled only after HTTPS is fully configured
  and tested; once HSTS is sent, browsers will hard-enforce HTTPS for the domain.
- Consider additional headers: `Referrer-Policy`, `Permissions-Policy`.

Conclusion
----------
The project has been updated with recommended HTTPS and redirect settings and
documentation to deploy with TLS. Review the deployment guide and enable these
settings in your production environment behind a properly configured proxy.
