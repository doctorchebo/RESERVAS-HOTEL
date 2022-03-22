from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.generics import *
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


from .pagination import DefaultPagination
from .filters import *
from .models import *
from .serializers import *

class ReservaItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method=='POST':
            return CrearReservaItemSerializer
        elif self.request.method=='PATCH':
            print('PUT')
            return ActualizarReservaItemSerializer
        return ReservaItemSerializer
    def get_queryset(self):
        return ReservaItem.objects.filter(reserva_id=self.kwargs['reserva_pk'])
    def get_serializer_context(self):
        return {'reserva_id': self.kwargs['reserva_pk']}
    
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(reserva_id=self.kwargs['reserva_pk'])
        
    def get_serializer_context(self):
        return {'reserva_id':self.kwargs['reserva_pk']}

class ReservasViewSet(ModelViewSet): 
    queryset=Reserva.objects.prefetch_related('items').all()
    serializer_class=ReservaSerializer

class ClientesViewSet(ModelViewSet):
    queryset = Cliente.objects.annotate(reservas_count=Count('reservas')).all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields=['nombre','apellido']
    pagination_class=DefaultPagination

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if Reserva.objects.filter(cliente_id=kwargs['pk']).count()>0:
           return Response({'mensaje':'No se puede borrar porque el cliente tiene reservas'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        return super().destroy(request, *args, **kwargs)

class HabitacionesViewSet(ModelViewSet):
    serializer_class=HabitacionSerializer
    filter_backends=[DjangoFilterBackend, OrderingFilter]
    filterset_class=HabitacionFilter
    pagination_class=DefaultPagination
    ordering_fields=['precio']

    def get_queryset(self):
        queryset=Habitacion.objects.all()
        bloque_id = self.request.query_params.get('bloque_id')
        if bloque_id is not None:
            queryset = queryset.filter(bloque_id=bloque_id) 
        return queryset

    def get_serializer_context(self):
        return {'request':self.request}
    # def destroy(self, request, *args, **kwargs):
    #     if Habitacion.objects.filter(pk=kwargs['pk'], dias_reservado__gt=0).count()>0:
    #         return Response({'mensaje':'No se puede borrar porque la Habitacion está reservada'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().destroy(request, *args, **kwargs)

class FacturasViewSet(ModelViewSet):
    queryset=Factura.objects.all()
    def get_serializer_class(self):
        if self.request.method=='POST':
            return CrearFacturaSerializer
        else:
            return FacturaSerializer
    def get_serializer_context(self):
        return {'request':self.request}





    