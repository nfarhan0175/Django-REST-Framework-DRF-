from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, Address
from orders.models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer, SellerOrderSerializer
from rest_framework import generics, status
from notifications.utils import create_notification
# forseller
from django.db.models import Prefetch
from products.api import permissions

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")           

class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address_id = serializer.validated_data["address"]
        address = Address.objects.filter(id=address_id,user=request.user).first()
        if not address:
            return Response({"error": "Address not found"},status=status.HTTP_404_NOT_FOUND)
        cart = Cart.objects.prefetch_related("cart_products__product").get(user=request.user)
        if not cart:
            return Response({"error": "Cart not found"},status=status.HTTP_400_BAD_REQUEST)
        cart_items = cart.cart_products.select_related("product")
        if not cart_items.exists():
            return Response({"error": "Cart is empty"},status=status.HTTP_400_BAD_REQUEST)
        payment_method = serializer.validated_data["payment_method"]
        order = Order.objects.create(user=request.user,address=address, payment_method=payment_method)
        total_price = 0
        for item in cart_items:
            product = item.product
            if item.quantity > product.stock:
                return Response({"error": (f"{product.name} has only "f"{product.stock} left")},status=status.HTTP_400_BAD_REQUEST)
            subtotal = product.final_price * item.quantity
            total_price += subtotal
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item.quantity,
                price=product.final_price,
                subtotal=subtotal,
            )
        order.total_price = total_price
        order.save(update_fields=["total_price"])
        # this 1 line is for testing the notification system, you can remove it later
        create_notification(user=request.user,title="Order Confirmed", message=f"Your order #{order.id} has been placed successfully.", notif_type="order")
        if payment_method == "COD":
            cart_items.delete()
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data,status=status.HTTP_201_CREATED)


# for seller
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return (Order.objects.filter(user=self.request.user).prefetch_related("items"))

class SellerOrderListView(generics.ListAPIView):
    serializer_class = SellerOrderSerializer
    permission_classes = [IsAuthenticated, permissions.IsSellerOrReadOnly]
    def get_queryset(self):
        seller = self.request.user
        seller_items = (OrderItem.objects.filter(product__seller=seller)
            .select_related("product"))
        return (Order.objects.filter(items__product__seller=seller).distinct()
            .prefetch_related(Prefetch("items", queryset=seller_items))
            .order_by("-created_at")
        )
