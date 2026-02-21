from django.db import models
from accounts.models import SearchSession

class PaymentTransaction(models.Model):
    """
    Tracks Razorpay payment transactions for auditing and debugging.
    """
    search_session = models.ForeignKey(
        SearchSession,
        on_delete=models.CASCADE,
        related_name='payment_transactions',
        null=True,
        blank=True
    )
    
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    
    amount = models.IntegerField(null=True, blank=True)  # Amount in paise
    currency = models.CharField(max_length=10, default='INR')
    
    status = models.CharField(max_length=50, default='created')  
    # Possible statuses could be: 'created', 'authorized', 'captured', 'failed', 'refunded', etc.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id} - {self.status}"

