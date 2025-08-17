from django.contrib import admin
from .models import ProductInfo, Category

admin.sites.AdminSite.site_header = "پنل مدیریت سایت"
admin.sites.AdminSite.site_title = "پنل مدیریت سایت"
admin.sites.AdminSite.index_title = "پنل مدیریت"

admin.site.register(Category)


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'purchase_count', 'category') 
    readonly_fields = ('purchase_count',)  

admin.site.register(ProductInfo, ProductInfoAdmin)
