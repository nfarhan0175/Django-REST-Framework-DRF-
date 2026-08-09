from django.shortcuts import render
from products.models import Category

# Create your views here.
def seller_dashboard(request):
    return render(request, "seller/dashboard.html")

def seller_product_list(request):
    return render(request, "seller/products.html")

def seller_product_add(request, id=None):
    categories = Category.objects.all()
    return render(request,"seller/add_product.html",{"categories": categories})

def seller_order_list(request):
    return render(request, "seller/orders.html")