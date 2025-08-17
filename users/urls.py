from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'users'

urlpatterns = [
    path('', index,name='index'),
    path('dashboard/',dashboard_view,name= 'dashboard'),
    path('login/',otp_login,name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',signup,name='signup'),
    path('login/verify',verify_code,name='verify'),
    path('login/verify/success/', success_page, name='success_page'),
    # path('success/', success_page, name='success_page'),  
    path('profile/', profile, name='profile'),
    # path('shop/', include('shop_app.urls')),
]
