import os

from django.http import HttpResponseForbidden


class LocalhostOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only allow access to Django admin from Docker host
        remote_addr = request.META.get("REMOTE_ADDR")
        allow_host = os.environ.get("ALLOW_ADMIN_HOST")
        print(remote_addr)
        if allow_host:
            if request.path.startswith("/admin") and remote_addr != allow_host:
                return HttpResponseForbidden("<h1>Forbidden</h1>")

        response = self.get_response(request)
        return response
