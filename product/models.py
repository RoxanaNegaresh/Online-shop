from django.db import models
from django.utils import timezone
from users.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length =70,verbose_name ="نام دسته بندی ")
    image = models.ImageField(upload_to='image/',verbose_name='عکس', default='media/imgae/default.png', blank=True, null=True)

    
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        
        
class ProductInfo(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'موجود'),
        ('out_of_stock', 'ناموجود'),
        ('coming_soon', 'به زودی'),
    ]
    name = models.CharField(max_length=70, verbose_name="نام")
    description = models.TextField(verbose_name="توضیحات")
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')
    price = models.BigIntegerField(verbose_name='قیمت', default=0)
    pr_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ تولید')
    exp_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انقضا")
    brand = models.CharField(max_length=50, null=True, blank=True, verbose_name="برند")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته‌بندی', related_name='products', default=1)
    image = models.ImageField(upload_to='image/', verbose_name='عکس', default='media/image/default.png', blank=True, null=True)
    purchase_count = models.PositiveIntegerField(default=0, verbose_name="تعداد خرید")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock', verbose_name='وضعیت')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

# class ProductLike(models.Model):
#     pass



class ProductComment(models.Model):
    product = models.ForeignKey('ProductInfo', on_delete=models.CASCADE, related_name='comments', verbose_name="محصول", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر", default=1)
    comment = models.TextField(verbose_name="نظر", default="بدون نظر")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "نظر محصول"
        verbose_name_plural = "نظرات محصولات"

    def __str__(self):
        return f'نظر توسط {self.user.username} برای {self.product.name}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

