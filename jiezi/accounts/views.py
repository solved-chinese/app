from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.forms import *
from accounts.models import UserCharacter, UserCharacterTag
from learning.models import CharacterSet


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
def manage_stack(request):
    filters = []
    warning = ''
    if 'delete_user_character' in request.GET:
        print('delete' + request.GET.get('delete_user_character'))
        UserCharacter.objects.get(id=request.GET.get('delete_user_character')).delete()
    elif 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        print('filters' + filters.__str__())
    elif 'add_set' in request.GET:
        try:
            CharacterSet.objects.get(id=request.GET.get('add_set')).add_to_user(request.user)
        except UserCharacterTag.SameNameException:
            warning = "You can't add this because you have a tag with the same name"
        request.user.user_character_tags.all().update(is_filtered=False)
        print('add set' + request.GET.get('add_set'))
    else: #reset filter at first load
        request.user.user_character_tags.all().update(is_filtered=False)


    # below filters the characters according to tags if given
    filtered_user_characters = []
    if len(filters) != 0:
        for user_character in request.user.user_characters.all():
            is_show = False
            for filter_id in filters:
                print("receive filter id" + filter_id)
                if UserCharacterTag.objects.get(id=filter_id).user_characters.filter(
                        id=user_character.id).exists():
                    is_show = True
                    break
            if is_show:
                print('yes')
                filtered_user_characters.append(user_character)
        for filter_id in filters:
            UserCharacterTag.objects.filter(id=filter_id).update(is_filtered=True)
    else:
        filtered_user_characters = request.user.user_characters.all()

    return render(request, 'accounts/manage_stack.html',
                  {'existing_character_sets': CharacterSet.objects.all(),
                   'filtered_characters': filtered_user_characters,
                   'warning': warning})
