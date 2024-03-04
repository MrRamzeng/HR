from django.contrib.auth.forms import UserCreationForm
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

