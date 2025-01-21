from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework import status
from django.utils import timezone


from .serializers import *

from .models import *

class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        color = self.request.query_params.get('color')
        memory = self.request.query_params.get('memory')
        context['color'] = color
        context['memory'] = memory
        return context     

class ProductAttributeAPIView(generics.ListAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        attribute_type = self.request.query_params.get('type_id')
        if attribute_type:
            attribute_type = int(attribute_type)
            queryset = queryset.filter(attribute_type__id=attribute_type)
        return queryset 
  
class AccessuaryAPIView(generics.ListAPIView):
    queryset = Accessuary.objects.all()
    serializer_class = AccessuarySerializer

class ProductSetAPIView(generics.ListAPIView):
    queryset = ProductSet.objects.all()
    serializer_class = ProductSetSerializer

class ClientAPIView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        type = self.request.query_params.get('type')
        if type:
            queryset = queryset.filter(type=type)
        return queryset

class RepairServiceAPIView(generics.ListAPIView):
    queryset = RepairService.objects.all()
    serializer_class = RepairServiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        return queryset
    
class ServiceCategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ServiceProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset


class DeviceRepairAPIView(generics.CreateAPIView):
    queryset = DeviceRepair.objects.all()
    serializer_class = DeviceRepairSerializer


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class PromoCodeAPIView(APIView):
    def post(self, request):
        serializer = PromoCodeCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        amount = serializer.validated_data.get('amount')
        promo_code = serializer.validated_data.get('promo_code')

        base_promo_code = PromoCode.objects.filter(name=promo_code).first()
        if not base_promo_code:
            return Response(
                data={"message": "Promo-kod mavjud emas yoki yaroqsiz."},
                status=status.HTTP_400_BAD_REQUEST
            )    
        if amount < base_promo_code.min_amount:
            return Response(
                {"message": "Bu promo-kod chegirma limitidan oshib ketdi."},
                status=status.HTTP_400_BAD_REQUEST
            )
        timezone_date = timezone.datetime.now().date()
        promo_code_date = base_promo_code.expiry_date 
        if promo_code_date < timezone_date:
            return Response(
                {"message": "Bu promo-kod tugatilgan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data={
            "message": "Promo-kod qabul qilindi."
        })
        
            



