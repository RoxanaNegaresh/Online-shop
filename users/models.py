from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "AD","Admin"
        SHOP_ADMIN = "SH","ShopAdmin"
        CUSTOMER = "CU","Customer"

    national_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="کد ملی")
    phone = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name="شماره تماس")
    address = models.TextField(null=True, blank=True, verbose_name="آدرس")
    last_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='آخرین آدرس آی پی')
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.CUSTOMER, verbose_name='نقش')


