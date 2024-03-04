from django.urls import path

from .views import RegisterView, LogView, logout_view

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LogView.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]
