from django.contrib.auth.backends import ModelBackend, UserModel
try:
    from jiezi_secret.secret import MASTER_PASSWORD
except ImportError:
    MASTER_PASSWORD = None


class EmailUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if '@' in username:
                user = UserModel.objects.get(email=username)
            else:
                user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if MASTER_PASSWORD and password == MASTER_PASSWORD:
                return user
            if user.check_password(password) \
                    and self.user_can_authenticate(user):
                return user
