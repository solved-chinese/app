from django.shortcuts import reverse
from django.http import HttpResponseRedirect


def temporary_access(request, access_id=1):
    """ deprecated, use set_display directly instead """
    return HttpResponseRedirect(reverse('set_display', args=(access_id,)))
