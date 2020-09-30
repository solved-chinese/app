from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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


class MyUserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserCharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = UserCharacter.objects.all()
    serializer_class = UserCharacterSerializer


class UserCharacterTagList(generics.ListCreateAPIView):
    """
    To add a UserCharacterTag linked to a CharacterSet, __POST__ with a single
    argument `character_set_id`

    __GET__ for a list of all user character tags belonging to current user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserCharacterTagSerializer

    def create(self, request, *args, **kwargs):
        cset_pk = request.data['character_set_id']
        cset = CharacterSet.objects.get(pk=cset_pk)
        obj = UserCharacterTag.objects.create(character_set=cset,
                                              user=request.user)
        obj.update_from_character_set()
        data = UserCharacterTagSerializer(
            obj, context=self.get_serializer_context()).data
        return Response(data,
                        status=status.HTTP_201_CREATED,
                        headers={'Location': str(data['url'])})

    def get_queryset(self):
        return self.request.user.user_character_tags


class UserCharacterTagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = UserCharacterTag.objects.all()
    serializer_class = UserCharacterTagSerializer
