from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)