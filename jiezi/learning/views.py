from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from learning.models import Character, Radical


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
    character = Character.objects.get(pk=character_pk)
    dict = {'character':character , 'radical_1':Radical.objects.get(pk=character.mnemonic_1)}
    try:
        radical_2=Radical.objects.get(pk=character.mnemonic_2)
        dict['radical_2'] = radical_2
    except:
        dict['radical_2'] = None
    try:
        radical_3=Radical.objects.get(pk=character.mnemonic_3)
        dict['radical_3'] = radical_3
    except:
        dict['radical_3'] = None
    return render(request, 'learning/learning_interface.html', dict)