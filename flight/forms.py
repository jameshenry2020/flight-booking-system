from django import forms
from django.forms import fields
from .models import Passenger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username', 'email','password1', 'password2']
        

GENGER_SELECT=(
    ('M', 'male'),
    ('F', 'female')
)
class AddPassengerForm(forms.ModelForm):
    class Meta:
        model=Passenger
        fields=['names','address','gender','age','next_of_kin', 'kins_mobile']
 

