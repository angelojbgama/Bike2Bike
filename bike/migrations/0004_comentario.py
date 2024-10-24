# Generated by Django 5.1.2 on 2024-10-21 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0003_alter_lugar_tipo'),
    ]

    operations = [
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
