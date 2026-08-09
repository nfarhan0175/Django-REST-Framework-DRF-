from django.shortcuts import render

# Create your views here.
def home(request):
    # return render(request, 'seller/add_product.html')
    return render(request, 'index.html')