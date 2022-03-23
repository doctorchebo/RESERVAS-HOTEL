from django.forms import ValidationError
from django.urls import set_urlconf
from rest_framework import serializers
from .models import *
from datetime import timedelta
from django.db.models import Q
from datetime import datetime, timedelta, date

# HABITACION
class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['id','nombre','reservado','precio']
class SimpleHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['id']

# BOOKING

def habitacion_disponible(self, validated_data):
    
    habitacion_id = validated_data['habitacion'].id
    print(validated_data)
    fi = validated_data['fecha_inicial']
    ff = validated_data['fecha_final']

    habitacion = Habitacion.objects.get(pk=habitacion_id)
    bookings = habitacion.bookings.exclude(fecha_inicial__gt=ff).exclude(fecha_final__lt=fi)
    return not bookings.exists()

class BookingSerializer(serializers.ModelSerializer):
    habitacion = HabitacionSerializer(read_only=True)
    dias=serializers.SerializerMethodField()
    def get_dias(self, booking:Booking):
        fi = int(booking.fecha_inicial.strftime("%Y%m%d"))
        ff = int(booking.fecha_final.strftime("%Y%m%d"))
        return ff-fi+1
    precio_total = serializers.SerializerMethodField()
    def get_precio_total(self,booking:Booking):
        fi = int(booking.fecha_inicial.strftime("%Y%m%d"))
        ff = int(booking.fecha_final.strftime("%Y%m%d"))
        dias = ff-fi+1
        return booking.habitacion.precio*dias
    class Meta:
        model=Booking
        fields=['id','habitacion','fecha_inicial','fecha_final','dias','precio_total']

class CrearBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=['habitacion','fecha_inicial','fecha_final']

    def create(self, validated_data):
        fi = validated_data['fecha_inicial']
        ff = validated_data['fecha_final']
        if ff<fi:
            raise serializers.ValidationError ({'error':'La fecha final no puede ser menor a la fecha inicial'})
        
        reserva_id = self.context['reserva_id']
        if habitacion_disponible(self,validated_data):
            return Booking.objects.create(reserva_id=reserva_id, **validated_data)
        else:
            raise serializers.ValidationError({'error':'Habitación no disponible para esas fechas'})
    def update(self, instance, validated_data):
        print(instance)
        fi = validated_data['fecha_inicial']
        ff = validated_data['fecha_final']
        if ff<fi:
            raise serializers.ValidationError ({'error':'La fecha final no puede ser menor a la fecha inicial'})
        if habitacion_disponible(self,validated_data):
            return instance
        else:
            raise serializers.ValidationError({'error':'Habitación no disponible para esas fechas'})

# class ActualizarBookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Booking
#         fields=['habitacion','fecha_inicial','fecha_final']

#     def update(self, instance, validated_data):
#         if habitacion_disponible(self, validated_data):
#             # return Booking.objects.update(**validated_data)
#             return instance
#         else:
#             raise serializers.ValidationError({'error':'Habitación no disponible para esas fechas'})

# CLIENTE
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre','apellido','telefono','email']

# RESERVA
class ReservaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    precio_total = serializers.SerializerMethodField()
    def get_precio_total(self, reserva:Reserva):
        return sum([booking.habitacion.precio*(int(booking.fecha_final.strftime("%Y%m%d"))-int(booking.fecha_inicial.strftime("%Y%m%d"))+1) for booking in reserva.bookings.all()])
    
    class Meta:
        model = Reserva
        fields = ['id','cliente','metodo_pago','estado','precio_total'] 
    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente')
        cliente = Cliente.objects.create(**cliente_data)
        return Reserva.objects.create(cliente=cliente, **validated_data)      

class ReservaActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reserva
        fields=['estado']

class ReservaCrearSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=9999999)
    cliente = ClienteSerializer()
    class Meta:
        model=Reserva
        fields=['id','cliente']
    def create(self, validated_data):
        cliente_data=validated_data.pop('cliente')
        id=validated_data.pop('id')
        try:
            cliente = Cliente.objects.get(pk=id)
        except:
            cliente = Cliente.objects.create(**cliente_data)
        return Reserva.objects.create(cliente=cliente)

# FACTURAS
class FacturaSerializer(serializers.ModelSerializer):
    precio_total=serializers.SerializerMethodField()
    def get_precio_total(self, factura:Factura):
        return sum([booking.habitacion.precio*(int(booking.fecha_final.strftime("%Y%m%d"))-int(booking.fecha_inicial.strftime("%Y%m%d"))+1) for booking in factura.reserva.bookings.all()])
    class Meta:
        model=Factura
        fields=['id','reserva', 'nombre','nit','reserva','precio_total','creado']

class CrearFacturaSerializer(serializers.ModelSerializer):
    precio_total=serializers.SerializerMethodField(read_only=True)
    def get_precio_total(self, factura:Factura):
        return sum([booking.habitacion.precio*(int(booking.fecha_final.strftime("%Y%m%d"))-int(booking.fecha_inicial.strftime("%Y%m%d"))+1) for booking in factura.reserva.bookings.all()])
    class Meta:
        model=Factura
        fields=['reserva','nombre','nit','precio_total']        
    
    def __init__(self, *args, **kwargs):
        super(CrearFacturaSerializer, self).__init__(*args, **kwargs)
        self.fields['reserva'].queryset = Reserva.objects.filter(facturas__isnull=True)

