# Generated by Django 5.0.6 on 2024-06-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0005_predicciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='predicciones',
            name='suma',
            field=models.IntegerField(default=0),
        ),
    ]
