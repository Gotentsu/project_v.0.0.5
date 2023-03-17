from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text="Required.Add a valid email address.")

    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(f"Email {email} s already in use.")

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        try:
            User.objects.get(firstname=firstname)
        except:
            return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        try:
            User.objects.get(lastname=lastname)
        except:
            return lastname

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(f"Username {username} s already in use.")


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")
