from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from learning.models import Character, Radical, Quiz
from django.contrib.auth.decorators import user_passes_test
import random
import openpyxl


def index(request):
    return render(request, 'index.html');

def about_us(request):
    return  render(request, 'about_us.html');

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
    return render(request, 'learning/learning_character.html', dict)


@login_required
def review_test(request):
    list = ['a_very_long_first', 'second', 'third', 'fourth', 'fifth']
    ans = 'second'
    question = '好'
    return review_interface(request, list=list, ans=ans, question=question)


@login_required
def review_interface(request, list=[], ans='', question=''):
    if request.method == 'POST':
        choice = int(request.POST.get('choice'))
        correct = request.user.quiz.ans_index
        if choice == correct:
            incorrect = -1
        else:
            incorrect = choice
        choices = [request.user.quiz.choice1, request.user.quiz.choice2, request.user.quiz.choice3,
                   request.user.quiz.choice4]
        return render(request, 'learning/review_interface.html',
                      {'choices': choices, 'question': request.user.quiz.question, 'correct': correct,
                       'incorrect': incorrect})
    else:
        choices = random.sample(list, 4)
        ans_index = -1
        for i in range(0, 4):
            if choices[i] == ans:
                ans_index = i
        if ans_index == -1:
            ans_index = random.randrange(4)
            choices[ans_index] = ans
        try:
            request.user.quiz.delete()
        except:
            pass
        Quiz(user=request.user, choice1=choices[0], choice2=choices[1], choice3=choices[2], choice4=choices[3],
             question=question, ans_index=ans_index).save()
        return render(request, 'learning/review_interface.html',
                      {'choices': choices, 'question': question, 'correct': -1, 'incorrect': -1})


@user_passes_test(lambda u: u.is_staff)
def load_radical(request):
    if "GET" == request.method:
        return render(request, 'learning/load_excel.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Radicals"]
        list = []
        n = worksheet.max_row
        m = worksheet.max_column
        for i in range(2, n + 1):
            pk = worksheet.cell(i, 1).value
            if pk is None:
                continue
            pk = int(pk)
            chinese = worksheet.cell(i, 2).value
            pinyin = worksheet.cell(i, 3).value
            definition = worksheet.cell(i, 4).value
            mnemonic_explanation = worksheet.cell(i, 5).value
            is_phonetic = True if str(worksheet.cell(i, 6).value) == '1' else False
            is_semantic = True if str(worksheet.cell(i, 7).value) == '1' else False
            message = ''
            try:
                if Radical.objects.filter(pk=pk).exists():
                    message += 'update R%04d ' % pk
                    Radical.objects.filter(pk=pk).update(chinese=chinese, pinyin=pinyin, definition=definition,
                                                         mnemonic_explanation=mnemonic_explanation,
                                                         is_phonetic=is_phonetic, is_semantic=is_semantic)
                else:
                    message += 'create R%04d ' % pk
                    Radical.objects.create(jiezi_id=pk, chinese=chinese, pinyin=pinyin, definition=definition,
                                           mnemonic_explanation=mnemonic_explanation, is_phonetic=is_phonetic,
                                           is_semantic=is_semantic)
            except Exception as e:
                message += str(e)
            else:
                message += 'success'
            list.append(message)
        return render(request, 'learning/load_excel.html', {"list": list})


@user_passes_test(lambda u: u.is_staff)
def load_character(request):
    if "GET" == request.method:
        return render(request, 'learning/load_excel.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Characters"]
        list = []
        n = worksheet.max_row
        m = worksheet.max_column
        for i in range(2, n + 1):
            pk = worksheet.cell(i, 2).value
            if pk is None or pk=='':
                continue
            pk = int(pk)
            chinese = worksheet.cell(i, 3).value
            pinyin = worksheet.cell(i, 4).value
            definition_1 = worksheet.cell(i, 5).value
            definition_2 = worksheet.cell(i, 6).value
            explanation_2 = worksheet.cell(i, 7).value
            definition_3 = worksheet.cell(i, 8).value
            explanation_3 = worksheet.cell(i, 9).value
            r1 = worksheet.cell(i, 10).value
            r2 = worksheet.cell(i, 11).value
            if r2 == '': r2=None
            r3 = worksheet.cell(i, 12).value
            if r3 == '': r3=None
            mnemonic_explanation = worksheet.cell(i, 13).value
            example1_word = worksheet.cell(i, 14).value
            example1_pinyin = worksheet.cell(i, 15).value
            example1_character = worksheet.cell(i, 16).value
            example1_meaning = worksheet.cell(i, 17).value
            example2_word = worksheet.cell(i, 18).value
            example2_pinyin = worksheet.cell(i, 19).value
            example2_character = worksheet.cell(i, 20).value
            example2_meaning = worksheet.cell(i, 21).value
            message = ''
            try:
                if Character.objects.filter(pk=pk).exists():
                    message += 'update C%04d: ' % pk
                    Character.objects.filter(pk=pk).update(chinese=chinese, pinyin=pinyin, definition_1=definition_1,
                                                           definition_2=definition_2, explanation_2=explanation_2,
                                                           explanation_3=explanation_3, definition_3=definition_3,
                                                           mnemonic_1=r1, mnemonic_2=r2, mnemonic_3=r3,
                                                           mnemonic_explanation=mnemonic_explanation,
                                                           example_1_word=example1_word,
                                                           example_1_pinyin=example1_pinyin,
                                                           example_1_character=example1_character,
                                                           example_1_meaning=example1_meaning,
                                                           example_2_word=example2_word,
                                                           example_2_pinyin=example2_pinyin,
                                                           example_2_character=example2_character,
                                                           example_2_meaning=example2_meaning)
                else:
                    message += 'create C%04d: ' % pk
                    Character.objects.create(jiezi_id=pk, chinese=chinese, pinyin=pinyin, definition_1=definition_1,
                                             definition_2=definition_2, explanation_2=explanation_2,
                                             explanation_3=explanation_3, definition_3=definition_3, mnemonic_1=r1,
                                             mnemonic_2=r2, mnemonic_3=r3, mnemonic_explanation=mnemonic_explanation,
                                             example_1_word=example1_word, example_1_pinyin=example1_pinyin,
                                             example_1_character=example1_character, example_1_meaning=example1_meaning,
                                             example_2_word=example2_word, example_2_pinyin=example2_pinyin,
                                             example_2_character=example2_character, example_2_meaning=example2_meaning)
            except Exception as e:
                message += str(e)
            else:
                message += 'success'
            list.append(message)
        return render(request, 'learning/load_excel.html', {"list": list})
