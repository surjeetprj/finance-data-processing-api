from django.contrib import admin
from .models import FinancialRecord

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'amount', 'transaction_type', 'date']
    list_filter = ['transaction_type', 'category', 'date']
    search_fields = ['title', 'user__username']