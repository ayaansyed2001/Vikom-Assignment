from django.contrib import admin
from .models import (
    Dealer,
    Inventory,
    InventoryAdjustment,
    Order,
    OrderItem,
    Product,
)

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Dealer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(InventoryAdjustment)
