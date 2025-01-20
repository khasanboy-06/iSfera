from django.contrib import admin

from .models import (Category, Product, ProductAttribute, 
                     ProductMemoryPrice, ProductImage, Memory, PromoCode, 
                     Order, OrderProduct, ProductSet, OrderProductSet,
                     Client, RepairService, DeviceRepair, Accessuary, AttributeType)

admin.site.register([Category, 
                     Product, 
                     ProductAttribute, 
                     ProductMemoryPrice, 
                     ProductImage, 
                     Memory,
                     PromoCode, 
                     Order, 
                     OrderProduct, 
                     ProductSet, 
                     OrderProductSet,
                     Client, 
                     RepairService, 
                     DeviceRepair,
                     Accessuary,
                     AttributeType])