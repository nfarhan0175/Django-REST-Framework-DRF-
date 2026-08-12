from products import models
from . import serializers, permissions
from rest_framework.response import Response
from rest_framework import viewsets # all crud operations easily
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsSellerOrReadOnly]
 
class ProductViewSet(viewsets.ModelViewSet): # for customer
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.ReadOnlyPermission]
    
    filter_backends = [SearchFilter, OrderingFilter] 
    search_fields = ["name", "description", "category__name"] 
    ordering_fields = ["price", "average_rating", "created_at"]

    def get_queryset(self):
        queryset = (
            models.ProductList.objects
            .select_related("category", "seller")
            .prefetch_related("images","reviews")
        )
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        min_price = self.request.query_params.get("min_price") 
        if min_price: 
            queryset = queryset.filter(price__gte=min_price) 
        max_price = self.request.query_params.get("max_price") 
        if max_price: 
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = models.ProductImage.objects.select_related("product")
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [permissions.IsSellerOrReadOnly]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.ProductImage.objects.filter(
                product__seller=self.request.user
            )
        return models.ProductImage.objects.none()

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewOwnerOrReadOnly]
    def get_queryset(self):
        queryset = models.Review.objects.select_related(
            "reviewer", "product")
        product_id = self.request.query_params.get("product")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class SellerProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, permissions.IsSellerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["name", "category__name"]
    def get_queryset(self):
        return (
            models.ProductList.objects
            .filter(seller=self.request.user)
            .select_related("category", "seller")
            .prefetch_related("images", "reviews")
        )    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)        
