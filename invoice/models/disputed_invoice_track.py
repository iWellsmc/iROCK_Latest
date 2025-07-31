from django.db import models

class DisputedInvoiceTrack(models.Model):
  id = models.AutoField(primary_key=True)
  user=models.ForeignKey('custom_auth.User',on_delete=models.CASCADE,blank=True, null=True)
  invoice=models.ForeignKey('Invoice',on_delete=models.CASCADE,blank=True, null=True)
  credit=models.ForeignKey('credit_note.CreditNote',on_delete=models.CASCADE,blank=True, null=True)
  stage=models.IntegerField(default=1,blank=True,null=True)
  status=models.BooleanField(default=True,blank=True,null=True)
  reason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
  module=models.ForeignKey('InvoiceGuard.Module',on_delete=models.CASCADE,blank=True,null=True)
  created_at=models.DateTimeField(editable=True,blank=True, null=True)
  vendor_confirmation=models.IntegerField(default=0,blank=True,null=True)
  returned_count=models.IntegerField(default=0,blank=True,null=True)