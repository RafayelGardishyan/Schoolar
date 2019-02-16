from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import Subject, List, Question

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
            return redirect("/")

    return render(request, "registration/register.html", {
        'userform': UserForm()
    })


def app_home(request):
    return render(request, "app/index.html")


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

        return JsonResponse(serializers.serialize('json', [n_list]), safe=False)

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
