from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def manage_library(request, set_id=None):
    if set_id:
        context = {'set': StudentCharacterTag.objects.get(pk=set_id)}
        return render(request, 'accounts/manage_set.html', context)
    return render(request, 'accounts/manage_library.html')