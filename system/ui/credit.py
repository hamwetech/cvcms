from django.contrib import admin

from system.models import Credit, CreditRepayment


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'credit_type', 'amount', 'status', 'issued_date', 'due_date')
    list_filter = ('credit_type', 'status')
    search_fields = ('farmer__name',)

@admin.register(CreditRepayment)
class CreditRepaymentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'amount', 'repayment_date', 'method')
    list_filter = ('method',)