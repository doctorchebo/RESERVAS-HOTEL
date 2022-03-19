from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class CuartoResource(resources.ModelResource):
    class Meta:
        model = Cuarto
class CuartoAdmin(ImportExportModelAdmin):
    resource_class=CuartoResource

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
class ClienteAdmin(ImportExportModelAdmin):
    resource_class=ClienteResource

class ReservaResource(resources.ModelResource):
    class Meta:
        model = Reserva
class ReservaAdmin(ImportExportModelAdmin):
    resource_class=ReservaResource

class DiasReservaResource(resources.ModelResource):
    class Meta:
        model = DiasReserva
class DiasReservaAdmin(ImportExportModelAdmin):
    resource_class=DiasReservaResource

class ServicioAdicionalResource(resources.ModelResource):
    class Meta:
        model = ServicioAdicional
class ServicioAdicionalAdmin(ImportExportModelAdmin):
    resource_class=ServicioAdicionalResource

class FacturaResource(resources.ModelResource):
    class Meta:
        model = Factura
class FacturaAdmin(ImportExportModelAdmin):
    resource_class=FacturaResource



admin.site.register(Cuarto, CuartoAdmin)
admin.site.register(Cliente, ClienteAdmin)    
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(DiasReserva, DiasReservaAdmin)
admin.site.register(ServicioAdicional, ServicioAdicionalAdmin)
admin.site.register(Factura, FacturaAdmin)