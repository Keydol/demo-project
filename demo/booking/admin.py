from django.contrib import admin
from django.db.models import Count

from .models import (
    AircraftsData,
    AirportsData,
    BoardingPasses,
    Bookings,
    Flights,
    Seats,
    TicketFlights,
    Ticket
)


class TicketsInline(admin.TabularInline):
    model = Ticket
    extra = 1


class SeatsInline(admin.TabularInline):
    model = Seats
    extra = 1


class AircraftsDataInline(admin.TabularInline):
    model = AircraftsData
    extra = 1


@admin.register(AircraftsData)
class AircraftsDataAdmin(admin.ModelAdmin):
    # fields = (('model', 'range'), 'aircraft_code')
    list_display = ('aircraft_code', 'view_model', 'range')
    ordering = ['range', 'aircraft_code']
    list_filter = ['range']
    #inlines = admin.ModelAdmin.inlines + [SeatsInline]

    def view_model(self, obj):
        return obj.model['en']


@admin.register(AirportsData)
class AirportsDataAdmin(admin.ModelAdmin):
    list_display = ('airport_code', 'view_airport_name', 'view_city', 'coordinates', 'timezone')
    ordering = ['airport_code', 'timezone']
    list_filter = ['timezone']

    def view_city(self, obj):
        return obj.city['en']

    def view_airport_name(self, obj):
        return obj.airport_name['en']


@admin.register(BoardingPasses)
class BoardingPassesAdmin(admin.ModelAdmin):
    #fields = ('ticket_no', 'flight_id', 'boarding_no', 'seat_no')
    raw_id_fields = ('ticket_no', )
    fields = ('ticket_no', 'boarding_no', 'seat_no')
    list_display = ('ticket_no', 'flight_id', 'boarding_no', 'seat_no')
    #ordering = ['ticket_no', 'flight_id']


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
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


@admin.register(Flights)
class FlightsAdmin(admin.ModelAdmin):
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




@admin.register(Seats)
class SeatsAdmin(admin.ModelAdmin):
    fields = ('id', 'aircraft_code', 'seat_no', 'fare_conditions')
    list_display = ('aircraft_code', 'seat_no', 'fare_conditions')
    ordering = ['aircraft_code', 'seat_no']
    list_filter = ['aircraft_code', 'seat_no']


@admin.register(TicketFlights)
class TicketFlightsAdmin(admin.ModelAdmin):
    raw_id_fields = ('ticket_no', 'flight')
    list_display = ('ticket_no', 'flight', 'fare_conditions', 'amount')
    ordering = ['ticket_no', 'amount']
    search_fields = ['ticket_no__ticket_no']


@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    raw_id_fields = ('book_ref', )
    fields = ('book_ref', 'ticket_no', ('passenger_id', 'passenger_name'), 'contact_data')

    list_display = ('ticket_no', 'book_ref', 'passenger_id', 'passenger_name')
    search_fields = ['passenger_name', 'ticket_no', 'passenger_id']
