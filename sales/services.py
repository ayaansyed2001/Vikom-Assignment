from django.db import transaction
from rest_framework.exceptions import ValidationError


def calculate_order_total(order):
    total = sum(item.line_total for item in order.items.all())
    order.total_amount = total
    order.save()


@transaction.atomic
def confirm_order(order):

    if order.status != "DRAFT":
        raise ValidationError("Only draft orders can be confirmed.")

    insufficient = []

    for item in order.items.all():
        stock = item.product.inventory.quantity

        if item.quantity > stock:
            insufficient.append({
                "product": item.product.name,
                "available": stock,
                "requested": item.quantity
            })

    if insufficient:
        raise ValidationError({
            "error": "Insufficient stock",
            "details": insufficient
        })

    for item in order.items.all():
        inv = item.product.inventory
        inv.quantity -= item.quantity
        inv.save()

    order.status = "CONFIRMED"
    order.save()


def deliver_order(order):

    if order.status != "CONFIRMED":
        raise ValidationError(
            "Only confirmed orders can be delivered."
        )

    order.status = "DELIVERED"
    order.save()


def restore_stock(order):
    for item in order.items.all():
        inv = item.product.inventory
        inv.quantity += item.quantity
        inv.save()