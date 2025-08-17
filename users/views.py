from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .forms import LoginForm , SignUpForm,OtpForm,VerifyCode
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from random import randint
import requests
from shop import settings
from kavenegar import *
from django.contrib import messages
from product.views import calculate_total_price, get_cart_and_liked_products
# Create your views here.

def index(request):
    request.session['admin2'] = "admin khers"
    res = HttpResponse(request,"Set Cookie")
    res.set_cookie("admin2","admin2 hastam")
    return res
    # return render(request=request,template_name='user/index.html')

@login_required
def dashboard_view(request):
    print("kharkose")
    return render(request=request,template_name='user/dashboard.html')

def signup(request):
    signup_form = SignUpForm()
    login_form = LoginForm()  
    
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data['password'])
            user.is_staff = True
            user.save()
    
    return render(request, 'user/signup.html', context={'signup_form': signup_form, 'login_form': login_form})



# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request=request,username = cd['username'],password = cd['password'])
#             if user is None:
#                 return HttpResponse(content='نام کاربری یا رمز عبور اشتباه است')
#             else:
#                 login(request=request,user=user)
#                 return render(request=request,template_name='user/inde.html')
#         else:
#             pass
#     else:
#         form = LoginForm()
#     return render(request=request,template_name='user/login.html',context={'form':form})

# def logout_user(request):
#     try:
#         user = User.objects.get(id = request.user.id)
#     except User.DoesNotExist:
#         print('yrdsssss')
#         return redirect('users:login')
#     logout(request=request)
#     print('yrdsssss2')
#     return render(request=request,template_name='user/inde.html')

def send_otp(phone_number):
    code = randint(1000,9999)
    # api_key = settings.API_KEY_SMS
    # message = f'your code is {code}'
    # # api = KavenegarAPI(api_key)
    # # data= {
    # #     "receptor": phone_number,
    # #     "message":message
    # # }
    # # res = api.sms_send(data)
    # # print("*",res)
    # url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"
    # data= {
    #     "receptor": phone_number,
    #     "message":message,
    #     "sender":"200050066"
    # }
    # res = requests.post(url=url,data=data)
    print(code)
    return code



def otp_login(request):
    if request.method == "POST":
        form = OtpForm(request.POST)  
        if form.is_valid():
            c_data = form.cleaned_data
            try:
                user = User.objects.get(phone=c_data.get("phone"))
                code = send_otp(user.phone)
                request.session["code"] = code
                messages.success(request, "کد تأیید به شماره شما ارسال شد.")
                return redirect('users:verify')  
            except User.DoesNotExist:
                messages.error(request, "شماره وارد شده در سیستم وجود ندارد.")
        else:
            messages.error(request, "فرم نامعتبر است. لطفاً شماره تلفن خود را به درستی وارد کنید.")
    else:
        form = OtpForm()  

    return render(request, "registration/login.html", {"form": form})


def verify_code(request):
    if request.method == "POST":
        form_data = VerifyCode(request.POST)
        if form_data.is_valid():
            c_data = form_data.cleaned_data
            code = str(request.session.get("code"))
            user_phone = c_data.get("phone")
            input_code = str(c_data.get("code"))

            if code == input_code:
                users = User.objects.filter(phone=user_phone)
                if users.count() == 1:
                    user = users.first()
                    login(request, user)
                    messages.success(request, "خوش آمدید!")
                    return redirect('users:profile')  
                elif users.count() > 1:
                    messages.error(request, "چندین کاربر با این شماره تلفن وجود دارد.")
                    return render(request, "registration/verify.html", {"form": form_data})
                else:
                    messages.error(request, "کاربر با این شماره تلفن یافت نشد.")
                    return render(request, "registration/verify.html", {"form": form_data})
            else:
                messages.error(request, "کد وارد شده صحیح نمی‌باشد.")
                return render(request, "registration/verify.html", {"form": form_data})
    else:
        form = VerifyCode()
    return render(request, "registration/verify.html", {"form": form})




def success_page(request):
    return render(request, 'registration/success_page.html')

@login_required
def profile(request):
    products_in_cart, products_liked = get_cart_and_liked_products(request)

    users = User.objects.all()

    total_price = calculate_total_price(request)

    context = {
        'users': users,
        'total_price': total_price,
        'products_in_cart': products_in_cart,
        'products_liked': products_liked,
    }

    return render(request, 'user/profile.html', context)

