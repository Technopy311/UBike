from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as core_models

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'New Fields',
            {
                'fields': (
                    'is_guard',
                    'base_role',
                    'name',
                    'user_type',
                    'last_name',
                    'run',
                ),
            },
        ),
    )

admin.site.register(core_models.User, CustomUserAdmin)
admin.site.register(core_models.Student, CustomUserAdmin)
admin.site.register(core_models.Professor, CustomUserAdmin)
admin.site.register(core_models.Academic, CustomUserAdmin)
admin.site.register(core_models.External, CustomUserAdmin)
admin.site.register(core_models.Staff, CustomUserAdmin)
admin.site.register(core_models.Guard, CustomUserAdmin)

#admin.site.register(core_models.Guard)
