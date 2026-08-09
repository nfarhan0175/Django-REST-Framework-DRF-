from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path("dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("products/", views.seller_product_list, name="seller_products"),
    path("products/add/", views.seller_product_add, name="seller_product_add"),
    path("products/add/<int:id>/",views.seller_product_add,name="seller_product_edit"),
    path("orders/", views.seller_order_list, name="seller_orders"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)