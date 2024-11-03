# custom_middleware.py
from django.utils.deprecation import MiddlewareMixin

class CustomXFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith("/media/document/"):
            response.headers["X-Frame-Options"] = "SAMEORIGIN"  # or other specific option
        return response
