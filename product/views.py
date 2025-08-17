from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductInfo, Category, Favorite
from .serializers import ProductSerializer

# Create your views here.
def index(request):
    product_tmp = ProductInfo.objects.all()
    products = ProductSerializer(product_tmp, many = True)
    if request.method == "POST":
        data = request.POST.get("product")
        print("*******",data)
        pr = request.session.get("selected")
        if pr is None:
            pr=[]
        pr.append(data)
        request.session["selected"] = pr
        print(pr)
    
    rt = render(request=request,template_name="index.html",context={"products":products.data})
    # rt.set_cookie("selected",pr)
    return rt

def view_cart(request):
    if request.method == "POST":
        data = request.POST.get("product")
        if data:
            pr = request.session.get("selected", [])
            
            if data in pr:
                pr.remove(data)
                request.session["selected"] = pr
            else:
                print(f"محصول {data} در لیست موجود نیست.")
    
    sessions = request.session.get("selected", [])
    
    products = ProductInfo.objects.filter(id__in=sessions)
    
    total_price = sum([item.price for item in products])
    
    return render(request, template_name="cart.html", context={
        "products": products,
        "total_price": total_price
    })
    
def calculate_total_price(request):
    sessions = request.session.get("selected", [])
    products = ProductInfo.objects.filter(id__in=sessions)
    total_price = sum([item.price for item in products])
    return total_price
    
def purchase_product(request, product_id):
    product = get_object_or_404(ProductInfo, id=product_id)
    product.purchase_count += 1
    product.save()
    return redirect('shop_app:home')  




def add_to_favorite(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(ProductInfo, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete() 
        print(favorite)
        return redirect('shop_app:home')  
    
    
def get_cart_and_liked_products(request):
    selected_ids = request.session.get("selected", [])
    
    products_in_cart = ProductInfo.objects.filter(id__in=selected_ids).distinct()
    products_liked = ProductInfo.objects.filter(id__in=selected_ids).exclude(id__in=selected_ids).distinct()

    return products_in_cart, products_liked









