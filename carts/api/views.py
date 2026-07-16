from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from carts import models
from products.models import ProductList
from .serializers import (
    CartSerializer, 
    CartProductSerializer,
    AddressSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart,context={"request": request})
        return Response(serializer.data)

class AddToCartView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        cart_product = models.CartProduct.objects.filter(cart=cart,product=product).first()
        if cart_product:
            new_quantity = cart_product.quantity + quantity
            if new_quantity > product.stock:
                return Response({"error":f"Only {product.stock} items available."},status=status.HTTP_400_BAD_REQUEST)
            cart_product.quantity = new_quantity
            cart_product.save()
        else:
            cart_product = models.CartProduct.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
        response_serializer = CartProductSerializer(cart_product,context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return get_object_or_404(models.CartProduct,id=self.kwargs["pk"],cart__user=self.request.user)
    def patch(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        if quantity > cart_item.product.stock:
            return Response({"error":f"Only {cart_item.product.stock} items available."},status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity = quantity
        cart_item.save()
        response_serializer = CartProductSerializer(cart_item,context={"request": request})
        return Response(response_serializer.data)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return get_object_or_404(models.CartProduct,id=self.kwargs["pk"],cart__user=self.request.user)
    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"message": "Item removed from cart"},status=status.HTTP_200_OK)

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return models.Address.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        if serializer.validated_data.get("is_default",False):
            models.Address.objects.filter(user=self.request.user,is_default=True).update(is_default=False)
        serializer.save(user=self.request.user)

       