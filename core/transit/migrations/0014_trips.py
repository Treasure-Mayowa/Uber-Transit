# Generated by Django 4.2.2 on 2023-09-20 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transit', '0013_alter_user_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transit.driver')),
                ('passengers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transit.location')),
            ],
        ),
    ]
