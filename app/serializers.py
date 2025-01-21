from rest_framework import serializers

from .models import (Category, Product, ProductAttribute, 
                     ProductMemoryPrice, ProductImage, Memory, PromoCode, 
                     Order, OrderProduct, ProductSet, OrderProductSet,
                     Client, RepairService, DeviceRepair, Accessuary, AttributeType)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id',
                  'name',
                  'image')

class ProductMemorySerializer(serializers.ModelSerializer):
    memory = serializers.IntegerField(source = 'memory.volume')
    class Meta:
        model = ProductMemoryPrice
        fields = ('id', 
                  'memory')

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 
                  'image')
        
        
class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeType
        fields = ('id', 'name')

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('attribute',
                  'value',)
    

class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()
    product_colors = serializers.SerializerMethodField()
    product_memories = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField() 
    
    class Meta:
        model = Product
        fields = ('id',
                  'product_images',
                  'product_colors',
                  'product_memories',
                  'name',
                  'poster',
                  'description',
                  'price',
                  'total_price',
                  'cash',
                  'expire_date',
                  'made_in',
                  'category',)
        
    def get_total_price(self, obj):
        base_price = obj.price
        memory_id = self.context.get('memory')
        
        if memory_id:
            try:
                additional_price = obj.product_memories.get(memory_id=memory_id).additional_price
                return base_price + additional_price
            except ProductMemoryPrice.DoesNotExist:
                return base_price
        return base_price

    def get_product_images(self, obj):
        queryset = obj.product_images.filter(color=self.context.get('color'))
        serializer = ProductImageSerializer(queryset, many=True, read_only=True)
        return serializer.data
    
    def get_product_colors(self, obj):
        colors = obj.product_images.values('id', 'color')
        return colors

    def get_product_memories(self, obj):
        memories = obj.product_memories.all()
        return ProductMemorySerializer(memories, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    product_colors = serializers.SerializerMethodField()
    product_memories = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_product_colors(self, obj):
        colors = obj.product_images.values('id', 'color')
        return colors
    
    def get_product_memories(self, obj):
        memories = obj.product_memories.all()
        return ProductMemorySerializer(memories, many=True).data    
    

class AccessuarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessuary
        fields = ('name',
                  'price',
                  'image',
                  'description',
                  )
        
class ProductSetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'poster')
        
class ProductSetSerializer(serializers.ModelSerializer):
    accessories = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField
    product_image = serializers.ImageField(source = 'product.poster')
    discount_price = serializers.SerializerMethodField()
    class Meta:
        model = ProductSet
        fields = ('id',
                  'product_id',
                  'product_image',
                  'accessories',
                  'choices',
                  'discount',
                  'discount_price')
        
    def get_accessories(self, obj):
        accessuaries = obj.accessories.all()
        serializer = AccessuarySerializer(accessuaries, many=True, read_only=True)
        return serializer.data
    
    def get_discount_price(self, obj):
        total_price = obj.product.price
        for accessory in obj.accessories.all():
            total_price += accessory.price
        discount_price = total_price - obj.discount
        return discount_price
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class RepairServiceSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source = 'product.name')
    category = serializers.CharField(source = 'product.category.name')
    class Meta:
        model = RepairService
        fields = ('name',
                  'price',
                  'fix_time',
                  'product',
                  'category')
        

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id',
                  'name')


class ServiceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',
                  'name')


class DeviceRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceRepair
        fields = ('id', 
                  'repair_service',
                  'name',
                  'phone',
                )

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'count']

class OrderCreateSerializer(serializers.ModelSerializer):
    order_products = serializers.ListField(
        child=serializers.JSONField(write_only=True),
        required=False,
        write_only=True,
        allow_empty=True
    )
    class Meta:
        model = Order
        fields = [
            'id',
            'full_name',
            'promo_code',
            'phone_number',
            'order_products',
        ]
    def create(self, validated_data):
        order_products = validated_data.pop("order_products")
        instance = Order.objects.create(**validated_data)
    
        for order_product in order_products:
            order_product = OrderProduct.objects.create(count=order_product.get('count'),
                                                        product_id=order_product.get('product_id'),
                                                        order_id=instance.id,
                                                        color_id=order_product.get('color_id'),
                                                        memory_id=order_product.get('memory_id'))

        return instance

class PromoCodeCheckSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    promo_code = serializers.CharField()