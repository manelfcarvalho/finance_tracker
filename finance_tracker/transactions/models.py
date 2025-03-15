from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True, null=True)  # Única declaração
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.get_transaction_type_display()}: €{self.amount} ({self.category})"