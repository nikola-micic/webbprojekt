from django import forms
from django.contrib.auth import password_validation
from core.models import CustomUser, Contact
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=("Username"),
        max_length=50,
        widget=forms.TextInput(attrs={
        "autocomplete": "username",
        "class": "text-center p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300",
        "style": "font-family: Roboto",
        "placeholder": "Username",
        })
    )
    password = forms.CharField(
        label=("Password"),
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
        "autocomplete": "password",
        "class": "text-center p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300",
        "placeholder": "Password",
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    # This allows inactive users to log in
    def confirm_login_allowed(self, user):
        pass

class UserCreateForm(UserCreationForm):
    username = forms.CharField(
        label=("Username"),
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "username", "class": "text-center p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Username"})
    )
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "text-center p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Email"})
    )
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "text-center p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "text-center p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Confirm password"}),
        help_text=("Enter the same password as before, for verification"),
    )
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "John"}))
    lastname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Doe"}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={"class": "p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Email"}))
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Title"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "w-[300px] h-[150px] p-1 focus:outline focus:outline-white rounded-md shadow-md shadow-gray-300 dark:shadow-gray-900 border border-gray-400 dark:border-gray-300", "placeholder": "Message"}), max_length=2000)

    class Meta:
        model = Contact
        fields = ("name", "lastname", "email", "title", "message")
