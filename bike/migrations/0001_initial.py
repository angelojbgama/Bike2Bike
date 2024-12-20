# Generated by Django 5.1.2 on 2024-11-04 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='eventos/')),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('responsavel', models.CharField(max_length=100)),
                ('contato', models.CharField(help_text='Email ou Telefone', max_length=100)),
                ('curtidas', models.PositiveIntegerField(default=0)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('tipo', models.CharField(choices=[('parque', 'Parque público'), ('museu', 'Museu ou galeria de arte'), ('restaurante', 'Restaurante ou café'), ('hotel', 'Hotel ou hospedagem'), ('mercado', 'Supermercado ou feira'), ('bike_reparo', 'Reparo de bicicleta')], default='parque', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='bike.lugar')),
            ],
        ),
    ]
