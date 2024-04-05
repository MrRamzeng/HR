from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise ValidationError('Адрес электронной почты уже зарегистрирован')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update(
        #     {
        #         'class': 'form-control',
        #         'placeholder': 'Username'
        #     }
        # )
        # self.fields['email'].widget.attrs.update(
        #     {
        #         'class': 'form-control',
        #         'placeholder': 'Email'
        #     }
        # )
        # self.fields['password'].widget.attrs.update(
        #     {
        #         'class': 'form-control',
        #         'placeholder': 'Password1'
        #     }
        # )
        # self.fields['password'].widget.attrs.update(
        #     {
        #         'class': 'form-control',
        #         'placeholder': 'Password1'
        #     }
        # )


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
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'id': 'password',
                'placeholder': '••••••••',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            }
        )
