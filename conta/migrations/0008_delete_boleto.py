# Generated by Django 4.2 on 2023-05-03 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0007_alter_boleto_conta_corrente'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Boleto',
        ),
    ]
