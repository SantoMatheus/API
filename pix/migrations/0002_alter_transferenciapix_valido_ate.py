# Generated by Django 4.2 on 2024-06-19 12:47

import common_modules.definir_vencimento_cobranca_use_case
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pix', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferenciapix',
            name='valido_ate',
            field=models.DateTimeField(default=common_modules.definir_vencimento_cobranca_use_case.DefinirVencimentoCobrancaUseCase.execute),
        ),
    ]