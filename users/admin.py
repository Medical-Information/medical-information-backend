from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'pk',
        'email',
        'first_name',
        'last_name',
        'role',
        'subscribed',
        'is_active',
        'is_staff',
    )
    list_filter = (
        'role',
        'subscribed',
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
        (
            _('Personal Info'),
            {'fields': ('first_name', 'last_name', 'role', 'avatar', 'subscribed')},
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'created_at',
                    'updated_at',
                ),
            },
        ),
    )
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )
    ordering = ('email',)

    add_form_template = 'admin/auth/user/stricter_add_form.html'
