# Generated by Django 3.2.3 on 2021-06-29 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaMPRO', '0026_alter_ordendeentrega_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordendecompra',
            name='orden_bodega',
        ),
        migrations.RemoveField(
            model_name='ordendeentrega',
            name='estado',
        ),
        migrations.AddField(
            model_name='ordendecompra',
            name='estado',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]