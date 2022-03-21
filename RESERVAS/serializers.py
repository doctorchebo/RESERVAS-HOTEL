from django.urls import set_urlconf
from rest_framework import serializers
from .models import *

class DiasReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiasReserva
        fields = ['Habitacion','fecha']

class HabitacionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    dias_reservado=DiasReservaSerializer(many=True, read_only=True)
    class Meta:
        model = Habitacion
        fields = ['id','numero_habitacion','reservado','baño_privado','tamaño_cama','aire_acondicionado','precio','bloque','dias_reservado']
    
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre','apellido','telefono','email','reservas_count']
    reservas_count = serializers.CharField(read_only=True)

class ReservaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cliente = ClienteSerializer()
    class Meta:
        model = Reserva
        fields = ['id','cliente','metodo_pago'] 
    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente')
        cliente = Cliente.objects.create(**cliente_data)
        return Reserva.objects.create(cliente=cliente, **validated_data)      

class ReservaActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reserva
        fields=['estado']

class ReservaItemSerializer(serializers.ModelSerializer):
    Habitacion=HabitacionSerializer()
    precio_total = serializers.SerializerMethodField()

    def obtener_precio_total(self, reserva_item:ReservaItem):
        return reserva_item.dias*reserva_item.Habitacion.precio

    class Meta:
        model=ReservaItem
        fields=['id','reserva','Habitacion','dias','precio_total']

class ReservaItemActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReservaItem
        fields=['dias']

class FacturaSerializer(serializers.ModelSerializer):
    reserva=ReservaSerializer(read_only=True)
    items = ReservaItemSerializer(many=True, read_only=True)
    precio_total=serializers.SerializerMethodField()

    def obtener_precio_total(self, factura):
        return sum([item.dias * item.Habitacion.precio for item in factura.items.all()])

    class Meta:
        model=Factura
        fields=['id','nombre','nit','reserva','items','precio_total']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id', 'reserva', 'descripcion','creado']

    def create(self, validated_data):
        reserva_id=self.context['reserva_id']
        return Review.objects.create(reserva_id=reserva_id, **validated_data)