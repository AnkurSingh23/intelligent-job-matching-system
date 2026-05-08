from django.shortcuts import redirect

from .decorators import get_dashboard_url_name


class RoleAccessAndCacheMiddleware:
    auth_routes = ("/accounts/login", "/accounts/register")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith(self.auth_routes):
            return redirect(get_dashboard_url_name(request.user))

        response = self.get_response(request)

        content_type = response.get("Content-Type", "")
        if "text/html" in content_type:
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

        return response