from django.contrib.auth.models import User
from django.test import TestCase

from .models import List, Question, Subject
from .forms import UserForm


class UserTestCase(TestCase):

    def test_user(self):
        # Test User form
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'email@example.com',
            'password': 'testPassword'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Test User username generation
        user = User.objects.get(first_name="Test")
        self.assertTrue(user.username != "" or user.username is not None)


class QuestionTestCase(TestCase):

    def setUp(self):
        Question.objects.create(question="Question", answer="Answer")

    def test_question(self):
        question = Question.objects.get(pk=1)
        self.assertTrue(question.question == "Question")
        self.assertTrue(question.answer == "Answer")


class SubjectTestCase(TestCase):

    def setUp(self):
        Subject.objects.create(name="Test Subject")

    def test_subject(self):
        subject = Subject.objects.get(pk=1)
        self.assertTrue(subject.name == "Test Subject")

class ListTestCase(TestCase):

    def setUp(self):
        # Create Test User
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'email@example.com',
            'password': 'testPassword'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Create Test Assets
        Question.objects.create(question="Question", answer="Answer")
        Subject.objects.create(name="Test Subject")

        # Get Test Assets
        user = User.objects.get(first_name="Test")
        subject = Subject.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        test_list = List.objects.create(
            owner=user,
            question_subject=subject,
            answer_subject=subject,
            name="Test List"
        )
        test_list.save()
        test_list.questions.add(question)

        # Save List
        test_list.save()

    def test_list(self):
        list = List.objects.get(pk=1)
        user = User.objects.get(first_name="Test")
        subject = Subject.objects.get(pk=1)
        question = Question.objects.get(pk=1)

        self.assertTrue(list.name == "Test List")
        self.assertTrue(list.question_subject == subject == list.answer_subject)
        self.assertTrue(list.questions.count() == 1)
        self.assertTrue(list.questions.all()[0] == question)
        self.assertTrue(list.owner == user)
