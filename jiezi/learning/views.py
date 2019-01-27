from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from learning.models import Character


def index(request):
    return render(request, 'index.html');


# @login_required
# def learning_interface(request):
#     return learning_character(request, Character.objects.get(id=17))
#
# @login_required
# def learning_time_selection(request):
#     pass

# @login_required
def learning_character(request, character_pk):
    return render(request, 'learning/learning_interface.html', {'character':Character.objects.get(pk=character_pk)})