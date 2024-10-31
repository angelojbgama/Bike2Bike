# Generated by Django 5.1.2 on 2024-10-24 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0011_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_fim',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_inicio',
            field=models.DateField(),
        ),
    ]