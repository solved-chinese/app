from django.urls import reverse


class AdminUrlMixin:
    def get_admin_url(self):
        return reverse('admin:{}_{}_change'.format(
            self._meta.app_label, self._meta.model_name), args=[self.pk])
