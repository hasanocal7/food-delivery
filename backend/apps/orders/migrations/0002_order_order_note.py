# Generated by Django 5.0.4 on 2024-04-29 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_note",
            field=models.TextField(blank=True, null=True),
        ),
    ]