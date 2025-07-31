from django.db import models

class CreditNoteManager(models.Manager):
    def getcreditnote_by_vendor(self,vendor_id):
        return self.filter(vendor_id=vendor_id,status=1).order_by('-id')
    def getcreditnote_by_creditstatus(self,vendor_id):
        return self.filter(vendor_id=vendor_id,status=1,credit_status=2).order_by('-id')
    def getcreditnote_by_id(self,credit_note_id):
        return self.get(id=credit_note_id,status=1)
    
class CreditNote(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    total_value=models.CharField(max_length=255,blank=True, null=True)
    exclusive_value=models.CharField(max_length=255,blank=True, null=True)
    total_value_excluisve_tax=models.CharField(max_length=255,blank=True, null=True)
    contract=models.ForeignKey("projects.ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment=models.ForeignKey("projects.Amendment",on_delete=models.CASCADE,blank=True, null=True)
    contracttype=models.CharField(max_length=255,verbose_name="contract type", blank=True, null=True)
    credit_status=models.SmallIntegerField(blank=True, null=True,default=1)
    approval_status=models.IntegerField(blank=True, null=True,default=1)
    #approval_status == 1 --approval INprogess, approval_status == 2 ---rejected , approval_status == 3 --returned, approval_status ==4 -- approved
    approval_date=models.DateTimeField(editable=True,blank=True, null=True)
    # invoice = models.ForeignKey("invoice.invoice",on_delete=models.CASCADE,blank=True, null=True,related_name='invoice')
    total_invoice_value=models.FloatField(max_length=50,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    usage_status=models.IntegerField(blank=True, null=True,default=1)
    history_status=models.IntegerField(blank=True, null=True,default=1)
    check_for_pending=models.BooleanField(blank=True,null=True,default=True)
    created_at=models.DateTimeField(editable=True,null=True,blank=True)
    dispute_status=models.IntegerField(blank=True, null=True,default=0)
    grossamnt_withoutexclusive=models.CharField(max_length=255, blank=True, null=True)
    objects=CreditNoteManager()

    # credit_note=models.Manager()

class CreditNoteExclusive(models.Model):
    id = models.AutoField(primary_key=True)
    credit=models.ForeignKey("CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    exclusive=models.ForeignKey("projects.VendorCompanyTaxPercentage",on_delete=models.CASCADE,blank=True, null=True)
    created_vendor=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    exclusive_percentage=models.CharField(max_length=10,blank=True, null=True)
    exclusive_calculated_value=models.CharField(max_length=255,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)

class CreditSupportDocumentsManager(models.Manager):
    def getsupportdocuments_by_creditnote_id(self,credit_note_id):
        return self.filter(credit_id=credit_note_id,status=1)
   


class CreditSupportDocuments(models.Model):
    id = models.AutoField(primary_key=True)
    credit=models.ForeignKey("CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    file=models.FileField(upload_to="creditdocuments",blank=True,null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    filetype=models.CharField(max_length=20,blank=True, null=True)
    objects=CreditSupportDocumentsManager()
    original_file_name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Save the original file name before saving the model instance
        if self.file and not self.original_file_name:
            self.original_file_name = self.file.name
        super().save(*args, **kwargs)

