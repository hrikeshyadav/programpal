from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


# class RoomForm(ModelForm):
#     class Meta:             ## for lin models.py and 
#         model = Room
#         field = '__all__'
#         exclude = ['host','participants']
        


class RoomForm(ModelForm):
    class Meta:
        model = Room          ## for lin models.py and 
        fields = '__all__'
        exclude = ['host', 'participants']


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['avatar', 'bio']