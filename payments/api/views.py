from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order
from payments.models import Payment
from payments.services import create_payment
from .serializers import (
    PaymentSerializer,
    CreatePaymentSerializer,
    PaymentSuccessSerializer,
)

class CreatePaymentView(generics.CreateAPIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data["order_id"]
        payment_method = serializer.validated_data["payment_method"]
        try:
            order = Order.objects.get(id=order_id,user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"},status=status.HTTP_404_NOT_FOUND)
        existing_payment = Payment.objects.filter(order=order).first()
        if existing_payment:
            return Response({"error": "Payment already exists for this order"},status=status.HTTP_400_BAD_REQUEST)
        payment, gateway = create_payment(order,payment_method)
        response_serializer = PaymentSerializer(payment)
        data = response_serializer.data
        if gateway:
            data["gateway"] = gateway
        return Response(data,status=status.HTTP_201_CREATED)
         
class PaymentSuccessView(generics.CreateAPIView):
    serializer_class = PaymentSuccessSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tran_id = serializer.validated_data["tran_id"]
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"},status=status.HTTP_404_NOT_FOUND)
        # এখানে পরে SSLCommerz validation API call করবে
        payment.status = "SUCCESS"
        payment.paid_at = timezone.now()
        payment.save()
        order = payment.order
        # stock reduce
        for item in order.items.select_related("product"):
            product = item.product
            if product.stock < item.quantity:
                return Response({"error": f"Insufficient stock for {product.name}"},status=status.HTTP_400_BAD_REQUEST)
            product.stock -= item.quantity
            product.save(update_fields=["stock"])
        order.status = "processing"
        order.save(update_fields=["status"])
        return Response({
                "message": "Payment successful",
                "order_id": order.id
            },status=status.HTTP_200_OK)

class PaymentFailView(generics.CreateAPIView):
    serializer_class = PaymentSuccessSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tran_id = serializer.validated_data["tran_id"]
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"},status=status.HTTP_404_NOT_FOUND)
        payment.status = "FAILED"
        payment.save()
        return Response({"message": "Payment failed"},status=status.HTTP_200_OK)            

class PaymentCancelView(generics.CreateAPIView):
    serializer_class = PaymentSuccessSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tran_id = serializer.validated_data["tran_id"]
        try:
            payment = Payment.objects.get(transaction_id=tran_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"},status=status.HTTP_404_NOT_FOUND)
        payment.status = "CANCELLED"
        payment.save()
        return Response({"message": "Payment cancelled"},status=status.HTTP_200_OK)        