# Generated by Django 4.0.3 on 2022-03-24 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RESERVAS', '0021_remove_cliente_apellido_remove_cliente_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'permissions': [('ver_historial', 'Puede ver historial')]},
        ),
    ]
