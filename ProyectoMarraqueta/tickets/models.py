from typing import Any, Iterable
from django.db import models


class RegistryTicket(models.Model):
    datetime = models.DateTimeField("Creation time", auto_now_add=True)
    keychain = models.ForeignKey("core.KeyChain", on_delete=models.CASCADE, null=True, default=None)
    solved = models.BooleanField("Solved?", default=False)

class EmergencyTicket(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    datetime = models.DateTimeField("Creation time", auto_now_add=True)
    message = models.CharField("Message", max_length=500, default=None)