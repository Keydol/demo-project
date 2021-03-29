from rest_framework.serializers import ModelSerializer
from .models import (
    AircraftData,
    AirportData,
    BoardingPass,
    Booking,
    Flight,
    Seat,
    TicketFlight,
    Ticket
)


class SeatsForAircraftDataSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'seat_no', 'fare_conditions', 'aircraft_code')


class BoardingPassForTicketFlightSerializer(ModelSerializer):
    class Meta:
        model = BoardingPass
        fields = ('id', 'ticket_no', 'flight_id', 'boarding_no', 'seat_no')


class AircraftDataSerializer(ModelSerializer):
    seats = SeatsForAircraftDataSerializer(many=True, read_only=True)

    class Meta:
        model = AircraftData
        fields = ('aircraft_code', 'model', 'range', 'seats')


class AirportDataSerializer(ModelSerializer):

    class Meta:
        model = AirportData
        fields = ('airport_code',
                  'airport_name',
                  'city',
                  'coordinates',
                  'timezone')


class TicketFlightSerializer(ModelSerializer):
    boarding_passes = BoardingPassForTicketFlightSerializer(many=True, read_only=True)

    class Meta:
        model = TicketFlight
        fields = ('id', 'fare_conditions', 'amount', 'ticket_no', 'flight', 'boarding_passes')


class BoardingPassSerializer(ModelSerializer):
    id = TicketFlightSerializer(many=False, read_only=True)

    class Meta:
        model = BoardingPass
        fields = ('id', 'ticket_no', 'flight_id', 'boarding_no', 'seat_no')


class TicketSerializer(ModelSerializer):
    ticket_flights = TicketFlightSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ('ticket_no',
                  'passenger_id',
                  'passenger_name',
                  'contact_data',
                  'book_ref',
                  'ticket_flights')


class BookingSerializer(ModelSerializer):

    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ('book_ref', 'book_date', 'total_amount', 'tickets')


class FlightSerializer(ModelSerializer):
    departure_airport = AirportDataSerializer(many=False, read_only=True)
    arrival_airport = AirportDataSerializer(many=False, read_only=True)
    aircraft_code = AircraftDataSerializer(many=False, read_only=True)
    ticket_flights = TicketFlightSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ('flight_id',
                  'flight_no',
                  'scheduled_departure',
                  'scheduled_arrival',
                  'status',
                  'actual_departure',
                  'actual_arrival',
                  'departure_airport',
                  'arrival_airport',
                  'aircraft_code',
                  'ticket_flights')


class SeatSerializer(ModelSerializer):
    aircraft_code = AircraftDataSerializer(many=False, read_only=True)

    class Meta:
        model = Seat
        fields = ('id', 'seat_no', 'fare_conditions', 'aircraft_code')
