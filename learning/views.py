import datetime
import random
import requests
import time
import hashlib
import base64
import os.path

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from learning.models import update_from_df, Character, Radical, Report
from accounts.models import User, UserCharacter
from jiezi.utils.json_serializer import chenyx_serialize




def display_character(request, character_pk, **context_kwargs):
    """ Display character with pk=character_pk, if it is not found,
    display the next one.
    context_kwargs are passed into render directly """
    try:
        character = Character.objects.get(pk=character_pk)
    except ObjectDoesNotExist:
        character = Character.objects.filter(pk__gt=character_pk).first()
        return redirect('display_character', character_pk=character.pk)

    character = Character.objects.filter(pk__gte=character_pk).first()
    radicals = [Radical.objects.get(pk=character.radical_1_id)]
    radicals.append(Radical.objects.get(pk=character.radical_2_id)
                    if character.radical_2_id else None)
    radicals.append(Radical.objects.get(pk=character.radical_3_id)
                    if character.radical_3_id else None)
    return render(request, 'learning/display_character.html',
                  {'character':character, 'radicals':radicals, **context_kwargs})


@login_required
def start_learning(request):
    minutes_to_learn = request.POST.get('minutes_to_learn')
    uc_tags_filter = request.POST.get('uc_tags_exclude',
        [uc_tag.pk for uc_tag in request.user.user_character_tags.all()])
    assert isinstance(minutes_to_learn, int)
    assert isinstance(uc_tags_filter, list)
    assert all(isinstance(number, int) for number in uc_tags_filter)

    if request.user.last_study_time.date() == timezone.now().date() - \
            datetime.timedelta(days=1):
        request.user.study_streak += 1
    else:
        request.user.study_streak = 1

    request.user.last_study_duration = datetime.timedelta(seconds=0)
    request.user.last_study_vocab_count = 0
    request.user.save()

    request.session['uc_tags_filter'] = uc_tags_filter
    request.session['end_learning_time'] = timezone.now() + \
        datetime.timedelta(minutes=minutes_to_learn)

    request.session.cycle_key()
    return redirect(f'/learning/status{request.session.session_key}')


@login_required
@csrf_exempt
def learning_process(request, session_key):
    """ This is the main view that controls the learning process
    Note session['next'] stores a list of callables with input request, and
    they should be called before transition_stage happens """
    MIN_LEARN_REVIEW_INTERVAL = 180 # seconds

    def transition_stage():
        """ this function decides whether to learn or review,
        :return (mode, uc), mode is 'learning', 'review', or None (nothing to do),
        uc UserCharacter object
        """
        to_learn = request.user.user_characters.filter(
            times_learned=0,
            tags__in=request.session.get('uc_tags_filter')
        ).first()
        to_review = request.user.user_characters.filter(
            time_last_learned__lt=timezone.now() - datetime.timedelta(seconds=MIN_LEARN_REVIEW_INTERVAL),
            tags__in=request.session.get('uc_tags_filter'),
            times_learned__gte=1
        ).first()
        # TODO review radical
        if to_review is None and to_learn is None:
            return None, None
        elif to_review is None:
            return 'learn', to_learn
        elif to_learn is None:
            return 'review', to_review
        else:
            # TODO add actual logic
            return 'learn', to_learn if random.random() < 0.5 else 'review', to_review

    def end_learning(msg=''):
        return render(request, 'simple_response.html', {
            'content': 'You are finished.<br>' + msg
        })

    def review(character, field_name):
        choices = ['B', 'C', 'D']  # TODO implement with correct choices
        random.shuffle(choices)
        correct_answer = random.randint(4)
        choices.insert(correct_answer, getattr(character, field_name))
        request.session['correct_answer'] = correct_answer
        return render('learning/review.html', {'choices': choices})

    def check_answer():
        correct_answer = request.session['correct_answer']
        is_correct = request.GET.get('user_answer') == correct_answer

        uc = UserCharacter.objects.get(pk=request.session['uc_pk'])
        uc.times_learned += 1
        uc.saved()
        uc.update(is_correct)

        if not is_correct and not request.session['is_tolerant']:
            character = UserCharacter.objects.get(pk=request.session['uc_pk']).character
            request.session['next'] = [
                lambda req: display_character(req, character.pk, is_next=True)
            ]
        return JsonResponse({'correct_answer': correct_answer})

    # prevents the user from resuming into previous session
    if request.session.session_key != session_key:
        return redirect('404')

    # record stats
    delta_time = timezone.now() - request.session['last_record_time']
    request.session['last_record_time'] = timezone.now()
    request.user.last_study_duration += delta_time
    request.user.total_study_duration += delta_time
    request.user.last_study_time = timezone.now()
    request.user.save()

    if request.session['end_learning_time'] > timezone.now():
        return end_learning()

    if request.method == 'POST':
        return check_answer()

    next_value = request.session.get('next', [])
    if next_value:
        request.session['next'] = next_value[1:]
        return next_value[0](request)

    mode, uc = transition_stage()
    if mode is None:
        return end_learning('Add more characters to your library.')

    request.session['uc_pk']=uc.pk
    if mode == 'learn': # here learn only means learning for first time
        uc.times_learned += 1
        uc.save()
        request.user.last_study_vocab_count += 1
        request.user.save()
        request.session['is_tolerant'] = True
        request.session['next'] = [
            lambda req: review(uc.character, 'pinyin'),
            lambda req: review(uc.character, 'definition_1'),
        ]
        return display_character(request, uc.character.pk, is_next=True)
    else:
        # TODO separate the stats of the two attributes
        request.session['is_tolerant'] = False
        if random.random < 0.5:
            return review(uc.character, 'pinyin')
        else:
            return  review(uc.character, 'definition_1')


def report(request):
    try:
        report = Report(origin=request.POST.get('origin'),
                        description_1=request.POST.get('description_1'),
                        description_2=request.POST.get('description_2'))
        if isinstance(request.user, User):
            report.user = request.user
        report.save()
        return render(request, 'simple_response.html', {
            'content':'Thank you for your response!'
        })
    except:
        return redirect('404')

def getAudio(request):

    URL = "http://api.xfyun.cn/v1/service/v1/tts"
    AUE = "raw"
    APPID = "5d2407a2"
    API_KEY = "1194c50ae845b966ade10e8b47ece15e"

    def getHeader():
        curTime = str(int(time.time()))
        # ttp=ssml
        param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"aisxping\",\"speed\":\"10\",\"engine_type\":\"intp65\"}"
        print("param:{}".format(param))

        paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
        print("x_param:{}".format(paramBase64))

        m2 = hashlib.md5()
        m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))

        checkSum = m2.hexdigest()
        print('checkSum:{}'.format(checkSum))

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'X-Real-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        print(header)
        return header


    def getBody(text):
        data = {'text': text}
        return data


    def writeFile(file, content):
        with open(file, 'wb') as f:
            f.write(content)
        f.close()

    def requestAudio(character):
        r = requests.post(URL, headers=getHeader(), data=getBody(character))

        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
            sid = r.headers['sid']
            if AUE == "raw":
                writeFile("static/audio/" + request.GET.get("pk") + ".wav", r.content)
            else:
                writeFile("static/audio/" + "xiaoyan" + ".mp3", r.content)
            return True
        else:
        #   error-code reference: https://www.xfyun.cn/document/error-code
            return False

    audioKey = request.GET.get("pk")
    if os.path.exists('static/audio/' + audioKey + '.wav'):
        return JsonResponse({'success': True})
    else:
        res = requestAudio(request.GET.get("t"))
        if res:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})



"""
@api {POST} /search/ Search
@apiDescription search characters using ONE given keyword, it will be search 
    against pinyin (without accent), chinese, 3 definitions
@apiGroup general

@apiParam   {String}        key_word  the keyword to be searched

@apiSuccess {Object[]} characters list of serialized Character objects
"""
@csrf_exempt
def search(request):
    keyword = request.POST.get('keyword')
    characters_1 = Character.objects.filter(
        Q(pinyin__unaccent__iexact=keyword) | Q(chinese__exact=keyword)
    )
    characters_2 = Character.objects.filter(
        Q(definition_1__icontains=keyword) | \
        Q(definition_2__icontains=keyword) | \
        Q(definition_3__icontains=keyword) | \
        Q(pinyin__unaccent__icontains=keyword)
    ).difference(characters_1)
    return JsonResponse({'characters':
        chenyx_serialize(characters_1)+chenyx_serialize(characters_2)
    })

"""
@api {POST} /learning/start_learning/  Start Learning
@apiDescription Start Learning
@apiSuccessExample learning/review.html
context dictionary:
'choices': a list of 4 strings
'question': string of the question

Display the question and choices with no next button
After the user selects an answer, ajax POST to the same url with following args:
    'user_answer': integer with range [0, 4), representing user's answer
The server responds with 'correct_answer', which is in the same range,
    display the result, provide next button, and when the user clicks next, 
    submit GET request with no args
refer to old master review page for how to do specific things
    https://github.com/chenyx512/jiezi/blob/old-master/jiezi/templates/learning/review_interface.html

@apiSuccessExample learning/display_character.html:
There shouldn't be any ajax in this
In context dictionary, if 'is_next', provide an next button that submits
    GET form to original url, otherwise keep the next button the same as before
@apiGroup learning

@apiParam  {int}     minutes_to_learn  how many minutes to learn
@apiParam  {int[]}   uc_tags_filter=None  (optional, None means everything) the
    ids of UserCharacterTags to INCLUDE
"""
