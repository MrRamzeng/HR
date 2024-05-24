from django.contrib.auth.base_user import BaseUserManager
from game.models import AccuracyGame


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        AccuracyGame.objects.create(user=user)
        AccuracyGame.objects.create(user=user, timer=60)
        AccuracyGame.objects.create(user=user, timer=120)
        AccuracyGame.objects.create(user=user, mode='D')
        AccuracyGame.objects.create(user=user, mode='D', timer=60)
        AccuracyGame.objects.create(user=user, mode='D', timer=120)
        AccuracyGame.objects.create(user=user, mode='S')
        AccuracyGame.objects.create(user=user, mode='S', timer=60)
        AccuracyGame.objects.create(user=user, mode='S', timer=120)
        AccuracyGame.objects.create(user=user, mode='ALL')
        AccuracyGame.objects.create(user=user, mode='ALL', timer=60)
        AccuracyGame.objects.create(user=user, mode='ALL', timer=120)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError()
        return self.create_user(email, password, **extra_fields)
