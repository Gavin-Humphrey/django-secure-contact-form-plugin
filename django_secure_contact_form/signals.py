from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactMessage

@receiver(post_save, sender=ContactMessage)
def post_contact_message_save(sender, instance, **kwargs):
    # Perform additional actions after a contact message is saved
    pass
