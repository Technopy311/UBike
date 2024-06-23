from django.contrib import admin
from .models import RegistryTicket, EmergencyTicket


class RegistryTicketAdmin(admin.ModelAdmin):
    list_display=["keychain", "solved", "datetime"]
    fields = ["keychain"]
    date_hierarchy = "datetime"
    readonly_fields = ["datetime"]

admin.site.register(RegistryTicket, RegistryTicketAdmin)

class EmergencyTicketAdmin(admin.ModelAdmin):
    fields = ["user", "keychain", "datetime"]
    list_display = ["user", "datetime"]
    date_hierarchy = "datetime"

admin.site.register(EmergencyTicket, EmergencyTicketAdmin)
