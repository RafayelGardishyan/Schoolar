from django.contrib.auth.models import User
from django.test import TestCase

from .models import List, Question, Subject
from .forms import UserForm


class UserTestCase(TestCase):

    def test_user(self):
        # Test User form
        print("Creating a user...")
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'email@example.com',
            'password': 'testPassword'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        print("User Created")

        print("Getting the user...")
        # Test User username generation
        user = User.objects.get(first_name="Test")
        self.assertTrue(user.username != "" or user.username is not None)
        print("User is gotten")

class QuestionTestCase(TestCase):

    def setUp(self):
        print("Setting up a question...")
        Question.objects.create(question="Question", answer="Answer")
        print("Question is set up")

    def test_question(self):
        print("Getting the question...")
        question = Question.objects.get(pk=1)
        self.assertTrue(question.question == "Question")
        self.assertTrue(question.answer == "Answer")
        print("Question is gotten")


class SubjectTestCase(TestCase):

    def setUp(self):
        print("Setting up a subject...")
        Subject.objects.create(name="Test Subject")
        print("Subject is set up")

    def test_subject(self):
        print("Getting the subject...")
        subject = Subject.objects.get(pk=1)
        self.assertTrue(subject.name == "Test Subject")
        print("Subject is gotten")

class ListTestCase(TestCase):

    def setUp(self):
        print("Setting up a list...")

        print("Setting up a user...")
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

        print("User is set up")

        print("Setting up a question...")
        # Create Test Assets
        Question.objects.create(question="Question", answer="Answer")

        print("Questions is set up")
        print("Setting up a subject...")
        Subject.objects.create(name="Test Subject")
        print("Subject is set up")

        print("Getting test assets for the list test...")
        # Get Test Assets
        user = User.objects.get(first_name="Test")
        subject = Subject.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        print("Assets are gotten")
        print("Creating a list...")
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
        print("List is created and saved")
        print("List is set up")

    def test_list(self):
        print("Getting list test assets...")
        list = List.objects.get(pk=1)
        user = User.objects.get(first_name="Test")
        subject = Subject.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        print("Assets are gotten")

        print("Testing assets...")
        self.assertTrue(list.name == "Test List")
        self.assertTrue(list.question_subject == subject == list.answer_subject)
        self.assertTrue(list.questions.count() == 1)
        self.assertTrue(list.questions.all()[0] == question)
        self.assertTrue(list.owner == user)

        print("Assets are tested")
        print("List is tested")
