from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers 
from . import views

router=routers.DefaultRouter()
router.register('reservas',views.ReservasViewSet, basename='reservas')
router.register('habitaciones',views.HabitacionesViewSet, basename='habitaciones'), 
router.register('clientes',views.ClientesViewSet)
router.register('facturas', views.FacturasViewSet)

reserva_router=routers.NestedDefaultRouter(router,'reservas', lookup='reserva')
reserva_router.register('items',views.ReservaItemViewSet, basename='item-reserva')

urlpatterns = router.urls + reserva_router.urls
    
