from django.urls import path
from .views import CreateOrderView, OrderListView

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("orderlist/", OrderListView.as_view(), name="orderlist"),
]