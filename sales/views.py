from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import OrderFilter
from .models import Dealer, Inventory, InventoryAdjustment, Order, Product
from .serializers import (
    DealerSerializer,
    InventorySerializer,
    OrderSerializer,
    ProductSerializer,
)
from .services import confirm_order, deliver_order, restore_stock


class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DealerListCreateView(APIView):
    def get(self, request):
        dealers = Dealer.objects.all()
        serializer = DealerSerializer(dealers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DealerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DealerDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Dealer, pk=pk)

    def get(self, request, pk):
        dealer = self.get_object(pk)
        serializer = DealerSerializer(dealer)
        return Response(serializer.data)

    def put(self, request, pk):
        dealer = self.get_object(pk)
        serializer = DealerSerializer(dealer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        dealer = self.get_object(pk)
        serializer = DealerSerializer(dealer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        dealer = self.get_object(pk)
        dealer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreateView(APIView):
    def get(self, request):
        queryset = Order.objects.all().order_by("-created_at")
        order_filter = OrderFilter(request.GET, queryset=queryset)

        if not order_filter.is_valid():
            return Response(order_filter.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order_filter.qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)

        if order.status != "DRAFT":
            return Response(
                {"error": "Only draft orders can be edited."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        order = self.get_object(pk)

        if order.status != "DRAFT":
            return Response(
                {"error": "Only draft orders can be edited."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order.status == "CONFIRMED":
            restore_stock(order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderConfirmView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        confirm_order(order)
        return Response({"message": "Order confirmed"})


class OrderDeliverView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        deliver_order(order)
        return Response({"message": "Order delivered"})


class InventoryListCreateView(APIView):
    def get(self, request):
        inventories = Inventory.objects.all()
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryDetailView(APIView):
    def get_object(self, product_id):
        return get_object_or_404(Inventory, product_id=product_id)

    def get(self, request, product_id):
        inventory = self.get_object(product_id)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    def put(self, request, product_id):
        inventory = self.get_object(product_id)
        return self._update_inventory(inventory, request.data)

    def patch(self, request, product_id):
        inventory = self.get_object(product_id)
        return self._update_inventory(inventory, request.data)

    def delete(self, request, product_id):
        inventory = self.get_object(product_id)
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update_inventory(self, inventory, payload):
        new_quantity = payload.get("quantity")

        if new_quantity is None:
            return Response(
                {"error": "Quantity field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_quantity = int(new_quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        change = new_quantity - inventory.quantity
        inventory.quantity = new_quantity
        inventory.save()

        InventoryAdjustment.objects.create(
            inventory=inventory,
            change=change,
            reason="Manual stock update",
            updated_by="admin",
        )

        return Response(
            {
                "message": "Inventory updated successfully",
                "new_stock": inventory.quantity,
                "change": change,
            }
        )
