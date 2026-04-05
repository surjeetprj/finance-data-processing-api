from django.db import models
from django.conf import settings

class FinancialRecord(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'INCOME','Income'
        EXPENCE = 'EXPENSE','Expense'
    
    # The user who created the record
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='finacial_records'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank = True,null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    category = models.CharField(max_length=100, help_text="e.g., Salary, Rent, Utilities")
    date = models.DateField()
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date','-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"
