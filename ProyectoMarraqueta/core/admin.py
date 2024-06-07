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
                        'run',
                    ),
                }
            )
        )

admin.site.register(core_models.User, CustomBaseUser)


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
admin.site.register(core_models.EspModule)
admin.site.register(core_models.Bicycle)
