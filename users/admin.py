from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
