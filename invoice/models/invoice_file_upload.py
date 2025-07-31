from django.db import models

class InvoiceFileUploadManager(models.Manager):
    def upload_invoice_files(self,workcompletevalue,pk,getinvoicefiles,invoiceid,vendor_id,support,file_name,contractid=None):
        print(getinvoicefiles,"INVOICE FILES")
        return self.create(work_completion=workcompletevalue,invoice_id=pk,support=support,support_file=getinvoicefiles,invoicecostinvoice_id=invoiceid,vendor_id=vendor_id,contractid=contractid,file_name=file_name)
    
    def getuploaded_files(self,pk,list_cost_ids):
        return self.filter(invoice_id=pk,invoicecostinvoice_id__in=list_cost_ids,status=1)
    
    def update_status(self,pk,new_list):
        return self.filter(invoice_id=pk).exclude(id__in=new_list).update(status=0)
    
    def get_invoice_id(self,id,status,invoicecostinvoice):
        """
        Return Multiple Objects 
        """
        return self.filter(invoice_id=id,status=status,invoicecostinvoice=invoicecostinvoice)
    
   
class InvoiceFileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    work_completion=models.CharField(max_length=255,blank=True, null=True)
    support=models.CharField(max_length=255,blank=True, null=True)
    support_file=models.FileField(upload_to="invoicedocuments",blank=True,null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    invoicecostinvoice=models.ForeignKey("InvoiceCostInvoice",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    filetype=models.CharField(max_length=20,blank=True, null=True)
    file_name=models.CharField(max_length=255,blank=True,null=True)
    # return_status=1 - invoice submission files  return_status=2 - returns upload files
    return_status=models.IntegerField(blank=True, null=True,default=1)
    objects=InvoiceFileUploadManager()
    