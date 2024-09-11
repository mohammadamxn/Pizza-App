from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction
from django.core.exceptions import ValidationError
import datetime


class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)



class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'pepperoni', 'chicken', 'ham', 'pineapple', 'jalapeno', 'onions', 'peppers', 'mushrooms']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['name', 'address', 'card_number', 'card_expiry', 'card_cvv']

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValidationError("Card number must be 16 digits long.")
        return card_number

    def clean_card_cvv(self):
        card_cvv = self.cleaned_data['card_cvv']
        if not card_cvv.isdigit() or len(card_cvv) != 3:
            raise ValidationError("CVV must be 3 digits long.")
        return card_cvv

    def clean_card_expiry(self):
        card_expiry = self.cleaned_data['card_expiry']
        try:
            expiry_date = datetime.datetime.strptime(card_expiry, "%m/%y")
            if expiry_date < datetime.datetime.now():
                raise ValidationError("The card expiry date has passed.")
        except ValueError:
            raise ValidationError("Expiry date must be in MM/YY format.")
        return card_expiry