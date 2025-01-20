from django.urls import path

from .views import (ProductDetailAPIView, CategoryAPIView, 
                    ProductListAPIView, AccessuaryAPIView,
                    ProductSetAPIView, ProductAttributeAPIView,
                    ClientAPIView, RepairServiceAPIView,
                    ServiceCategoryAPIView, ServiceProductAPIView,
                    DeviceRepairAPIView, OrderAPIView, PromoCodeAPIView)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('products-list/', ProductListAPIView.as_view()),
    path('product/<int:pk>/', ProductDetailAPIView.as_view()),
    path('product-attribute/', ProductAttributeAPIView.as_view()),
    path('productset/', ProductSetAPIView.as_view()),
    path('accessuary/', AccessuaryAPIView.as_view()),
    
    path('service_category/', ServiceCategoryAPIView.as_view()),
    path('service-product/', ServiceProductAPIView.as_view()),
    path('repair-service/', RepairServiceAPIView.as_view()),
    path('device-repair/', DeviceRepairAPIView.as_view()),
    path('client/', ClientAPIView.as_view()),
    

    path('order/', OrderAPIView.as_view()),
    path('promo-code/', PromoCodeAPIView.as_view()),

]

    

    