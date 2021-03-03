from django.utils.timezone import now


class UpdateLastLoginMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_login = now()
            request.user.save(update_fields=('last_login',))
        response = self.get_response(request)
        return response
