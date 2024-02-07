from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('book/<int:id>/', views.book, name='book')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)