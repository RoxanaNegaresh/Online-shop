from django.urls import path, include
from .views import *
from django.contrib.auth.views import *

app_name='shop_app'

urlpatterns=[
    path('home/', home, name='home'),
    path('explore/', explore, name='explore'),
    path('details/<int:id>/', details, name='details'),
    path('create/', create, name='create'),
    path('author/', author, name='author'),
    path('users/', include('users.urls')),

    

    
]
