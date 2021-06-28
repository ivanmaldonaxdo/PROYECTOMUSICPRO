# Generated by Django 3.2.3 on 2021-06-27 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaMPRO', '0017_auto_20210626_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='direcciondeenvio',
            name='pais',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sucursaldeentrega',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TiendaMPRO.sucursal'),
        ),
    ]
