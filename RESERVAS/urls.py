from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers 
from . import views

router=routers.DefaultRouter()
router.register('reservas',views.ReservasViewSet, basename='reservas')
router.register('habitaciones',views.HabitacionesViewSet, basename='habitaciones'), 
router.register('clientes',views.ClientesViewSet)
router.register('facturas', views.FacturasViewSet)

booking_router=routers.NestedDefaultRouter(router,'reservas', lookup='reserva')
booking_router.register('bookings',views.BookingViewSet, basename='booking-reserva')

urlpatterns = router.urls + booking_router.urls
    
