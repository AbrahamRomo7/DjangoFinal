# Generated by Django 5.0.6 on 2024-06-14 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partidos',
            name='barcelona_total',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='partidos',
            name='fecha',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='partidos',
            name='ganador',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='partidos',
            name='madrid_total',
            field=models.IntegerField(blank=True),
        ),
    ]
