from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
)
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
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'id': 'username',
                'autocomplete': 'false',
                'type': 'text',
                'placeholder': 'Username',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'id': 'email',
                'autocomplete': 'false',
                'type': 'email',
                'placeholder': 'example@company.com',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'id': 'password1',
                'autocomplete': 'false',
                'placeholder': '••••••••',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'id': 'password2',
                'autocomplete': 'false',
                'placeholder': '••••••••',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )


class LoginForm(AuthenticationForm):

    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise ValidationError('Адрес электронной почты не зарегистрирован.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'id': 'email',
                'autocomplete': 'email',
                'type': 'email',
                'placeholder': 'example@company.com',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'id': 'password',
                'placeholder': '••••••••',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )


class ResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise ValidationError('Адрес электронной почты не зарегистрирован.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {
                'id': 'email',
                'autocomplete': '',
                'placeholder': 'example@company.com',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )


class ResetDone(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)

        self.fields['new_password1'].widget.attrs.update(
            {
                'id': 'password1',
                'name': 'password1',
                'autocomplete': 'false',
                'placeholder': '••••••••',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['new_password2'].widget.attrs.update(
            {
                'id': 'password2',
                'name': 'password2',
                'autocomplete': 'false',
                'placeholder': '••••••••',
                'class': 'block w-full p-2.5 bg-gray-50 border border-gray-300 '
                         'rounded-lg text-gray-900 sm:text-sm '
                         'focus:border-primary-600 focus:ring-primary-600 '
                         'dark:bg-gray-700 dark:border-gray-600 '
                         'dark:placeholder-gray-400 dark:text-white '
                         'dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )