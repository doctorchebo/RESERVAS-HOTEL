# Generated by Django 4.0.3 on 2022-03-24 22:00

import RESERVAS.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RESERVAS', '0023_imagenhabitacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenhabitacion',
            name='habitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='RESERVAS.habitacion'),
        ),
        migrations.AlterField(
            model_name='imagenhabitacion',
            name='imagen',
            field=models.ImageField(upload_to='RESERVAS/images', validators=[RESERVAS.validators.validar_tamaño_imagen]),
        ),
    ]
