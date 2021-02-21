from django.contrib.auth.backends import ModelBackend, UserModel


class EmailUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if '@' in username:
                user = UserModel.objects.get(email__iexact=username)
            else:
                user = UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) \
                    and self.user_can_authenticate(user):
                return user
