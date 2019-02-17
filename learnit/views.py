import json
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.shortcuts import render, redirect
from django.template.loader import get_template

from .forms import UserForm
from .models import Subject, List, Question, TestResults


def index(request):
    if request.user.is_authenticated:
        return redirect('/app/home')
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.username = user.first_name
            user.save()

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

            return redirect("/")
            # return render(request, 'registration/success.html', {'user': user})

    return render(request, "registration/register.html", {
        'userform': UserForm()
    })


def app_home(request):
    return render(request, "app/index.html", {
        'username': request.user.username
    })


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

    return render(request, 'app/add.html', {
        'subjects': subjects
    })


def lists(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    n_lists = List.objects.filter(owner=request.user)
    return render(request, 'app/lists.html', {
        'lists': n_lists,
        'username': request.user.username
    })


def test(request, list_id):
    try:
        list = List.objects.get(pk=list_id, owner=request.user)
    except:
        return redirect('/app/lists')

    return render(request, 'app/test.html', {
        'questions': list.questions.all()
    })


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

    result = TestResults()
    result.user = request.user
    result.grade = float(request.POST["average_score"])
    result.save()

    diff_quest = json.loads(request.POST["difficult_words"])

    for question in diff_quest:
        result.difficult_questions.add(Question.objects.get(question=question["question"], answer=question["answer"]))

    result.save()

    return redirect('/app/result/' + str(result.pk))


def results(request, result_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'app/result.html', {
        'result': TestResults.objects.get(pk=result_id)
    })


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    n_results = TestResults.objects.filter(user=user)

    return render(request, 'registration/profile.html', {
        'user': user,
        'results': n_results
    })
