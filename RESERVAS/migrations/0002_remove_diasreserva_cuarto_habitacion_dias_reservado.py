# Generated by Django 4.0.3 on 2022-03-20 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RESERVAS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diasreserva',
            name='cuarto',
        ),
        migrations.AddField(
            model_name='habitacion',
            name='dias_reservado',
            field=models.ManyToManyField(null=True, to='RESERVAS.diasreserva'),
        ),
    ]
