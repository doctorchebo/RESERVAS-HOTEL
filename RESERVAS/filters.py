from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters
from .models import *

class HabitacionFilter(FilterSet):
    class Meta:
        model= Habitacion
        fields = {
            'precio':['gte','lte'],
            'dias_reservado':['lt','gt']
        }
        
class ClienteFilter(FilterSet):
    class Meta:
        model=Cliente
        fields='__all__'