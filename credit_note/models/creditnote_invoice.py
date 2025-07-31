from django.db import models

class CreditNoteInvoiceManager(models.Manager):
    def getcreditnoteinvoice(self,credit_note_id):
        return self.filter(credit_id=credit_note_id,status=1).values_list('invoice_id',flat=True)
  

class CreditNoteInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    credit=models.ForeignKey("CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    invoice=models.ForeignKey("invoice.Invoice",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    objects=CreditNoteInvoiceManager()


class CreditNoteContractInvoiceManager(models.Manager):
    def getcreditnoteinvoice_by_creditnoteid(self,credit_note_id):
        return self.filter(credit_id=credit_note_id)
    
    def get_credit_notes_byvendor_currency_approvedstatus(self,vendor_id,currencies,company_id,status):
        return self.filter(symbol__in=currencies,credit__vendor_id=vendor_id,credit__credit_status=2,credit__company_id=company_id,credit__approval_status=status)
    
    def get_return_rejected_credit_notes_byvendor_currency(self,vendor_id,currencies,company_id):
        return self.filter(symbol__in=currencies,credit__vendor_id=vendor_id,credit__credit_status=2,credit__company_id=company_id,credit__approval_status__gte=2).exclude(credit__approval_status=4)
  
class CreditNoteContractInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    credit=models.ForeignKey("CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    vendor_split_invoice=models.ForeignKey("projects.VendorInvoiceSplit",on_delete=models.CASCADE,blank=True, null=True)
    currency_split=models.CharField(max_length=255,verbose_name="contract type", blank=True, null=True)
    percentage=models.CharField(max_length=255, blank=True, null=True)
    symbol=models.CharField(max_length=255, blank=True, null=True)
    credit_note_no=models.CharField(max_length=255,blank=True, null=True)
    date=models.DateTimeField(editable=True,blank=True, null=True)
    base_currency_amount=models.CharField(max_length=255,blank=True, null=True)
    exchange_rate=models.CharField(max_length=255,blank=True, null=True)
    payment_currency_amount=models.CharField(max_length=255,blank=True, null=True)
    file=models.FileField(upload_to="creditdocuments",blank=True,null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    pending_value=models.CharField(max_length=255,blank=True, null=True)
    payment_terms=models.ForeignKey("projects.VendorPaymentTerms",on_delete=models.CASCADE,blank=True, null=True)
    new_netpayable=models.CharField(max_length=255,blank=True, null=True)
    objects=CreditNoteContractInvoiceManager()
    original_file_name=models.CharField(max_length=255,blank=True, null=True)
    def save(self, *args, **kwargs):
        # Save the original file name before saving the model instance
        if self.file and not self.original_file_name:
            self.original_file_name = self.file.name
        super().save(*args, **kwargs)
