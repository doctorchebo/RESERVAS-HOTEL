from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from rest_framework_nested import routers
from . import views

router=DefaultRouter()
router.register('reservas',views.ReservasViewSet, basename='reservas')
router.register('habitaciones',views.HabitacionesViewSet)
router.register('clientes',views.ClientesViewSet)
router.register('facturas', views.FacturasViewSet)

reservas_router = routers.NestedDefaultRouter(router, 'reservas', lookup='reserva')
reservas_router.register('items', views.ReservaItemViewSet, basename='reserva-items')

urlpatterns = router.urls + reservas_router.urls
    
