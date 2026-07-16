from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('product-images', views.ProductImageViewSet, basename='product-images')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('reviews', views.ReviewViewSet, basename='reviews')

urlpatterns = [ 
    path('', include(router.urls)),
]
