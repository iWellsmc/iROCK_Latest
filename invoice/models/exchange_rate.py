from django.db import models


class PastExchangeRate(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("InvoiceCostInvoice",on_delete=models.CASCADE,blank=True, null=True)
    invoice_base_amount=models.CharField(max_length=255,blank=True, null=True)
    invoice_exchange_rate=models.CharField(max_length=255,blank=True, null=True)
    invoice_total_amount=models.CharField(max_length=255,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True, blank=True,null=True)
    status=models.BooleanField(default=True)