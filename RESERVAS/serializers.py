from django.urls import set_urlconf
from rest_framework import serializers
from .models import *

class DiasReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiasReserva
        fields = ['cuarto','fecha']

class CuartoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Cuarto
        fields = ['id','numero_habitacion','baño_privado','tamaño_cama','aire_acondicionado','precio']
    
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre','apellido','telefono','email','reservas']
    
    reservas = serializers.IntegerField(read_only=True)

class ReservaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    cliente = ClienteSerializer(read_only=True)
    class Meta:
        model = Reserva
        fields = ['id','cliente','metodo_pago']

class ReservaActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reserva
        fields=['estado']

class ReservaItemSerializer(serializers.ModelSerializer):
    cuarto=CuartoSerializer()
    precio_total = serializers.SerializerMethodField()

    def obtener_precio_total(self, reserva_item:ReservaItem):
        return reserva_item.dias*reserva_item.cuarto.precio

    class Meta:
        model=ReservaItem
        fields=['id','reserva','cuarto','dias','precio_total']

class ReservaItemActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReservaItem
        fields=['dias']

class FacturaSerializer(serializers.ModelSerializer):
    reserva=ReservaSerializer(read_only=True)
    items = ReservaItemSerializer(many=True, read_only=True)
    precio_total=serializers.SerializerMethodField()

    def obtener_precio_total(self, factura):
        return sum([item.dias * item.cuarto.precio for item in factura.items.all()])

    class Meta:
        model=Factura
        fields=['id','nombre','nit','reserva','items','precio_total']
