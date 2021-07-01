# Generated by Django 3.2.3 on 2021-06-30 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaMPRO', '0030_remove_ordendecompra_date_orderd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direcciondeenvio',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='direcciondeenvio',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TiendaMPRO.ordendecompra'),
        ),
        migrations.AlterField(
            model_name='sucursaldeentrega',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TiendaMPRO.sucursal'),
        ),
    ]