from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import secrets

class Airport(models.Model):
    code=models.CharField(max_length=3)
    city=models.CharField(max_length=60)

    def __str__(self):
        return f"{self.city}({self.code})"



class DayofFlight(models.Model):
    date=models.DateField()    
     
    def __str__(self):
        return f"{self.date}"




class Flight(models.Model):
    flight_no=models.IntegerField()
    origin=models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departure')
    destination=models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrival')
    departure_time=models.TimeField()
    arrival_time=models.TimeField()
    departure_date=models.ForeignKey(DayofFlight, related_name='flight', on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.origin.code} to {self.destination.code}"

class FlightClass(models.Model):
    name=models.CharField(max_length=200)
    class_price=models.DecimalField(max_digits=7, decimal_places=2)
    num_seats=models.IntegerField(blank=True, null=True)
    flight=models.ForeignKey(Flight, related_name='klass', on_delete=models.CASCADE)

    def __str__(self):
        return f"flight-{self.flight.id}-{self.name}-class"

    def get_absolute_url(self):
        return reverse('chosen-flight', kwargs={'pk':self.id})

class AirlineBooking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    flight=models.ForeignKey(FlightClass, on_delete=models.CASCADE)
    is_booked=models.BooleanField(default=False)
    passengers=models.ManyToManyField("Passenger")
    flight_status=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.flight.name} -flight"



GENGER_CHOICE=(
    ("male", "M"),
    ("female", "F")
)
class Passenger(models.Model):
    flight=models.ForeignKey(FlightClass, on_delete=models.CASCADE)
    names=models.CharField(max_length=200)
    address=models.TextField()
    gender=models.CharField(max_length=6, choices=GENGER_CHOICE)
    age=models.IntegerField()
    next_of_kin=models.CharField(max_length=200)
    kins_mobile=models.CharField(max_length=15)
    ticket_no=models.CharField(max_length=7, blank=True)
    seat_number=models.IntegerField(default=1)

    def __str__(self):
        return self.names

    def save(self, *args, **kwargs):
        if self.ticket_no =="":
            self.ticket_no=str(uuid.uuid4()).replace("-","").upper()[:5]
            self.seat_number =self.seat_number + 1
        return super().save(*args, **kwargs)
        
 
    
class Payment(models.Model):
    flight=models.ForeignKey(FlightClass, on_delete=models.DO_NOTHING, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.CharField(max_length=10)
    ref_code=models.CharField(max_length=255)
    verified=models.BooleanField(default=False)
    completed=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-booking"

    def save(self,*args, **kwargs):
        while not self.ref_code:
            ref=secrets.token_urlsafe(50)
            obj_similar=Payment.objects.filter(ref_code=ref)
            if not obj_similar:
                self.ref_code=ref
        return super().save(*args, **kwargs)
        

