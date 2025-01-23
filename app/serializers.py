from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'image')


class ProductMemoryPriceSerializer(serializers.ModelSerializer):
    memory_volume = serializers.IntegerField(source='memory.volume', read_only=True)

    class Meta:
        model = models.ProductMemoryPrice
        fields = ['id', 'memory_volume']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('id', 'image',)


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('id', 'color')


class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_colors = ProductColorSerializer(source='product_images',many=True)
    products_memories = ProductMemoryPriceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id',
            'product_images',
            'product_colors',
            'products_memories',
            'name',
            'poster',
            'description',
            'price',
            'cash',
            'service_duration',
            'made_in',
            'category',
        )


class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_colors = ProductColorSerializer(source='product_images',many=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Accessory
        fields = (
            'name',
            'price',
            'image',
            'description',
        )
class AttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeType
        fields = ('id', 'name')


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductAttribute
        fields = ('attribute', 'value',)


class ProductSetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'poster')


class ProductSetSerializer(serializers.ModelSerializer):
    accessories = AccessorySerializer(many=True)
    product_id = serializers.SerializerMethodField
    product_image = serializers.ImageField(source='product.poster')
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductSet
        fields = (
            'id',
            'product_id',
            'product_image',
            'accessories',
            'choices',
            'discount',
            'discount_price')


    def get_discount_price(self, obj):
        total_price = obj.product.price
        for accessory in obj.accessories.all():
            total_price += accessory.price
        discount_price = total_price - obj.discount
        return discount_price


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'


class RepairServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RepairService
        fields = (
            'name',
            'price',
            'fix_time',
        )


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')


class ServiceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'name')


class DeviceRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceRepair
        fields = (
            'id',
            'repair_service',
            'name',
            'phone',
        )


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = ['product', 'count', 'color', 'memory']


class OrderCreateSerializer(serializers.ModelSerializer):
    order_products = serializers.ListField(
        child=serializers.JSONField(write_only=True),
        required=False,
        write_only=True,
        allow_empty=True
    )
    order_set = serializers.ListField(
        child=serializers.JSONField(write_only=True),
        required=False,
        write_only=True,
        allow_empty=True
    )

    class Meta:
        model = models.Order
        fields = [
            'id',
            'full_name',
            'promo_code',
            'phone_number',
            'order_products',
            'order_set',
        ]
    def create(self, validated_data):
        order_products = validated_data.pop("order_products", [])
        order_sets = validated_data.pop("order_set", [])
        instance = models.Order.objects.create(**validated_data)
        order_products_items = [models.OrderProduct(order=instance, **order_product) for order_product in order_products]
        if order_products_items:
            models.OrderProduct.objects.bulk_create(order_products_items)
        if order_sets:
            set_items = [models.OrderProductSet(order=instance, **order) for order in order_sets]
            models.OrderProductSet.objects.bulk_create(set_items)
            
        return instance


class PromoCodeCheckSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    promo_code = serializers.CharField()
