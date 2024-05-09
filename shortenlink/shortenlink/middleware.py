import os

from django.http import HttpResponseForbidden


class LocalhostOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only allow access to Django admin from Docker host
        remote_addr = request.META.get(
            "HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR")
        )
        allow_host = os.environ.get("ALLOW_ADMIN_HOST")
        if allow_host:
            if request.path.startswith("/admin") and remote_addr != allow_host:
                return HttpResponseForbidden(f"<h1>Forbidden {remote_addr}</h1>")

        response = self.get_response(request)
        return response
