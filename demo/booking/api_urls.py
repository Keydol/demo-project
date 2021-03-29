from rest_framework import routers

from .viewsets import (
    AircraftDataViewSet,
    AirportDataViewSet,
    BoardingPassViewSet,
    BookingVewSet,
    FlightViewSet,
    SeatViewSet,
    TicketFlightViewSet,
    TicketViewSet
)

router = routers.DefaultRouter()
router.register(r'aircrafts-data', AircraftDataViewSet, basename='aircrafts-data')
router.register(r'airports-data', AirportDataViewSet, basename='airports-data')
router.register(r'boarding-passes', BoardingPassViewSet, basename='boarding-passes')
booking_router = router.register(r'bookings', BookingVewSet, basename='bookings')
router.register(r'flights', FlightViewSet, basename='flights')
router.register(r'seats', SeatViewSet, basename='seats')
router.register(r'tickets-flight', TicketFlightViewSet, basename='tickets-flight')
router.register(r'tickets', TicketViewSet, basename='tickets')
# booking_router.register(r'booking-tickets', TicketViewSet, basename='booking-tickets', parents_query_lookups['book_ref'])

urlpatterns = router.urls
