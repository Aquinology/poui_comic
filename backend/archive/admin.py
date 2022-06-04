from django.contrib import admin
from auth_system.admin import CustomUserAdmin
from .models import *


class ProfileAdmin(CustomUserAdmin):
    fieldsets = (
        *CustomUserAdmin.fieldsets,
        (
            'Profile fields',
            {
                'fields': (
                    'read_chapters',
                ),
            },
        ),
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team)
admin.site.register(Role)
admin.site.register(Member)
admin.site.register(Genre)
admin.site.register(Manga)
admin.site.register(Rating)
admin.site.register(Section)
admin.site.register(Chapter)
admin.site.register(Page)
