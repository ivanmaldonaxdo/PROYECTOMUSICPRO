# Generated by Django 3.2.3 on 2021-06-28 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaMPRO', '0020_ordendecompra_aceptada'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendecompra',
            name='despachada',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.CreateModel(
            name='OrdenDeEntrega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(blank=True, max_length=200)),
                ('ciudad', models.CharField(blank=True, max_length=200)),
                ('pais', models.CharField(blank=True, max_length=200)),
                ('fecha_de_entrega', models.DateTimeField()),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TiendaMPRO.ordendecompra')),
            ],
        ),
    ]