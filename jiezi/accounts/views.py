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
def manage_stack_left(request):
    return render(request, 'accounts/manage_stack_left.html')


def manage_stack_new_set_modal(request):
    sets = []
    for set in CharacterSet.objects.all():
        if not request.user.user_character_tags.filter(name=set.name):
            sets.append(set)
    return render(request, 'accounts/manage_stack_new_character.html', {'sets': sets})


@login_required
def manage_stack(request):
    if request.method == 'POST':
        print(request.POST)
        data = {}
        delete_user_character_pk = request.POST.get('delete_user_character_pk')
        delete_user_character_tag_pk = request.POST.get('delete_user_character_tag_pk')
        delete_tag_pk = request.POST.get('delete_tag_pk')
        add_set_pk = request.POST.get('add_set_pk')
        try:
            if delete_user_character_pk is not None:
                delete_user_character = request.user.user_characters.get(pk=(int)(delete_user_character_pk))
                if request.POST.get('delete_character_from_library'):
                    delete_user_character.delete()
                    data['character_pk'] = delete_user_character_pk
                    data['tag_pk'] = '-1'
                else:
                    delete_user_character_tag = request.user.user_character_tags.get(pk=(int)(delete_user_character_tag_pk))
                    delete_user_character_tag.user_characters.remove(delete_user_character)
                    data['character_pk'] = delete_user_character_pk
                    data['tag_pk'] = delete_user_character_tag_pk
                    return JsonResponse(data)
            elif add_set_pk is not None:
                CharacterSet.objects.get(pk=(int)(add_set_pk)).add_to_user(request.user)
                data['add_set_pk'] = add_set_pk
                return JsonResponse(data)
            elif delete_tag_pk is not None:
                delete_tag = request.user.user_character_tags.get(pk=(int)(delete_tag_pk))
                if request.POST.get('delete_tag_characters_from_library'):
                    for user_character in delete_tag.user_characters.all():
                        user_character.delete()
                delete_tag.delete()
                data['status'] = 'good'
            return JsonResponse(data)

        except Exception as e:
            response = JsonResponse({"error": ("there was an error" + str(e))})
            response.status_code = 500
            return response
    else:
        return render(request, 'accounts/manage.html')
