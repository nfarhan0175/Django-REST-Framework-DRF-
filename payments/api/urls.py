from django.urls import path
from .views import CreatePaymentView, PaymentSuccessView, PaymentFailView, PaymentCancelView

urlpatterns = [
    path("create/",CreatePaymentView.as_view(),name="create-payment"),
    path("success/",PaymentSuccessView.as_view(),name="payment-success"),
    path("fail/",PaymentFailView.as_view(),name="payment-fail"),
    path("cancel/",PaymentCancelView.as_view(),name="payment-cancel"),
]