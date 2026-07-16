from django.db import models
from accounts.models import User, UserProfile
from products.models import ProductList
from django.conf import settings

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street = models.TextField()
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.full_name} - {self.city}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="carts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.cart_products.all())    

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_products", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, related_name="cart_products", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    def __str__(self):        
        return f"{self.quantity} of {self.product.name}"
    @property  
    def subtotal(self):
        return self.product.final_price * self.quantity        