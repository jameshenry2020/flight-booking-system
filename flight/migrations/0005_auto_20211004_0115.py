# Generated by Django 3.1.7 on 2021-10-04 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0004_auto_20211004_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='ticket_no',
            field=models.CharField(blank=True, max_length=7),
        ),
    ]