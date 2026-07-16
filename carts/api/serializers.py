from rest_framework import serializers
from carts import models
from products.models import ProductList

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
        read_only_fields = ["user"]

class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ProductList.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]
        if quantity > product.stock:
            raise serializers.ValidationError(f"Only {product.stock} items available in stock.")
        return attrs

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    def update(self, instance, validated_data):
        instance.quantity = validated_data["quantity"]
        instance.save()
        return instance
        
class CartProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name",read_only=True)
    product_price = serializers.DecimalField(source="product.final_price",max_digits=10,decimal_places=2,read_only=True)
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = models.CartProduct
        fields = "__all__"

    def get_product_image(self, obj):
        image = obj.product.images.first()
        if image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None
        
    def get_subtotal(self, obj):
        return obj.product.final_price * obj.quantity        

class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True,read_only=True)
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = models.Cart
        fields = "__all__"