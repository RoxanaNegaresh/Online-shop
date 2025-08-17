from django.shortcuts import render, redirect, get_object_or_404
from product.models import Category, ProductInfo, ProductComment
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from product.serializers import ProductSerializer



def home(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        print("Received product_id:", product_id)
        
        if not request.user.is_authenticated:
            return redirect('users:signup')

        if product_id:
            product_id = str(product_id)
            liked = request.session.get("selected", [])
            liked = [item for item in liked if item]
            print("Current liked list:", liked)

            if product_id not in liked:
                liked.append(product_id)
                request.session["selected"] = liked
                print("Product added:", liked)
            else:
                print("Product already in liked list")
        else:
            print("Invalid product ID")

    category = Category.objects.all()
    selected_category_id = request.GET.get('category_id', None)

    if selected_category_id:
        products = ProductInfo.objects.filter(category_id=selected_category_id, purchase_count__gt=100)
    else:
        products = ProductInfo.objects.filter(purchase_count__gt=100)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_data = list(products.values('id', 'name', 'image', 'description', 'price', 'brand'))
        return JsonResponse({'products': products_data})

    selected_ids = request.session.get("selected", [])
    products_in_cart = ProductInfo.objects.filter(id__in=selected_ids).distinct()
    products_liked = ProductInfo.objects.filter(id__in=selected_ids).exclude(id__in=selected_ids).distinct()

    products_selected = ProductSerializer(products, many=True)
    products_in_cart_serialized = ProductSerializer(products_in_cart, many=True)
    products_liked_serialized = ProductSerializer(products_liked, many=True)

    context = {
        "category": category,
        "products": products,
        "products_selected": products_selected.data,
        "products_in_cart": products_in_cart_serialized.data,
        "products_liked": products_liked_serialized.data,
    }

    return render(request, "shop/home.html", context)



def create(request):
    return render(request=request, template_name="shop/create.html", context={})

def author(request):
    return render(request=request, template_name="shop/author.html", context={})

def explore(request):
    if request.method == 'POST':
        products = ProductInfo.objects.all()
    else:
        products = ProductInfo.objects.all()

    return render(request, "shop/explore.html", {"products": products})




def details(request, id):
    product = get_object_or_404(ProductInfo, id=id)
    other_products = ProductInfo.objects.all().exclude(id=product.id)[:6]
    similar_products = ProductInfo.objects.filter(category=product.category).exclude(id=product.id)[:6]

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_text = request.POST.get('comment', '')
            if comment_text:
                ProductComment.objects.create(
                    product=product,
                    user=request.user,
                    comment=comment_text
                )
            return redirect('shop_app:details', id=id)  

    return render(request, 'shop/details.html', {
        'product': product,
        'similar_products': similar_products,
        'other_products': other_products
    })





