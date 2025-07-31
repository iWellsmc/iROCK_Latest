from django.db import models

class InvoiceExclusiveManager(models.Manager):
    def get_by_id(self,id):
        """
        Return Multiple Objects from InvoiceExclusive Model
        """
        return self.filter(invoice_id=id,status=1)
    
class InvoiceExclusive(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    exclusive=models.ForeignKey("projects.VendorCompanyTaxPercentage",on_delete=models.CASCADE,blank=True, null=True)
    exclusive_calculated_value=models.CharField(max_length=255,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    tax_percentage=models.CharField(max_length=100, blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    objects=InvoiceExclusiveManager()