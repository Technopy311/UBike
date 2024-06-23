from django.db.models.signals import post_save
from .models import RegistryTicket
from core.models import KeyChain

from django.dispatch import receiver
from core.models import User

@receiver(post_save, sender=User)
def generateRegistryTicket(sender, created, instance, **kwargs):
    """
    Create RegistryTicket whenever a new user registers in the application.
    Returns True or false.
    True if successful ticket creation.
    False if not.
    """
    if created:
        try:
            new_keychain = KeyChain(
                user=instance, 
                uuid=""
            )
            new_keychain.save()
        except Exception:
            pass
    
        try:
            new_ticket = RegistryTicket(keychain=new_keychain)
            new_ticket.save()
        except KeyError:
            pass
        except Exception:
            pass
        