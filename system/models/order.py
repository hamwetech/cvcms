from django.db import models
from django.utils import timezone
from conf.models import ProductUnit
from system.models import Farmer
from system.models.modelmixin import TimeStampMixin


class Supplier(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'supplier'

    def __unicode__(self):
        return self.name


class Category(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'category'

    def __unicode__(self):
        return self.name


class Item(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.ForeignKey(ProductUnit, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'item'

    def __unicode__(self):
        return self.name


class Order(TimeStampMixin):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('DELIVERY_REJECTED', 'Delivery Rejected'),
        ('COLLECTED', 'Collected'),
        ('PAID', 'Fully Paid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
    ]

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    order_reference = models.CharField(max_length=255, blank=True, editable=False)
    order_price = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='PENDING')
    order_date = models.DateTimeField(default=timezone.now)

    accept_date = models.DateTimeField(null=True, blank=True)
    reject_date = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=120, null=True, blank=True)

    ship_date = models.DateTimeField(null=True, blank=True)

    delivery_accept_date = models.DateTimeField(null=True, blank=True)
    delivery_reject_date = models.DateTimeField(null=True, blank=True)
    delivery_reject_reason = models.CharField(max_length=120, null=True, blank=True)

    collect_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'member_order'

    def __str__(self):
        return self.order_reference or ""

    # Auto-generate reference on save
    def save(self, *args, **kwargs):
        if not self.order_reference:
            self.order_reference = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}-{self.farmer.id}"
        super().save(*args, **kwargs)

    def get_orders(self):
        return OrderItem.objects.filter(order=self)

    @property
    def total(self):
        return sum(item.price for item in self.items.all())

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def balance(self):
        return self.total - self.total_paid

    def accept(self):
        self.status = 'ACCEPTED'
        self.accept_date = timezone.now()
        self.save()

    def reject(self, reason):
        self.status = 'REJECTED'
        self.reject_date = timezone.now()
        self.reject_reason = reason
        self.save()

    def ship(self):
        self.status = 'SHIPPED'
        self.ship_date = timezone.now()
        self.save()

    def accept_delivery(self):
        self.status = 'DELIVERED'
        self.delivery_accept_date = timezone.now()
        self.save()

    def reject_delivery(self, reason):
        self.status = 'DELIVERY_REJECTED'
        self.delivery_reject_date = timezone.now()
        self.delivery_reject_reason = reason
        self.save()

    def collect(self):
        self.status = 'COLLECTED'
        self.collect_date = timezone.now()
        self.save()

    def update_payment_status(self):
        if self.balance <= 0:
            self.status = 'PAID'
        elif self.total_paid > 0:
            self.status = 'PARTIALLY_PAID'
        else:
            self.status = 'PENDING'
        self.save()


class OrderItem(TimeStampMixin):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

    class Meta:
        db_table = 'order_item'

    def __str__(self):
        return f"{self.item.name}"

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class OrderPayment(TimeStampMixin):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mobile_money', 'Mobile Money'),
    ]

    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=120, blank=True, null=True)  # Bank slip / MM ref
    notes = models.TextField(blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.order.order_reference} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_payment_status()