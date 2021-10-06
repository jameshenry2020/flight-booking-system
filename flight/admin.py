from django.contrib import admin
from .models import Airport, Flight,DayofFlight, FlightClass,AirlineBooking,Passenger, Payment

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(DayofFlight)
admin.site.register(FlightClass)
admin.site.register(AirlineBooking)
admin.site.register(Passenger)
admin.site.register(Payment)
