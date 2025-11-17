from django.contrib import admin

from system.models.order import Supplier, Category, Order, OrderItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    min_num = 1
    fields = ("item", "quantity", "unit_price", "price")
    readonly_fields = ("price",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('item')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_reference", "farmer", "order_price", "status", "order_date")
    list_filter = ("status", "order_date", "farmer")
    search_fields = ("order_reference", "farmer__name")

    readonly_fields = (
        "order_reference",
        "order_price",
        "accept_date",
        "reject_date",
        "ship_date",
        "delivery_accept_date",
        "delivery_reject_date",
        "collect_date",
    )

    inlines = [OrderItemInline]

    fieldsets = (
        ("Order Details", {
            "fields": ("farmer", "order_reference", "order_date", "status"),
        }),
        # ("Order Processing", {
        #     "classes": ("collapse",),
        #     "fields": (
        #         "accept_date",
        #         "reject_date",
        #         "reject_reason",
        #         "ship_date",
        #         "delivery_accept_date",
        #         "delivery_reject_date",
        #         "delivery_reject_reason",
        #         "collect_date",
        #     ),
        # }),
        # ("Total", {
        #     "fields": ("order_price",),
        # }),
    )