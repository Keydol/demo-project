# Generated by Django 3.1.7 on 2021-03-26 11:47

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AircraftsData',
            fields=[
                ('aircraft_code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('model', django.contrib.postgres.fields.jsonb.JSONField()),
                ('range', models.IntegerField()),
            ],
            options={
                'db_table': 'aircrafts_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AirportsData',
            fields=[
                ('airport_code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('airport_name', django.contrib.postgres.fields.jsonb.JSONField()),
                ('city', django.contrib.postgres.fields.jsonb.JSONField()),
                ('coordinates', models.TextField()),
                ('timezone', models.TextField()),
            ],
            options={
                'db_table': 'airports_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('book_ref', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('book_date', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'bookings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_no', models.CharField(max_length=6)),
                ('scheduled_departure', models.DateTimeField()),
                ('scheduled_arrival', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('actual_departure', models.DateTimeField(blank=True, null=True)),
                ('actual_arrival', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'flights',
                'managed': False,
                'default_related_name': 'flights',
            },
        ),
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('seat_no', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('fare_conditions', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'seats',
                'managed': False,
                'default_related_name': 'seats',
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('ticket_no', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('passenger_id', models.CharField(max_length=20)),
                ('passenger_name', models.TextField()),
                ('contact_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tickets',
                'managed': False,
                'default_related_name': 'tickets',
            },
        ),
        migrations.CreateModel(
            name='TicketFlights',
            fields=[
                ('ticket_no', models.OneToOneField(db_column='ticket_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='ticket_flights', serialize=False, to='booking.tickets')),
                ('fare_conditions', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'ticket_flights',
                'managed': False,
                'default_related_name': 'ticket_flights',
            },
        ),
        migrations.CreateModel(
            name='BoardingPasses',
            fields=[
                ('ticket_no', models.OneToOneField(db_column='ticket_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='flights', serialize=False, to='booking.ticketflights')),
                ('flight_id', models.IntegerField()),
                ('boarding_no', models.IntegerField()),
                ('seat_no', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'boarding_passes',
                'managed': False,
                'default_related_name': 'flights',
            },
        ),
    ]