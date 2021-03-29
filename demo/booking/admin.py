from django.contrib import admin
from django.db.models import Count

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


class TicketsInline(admin.TabularInline):
    model = Ticket
    extra = 1


class SeatsInline(admin.TabularInline):
    model = Seat
    extra = 1


class TicketFlightsInline(admin.TabularInline):
    model = TicketFlight
    extra = 1

    raw_id_fields = ('flight', )


@admin.register(AircraftData)
class AircraftDataAdmin(admin.ModelAdmin):
    # fields = (('model', 'range'), 'aircraft_code')
    list_display = ('aircraft_code', 'view_model', 'range')
    ordering = ['range', 'aircraft_code']
    list_filter = ['range']
    inlines = [SeatsInline]

    def view_model(self, obj):
        return obj.model['en']


@admin.register(AirportData)
class AirportDataAdmin(admin.ModelAdmin):
    list_display = ('airport_code', 'view_airport_name', 'view_city', 'coordinates', 'timezone')
    ordering = ['airport_code', 'timezone']
    list_filter = ['timezone']

    def view_city(self, obj):
        return obj.city['en']

    def view_airport_name(self, obj):
        return obj.airport_name['en']


@admin.register(BoardingPass)
class BoardingPassAdmin(admin.ModelAdmin):
    raw_id_fields = ('id',)
    fields = ('id', 'ticket_no', 'flight_id', 'boarding_no', 'seat_no')
    list_display = ('pk', 'ticket_no', 'flight_id', 'boarding_no')
    search_fields = ('ticket_no', )

    # def get_queryset(self, request):
    #     qs = super(BoardingPassesAdmin, self).get_queryset(request)
    #     print(qs[:10])
    #     return qs
    #    return super().get_queryset(request).distinct('id')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('book_ref', "book_date", "total_amount", 'view_tickets_count')
    ordering = ['-book_date']
    list_filter = ['book_date']
    search_fields = ('book_ref', 'book_date')
    inlines = [TicketsInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(tickets_count=Count('tickets'))

    def view_tickets_count(self, obj):
        return obj.tickets_count


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_id',
                    'flight_no',
                    'scheduled_departure',
                    'scheduled_arrival',
                    'departure_airport',
                    'arrival_airport')
    ordering = ['flight_id']
    list_filter = ['departure_airport',
                   'arrival_airport',
                   'scheduled_departure',
                   'scheduled_arrival']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    fields = ('id', 'aircraft_code', 'seat_no', 'fare_conditions')
    list_display = ('aircraft_code', 'seat_no', 'fare_conditions')
    ordering = ['aircraft_code', 'seat_no']
    list_filter = ['aircraft_code', 'seat_no']


@admin.register(TicketFlight)
class TicketFlightAdmin(admin.ModelAdmin):
    raw_id_fields = ('ticket_no', 'flight')
    list_display = ('ticket_no', 'flight', 'fare_conditions', 'amount')
    ordering = ['ticket_no', 'amount']
    search_fields = ['ticket_no__ticket_no']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    raw_id_fields = ('book_ref', )
    fields = ('book_ref', 'ticket_no', ('passenger_id', 'passenger_name'), 'contact_data')

    list_display = ('ticket_no', 'book_ref', 'passenger_id', 'passenger_name')
    search_fields = ['passenger_name', 'ticket_no', 'passenger_id']

    inlines = [TicketFlightsInline]
