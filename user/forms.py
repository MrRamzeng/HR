from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise ValidationError('Адрес электронной почты уже зарегистрирован.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('Имя пользователя уже занято.')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'id': 'username',
                'autocomplete': 'false',
                'type': 'text',
                'placeholder': 'Username',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 block w-full p-2.5 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'id': 'email',
                'autocomplete': 'false',
                'type': 'email',
                'placeholder': 'name@example.com',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 block w-full p-2.5 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'id': 'password1',
                'autocomplete': 'false',
                'placeholder': '••••••••',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 block w-full p-2.5 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'id': 'password2',
                'autocomplete': 'false',
                'placeholder': '••••••••',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 block w-full p-2.5 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )


class LoginForm(AuthenticationForm):

    def clean_username(self):
        email = self.cleaned_data.get('username')
        print(email)
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise ValidationError('Адрес электронной почты не зарегистрирован.')
        return email

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'id': 'email',
                'autocomplete': 'email',
                'type': 'email',
                'placeholder': 'name@example.com',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 block w-full p-2.5 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'id': 'password',
                'placeholder': '••••••••',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 block w-full p-2.5 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
