from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView, RemoveFromCartView, AddressListCreateView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/item/<int:pk>/",UpdateCartItemView.as_view(), name="cart-update"),
    path("cart/item/<int:pk>/remove/", RemoveFromCartView.as_view(), name="cart-remove"),
    path("addresses/", AddressListCreateView.as_view(), name="address-list-create"),
] 