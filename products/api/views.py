from products import models
from . import serializers, permissions
from rest_framework.response import Response
from rest_framework import viewsets # all crud operations easily
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsSellerOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.ProductList.objects.select_related(
        "category","seller"
    ).prefetch_related(
        "images",
        "reviews"
    )
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsSellerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)  
             
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = models.ProductImage.objects.select_related("product")
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [permissions.IsSellerOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.select_related(
        "reviewer",
        "product"
    )
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)     