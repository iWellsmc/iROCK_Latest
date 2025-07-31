from django.db import models

class CreditNoteMapping(models.Model):
  id=models.AutoField(primary_key=True)
  credit_note=models.ForeignKey('credit_note.CreditNote',on_delete=models.CASCADE,blank=True, null=True)
  user=models.ForeignKey('custom_auth.User',on_delete=models.CASCADE,blank=True, null=True)
  company=models.ForeignKey('custom_auth.Companies',on_delete=models.CASCADE,blank=True, null=True)
  invoice=models.ForeignKey('Invoice',on_delete=models.CASCADE,blank=True, null=True)
  status=models.BooleanField(default=True,blank=True,null=True)


class CreditNoteMappingBase(models.Model):
  id=models.AutoField(primary_key=True)
  invoice=models.ForeignKey('Invoice',on_delete=models.CASCADE,blank=True, null=True)
  invoice_split=models.ForeignKey('projects.VendorInvoiceSplit',on_delete=models.CASCADE,blank=True, null=True)
  credit_note=models.ForeignKey('credit_note.CreditNote',on_delete=models.CASCADE,blank=True, null=True)
  credit_note_split=models.ForeignKey('credit_note.CreditNoteContractInvoice',on_delete=models.CASCADE,blank=True, null=True)
  credit_note_value=models.CharField(max_length=255, blank=True, null=True)
  credit_payable=models.CharField(max_length=255, blank=True, null=True)
  pending_credit_value=models.CharField(max_length=255, blank=True, null=True)
  user=models.ForeignKey('custom_auth.User',on_delete=models.CASCADE,blank=True, null=True)
  company=models.ForeignKey('custom_auth.Companies',on_delete=models.CASCADE,blank=True, null=True)
  status=models.BooleanField(default=True,blank=True,null=True)
  