# Generated by Django 4.2 on 2024-06-19 12:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('boleto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamentoboleto',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]