# Generated by Django 4.0.3 on 2022-03-21 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RESERVAS', '0004_alter_habitacion_dias_reservado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitacion',
            name='dias_reservado',
            field=models.ManyToManyField(blank=True, to='RESERVAS.diasreserva'),
        ),
    ]
