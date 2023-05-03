# Generated by Django 4.2 on 2023-04-29 00:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0003_boleto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleto',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='boleto',
            name='num_conta',
            field=models.CharField(max_length=6),
        ),
    ]