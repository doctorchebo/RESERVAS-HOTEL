from django.urls import set_urlconf
from rest_framework import serializers
from .models import *
from datetime import timedelta
from django.db.models import Q
from datetime import datetime, timedelta, date

# HABITACION
class HabitacionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Habitacion
        fields = ['id','numero_habitacion','reservado','baño_privado','tamaño_cama','aire_acondicionado','precio','bloque']

class SimpleHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Habitacion
        fields=['numero_habitacion','reservado']

# CLIENTE
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre','apellido','telefono','email','reservas_count']
    reservas_count = serializers.CharField(read_only=True)

# ITEM RESERVA  


# RESERVA
class ReservaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cliente = ClienteSerializer()
    precio_total = serializers.SerializerMethodField()

    def get_precio_total (self, reserva:Reserva):
        return sum(item.cuarto.precio*item.dias for item in reserva.items.all())
    class Meta:
        model = Reserva
        fields = ['id','cliente','metodo_pago','precio_total','estado'] 
    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente')
        cliente = Cliente.objects.create(**cliente_data)
        return Reserva.objects.create(cliente=cliente, **validated_data)      

class ReservaActualizarSerializer(serializers.ModelSerializer):

    class Meta:
        model=Reserva
        fields=['estado',]

class ReservaCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reserva
        fields=['cliente']

# FACTURAS
class FacturaSerializer(serializers.ModelSerializer):
    precio_total=serializers.SerializerMethodField()
    def get_precio_total(self, factura:Factura):
        return sum([(item.cuarto.fecha_final-item.cuarto.fecha_inicial+timedelta(days=1)).days*item.cuarto.precio for item in factura.reserva.items.all()])
    class Meta:
        model=Factura
        fields=['id','reserva', 'nombre','nit','reserva','precio_total','creado']

class CrearFacturaSerializer(serializers.ModelSerializer):
    precio_total=serializers.SerializerMethodField(read_only=True)
    def get_precio_total(self, factura:Factura):
        return sum([(item.cuarto.fecha_final-item.cuarto.fecha_inicial+timedelta(days=1)).days*item.cuarto.precio for item in factura.reserva.items.all()])
    class Meta:
        model=Factura
        fields=['reserva','nombre','nit','precio_total']        
    
    def __init__(self, *args, **kwargs):
        super(CrearFacturaSerializer, self).__init__(*args, **kwargs)
        self.fields['reserva'] = serializers.ChoiceField(choices=Reserva.objects.filter(facturas__isnull=True))

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=['reserva','fecha_inicial','fecha_final']