from typing import Any, Iterable
from django.db import models


class RegistryTicket(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    datetime = models.DateTimeField("Creation time", auto_now_add=True)
    keychain = models.ForeignKey("core.KeyChain", on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.keychain.uuid != None:    
            self.keychain.user = self.user
        
        super(RegistryTicket, self).save(*args, **kwargs)


class EmergencyTicket(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    datetime = models.DateTimeField("Creation time", auto_now_add=True)
    message = models.CharField("Message", max_length=500, default=None)