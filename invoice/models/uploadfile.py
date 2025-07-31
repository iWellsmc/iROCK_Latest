from django.db import models

class FileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_list = models.ForeignKey('InvoiceCostInvoice', on_delete=models.CASCADE, null=True,blank=True)
    file=models.FileField(blank=True)
