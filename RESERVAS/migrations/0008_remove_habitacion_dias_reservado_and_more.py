# Generated by Django 4.0.3 on 2022-03-21 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RESERVAS', '0007_remove_reservaitem_precio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitacion',
            name='dias_reservado',
        ),
        migrations.AlterField(
            model_name='reservaitem',
            name='reserva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='RESERVAS.reserva'),
        ),
        migrations.DeleteModel(
            name='DiasReserva',
        ),
    ]
