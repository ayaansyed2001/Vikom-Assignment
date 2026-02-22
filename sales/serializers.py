from rest_framework import serializers
from .models import *
from .services import calculate_order_total


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(
        source="inventory.quantity",
        read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class DealerSerializer(serializers.ModelSerializer):
    orders = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Dealer
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):

    def validate(self, data):
        order = self.instance.order if self.instance else data.get("order")

        if order and order.status != "DRAFT":
            raise serializers.ValidationError(
                "Cannot modify confirmed/delivered order."
            )
        return data

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
        read_only_fields = ("line_total",)


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    # CREATE ORDER
    def create(self, validated_data):

        items_data = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                unit_price=item["product"].price,
            )

        from .services import calculate_order_total
        calculate_order_total(order)

        return order

    # UPDATE ORDER (THIS FIXES YOUR ERROR)
    def update(self, instance, validated_data):

        items_data = validated_data.pop("items", None)

        # Update dealer if changed
        instance.dealer = validated_data.get(
            "dealer", instance.dealer
        )
        instance.save()

        if items_data is not None:
  
            # Delete old items
            instance.items.all().delete()

            # Create new items
            for item in items_data:
                OrderItem.objects.create(
                    order=instance,
                    product=item["product"],
                    quantity=item["quantity"],
                    unit_price=item["product"].price,
                )

        from .services import calculate_order_total
        calculate_order_total(instance)

        return instance