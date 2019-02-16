from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.question + " : " + self.answer


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question_subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, related_name='question_subject')
    answer_subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, related_name='answer_subject')
    questions = models.ManyToManyField(to=Question)

    def __str__(self):
        return self.name

    def get_test(self):
        return str(self.pk)
