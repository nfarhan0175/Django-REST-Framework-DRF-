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
        read_only_fields = ("user","total_price","status","created_at",)

class CreateOrderSerializer(serializers.Serializer):
    address = serializers.IntegerField()        