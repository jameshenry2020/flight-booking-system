# Generated by Django 3.1.7 on 2021-10-05 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0006_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
