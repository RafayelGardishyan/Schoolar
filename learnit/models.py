import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Question(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.question + " : " + self.answer


class Subject(models.Model):
    name = models.CharField(max_length=255)
    name_dutch = models.CharField(max_length=255, default="UNKNOWN")
    tts_support = models.BooleanField(default=False)

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

    def get_edit_url(self):
        return reverse('edit_list', args=[self.pk])


class TestResults(models.Model):
    grade = models.FloatField()
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    initial_question_amount = models.IntegerField(default=0)
    total_question_amount = models.IntegerField(default=0)
    difficult_questions_amount = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    difficult_questions = models.ManyToManyField(to=Question)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    # list = models.ForeignKey(to=List, on_delete=models.CASCADE, default=List.objects.get())

    def get_difficult_words_count(self):
        return self.difficult_questions.all().count()

    def get_time_difference(self):
        dateTimeA = datetime.datetime.combine(datetime.date.today(), self.end_time)
        dateTimeB = datetime.datetime.combine(datetime.date.today(), self.start_time)
        # Get the difference between datetimes (as timedelta)
        dateTimeDifference = dateTimeA - dateTimeB
        # Divide difference in seconds by number of seconds in hour (3600)
        return dateTimeDifference.total_seconds()


class Settings(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    interface_theme = models.IntegerField(default=0)
    interface_language = models.IntegerField(default=0)

