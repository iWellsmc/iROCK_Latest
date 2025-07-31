from django.db import models

class DiscountModel(models.Manager):
    def get_invoice_id(self,id,status):
        """
        Return Multiple Objects 
        """
        return self.filter(invoice_id=id,status=status)

class InvoiceDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    discount_name=models.CharField(max_length=255,blank=True, null=True)
    discount_type=models.CharField(max_length=255,blank=True, null=True)
    discount_value=models.CharField(max_length=255,blank=True, null=True)
    discount_calculated_value=models.CharField(max_length=255,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    objects=DiscountModel()

class InvoiceOthersAmount(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    description=models.CharField(max_length=255,blank=True, null=True)
    amount=models.CharField(max_length=255,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
