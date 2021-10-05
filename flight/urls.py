from django.urls import path
from .views import *

urlpatterns=[
    path('',FlightSearchPage.as_view(), name='flight-search'),
    path('destination/choice/', DestinationChoices.as_view(), name='destination'),
    path('flight-search/', SearchFlight.as_view(), name='search'),
    path('flight-selected/<int:pk>/', SelectedFlight.as_view(), name='chosen-flight'),
    path('signup/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('booking-process/<int:flight_id>/', booking_process, name='booking'),
    path('add-passenger/<int:flight_id>/', AddPassenger, name='passenger'),
    path('payment/<int:flight_id>/', PaymentView.as_view(), name='payment')

]