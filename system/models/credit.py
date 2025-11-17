import calendar
from datetime import date
from django.utils import timezone

# from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from conf.models import District, County, SubCounty, Parish, Product, Crop, ProductVariation
from system.models.modelmixin import TimeStampMixin
from . import Farmer
from .land import land_upload_path

User = settings.AUTH_USER_MODEL


class Credit(TimeStampMixin):
    CREDIT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('produce', 'Produce'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="credits")
    credit_type = models.CharField(max_length=20, choices=CREDIT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    produce_type = models.CharField(max_length=100, blank=True, null=True)  # e.g., maize, milk
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # %
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    issued_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'credit'
        verbose_name_plural = 'Credit'

    def __str__(self):
        return f"{self.farmer.name} - {self.credit_type} - {self.amount}"

    @property
    def total_due(self):
        """Calculate total due including interest"""
        if self.interest_rate > 0:
            return self.amount + (self.amount * self.interest_rate / 100)
        return self.amount

    @property
    def total_paid(self):
        """Sum of all repayments"""
        return sum(r.amount_paid for r in self.repayments.all())

    @property
    def balance(self):
        return self.total_due - self.total_paid

    def update_status(self):
        if self.balance <= 0:
            self.status = 'paid'
        elif self.due_date < timezone.now().date():
            self.status = 'overdue'
        else:
            self.status = 'active'
        self.save()


class CreditRepayment(TimeStampMixin):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    repayment_date = models.DateField(default=timezone.now)
    method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('produce', 'Produce')])
    produce_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'credit_repayment'
        verbose_name_plural = 'Credit Repayment'

    def __str__(self):
        return f"Repayment {self.amount} for {self.credit.farmer.name}"

    @property
    def remaining_balance(self):
        return self.credit.total_due - sum(r.amount for r in self.credit.repayments.all())