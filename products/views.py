from django.shortcuts import render
from . import models

def product_list(request):
    return render(request, "products/product_list.html")

def product_detail(request, product_id):
    return render(
        request,"products/product_detail.html",{"product_id": product_id})

# ==========================================
# seller views
# ==========================================
def seller_dashboard(request):
    return render(request, "seller/dashboard.html")

def seller_product_list(request):
    return render(request, "seller/products.html")

def seller_product_add(request):
    return render(request, "seller/add_product.html")

def seller_order_list(request):
    return render(request, "seller/orders.html")