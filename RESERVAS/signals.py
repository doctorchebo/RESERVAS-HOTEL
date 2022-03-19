from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from .models import *

@receiver(m2m_changed, sender=Reserva.cuarto.through)
def m2m_cambiar_estado_cuarto(sender, instance, action, **kwargs):
    if action == 'pre_add' or action == 'post_add':
        for item in instance.cuarto.all():
            item.estado = False
            item.save()
    elif action == 'pre_remove' or action == 'post_remove':
        for item in instance.cuarto.all():
            item.estado = True
            item.save()




