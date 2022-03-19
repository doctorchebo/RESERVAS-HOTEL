from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

class ReservaItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset=Reserva.objects.all()
    def get_serializer_class(self):
        if self.request.method=='GET':
            return ReservaItemSerializer
        elif self.request.method=='PATCH':
            return ReservaItemActualizarSerializer
    def get_serializer_context(self):
        return {'item_id': self.kwargs['pk']}

    def get_queryset(self):
        return ReservaItem.objects.filter(id='item_id')

class ReservasViewSet(ModelViewSet):
    queryset=Reserva.objects.all()
    serializer_class=ReservaSerializer

    def get_serializer_context(self):
        return {'request':self.request}

    def get_serializer_class(self):
        if self.request.method=='GET':
            return ReservaSerializer
        elif self.request.method=='POST':
            return ReservaSerializer
        elif self.request.method=='PATCH':
            return ReservaActualizarSerializer

class ClientesViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if Reserva.objects.filter(cliente_id=kwargs['pk']).count()>0:
           return Response({'mensaje':'No se puede borrar porque el cliente tiene reservas'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        return super().destroy(request, *args, **kwargs)

class HabitacionesViewSet(ModelViewSet):
    queryset=Cuarto.objects.all()
    serializer_class=CuartoSerializer
    def get_serializer_context(self):
        return {'request':self.request}
    def destroy(self, request, *args, **kwargs):
        if Cuarto.objects.filter(pk=kwargs['pk'], dias_reservado__gt=0).count()>0:
            return Response({'mensaje':'No se puede borrar porque el cuarto está reservado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class FacturasViewSet(ModelViewSet):
    queryset=Factura.objects.all()
    serializer_class=FacturaSerializer
    def get_serializer_context(self):
        return {'request':self.request}





    