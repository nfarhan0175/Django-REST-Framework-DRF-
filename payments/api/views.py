from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order
from payments.models import Payment
from payments.services import create_payment, validate_payment
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
        val_id = serializer.validated_data["val_id"]
        try:
            payment = Payment.objects.select_related("order").get(transaction_id=tran_id)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # যদি আগে থেকেই SUCCESS হয়ে থাকে
        if payment.status == "SUCCESS":
            return Response(
                {
                    "message": "Payment already processed",
                    "order_id": payment.order.id,
                },
                status=status.HTTP_200_OK,
            )

        # SSLCommerz Validation
        validation = validate_payment(val_id)

        print("SSL Validation:", validation)

        if validation.get("status") != "VALID":
            payment.status = "FAILED"
            payment.save(update_fields=["status"])

            return Response(
                {"error": "Payment validation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Transaction ID check
        if validation.get("tran_id") != payment.transaction_id:
            return Response(
                {"error": "Transaction ID mismatch"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Amount check
        try:
            gateway_amount = float(validation.get("amount"))
            payment_amount = float(payment.amount)

            if gateway_amount != payment_amount:
                return Response(
                    {"error": "Amount mismatch"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception:
            return Response(
                {"error": "Invalid amount received"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Payment Success
        payment.status = "SUCCESS"
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "paid_at"])
        order = payment.order
        # Reduce Stock
        for item in order.items.select_related("product"):
            product = item.product
            if product.stock < item.quantity:
                return Response(
                    {
                        "error": f"Insufficient stock for {product.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            product.stock -= item.quantity
            product.save(update_fields=["stock"])
        # Update Order
        order.status = "processing"
        order.save(update_fields=["status"])
        return Response(
            {
                "message": "Payment successful",
                "order_id": order.id,
            },
            status=status.HTTP_200_OK,
        )

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