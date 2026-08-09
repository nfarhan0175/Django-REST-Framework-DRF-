import uuid
import requests
from payments.models import Payment
from django.conf import settings

def initiate_sslcommerz(payment):
    payload = {
        "store_id": settings.SSL_STORE_ID,
        "store_passwd": settings.SSL_STORE_PASSWORD,
        "total_amount": str(payment.amount),
        "currency": "BDT",
        "tran_id": payment.transaction_id,
        "success_url": "http://127.0.0.1:8002/payments/api/success/",
        "fail_url": "http://127.0.0.1:8002/payments/api/fail/",
        "cancel_url": "http://127.0.0.1:8002/payments/api/cancel/",
        
        # customer information
        "cus_name": payment.order.user.username,
        "cus_email": payment.order.user.email,
        "cus_add1": payment.order.address.street,
        "cus_city": payment.order.address.city,
        "cus_postcode": payment.order.address.postal_code,
        "cus_country": "Bangladesh",

        # payment information
        "shipping_method": "NO",
        "product_name": "Ecommerce Product",
        "product_category": "General",
        "product_profile": "general",
    }    
    if settings.SSL_SANDBOX:
        url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
    else:
        url = "https://securepay.sslcommerz.com/gwprocess/v4/api.php"
    response = requests.post(url,data=payload)
    return response.json()

def create_payment(order, payment_method):
    payment = Payment.objects.create(
        order=order,
        payment_method=payment_method,
        amount=order.total_price,
        transaction_id=str(uuid.uuid4())
    )
    gateway_response = None
    if payment_method == "SSLCOMMERZ":
        gateway_response = initiate_sslcommerz(payment)
    return payment, gateway_response    

def validate_payment(val_id):
    if settings.SSL_SANDBOX:
        url = "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"
    else:
        url = "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php"
    params = {
        "val_id": val_id,
        "store_id": settings.SSL_STORE_ID,
        "store_passwd": settings.SSL_STORE_PASSWORD,
        "format": "json",
    }
    response = requests.get(url, params=params)
    return response.json()