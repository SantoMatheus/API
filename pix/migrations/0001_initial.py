# Generated by Django 4.2 on 2024-06-18 13:57

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChavePix',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('valor_chave', models.CharField(max_length=150)),
                ('tipo', models.CharField(choices=[('CELULAR', 'CELULAR'), ('CNPJ', 'CNPJ'), ('CPF', 'CPF'), ('EMAIL', 'EMAIL'), ('EVP', 'EVP')], max_length=50)),
                ('esta_ativa', models.BooleanField(default=True)),
                ('conta_corrente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conta.contacorrente')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransferenciaPix',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('aguardando_pagamento', 'aguardando pagamento'), ('pago', 'pago'), ('cancelado', 'cancelado'), ('vencido', 'vencido'), ('pagamento_devolvido', 'pagamento devolvido')], default='aguardando_pagamento', max_length=20)),
                ('valido_ate', models.DateTimeField(default=None)),
                ('valor', models.FloatField()),
                ('conta_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chave_pix_destino', to='pix.chavepix')),
                ('conta_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_corrente_origem', to='conta.contacorrente')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PagamentoPix',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('cobranca_pix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cobranca_id', to='pix.transferenciapix')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DevolucaoPix',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('valor_a_devolver', models.FloatField()),
                ('pagamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamento_id', to='pix.pagamentopix')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
