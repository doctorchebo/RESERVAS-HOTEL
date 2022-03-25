from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers

from RESERVAS.models import ImagenHabitacion
from RESERVAS.serializers import ImagenHabitacionSerializer 
from . import views

router=routers.DefaultRouter()
router.register('reservas',views.ReservasViewSet, basename='reservas')
router.register('habitaciones',views.HabitacionesViewSet, basename='habitaciones'), 
router.register('clientes',views.ClientesViewSet)
router.register('facturas', views.FacturasViewSet)

booking_router=routers.NestedDefaultRouter(router,'reservas', lookup='reserva')
booking_router.register('bookings',views.BookingViewSet, basename='booking-reserva')

imagen_habitacion_router=routers.NestedDefaultRouter(router,'habitaciones', lookup='habitacion')
imagen_habitacion_router.register('imagenes',views.ImagenHabitacionViewSet, basename='imagen-habitacion')

urlpatterns = router.urls + booking_router.urls + imagen_habitacion_router.urls
    
