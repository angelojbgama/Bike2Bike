# Generated by Django 5.1.2 on 2024-10-24 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0009_alter_comentario_estrelas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='estrelas',
        ),
        migrations.DeleteModel(
            name='AvaliacaoComentario',
        ),
    ]
