# Generated by Django 5.1.7 on 2025-03-14 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0002_transaction_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="category",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
