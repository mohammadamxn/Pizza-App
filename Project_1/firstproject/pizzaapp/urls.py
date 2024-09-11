from django.urls import path
from . import views
from .forms import *

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('orders/', views.orders, name="orders"),
    
    path('createpizza/', views.createpizza, name="createpizza"),
    path('delivery/<int:pid>', views.delivery, name="delivery"), #THIS
    path('orderplaced/', views.orderplaced, name="orderplaced")

]