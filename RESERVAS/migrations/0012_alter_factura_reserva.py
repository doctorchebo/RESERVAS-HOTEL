# Generated by Django 4.0.3 on 2022-03-22 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RESERVAS', '0011_remove_reservaitem_dias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='reserva',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facturas', to='RESERVAS.reserva'),
        ),
    ]
