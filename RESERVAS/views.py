from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from rest_framework.generics import *
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework import status
from rest_framework.decorators import action
from datetime import datetime, date, timedelta

from .permissions import IsAdminOrReadOnly, FullDjangoPermission, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
from .filters import *
from .models import *
from .serializers import *

class ReservasViewSet(ModelViewSet):
    permission_classes = [FullDjangoPermission]
    queryset=Reserva.objects.prefetch_related('bookings').all()

    def get_serializer_context(self):
        return {'usuario_id':self.request.user.id}
    def get_serializer_class(self):
        if self.request.method=='PUT' or self.request.method=='PATCH': 
            return ReservaActualizarSerializer
        elif self.request.method=='POST':
            return ReservaCrearSerializer
        else:
            return ReservaSerializer
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def mis_reservas(self, request):
        try:
            reservas = Reserva.objects.get(cliente__usuario_id=request.user.id)
            serializer=ReservaSerializer(reservas)
            return Response(serializer.data)
        except:
            return Response({'error':'Usted no tiene ninguna reserva'})

    
class BookingViewSet(ModelViewSet):
    http_method_names=['post','get','patch','delete']
    serializer_class=BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(reserva_id=self.kwargs['reserva_pk'])
    def get_serializer_class(self):
        if self.request.method=='POST':
            return CrearBookingSerializer
        return BookingSerializer
    def get_serializer_context(self):
        return {'reserva_id':self.kwargs['reserva_pk']}

class ClientesViewSet(ModelViewSet):
    queryset = Cliente.objects.annotate(reservas_count=Count('reservas')).all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields=['nombre','apellido']
    pagination_class=DefaultPagination
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if Reserva.objects.filter(cliente_id=kwargs['pk']).count()>0:
           return Response({'mensaje':'No se puede borrar porque el cliente tiene reservas'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def historial(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET','PUT'])    
    def me(self, request):
        (cliente, created) = Cliente.objects.get_or_create(usuario_id=request.user.id)
        if request.method=='GET':
            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=ClienteSerializer(cliente, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
class HabitacionesViewSet(ModelViewSet):
    serializer_class=HabitacionSerializer
    filter_backends=[DjangoFilterBackend, OrderingFilter]
    filterset_class=HabitacionFilter
    pagination_class=DefaultPagination
    ordering_fields=['precio']
    permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        queryset=Habitacion.objects.prefetch_related('imagenes').all()
        bloque_id = self.request.query_params.get('bloque_id')
        fecha_inicial = self.request.query_params.get('fecha_inicial')
        fecha_final = self.request.query_params.get('fecha_final')

        if bloque_id is not None:
            queryset = queryset.filter(bloque_id=bloque_id) 
        elif fecha_inicial is not None or fecha_final is not None:
            fecha_inicial = datetime.strptime(fecha_inicial,'%Y-%m-%d')-timedelta(days=1)
            fecha_final = datetime.strptime(fecha_final,'%Y-%m-%d')+timedelta(days=1)

            queryset = queryset.filter(Q(fecha_inicial__lt=fecha_inicial,fecha_final__lt=fecha_inicial)|Q(fecha_inicial__gt=fecha_final,fecha_final__gt=fecha_final)|Q(fecha_inicial__isnull=True, fecha_final__isnull=True)|Q(fecha_final__lt=fecha_inicial)|Q(fecha_inicial__gt=fecha_final))

        return queryset

    def get_serializer_context(self):
        return {'request':self.request}

class FacturasViewSet(ModelViewSet):
    queryset = Factura.objects.select_related('reserva').all()
    permission_classes=[IsAdminUser]
    def get_serializer_class(self):
        if self.request.method=='POST':
            return CrearFacturaSerializer
        else:
            return FacturaSerializer
    def get_serializer_context(self):
        return {'request':self.request}

class ImagenHabitacionViewSet(ModelViewSet):
    def get_queryset(self):
        return ImagenHabitacion.objects.filter(habitacion_id=self.kwargs['habitacion_pk'])
    def get_serializer_context(self):
        return {'habitacion_id':self.kwargs['habitacion_pk']}
    
    serializer_class=ImagenHabitacionSerializer




    