# Generated by Django 3.1.7 on 2021-10-03 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flight', '0002_auto_20210706_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('gender', models.CharField(choices=[('male', 'M'), ('female', 'F')], max_length=6)),
                ('age', models.IntegerField()),
                ('next_of_kin', models.CharField(max_length=200)),
                ('kins_mobile', models.CharField(max_length=15)),
                ('ticket_no', models.CharField(blank=True, max_length=7, null=True)),
                ('seat_number', models.IntegerField()),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flightclass')),
            ],
        ),
        migrations.CreateModel(
            name='AirlineBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_booked', models.BooleanField(default=False)),
                ('flight_status', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flightclass')),
                ('passengers', models.ManyToManyField(to='flight.Passenger')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
