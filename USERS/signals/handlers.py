from django.dispatch import receiver
from RESERVAS.signals import reserva_creada

@receiver(reserva_creada)
def on_reserva_creada(sender, **kwargs):
    print(kwargs['cliente'])