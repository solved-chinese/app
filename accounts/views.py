from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import SignUpForm
from learning.models import CharacterSet, Character, Radical
from accounts.models import UserCharacter, UserCharacterTag
from jiezi.utils.json_serializer import chenyx_serialize

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def manage_library(request, set_id=None):
    if set_id:
        context = {'set_id': set_id}
        return render(request, 'accounts/manage_library_set.html', context)
    return render(request, 'accounts/manage_library.html')

@login_required
def dashboard(request):
    if request.GET.get('endsession', False):
        request.session['is_learning'] = False
    active = request.GET.get('active', 'Dashboard')

    if active == 'Staff' and request.user.is_staff != True:
        HttpResponseRedirect(reverse('dashboard')+"?active=Dashboard")

    return render(request, 'accounts/dashboard.html', {'active': active})

@login_required
def alt_profile(request):
    if request.method == 'POST':
        currentUser = request.user
        currentUser.email = request.POST.get("email")
        currentUser.first_name = request.POST.get("first_name")
        currentUser.last_name = request.POST.get("last_name")
        currentUser.cn_level = request.POST.get("cn_level")
        currentUser.save()
        return HttpResponseRedirect(reverse('dashboard')+"?active=Profile")
    else:
        return render(request, 'accounts/dashboard.html', {'active': 'Dashboard'})


"""
@api {POST} /accounts/add_set/ Add set
@apiDescription Make an copy of an existing character set in user's library
@apiGroup accounts

@apiParam   {int}   set_id        the id of the set to be added
@apiError (Error 400) {String} msg   the detail of the exception
"""
@csrf_exempt
def add_set(request):
    try:
        CharacterSet.objects.get(pk=request.POST.get('set_id')).add_to_user(request.user)
        response = JsonResponse({'msg': 'good'})
    except Exception as e:
        response = JsonResponse({'msg': str(e)}, status=400)
    return response


"""
@api {POST} /accounts/delete_character/ Delete character
@apiGroup accounts

@apiParam   {int}   character_id  the Jiezi id of the character
@apiParam   {int}   set_id        (optional) the id of the user set for the character to be 
    deleted from, otherwise the character will be delete from all user sets of the current user
"""
@csrf_exempt
def delete_character(request):
    try:
        uc = UserCharacter.objects.get(character__pk=request.POST.get('character_id'), user=request.user)
        set_id = request.POST.get('set_id')
        if set_id:
            UserCharacterTag.objects.get(pk=set_id).user_characters.remove(uc)
        else:
            uc.delete()
        response = JsonResponse({'msg': 'good'})
    except Exception as e:
        response = JsonResponse({'msg': str(e)}, status=400)
    return response


"""
@api {POST} /accounts/delete_set/ Delete set
@apiDescription Delete a user set
@apiGroup accounts

@apiParam   {int}        set_id                the id of the user set to be deleted from
@apiParam   {Boolean} is_delete_characters=False  (optional) false will not delete the characters 
    in this set from the user library, even if they don't belong to any sets 
"""
@csrf_exempt
def delete_set(request):
    try:
        set = UserCharacterTag.objects.get(pk=request.POST.get('set_id'))
        if request.POST.get('is_delete_characters'):
            for uc in set.user_characters.all():
                uc.delete()
        set.delete()
        response = JsonResponse({'msg': 'good'})
    except Exception as e:
        response = JsonResponse({'msg': str(e)}, status=400)
    return response


"""
@api {POST} /accounts/rename_set/ Rename set
@apiDescription Rename a user set
@apiGroup accounts

@apiParam   {int}        set_id            the id of the user set to change name
@apiParam   {String}        new_name          this cannot be the same as the name of a current set
"""
@csrf_exempt
def rename_set(request):
    try:
        set = UserCharacterTag.objects.get(pk=request.POST.get('set_id'))
        set.name = request.POST.get('new_name')
        set.save()
        response = JsonResponse({'msg': 'good'})
    except Exception as e:
        response = JsonResponse({'msg': str(e)}, status=400)
    return response


"""
@api {POST} /accounts/get_available_sets/ Get available sets
@apiDescription Get available existing character sets to add
@apiGroup accounts

@apiSuccess {Object[]} sets list of serialized UserCharacterTag objects
"""
@csrf_exempt
def get_available_sets(request):
    sets = []
    for set in CharacterSet.objects.all():
        if not request.user.user_character_tags.filter(name=set.name).exists():
            sets.append(set)
    return JsonResponse({'sets': chenyx_serialize(sets)})
