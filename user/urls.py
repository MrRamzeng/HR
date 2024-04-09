from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .forms import ResetForm, ResetDone
from .views import RegisterView, LogView, logout_view

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LogView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path(
        'reset/account/', PasswordResetView.as_view(
            template_name='user/reset/reset.html',
            form_class=ResetForm
        ), name='password_reset'
    ),
    path(
        'reset/sent/', PasswordResetDoneView.as_view(
            template_name='user/reset/sent.html'
        ), name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
            template_name='user/reset/form.html', form_class=ResetDone
        ), name='password_reset_confirm'
    ),
    path(
        'reset/complete/', PasswordResetCompleteView.as_view(
            template_name='user/reset/complete.html'
        ), name='password_reset_complete'
    )

]
