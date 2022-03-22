from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters
from .models import *

class HabitacionFilter(FilterSet):
    fecha_inicial__gte= filters.DateFilter(field_name='fecha_inicial', lookup_expr='gte')
    fecha_final__lte= filters.DateFilter(field_name='fecha_final', lookup_expr='lte')
    class Meta:
        model= Habitacion
        fields = {
            'precio':['gte','lte'],
            # 'fecha_inicial':['lt'],
            # 'fecha_final':['gt']
        }
    
class ClienteFilter(FilterSet):
    class Meta:
        model=Cliente
        fields='__all__'