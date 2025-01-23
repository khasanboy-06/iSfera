from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='poster/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    description = models.TextField()
    price = models.FloatField()
    cash = models.BooleanField(default=True)
    service_duration = models.CharField(max_length=255)
    made_in = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    color = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')


class Memory(models.Model):
    volume = models.IntegerField()

    def __str__(self):
        return str(self.volume)


class ProductMemoryPrice(models.Model):
    additional_price = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_memories')
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='product_memories_price')

    def __str__(self):
        return f"{self.product.name}"


class AttributeType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes')
    attribute_type = models.ForeignKey(
        AttributeType,
        on_delete=models.CASCADE,
        related_name='attribute_types'
    )
    attribute = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} --> {self.attribute} --> {self.value}"


class PromoCode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    min_amount = models.DecimalField(max_digits=10, decimal_places=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        MODERATION = ('moderation', 'Moderation')
        APPROVED = ('approved', 'Approved')
        CANCELLED = ('cancelled', 'Cancelled')

    class Delivery(models.TextChoices):
        BY_YOURSELF = ('take_away', 'take_away')
        IN_CITY = ('free', 'free')
        IN_COUNTRY = ('paid', 'paid')

    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(null=True)
    status = models.CharField(
        max_length=100,
        choices=StatusChoices.choices,
        default=StatusChoices.MODERATION
    )
    delivery = models.CharField(max_length=122, choices=Delivery.choices)

    def __str__(self):
        return f"Order for {self.full_name} ({self.status})"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    count = models.IntegerField()
    color = models.ForeignKey(
        ProductImage,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_colors')
    memory = models.ForeignKey(
        ProductMemoryPrice,
        on_delete=models.SET_NULL,
        null=True,
        related_name='memory_products'
    )

    def __str__(self):
        return f"{self.product.name} x{self.count}"


class Accessory(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='accessories/')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='accessories')

    def __str__(self):
        return self.name


class ProductSet(models.Model):
    VIP_CHOICES = (
        ("VIP", "VIP"),
        ("Standard", "Standard"),
        ("Mini", "Mini"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sets')
    accessories = models.ManyToManyField(Accessory, related_name='accessories')
    choices = models.CharField(choices=VIP_CHOICES, max_length=100)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.choices}"


class OrderProductSet(models.Model):
    product_set = models.ForeignKey(ProductSet, on_delete=models.CASCADE)
    price = models.FloatField()
    count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_productsets')

    def __str__(self):
        return f"{self.product_set.product.name} x {self.count}"


# Service Landing Page Models
class Client(models.Model):
    CLIENT_CHOICES = (
        ("individual", "Individual"),
        ("company", "Company"),
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='clients/')
    profession = models.CharField(max_length=100)
    type = models.CharField(choices=CLIENT_CHOICES, max_length=100)

    def __str__(self):
        return self.name


class RepairService(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    fix_time = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='repair_products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='repair_categories')

    def __str__(self):
        return self.name


class DeviceRepair(models.Model):
    repair_service = models.ForeignKey(RepairService, on_delete=models.CASCADE, related_name='repair_services')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.repair_service}"


