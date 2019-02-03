from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from learning.models import Character, Radical
import random

def index(request):
    return render(request, 'index.html');


# @login_required
# def learning_interface(request):
#     return learning_character(request, Character.objects.get(id=17))
#
# @login_required
# def learning_time_selection(request):
#     pass

#@login_required
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
    return render(request, 'learning/learning_character.html', dict)

def review_test(request):
    list=[(1,'赶来韩寒凭感觉i 安排概念和哪；急哦'),(2,'second'),(3,'third'),(4,'fourth')]
    ans=1
    return review_interface(request, list, ans)

#list of tuple (pk, tested_choice), ans also a tuple
#@login_required
def review_interface(request, list, ans):
    choices = random.sample(list, 4)
    ans_index = -1
    for i in range(0,4):
        if choices[i][0] == ans:
            ans_index = i
    if ans_index == -1:
        ans_index = random.randrange(4)
        choices[ans_index]=ans
    return render(request, 'learning/review_interface.html', {'choices':choices})

