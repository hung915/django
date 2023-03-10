from typing import Any
from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low")
        ]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    # fields = [""]
    # exclude = []
    # readonly_fields = []
    autocomplete_fields = ["collection"]
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ["title", "unit_price", "slug", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InventoryFilter]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "LOW"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer_name"]
    # list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["customer"]

    def customer_name(self, order):
        return order.customer.first_name + " " + order.customer.last_name


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products"]
    list_per_page = 10
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + "?"
            + urlencode(
                {'collection__id': collection.id}
            )
        )
        return format_html("<a href={}>{}</a>", url, collection.products_count)


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 10
    search_fields = ["first_name", "last_name"]

    @admin.display(ordering="orders_count")
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + "?"
            + urlencode(
                {'customer__id': customer.id}
            )
        )
        return format_html("<a href={}>{}</a>", url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count("order")
        )
# admin.site.register(models.Product, ProductAdmin)
