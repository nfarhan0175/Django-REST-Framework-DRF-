from django.urls import path
from .views import CreateOrderView, OrderListView, SellerOrderListView

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("orderlist/", OrderListView.as_view(), name="orderlist"),
    path("seller_orders/", SellerOrderListView.as_view(), name="seller-orders" ),
]