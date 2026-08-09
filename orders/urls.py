from django.urls import path, include
from . import views

urlpatterns = [
    path('order/', views.order, name='order_list'),
    path('checkout/', views.checkout, name='checkout'),
]