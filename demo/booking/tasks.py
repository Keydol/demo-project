# Create your tasks here
import time

from celery import shared_task
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


@shared_task
def create_new_airport_data(airport_code):
    airport_name = {
        "en": "test Yakutsk",
        "ru": "test Якутск"
    }
    city = {
        "en": "test Yakutsk",
        "ru": "test Якутск"
    }
    coordinates = (129.77099609375, 62.093299865722656)
    timezone = 'test timezone'
    new_object = AirportData.objects.create(airport_code=airport_code,
                                            airport_name=airport_name,
                                            city=city,
                                            coordinates=coordinates,
                                            timezone=timezone)
    return new_object


@shared_task
def count_booking():
    time.sleep(10)
    return Booking.objects.count()
