from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OtherDeductionsManager(models.Manager):
  def getotherdeduction_by_splitid(self,split_id):
    try:
      return self.get(invoice_split_id=split_id,status=1)
    except ObjectDoesNotExist:
        return ""
class OtherAdditionsManager(models.Manager):
  def getotheraddition_by_splitid(self,split_id):
    try:
      return self.get(invoice_split_id=split_id,status=1)
    except ObjectDoesNotExist:
        return ""


class OtherDeductions(models.Model):
  id=models.AutoField(primary_key=True)
  invoice=models.ForeignKey('Invoice',on_delete=models.CASCADE,blank=True, null=True)
  invoice_split=models.ForeignKey("InvoiceCostInvoice",on_delete=models.CASCADE,blank=True, null=True)
  company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
  description=models.CharField(max_length=255,blank=True, null=True)
  amount=models.CharField(max_length=30,blank=True, null=True)
  balance=models.CharField(max_length=40,blank=True, null=True)
  status=models.BooleanField(default=True,blank=True,null=True) 
  objects=OtherDeductionsManager()
  
class OtherAdditions(models.Model):
  id=models.AutoField(primary_key=True)
  invoice=models.ForeignKey('Invoice',on_delete=models.CASCADE,blank=True, null=True)
  invoice_split=models.ForeignKey("InvoiceCostInvoice",on_delete=models.CASCADE,blank=True, null=True)
  company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
  description=models.CharField(max_length=255,blank=True, null=True)
  amount=models.CharField(max_length=30,blank=True, null=True)
  balance=models.CharField(max_length=40,blank=True, null=True)
  status=models.BooleanField(default=True,blank=True,null=True) 
  objects=OtherAdditionsManager()
