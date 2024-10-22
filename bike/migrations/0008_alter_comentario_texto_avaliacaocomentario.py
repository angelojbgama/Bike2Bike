# Generated by Django 5.1.2 on 2024-10-22 18:24

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0007_alter_comentario_texto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AvaliacaoComentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estrelas', models.PositiveSmallIntegerField(help_text='Avaliação de 1 a 5 estrelas', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='bike.comentario')),
            ],
        ),
    ]
