# Generated by Django 4.2.5 on 2023-09-17 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transit", "0002_driver"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
    ]