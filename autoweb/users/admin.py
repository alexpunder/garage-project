from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser

admin.site.empty_value_display = 'Не задано'


class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'phone_number'
    )
    list_display_links = (
        'email',
    )
    search_fields = (
        'email', 'first_name', 'last_name', 'phone_number'
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone_number',)
        }),
    )
    list_per_page = 25


admin.site.register(CustomUser, CustomUserAdmin)
