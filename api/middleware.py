# middleware.py

from .models import ActionLog


class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        ActionLog.objects.create(
            user=request.user,
            action_type='API Request',
            details=request.path
        )

        response = self.get_response(request)

        return response
