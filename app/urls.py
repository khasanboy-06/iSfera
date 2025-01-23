from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoryAPIView.as_view()),
    path('products-list/', views.ProductListAPIView.as_view()),
    path('product/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('product-attribute/', views.ProductAttributeAPIView.as_view()),
    path('productset/', views.ProductSetAPIView.as_view()),
    path('accessuary/', views.AccessoryAPIView.as_view()),
    
    path('service_category/', views.ServiceCategoryAPIView.as_view()),
    path('service-product/', views.ServiceProductAPIView.as_view()),
    path('repair-service/', views.RepairServiceAPIView.as_view()),
    path('device-application/', views.DeviceRepairAPIView.as_view()),
    path('client/', views.ClientAPIView.as_view()),
    

    # path('order/', OrderAPIView.as_view()),
    path('order-create/', views.OrderCreateAPIView.as_view()),
    path('promo-code-check/', views.PromoCodeAPIView.as_view()),
]

    

    