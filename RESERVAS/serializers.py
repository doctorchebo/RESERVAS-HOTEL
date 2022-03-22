from django.urls import set_urlconf
from rest_framework import serializers
from .models import *

# class DiasReservaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiasReserva
#         fields = ['Habitacion','fecha']

class HabitacionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Habitacion
        fields = ['id','numero_habitacion','reservado','baño_privado','tamaño_cama','aire_acondicionado','precio','bloque','fecha_inicial','fecha_final']

class SimpleHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Habitacion
        fields=['numero_habitacion','reservado']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre','apellido','telefono','email','reservas_count']
    reservas_count = serializers.CharField(read_only=True)

class ReservaItemSerializer(serializers.ModelSerializer):
    cuarto=HabitacionSerializer()
    precio_total = serializers.SerializerMethodField()

    def get_precio_total(self, reserva_item:ReservaItem):
        return reserva_item.dias*reserva_item.cuarto.precio

    class Meta:
        model=ReservaItem
        fields=['id','cuarto','dias','fecha_inicial', 'fecha_final', 'precio_total']
        
class CrearReservaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReservaItem
        fields=['id','cuarto','dias']
    def create(self, validated_data):
        reserva_id=self.context['reserva_id']
        return ReservaItem.objects.create(reserva_id=reserva_id, **validated_data)

class ActualizarReservaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReservaItem
        fields=['cuarto','dias','fecha_inicial', 'fecha_final']

class SimpleReservaItemSerializer(serializers.ModelSerializer):
    cuarto=SimpleHabitacionSerializer()
    class Meta:
        model=ReservaItem
        fields=['cuarto','dias']        

class ReservaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cliente = ClienteSerializer()
    habs_reservadas = SimpleReservaItemSerializer(source='items', read_only=True, many=True)
    precio_total = serializers.SerializerMethodField()

    def get_precio_total (self, reserva:Reserva):
        return sum(item.cuarto.precio*item.dias for item in reserva.items.all())
    class Meta:
        model = Reserva
        fields = ['id','cliente','metodo_pago','habs_reservadas','precio_total'] 
    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente')
        cliente = Cliente.objects.create(**cliente_data)
        return Reserva.objects.create(cliente=cliente, **validated_data)      


class ReservaActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reserva
        fields=['estado']

class ReservaItemActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReservaItem
        fields=['dias']

class FacturaSerializer(serializers.ModelSerializer):
    items = ReservaItemSerializer(many=True, read_only=True)
    precio_total=serializers.SerializerMethodField()
    def get_precio_total(self, factura:Factura):
        return sum([item.dias*item.cuarto.precio for item in factura.reserva.items.all()])
    class Meta:
        model=Factura
        fields=['id','reserva', 'nombre','nit','reserva','items','precio_total','creado']

class CrearFacturaSerializer(serializers.ModelSerializer):
    precio_total=serializers.SerializerMethodField()
    def get_precio_total(self, factura:Factura):
        return sum([item.dias*item.cuarto.precio for item in factura.reserva.items.all()])
    class Meta:
        model=Factura
        fields=['reserva','nombre','nit','precio_total']        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id', 'reserva', 'descripcion','creado']

    def create(self, validated_data):
        reserva_id=self.context['reserva_id']
        return Review.objects.create(reserva_id=reserva_id, **validated_data)