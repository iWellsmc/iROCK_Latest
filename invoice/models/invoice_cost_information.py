from django.db import models

class InvoiceCostInformationManager(models.Manager):
    def upload_invoice_files(self,pk,get_total_value,grossamountwithdis,totalexclusivetax,totalalltax,paymentterm,vendor_id,contractid):
        return self.create(invoice_id=pk,total_invoice_value=get_total_value,total_discount_value=grossamountwithdis,total_exclusive_value=totalexclusivetax,finalvalue=totalalltax,payment_terms_id=paymentterm,vendor_id=vendor_id,contractid=contractid)
    
    def getinvoice_cost_information(self,pk):
        return self.filter(invoice_id=pk).first()
    
    def get_invoice_id(self,id,status):
        """
        Return Multiple Objects 
        """
        return self.filter(invoice_id=id,status=status)

    def create_invoicecostinformation(self,pk,get_total_value,grossamountwithdis,totalexclusivetax,totalalltax,paymentterm,getvendordetails,contractid,others):
        return self.create(invoice_id=pk,total_invoice_value=get_total_value,total_discount_value=grossamountwithdis,total_exclusive_value=totalexclusivetax,finalvalue=totalalltax,payment_terms_id=paymentterm,vendor_id=getvendordetails,contractid=contractid,total_after_otherdetails=others)
    
   
class InvoiceCostInformation(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    total_invoice_value=models.CharField(max_length=20,verbose_name="total invoice value", blank=True, null=True)
    total_discount_value=models.CharField(max_length=20,verbose_name="total discount value", blank=True, null=True)
    total_after_otherdetails=models.CharField(max_length=20,verbose_name="total other details value", blank=True, null=True)
    total_exclusive_value=models.CharField(max_length=20,verbose_name="total exclusive value", blank=True, null=True)
    finalvalue=models.CharField(max_length=20,verbose_name="final value", blank=True, null=True)
    payment_terms=models.ForeignKey("projects.VendorPaymentTerms",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    exchangerate_confirm_status=models.IntegerField(blank=True,null=True,default=0)
    tax_confirm_status=models.IntegerField(blank=True,null=True,default=0)
    deductions=models.IntegerField(blank=True,null=True,default=0)
    additions=models.IntegerField(blank=True,null=True,default=0)

    status=models.IntegerField(blank=True, null=True,default=1)
    objects=InvoiceCostInformationManager()