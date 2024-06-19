# Generated by Django 4.2 on 2024-06-18 13:57

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContaCorrente',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=55)),
                ('cpf', models.CharField(max_length=11)),
                ('saldo', models.FloatField(db_column='SALDO', default=0)),
                ('agencia', models.CharField(max_length=6)),
                ('num_conta', models.CharField(max_length=6)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('valor', models.FloatField()),
                ('conta_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_destino', to='conta.contacorrente')),
                ('conta_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_origem', to='conta.contacorrente')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Saque',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('valor', models.FloatField()),
                ('conta_corrente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_corrente_saque', to='conta.contacorrente')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('valor', models.FloatField()),
                ('conta_corrente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_corrente_deposito', to='conta.contacorrente')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
