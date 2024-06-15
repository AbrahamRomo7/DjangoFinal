# Generated by Django 5.0.6 on 2024-06-15 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_estadiogoles'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadioFechaGoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('goles', models.IntegerField()),
                ('estadio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log.estadio')),
            ],
        ),
    ]
