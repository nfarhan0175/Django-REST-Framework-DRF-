"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # api paths
    path('products/api/', include('products.api.urls')),
    path('accounts/api/', include('accounts.api.urls')),
    path('carts/api/', include('carts.api.urls')),
    path('orders/api/', include('orders.api.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path('notifications/api/', include('notifications.urls')),
    path('payments/api/', include('payments.api.urls')),

    # frontend paths
    path('seller/', include('seller.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('carts/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('home/', views.home, name='home'),
    # swagger/OpenApi
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)