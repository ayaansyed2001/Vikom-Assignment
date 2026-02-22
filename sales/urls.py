from django.urls import path
from .views import (
    DealerDetailView,
    DealerListCreateView,
    InventoryDetailView,
    InventoryListCreateView,
    OrderConfirmView,
    OrderDeliverView,
    OrderDetailView,
    OrderListCreateView,
    ProductDetailView,
    ProductListCreateView,
)

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),

    path("dealers/", DealerListCreateView.as_view(), name="dealer-list"),
    path("dealers/<int:pk>/", DealerDetailView.as_view(), name="dealer-detail"),

    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/confirm/", OrderConfirmView.as_view(), name="order-confirm"),
    path("orders/<int:pk>/deliver/", OrderDeliverView.as_view(), name="order-deliver"),

    path("inventory/", InventoryListCreateView.as_view(), name="inventory-list"),
    path("inventory/<int:product_id>/", InventoryDetailView.as_view(), name="inventory-detail"),
]
