from django.contrib import admin
from .models import Reservation, ReservationFlight, ReservationPassenger, PaymentTransaction

admin.site.register(Reservation)
admin.site.register(ReservationFlight)
admin.site.register(ReservationPassenger)
admin.site.register(PaymentTransaction)