from django.db import models

class PaymentHistory(models.Model):
    id=models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True,default=1)
    currency=models.ForeignKey("Basecountries",on_delete=models.CASCADE,blank=True, null=True)
    amount=models.CharField(max_length=255,blank=True, null=True)
    invoicedate=models.CharField(max_length=255,blank=True, null=True)
    invoicenumber=models.CharField(max_length=255,blank=True, null=True)
    file=models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)

class PaymentHistoryFile(models.Model):
    id=models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    file=models.FileField(upload_to ='uploads/',blank=True,null=True)
    status=models.IntegerField(blank=True,default=1)
    payment_history = models.ForeignKey("PaymentHistory",on_delete=models.CASCADE,blank=True, null=True)