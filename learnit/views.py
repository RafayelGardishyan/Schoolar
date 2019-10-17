import datetime
import json
import random
import string

from django.core.mail import send_mail
from django.http import BadHeaderError, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils import timezone

from .forms import UserForm
from .models import Subject, \
    List, Question, TestResults, \
    Settings


def BinarySearch(lys, val):
    for i in range(len(lys)):
        if lys[i].pk == val.pk:
            return i
    return None


def generate_context(request, context):
    if request.user.is_authenticated:
        settings = Settings.objects.get(user=request.user)
        context['settings_theme'] = settings.interface_theme
        context['settings_lang'] = settings.interface_language

    return context


def index(request):
    if request.user.is_authenticated:
        return redirect('/app/home')
    return render(request, "index.html")


def get_language_code(request):
    return JsonResponse(
        dict(
            german="de-DE",
            english="en-GB",
            spanish="es-ES",
            french="fr-FR",
            hindu="hi-IN",
            indonesian="id-ID",
            italian="it-IT",
            japan="ja-JP",
            korean="ko-KR",
            dutch="nl-NL",
            polish="pl-PL",
            brasilian="pt-BR",
            russian="ru-RU",
            chinese="zh-CN"
        ), safe=False)


def register(request):
    if request.user.is_authenticated:
        return redirect('/app/home')
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()

            settings = Settings()
            settings.user = user
            settings.save()

            template = get_template('emails/registration.txt')
            content = template.render({'username': user.username})
            if not user.email:
                raise BadHeaderError('No email address given for {0}'.format(user))

            send_mail(
                '[Learn It] Account registration',
                content,
                'noreply@learnit.com',
                [user.email],
                fail_silently=False,
            )

            print('Sent mail to: {}'.format(user.email))

            # return redirect("/login")

            return render(request, 'registration/success.html', generate_context(request, {'user': user}))

    return render(request, "registration/register.html", generate_context(request, {
        'userform': UserForm()
    }))


def app_home(request):
    results = TestResults.objects.filter(user=request.user)
    lists = []
    for result in results:
        if result.list not in lists:
            lists.append(result.list)

    return render(request, "app/index.html", generate_context(request, {
        'username': request.user.username,
        'lists': lists
    }))


def logged_out(request):
    return render(request, "registration/logout.html")


def add_list(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        n_list = List()
        n_list.name = request.POST["name"]
        n_list.question_subject = Subject.objects.get(pk=request.POST["question_subject"])
        n_list.answer_subject = Subject.objects.get(pk=request.POST["answer_subject"])
        n_list.owner = request.user
        n_list.save()
        questions = []

        go = True
        n_index = 1
        while go:
            question = Question()
            try:
                question.question = request.POST["question_" + str(n_index)]
                question.answer = request.POST["answer_" + str(n_index)]
                if question.answer != "" and question.question != "":
                    question.save()
                    questions.append(question)
                n_index += 1
            except KeyError:
                go = False

        for question in questions:
            n_list.questions.add(question)

        n_list.save()

        return redirect("/app/lists")

    subjects = Subject.objects.all()

    return render(request, 'app/add.html', generate_context(request, {
        'subjects': subjects
    }))


def edit_list(request, list):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        n_list = List.objects.get(pk=list)
        n_list.name = request.POST["name"]
        n_list.question_subject = Subject.objects.get(pk=request.POST["question_subject"])
        n_list.answer_subject = Subject.objects.get(pk=request.POST["answer_subject"])
        n_list.owner = request.user
        n_list.save()
        questions = []

        go = True
        n_index = 1
        while go:
            question = Question()
            try:
                question.question = request.POST["question_" + str(n_index)]
                question.answer = request.POST["answer_" + str(n_index)]
                if question.answer != "" and question.question != "":
                    question.save()
                    questions.append(question)
                n_index += 1
            except KeyError:
                go = False

        n_list.questions.clear()

        for question in questions:
            n_list.questions.add(question)

        n_list.save()

        return redirect("/app/lists")

    subjects = Subject.objects.all()
    g_list = List.objects.get(pk=list)
    question_id = BinarySearch(subjects, g_list.question_subject)
    answer_id = BinarySearch(subjects, g_list.answer_subject)

    return render(request, 'app/edit.html', generate_context(request, {
        'subjects': subjects,
        'list': g_list,
        'subject_ids': {
            'question': question_id,
            'answer': answer_id
        }
    }))


def lists(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    n_lists = List.objects.filter(owner=request.user)
    return render(request, 'app/lists.html', generate_context(request, {
        'lists': n_lists,
        'username': request.user.username
    }))


def test(request, list_id):
    try:
        n_list = List.objects.get(pk=list_id, owner=request.user)
    except:
        return redirect('/app/lists')

    if not request.GET:
        return render(request, 'app/test_setup.html', generate_context(request, {
            'list': n_list
        }))

    if Settings.objects.get(user=request.user).interface_language == 0:
        lang = "english"
    else:
        lang = "dutch"

    if request.GET["question_subject"] == "question":
        if n_list.question_subject.tts_support:
            lang = n_list.question_subject.name.lower()
    elif request.GET["question_subject"] == "answer":
        if n_list.answer_subject.tts_support:
            lang = n_list.answer_subject.name.lower()

    print(lang)

    settings = {
        'question_subject': request.GET["question_subject"],
        'mode': request.GET["test_mode"],
        'delay': float(request.GET["delay"])*1000,
        'case_sensitive': request.GET['case_sensitive'],
        'tts_enabled': request.GET['tts'],
        'tts_lang': lang
    }

    request.session["current_list"] = n_list.pk

    return render(request, 'app/test_translate.html', generate_context(request, {
        'questions': n_list.questions.all(),
        'list': n_list,
        'settings': json.dumps(settings)
    }))


def delete(request, list_id):
    try:
        n_list = List.objects.get(pk=list_id, owner=request.user)
    except:
        return redirect('/app/lists')

    for question in n_list.questions.all():
        question.delete()

    n_list.delete()

    return redirect("/app/lists")


def register_results(request):
    if request.method != 'POST':
        return redirect('/')

    stats = json.loads(request.POST["stats"])

    result = TestResults()
    result.user = request.user
    result.grade = float(stats["averageScore"])
    result.initial_question_amount = stats["initialQuestionAmount"]
    result.total_question_amount = stats["totalQuestionAmount"]
    result.difficult_questions_amount = stats["difficultQuestionAmount"]
    result.correct_answers = stats["correctAnswers"]
    result.wrong_answers = stats["wrongAnswers"]
    result.start_time = datetime.time(stats["startTime"][0], stats["startTime"][1], stats["startTime"][2])
    result.end_time = datetime.time(stats["endTime"][0], stats["endTime"][1], stats["endTime"][2])
    result.list = List.objects.get(pk=request.session["current_list"])

    result.save()

    diff_quest = json.loads(request.POST["difficult_words"])

    for question in diff_quest:
        try:
            result.difficult_questions.add(
                Question.objects.get(question=question["question"], answer=question["answer"]))
        except:
            result.difficult_questions.add(
                Question.objects.filter(question=question["question"], answer=question["answer"])[0])


    result.save()

    return redirect('/app/result/' + str(result.pk))


def results(request, result_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'app/result.html', generate_context(request, {
        'result': TestResults.objects.get(pk=result_id)
    }))


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    n_results = TestResults.objects.filter(user=user)

    return render(request, 'registration/profile.html', generate_context(request, {
        'user': user,
        'results': n_results
    }))


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        user = request.user
        user.username = request.POST["username"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.save()

        settings = Settings.objects.get(user=user)
        settings.interface_theme = int(request.POST["theme"])
        settings.interface_language = int(request.POST["lang"])
        settings.save()

        return redirect('/user/profile')

    return render(request, 'registration/edit_profile.html', generate_context(request, {'user': request.user}))
