# Generated by Django 3.2.19 on 2024-06-24 15:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0002_contacorrente_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacorrente',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deposito',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saque',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transferencia',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contacorrente',
            name='status',
            field=models.CharField(choices=[('ativo', 'ativo'), ('cancelado', 'cancelado'), ('bloqueado', 'bloqueado')], default='ativo', max_length=9),
        ),
    ]
