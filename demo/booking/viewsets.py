from rest_framework.viewsets import ModelViewSet
from .serializers import (
    AircraftDataSerializer,
    AirportDataSerializer,
    BoardingPassSerializer,
    BookingSerializer,
    FlightSerializer,
    SeatSerializer,
    TicketFlightSerializer,
    TicketSerializer
)
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

from .tasks import send_change_flight_date

from .paginations import (
    BasePagination,
)


class AircraftDataViewSet(ModelViewSet):
    serializer_class = AircraftDataSerializer
    queryset = AircraftData.objects.all()


class AirportDataViewSet(ModelViewSet):
    serializer_class = AirportDataSerializer
    queryset = AirportData.objects.all()


class BoardingPassViewSet(ModelViewSet):
    serializer_class = BoardingPassSerializer
    queryset = BoardingPass.objects.all()
    pagination_class = BasePagination


class BookingVewSet(ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    pagination_class = BasePagination


class FlightViewSet(ModelViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    pagination_class = BasePagination

    def perform_update(self, serializer):
        flight_id = str(self.request).split('/')[-2]
        flight = Flight.objects.get(flight_id=flight_id)
        old_departure_date = flight.scheduled_departure
        old_arrival_date = flight.scheduled_arrival
        instance = serializer.save()
        send_change_flight_date(old_departure_date, old_arrival_date, instance.flight_id)


class SeatViewSet(ModelViewSet):
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()
    pagination_class = BasePagination


class TicketFlightViewSet(ModelViewSet):
    serializer_class = TicketFlightSerializer
    queryset = TicketFlight.objects.all()
    pagination_class = BasePagination


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    pagination_class = BasePagination
