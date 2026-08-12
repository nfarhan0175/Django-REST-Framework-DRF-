from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class ProductList(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError("Discount price cannot be greater than price")
    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    @property
    def is_available(self):
        return self.stock > 0
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"Image for {self.product.name}" 

class Review(models.Model):
    product = models.ForeignKey(ProductList, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    def __str__(self):
        return f"{self.reviewer} - {self.rating}"       
 