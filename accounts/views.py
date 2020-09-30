from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.forms import SignUpForm
from learning.models import CharacterSet
from accounts.models import UserCharacter, UserCharacterTag, User
from jiezi.utils.json_serializer import chenyx_serialize
from jiezi.permissions import IsOwner
from .serializers import UserSerializer, UserCharacterSerializer, \
    UserCharacterTagSerializer


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
        context = {'set': UserCharacterTag.objects.get(pk=set_id)}
        return render(request, 'accounts/manage_set.html', context)
    return render(request, 'accounts/manage_library.html')


@login_required
def profile(request):
    if request.GET.get('endsession', False):
        request.session['is_learning'] = False

    return render(request, 'accounts/profile.html')


@login_required
def staff_panel(request):
    if request.GET.get('endsession', False):
        request.session['is_learning'] = False

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'accounts/staff_panel.html')


@login_required
def alt_profile(request):
    if request.method == 'POST':
        currentUser = request.user
        currentUser.email = request.POST.get("email")
        currentUser.first_name = request.POST.get("first_name")
        currentUser.last_name = request.POST.get("last_name")
        currentUser.cn_level = request.POST.get("cn_level")
        currentUser.save()
        return HttpResponseRedirect(reverse('profile'))
    else:
        return render(request, 'accounts/profile.html')


"""
@api {POST} /accounts/add_set/ Add set
@apiDescription Make an copy of an existing CharacterSet in user's library as
    an UserCharacterTag with the same name
@apiGroup accounts

@apiParam   {int}   set_id        the id of the CharacterSet to be added
@apiError (Error 400) {String} msg   the detail of the exception
"""
@login_required
def add_set(request):
    try:
        new_set_id = CharacterSet.objects.get(pk=request.POST.get('set_id')).add_to_user(request.user)
        response = JsonResponse({'msg': 'good', 'id': new_set_id})
    except Exception as e:
        response = JsonResponse({'msg': str(e)}, status=400)
    return response


"""
@api {POST} /accounts/delete_character/ Delete character
@apiGroup accounts

@apiParam   {int}   character_id  the id of the Character to be deleted
@apiParam   {int}   set_id        (optional) the id of the UserCharacterTag for
the character to be deleted from, otherwise the character will be delete from 
all UserCharacterTags of the current user """
@login_required
def delete_character(request):
    try:
        uc = UserCharacter.objects.get(character__pk=request.POST.get('character_id'),
                                       user=request.user)
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
@api {POST} /accounts/get_available_sets/ Get available sets
@apiDescription Get available existing CharacterSets to add
@apiGroup accounts

@apiSuccess {Object[]} sets list of serialized CharacterSet objects
"""
@login_required
def get_available_sets(request):
    sets = []
    for set in CharacterSet.objects.all():
        if not request.user.user_character_tags.filter(name=set.name).exists():
            sets.append(set)
    return JsonResponse({'sets': chenyx_serialize(sets, ['characters'])})


class MyUserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserCharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = UserCharacter.objects.all()
    serializer_class = UserCharacterSerializer


class UserCharacterTagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = UserCharacterTag.objects.all()
    serializer_class = UserCharacterTagSerializer
