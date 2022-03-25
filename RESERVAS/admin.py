from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .models import *

class ImagenHabitacionInline(admin.TabularInline):
    model=ImagenHabitacion
    readonly_fields=['thumbnail']
    extra=0

    def thumbnail(self, instance):
        if instance.imagen.name != '':
            return format_html(f'<img src="{instance.imagen.url}" class="thumbnail"/>')
        return ''

class HabitacionResource(resources.ModelResource):
    class Meta:
        model=Habitacion

@admin.register(Habitacion)
class HabitacionAdmin(ImportExportModelAdmin):
    resource_class = HabitacionResource
    inlines = [ImagenHabitacionInline]
    class Media:
        css = {
            'all':['RESERVAS/style.css']
        }

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
class ClienteAdmin(ImportExportModelAdmin):
    resource_class=ClienteResource

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0

class ReservaResource(resources.ModelResource):
    class Meta:
        model = Reserva

@admin.register(Reserva)
class ReservaAdmin(ImportExportModelAdmin):
    inlines=[BookingInline]
    resource_class=ReservaResource

class FacturaResource(resources.ModelResource):
    class Meta:
        model = Factura
class FacturaAdmin(ImportExportModelAdmin):
    resource_class=FacturaResource


admin.site.register(Cliente, ClienteAdmin)    
admin.site.register(Factura, FacturaAdmin)
