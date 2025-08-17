from django.urls import path
from .views import *
from shop_app import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'products'

urlpatterns = [
    path('', index,name='index'),
    path('cart/', view_cart,name='cart'),

]
