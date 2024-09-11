import re
from django.shortcuts import render, get_object_or_404
import random
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('orders')


class UserLoginView(LoginView):
    template_name='login.html'


@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def orders(request):
    orders = Orders.objects.filter(user=request.user)      
    return render(request, 'orders.html', {'orders': orders})


@login_required
def createpizza(request):
    if request.method == "POST":
				
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save() 
						
            return redirect('delivery', pid = pizza.id)
        else:
						
            return render(request, 'create_pizza.html', {'form': form})
    else:
        form = PizzaForm()
        return render(request, 'create_pizza.html', {'form': form})


@login_required
def delivery(request, pid):
    if request.method == "POST":
        pizza = get_object_or_404(Pizza, id=pid)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.pizza = pizza
            order.user = request.user 
            order.save()
            return render(request, 'order_placed.html', {'order':order})
        else:
            return render(request, 'delivery.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'delivery.html', {'form': form})

def orderplaced(request):
    return render(request, 'order_placed.html')