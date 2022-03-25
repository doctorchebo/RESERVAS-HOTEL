from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from RESERVAS.models import *
from django.conf import settings

# @receiver(m2m_changed, sender=Reserva.cuarto.through)
# def m2m_cambiar_estado_cuarto(sender, instance, action, **kwargs):
#     if action == 'pre_add' or action == 'post_add':
#         for item in instance.cuarto.all():
#             item.estado = False
#             item.save()
#     elif action == 'pre_remove' or action == 'post_remove':
#         for item in instance.cuarto.all():
#             item.estado = True
#             item.save()
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_cliente_al_crear_usuario(sender,**kwargs):
    if kwargs['created']:
        Cliente.objects.create(usuario=kwargs['instance'])



