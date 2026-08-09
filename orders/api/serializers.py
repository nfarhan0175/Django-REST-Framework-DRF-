from rest_framework import serializers
from orders import models

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = models.OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = models.Order
        fields = "__all__"  
        read_only_fields = ("user", "total_price", "status", "created_at",)

class CreateOrderSerializer(serializers.Serializer):
    address = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=[
            ("COD","Cash On Delivery"),
            ("SSLCOMMERZ","SSLCommerz")
        ]
    )   

# for seller
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = models.OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True )
    class Meta:
        model = models.Order
        fields = "__all__"
        read_only_fields = ("user", "total_price", "status", "created_at")

class SellerOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = models.OrderItem
        fields = ("id", "product", "product_name", "quantity", "price", "subtotal")

class SellerOrderSerializer(serializers.ModelSerializer):
    items = SellerOrderItemSerializer(many=True, read_only=True)
    seller_total = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = models.Order
        fields = ("id", "customer_name", "status", "created_at", "items", "seller_total")
    def get_seller_total(self, obj):
        return sum(item.subtotal for item in obj.items.all())