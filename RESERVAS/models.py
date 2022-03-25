from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from .validators import validar_tamaño_imagen

class Cliente(models.Model):
    TIPO_IDENTIFICACION = (
        ('ID', 'Cédula de Identidad'),
        ('L', 'Licencia de Conducir'),
        ('P', 'Pasaporte'),
    )
    tipo_id = models.CharField(max_length=3, choices=TIPO_IDENTIFICACION, blank=True, null=True)
    numero_id = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.BigIntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    fecha_nacimiento=models.DateField(blank=True, null=True)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id} {self.usuario}'
    class Meta:
        permissions=[
            ('ver_historial','Puede ver historial'),
        ]
class Reserva(models.Model):
    PENDIENTE = 'P'
    PAGADO = 'A'
    ELIMINADO = 'E'
    
    ESTADO = (
        (PENDIENTE, 'Pendiente'),
        (PAGADO, 'Pagado'),
        (ELIMINADO, 'Eliminado'),
    )
    EFECTIVO = 'E'
    TARJETA = 'T'
    TRANSFERENCIA = 'R'

    METODO_PAGO = (
        (EFECTIVO, 'Efectivo'),
        (TARJETA, 'Tarjeta'),
        (TRANSFERENCIA, 'Transferencia'),
    )
    estado = models.CharField(max_length=1, choices=ESTADO)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    metodo_pago = models.CharField(max_length=3, choices=METODO_PAGO)
    creado = models.DateField(auto_now_add=True, null=True)
    modificado = models.DateField(auto_now=True, null=True)
    def __str__(self):
        return f'Reserva Nº {self.id} {self.cliente.usuario.last_name} {self.cliente.usuario.first_name}'

class Habitacion(models.Model):    
    SIMPLE = 'S'
    MATRIMONIAL = 'M'
    KING_SIZE = 'KS'

    TAMAÑO_CAMA = (
        (MATRIMONIAL, 'Matrimonial'),
        (KING_SIZE, 'King Size'),
        (SIMPLE, 'Simple'),
    )
    nombre = models.CharField(max_length=255, blank=True, null=True)
    aire_acondicionado = models.BooleanField(default=False)
    slug = models.SlugField()
    precio = models.PositiveBigIntegerField()
    reservado= models.BooleanField(null=True)
    class Meta:
        indexes = [
            models.Index(fields=['nombre'])
        ]
    def __str__(self):
        return f'Hab. Nº {self.nombre}'

class ImagenHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='RESERVAS/images', validators=[validar_tamaño_imagen])

class Booking(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='bookings')
    habitacion=models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='bookings')
    fecha_inicial=models.DateField(null=True)
    fecha_final=models.DateField(null=True)

class Factura(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, related_name='facturas')
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nit = models.BigIntegerField(blank=True, null=True)
    creado=models.DateField(auto_now_add=True)


