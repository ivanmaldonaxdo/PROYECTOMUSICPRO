# Generated by Django 3.2.3 on 2021-05-27 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaMPRO', '0010_estrategiadeventa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estrategiadeventa',
            old_name='fecha_creacion',
            new_name='fecha_creacion_modificacion',
        ),
        migrations.RemoveField(
            model_name='estrategiadeventa',
            name='fecha_publicacion',
        ),
    ]
