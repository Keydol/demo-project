from celery import shared_task
from django.db.models import F, Value, Sum
from demo import settings
from demo.celery import app
from django.core.mail import send_mail
import requests
from datetime import datetime, timedelta
from django.core import exceptions
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


@app.task
def send_change_flight_date(old_departure_date, old_arrival_date, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    message = '*CHANGED DATE*\n\n' \
              f'*Old departure date*: {old_departure_date}\n' \
              f'*New departure date*: {flight.scheduled_departure}\n\n' \
              f'*Old arrival date*: {old_arrival_date}\n' \
              f'*New arrival date*: {flight.scheduled_arrival}\n\n' \
              f'*Id*: {flight.flight_id}\n' \
              f'*No*: {flight.flight_no}\n' \
              f'*Departure airport*: {flight.departure_airport}\n' \
              f'*Arrival airport*: {flight.arrival_airport}'
    requests.get(f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage?chat_id=461238992&parse_mode=MARKDOWN&text={message}")


app.conf.beat_schedule = {
    'chek': {
        'task': 'booking.tasks.chek_impend_flights',
        'schedule': 10.0,
    },
}
app.conf.timezone = 'UTC'


@app.task
def chek_impend_flights():
    flights = Flight.objects.filter(scheduled_departure__range=[datetime.now() + timedelta(hours=3),
                                                                datetime.now() +
                                                                timedelta(minutes=10) +
                                                                timedelta(hours=3)])

    message = 'Рейси на найближчі 10 хвилин:\n\n'

    for flight in flights:
        message += f"*id*: {flight.flight_id}\n" \
                   f"*Маршрут*: {flight.departure_airport} - {flight.arrival_airport}\n" \
                   f"*Час відправлення*: {flight.scheduled_departure}\n" \
                   f"*Час прибуття*: {flight.scheduled_arrival}\n" \
                   f"----------\n\n"

    requests.get(f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage?chat_id=461238992&parse_mode=MARKDOWN&text={message}")


@app.task
def update_bookings_amount(percent):
    Booking.objects.all().update(total_amount=F('total_amount') + F('total_amount') * Value(100 / percent))


@app.task
def send_ticket_info(ticket_no):
    try:
        result = Ticket.objects.get(ticket_no=ticket_no)
        message = f"TICKET DETAIL\n" \
                  f"Ticket no: {result.ticket_no}\n" \
                  f"Book ref: {result.book_ref.book_ref}\n" \
                  f"Book date: {result.book_ref.book_date}\n" \
                  f"Passenger id: {result.passenger_id}\n" \
                  f"Passenger_name: {result.passenger_name}\n" \
                  f"\nCONTACT DATA\n" \
                  f"Phone: {result.contact_data['phone']}"
        send_mail(
            subject='Ticket',
            message=message,
            from_email='arsentest1mail@gmail.com',
            recipient_list=['stockiiarsen@gmail.com'],
            fail_silently=False
        )
    except exceptions.ObjectDoesNotExist:
        send_mail(
            subject='Ticket Error',
            message=f"Ticket {ticket_no} not found",
            from_email='arsentest1mail@gmail.com',
            recipient_list=['stockiiarsen@gmail.com'],
            fail_silently=False
        )


@app.task
def send_amount_data_to_telegram(chat_id):
    # chat_id = 461238992
    message = 'Amount:\n' \
              f'*AircraftsData*: {AircraftData.objects.count()}\n' \
              f'*AirportsData*: {AirportData.objects.count()}\n' \
              f'*BoardingPasses*: {BoardingPass.objects.count()}\n' \
              f'*Bookings*: {Booking.objects.count()}\n' \
              f'*Flights*: {Flight.objects.count()}\n' \
              f'*Seats*: {Seat.objects.count()}\n' \
              f'*TicketFlights*: {TicketFlight.objects.count()}\n' \
              f'*Tickets*: {Ticket.objects.count()}\n'

    requests.get(f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage?chat_id={chat_id}&parse_mode=MARKDOWN&text={message}")


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
