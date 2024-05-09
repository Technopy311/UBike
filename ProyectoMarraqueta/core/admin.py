from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as core_models

class CustomBaseUser(UserAdmin):
    
    fieldsets = (
            *UserAdmin.fieldsets,
            (
                'Base Fields',
                {
                    'fields':(
                        'is_guard',
                        'user_type',
                        'run',
                    ),
                }
            )
        )

admin.site.register(core_models.User, CustomBaseUser)


class CustomUserStudent(CustomBaseUser):
    fieldsets = (
        *CustomBaseUser.fieldsets,
        (
            'Student Fields',
            {
                'fields':(
                    'career',
                    'usm_role',
                ),
            }
        )
    )

admin.site.register(core_models.Student, CustomUserStudent)


class CustomuUserProfessor(CustomBaseUser):
    fieldsets = (
        *CustomBaseUser.fieldsets,
        (
            'Professor Fields',
            {
                'fields':(
                    'department',
                    'usm_role',
                ),
            }
        )
    )

admin.site.register(core_models.Professor, CustomuUserProfessor)


class CustomuUserAcademic(CustomBaseUser):
    fieldsets = (
        *CustomBaseUser.fieldsets,
        (
            'Academic Fields',
            {
                'fields':(
                    'connection',
                ),
            }
        )
    )

admin.site.register(core_models.Academic, CustomuUserAcademic)


class CustomuUserExternal(CustomBaseUser):
    fieldsets = (
        *CustomBaseUser.fieldsets,
        (
            'External Fields',
            {
                'fields':(
                    'connection',
                ),
            }
        )
    )

admin.site.register(core_models.External, CustomuUserExternal)


class CustomuUserStaff(CustomBaseUser):
    fieldsets = (
        *CustomBaseUser.fieldsets,
        (
            'Staff Fields',
            {
                'fields':(
                    'charge',
                ),
            }
        )
    )

admin.site.register(core_models.Staff, CustomuUserStaff)


class CustomuUserGuard(CustomBaseUser):
    fieldsets = (
        *CustomBaseUser.fieldsets,
        (
            'Guard Fields',
            {
                'fields':(
                    'connection',
                ),
            }
        )
    )

admin.site.register(core_models.Guard, CustomuUserGuard)



admin.site.register(core_models.BicycleHolder)
admin.site.register(core_models.KeyChain)
admin.site.register(core_models.PicowModule)
admin.site.register(core_models.Bicycle)
