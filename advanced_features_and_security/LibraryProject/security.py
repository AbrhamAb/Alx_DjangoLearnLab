class ContentSecurityPolicyMiddleware:
    """Simple middleware to add a Content-Security-Policy header.

    This is intentionally minimal. For production use, prefer the
    `django-csp` package which provides a full-featured implementation.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Define a conservative default CSP
        self.csp = "default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self' 'unsafe-inline'"

    def __call__(self, request):
        response = self.get_response(request)
        # Only set CSP when it's not already set
        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = self.csp
        return response
