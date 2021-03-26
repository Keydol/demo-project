from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.


class AircraftsData(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = JSONField()
    range = models.IntegerField()

    def __str__(self):
        return f"{self.aircraft_code}"

    class Meta:
        managed = False
        db_table = 'aircrafts_data'


class AirportsData(models.Model):
    airport_code = models.CharField(primary_key=True, max_length=3)
    airport_name = JSONField()
    city = JSONField()
    coordinates = models.TextField()  # This field type is a guess.
    timezone = models.TextField()

    def __str__(self):
        return f"{self.airport_code}: {self.airport_name['ru']}"

    class Meta:
        managed = False
        db_table = 'airports_data'


class BoardingPasses(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    ticket_no = models.ForeignKey('TicketFlights', models.DO_NOTHING, db_column='ticket_no')
    flight_id = models.IntegerField()
    boarding_no = models.IntegerField()
    seat_no = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)
        default_related_name = 'boarding_passes'


class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book_ref}"

    class Meta:
        managed = False
        db_table = 'bookings'


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(AirportsData,
                                          models.DO_NOTHING,
                                          db_column='departure_airport',
                                          related_name='get_flights')
    arrival_airport = models.ForeignKey(AirportsData,
                                        models.DO_NOTHING,
                                        db_column='arrival_airport')
    status = models.CharField(max_length=20)
    aircraft_code = models.ForeignKey(AircraftsData,
                                      models.DO_NOTHING,
                                      db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.flight_id} : {self.flight_no}"

    class Meta:
        managed = False
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)
        default_related_name = 'flights'


class Seats(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    aircraft_code = models.ForeignKey(AircraftsData, models.DO_NOTHING, db_column='aircraft_code')
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)
        default_related_name = 'seats'


class TicketFlights(models.Model):
    ticket_no = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticket_no', primary_key=True)
    flight = models.ForeignKey(Flights, models.DO_NOTHING)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ticket_no}"

    class Meta:
        managed = False
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight'),)
        default_related_name = 'ticket_flights'


class Ticket(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey(Bookings, models.DO_NOTHING, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.ticket_no}"

    class Meta:
        managed = False
        db_table = 'tickets'
        default_related_name = 'tickets'
