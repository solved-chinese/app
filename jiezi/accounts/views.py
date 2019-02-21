from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.forms import *
from learning.models import CharacterSet, Character, Radical


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # why? this seems to create the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user.raw_password = raw_password
            user.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def manage_stack(request, is_left=False, is_right=False, is_new_set=False):
    if is_left:
        return render(request, 'accounts/manage_stack_left.html')
    if is_right:
        character = Character.objects.get(pk=1)
        dict = {'character': character, 'radical_1': Radical.objects.get(pk=character.mnemonic_1)}
        try:
            radical_2 = Radical.objects.get(pk=character.mnemonic_2)
            dict['radical_2'] = radical_2
        except:
            dict['radical_2'] = None
        try:
            radical_3 = Radical.objects.get(pk=character.mnemonic_3)
            dict['radical_3'] = radical_3
        except:
            dict['radical_3'] = None
        return render(request, 'learning/learning_character_pure.html', dict)
    if is_new_set:
        sets=[]
        for set in CharacterSet.objects.all():
            if not request.user.user_character_tags.filter(name=set.name):
                sets.append(set)
        return render(request, 'accounts/manage_stack_new_character.html', {'sets':sets})
    if request.method=='POST':
        print(request.POST)
        data={}
        delete_user_character_pk = request.POST.get('delete_user_character_pk')
        delete_user_character_tag_pk = request.POST.get('delete_user_character_tag_pk')
        add_set_pk = request.POST.get('add_set_pk')
        try:
            if delete_user_character_pk is not None:
                delete_user_character=request.user.user_characters.get(pk=(int)(delete_user_character_pk))
                if request.POST.get('delete_character_from_library'):
                    delete_user_character.delete()
                    data['character_pk']=delete_user_character_pk
                    data['tag_pk']='-1'
                else:
                    delete_user_character_tag=request.user.user_character_tags.get(pk=(int)(delete_user_character_tag_pk))
                    delete_user_character_tag.user_characters.remove(delete_user_character)
                    data['character_pk'] = delete_user_character_pk
                    data['tag_pk'] = delete_user_character_tag_pk
            elif add_set_pk is not None:
                CharacterSet.objects.get(pk=(int)(add_set_pk)).add_to_user(request.user)
                data['add_set_pk']=add_set_pk
            return JsonResponse(data)
        except Exception as e:
            response=JsonResponse({"error" : ("there was an error"+str(e))})
            response.status_code=500
            return response
    else:
        return render(request,'accounts/manage.html')
# @login_required
# def manage_stack(request): #TODO the checkbox selection has bug in resetting after a request
#     filters = []
#     warning = ''
#     if 'delete_user_character' in request.GET:
#         print('delete' + request.GET.get('delete_user_character'))
#         UserCharacter.objects.get(id=request.GET.get('delete_user_character')).delete()
#     elif 'filters' in request.GET:
#         filters = request.GET.getlist('filters')
#         print('filters' + filters.__str__())
#     elif 'add_set' in request.GET:
#         try:
#             CharacterSet.objects.get(id=request.GET.get('add_set')).add_to_user(request.user)
#         except UserCharacterTag.SameNameException:
#             warning = "You can't add this because you have a tag with the same name"
#         request.user.user_character_tags.all().update(is_filtered=False)
#         print('add set' + request.GET.get('add_set'))
#     else: #reset filter at first load
#         request.user.user_character_tags.all().update(is_filtered=False)
#
#
#     # below filters the characters according to tags if given
#     filtered_user_characters = []
#     if len(filters) != 0:
#         for user_character in request.user.user_characters.all():
#             is_show = False
#             for filter_id in filters:
#                 print("receive filter id" + filter_id)
#                 if UserCharacterTag.objects.get(id=filter_id).user_characters.filter(
#                         id=user_character.id).exists():
#                     is_show = True
#                     break
#             if is_show:
#                 print('yes')
#                 filtered_user_characters.append(user_character)
#         for filter_id in filters:
#             UserCharacterTag.objects.filter(id=filter_id).update(is_filtered=True)
#     else:
#         filtered_user_characters = request.user.user_characters.all()
#
#     return render(request, 'accounts/manage_stack.html',
#                   {'existing_character_sets': CharacterSet.objects.all(),
#                    'filtered_characters': filtered_user_characters,
#                    'warning': warning})
