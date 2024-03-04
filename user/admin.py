from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class Administrator(UserAdmin):
    list_filter = 'is_superuser',
    list_display = ('username', 'email', 'is_superuser')
    search_fields = ('username', 'email')
    readonly_fields = ('username', 'email')
    fieldsets = (
        ('О пользователе', {
            'fields': (('username', 'email'), 'password')
        }),
        ('Разрешения', {
            'fields': ('is_superuser',)
        })
    )

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.save()
