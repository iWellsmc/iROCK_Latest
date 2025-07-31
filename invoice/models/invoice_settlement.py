from django.db import models

class SettlementInvoice(models.Model):
  id = models.AutoField(primary_key=True)
  invoice=models.ForeignKey('Invoice',on_delete=models.CASCADE,blank=True, null=True)
  invoicecostinvoice=models.ForeignKey('InvoiceCostInvoice',on_delete=models.CASCADE,blank=True, null=True)
  accepted_percentage=models.CharField(max_length=255,blank=True, null=True)
  disputed_percentage=models.CharField(max_length=255,blank=True, null=True)
  invoicevalue_accepted=models.CharField(max_length=255,blank=True, null=True)
  invoice_value=models.CharField(max_length=255,blank=True, null=True)
  settlement=models.CharField(max_length=255,blank=True, null=True)
  invoicevalue_declined=models.CharField(max_length=255,blank=True, null=True)
  user=models.ForeignKey('custom_auth.User',on_delete=models.CASCADE,blank=True, null=True)
  company=models.ForeignKey('custom_auth.companies',on_delete=models.CASCADE,blank=True,null=True)
  module=models.ForeignKey('InvoiceGuard.Module',on_delete=models.CASCADE,blank=True,null=True) 
  old_value=models.CharField(max_length=255,blank=True, null=True)
  #if vendor accepts settlement acceptance_status=2, if declined acceptance_status = 3
  acceptance_status=models.IntegerField(default=1,blank=True,null=True)
  status=models.BooleanField(default=True,blank=True,null=True)
