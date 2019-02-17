import random
import string

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.username = user.first_name + str(random.randint(1111, 9999)) + random.choice(string.ascii_lowercase)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
