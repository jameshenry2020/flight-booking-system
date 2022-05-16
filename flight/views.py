from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from .models  import AirlineBooking, Airport, Flight, FlightClass, Passenger, Payment
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AddPassengerForm, UserRegisterForm
from django.forms import formset_factory
from django.conf import settings
from .paystack import PayStack
from django.contrib import messages


# Create your views here.
class FlightSearchPage(View):
    def get(self, request, *args, **kwargs):
        context={}
        airports=Airport.objects.all()
        context['airports']=airports
        return render(request, 'flight/index.html', context)
    

class DestinationChoices(View):
    def get_destination(self, flight): 
        return flight.destination

    def get(self, request):
        select_origin=request.GET.get('flight_origin')
        flights=Flight.objects.filter(origin__code__icontains=select_origin)
        destinations=list(set(map(self.get_destination, flights)))      
        context={
            'destination':destinations
        }
        return render(request, 'flight/destination.html',context)


class SearchFlight(View):
    def get(self, request, *args, **kwargs):
        origin=request.GET.get('origin')
        destination=request.GET.get('destination')
        date=request.GET.get('departure')
        adults=request.GET.get('adult')
        children=request.GET.get('children')
        if origin is not None and destination is not None:
            queryset=Flight.objects.filter(Q(origin__code__iexact=origin),  Q(destination__code__iexact=destination))
        if date is not None:
            queryset.filter(departure_date__date=date)
            # store passenager info in session
            request.session['num_adults']=adults
            request.session['num_children']=children
        context={
        'search_queries':queryset
        }
        return render(request, "flight/search.html", context)

class SelectedFlight(View):
    def get(self, request, *args, **kwargs):
       f_klass=FlightClass.objects.get(id=self.kwargs['pk'])
       price=f_klass.class_price
       adult_n=request.session.get('num_adults')
       children_n=request.session.get('num_children')
    
       num_passanger=int(adult_n) + int(children_n)
       adult_total=int(adult_n) * price
       children_total=int(children_n) * price
       total_price=num_passanger * price
       context={
           'total_cost_price':total_price,
           "num_adults":int(adult_n),
           "num_children":int(children_n),
           "flight_info":f_klass, 
           "children_total_price":children_total,
           "adult_total_price":adult_total
       }

       return render(request, "flight/detail.html", context)



def AddPassenger(request, flight_id):
        context={}
        adult_n=request.session.get('num_adults')
        children_n=request.session.get('num_children')
        num_of_passenger=int(adult_n) + int(children_n)
        context['num_passenger']=num_of_passenger
        flight=FlightClass.objects.get(id=flight_id)
        if num_of_passenger > 1:
            Passengerformsets=formset_factory(AddPassengerForm, extra=num_of_passenger)
            context['passengerformsets']=Passengerformsets
            get_booking=AirlineBooking.objects.get(user=request.user, is_booked=False)
            if request.method =="POST":
                p_forms=Passengerformsets(request.POST) 
                if (p_forms.is_valid()):
                    for f in p_forms:
                        instances=f.save(commit=False)
                        instances.flight=flight
                        instances.save()   
                        get_booking.passengers.add(instances)
                    return redirect('payment', flight_id=flight.id)
            return render(request, "flight/passenger.html", context)    
        else:
            form = AddPassengerForm()
            get_booking=AirlineBooking.objects.get(user=request.user, is_booked=False)
            if request.method =="POST":
                form=AddPassengerForm(request.POST) 
                if form.is_valid():  
                    instances=form.save(commit=False)
                    instances.flight=flight
                    instances.save()   
                    get_booking.passengers.add(instances)
                    return redirect('payment', flight_id=flight.id)
            context['form']=form
            context['flight_info']=flight

            # return render(request, "flight/passenger.html", context)    
        return render(request, "flight/passenger.html", context)
        

class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        flight=FlightClass.objects.get(id=self.kwargs['flight_id'])
        price=flight.class_price
        adult_n=request.session.get('num_adults')
        children_n=request.session.get('num_children')
        num_passanger=int(adult_n) + int(children_n) 
        amount=num_passanger * price
        payment, created=Payment.objects.get_or_create(user=request.user, amount=amount)
        print('payment ref: ', payment.ref_code )
        context={
            'amt':amount,
            'amount':amount * 100,
            'ref':payment.ref_code,
            'num_adults':adult_n,
            'num_children':children_n,
            'paystack_public_key':settings.PAYSTACK_API_PUBLIC_KEY
        }
        return render(request, "flight/payment.html" , context)


@login_required
def payment_verification(request, ref):
    payment=get_object_or_404(Payment, ref_code=ref)
    flight_booking=get_object_or_404(AirlineBooking, user=request.user, is_booked=False)
    paystack=PayStack()
    status, result=paystack.verify_payment(ref)
    if status:
        payment.verified=True
        payment.completed=True
        payment.save()
        flight_booking.is_booked=True
        flight_booking.save()
        messages.success(request, 'payment completed successfully')
        return redirect('dashboard', user_id=request.user.id)
    messages.warning(request, 'payment failed')
    return redirect('payment', flight_id=flight_booking.flight.id)
    
@login_required
def check_flight(request):   
    q1=request.GET.get('ref', None)
    q2=request.GET.get('flight_id',None)
    if q1 is not None and q2 is not None:
        lookups=Q(ref_code__iexact=q1) & Q(flight__flight__flight_no=q2)
        queryset=Payment.objects.filter(lookups)
        fg=queryset[0].flight
        booked_members=AirlineBooking.objects.filter(user=request.user, flight=fg, is_booked=True)
        print(booked_members[0].passengers.all())
    context={
          'bookings':queryset,
          'passenger_booked':booked_members
    }
    return render(request, "flight/ticket.html", context)
    
        
            
            
                # fg=queryset[0].flight
                # 
                
                # context['mypassengers']=passengers

    pass


    

def register_view(request):
    next=request.session.get('next', '')
    url='/login/'
    context={}
    form=UserRegisterForm(request.POST or None)
    context['form']=form
    if form.is_valid():
        form.save()
        if next is not None:
            url+='?next='+ next
            return redirect(url)
        return redirect('login')
    return render(request,  "flight/signup.html", context)


def login_view(request):
    nxt = request.GET.get("next", None)
    if nxt is not None:
        request.session['next']=nxt
        print('next parameter', nxt)
    context={}
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if nxt is not None:
                return redirect(request.GET.get('next'))
            return redirect('dashboard', user_id=request.user.id)
        context["error"]="invalid credentials",     
    return render(request, "flight/login.html", context)

@login_required
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect('login')
    return render(request, "flight/logout.html", {})

@login_required
def dashboard_view(request, user_id):
    complete_booking=Payment.objects.filter(user=request.user, verified=True)
    context={
        'bookings':complete_booking 
    }
    return render(request, "flight/dashboard.html", context)

@login_required
def booking_process(request, flight_id):
    flight=get_object_or_404(FlightClass, id=flight_id)
    user=request.user
    status="processing ticket"
    create_booking=AirlineBooking.objects.create(user=user,flight=flight, flight_status=status)
    return redirect('passenger', flight_id=flight.id)

    
