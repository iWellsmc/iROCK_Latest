from django.db import models
from datetime import datetime

class Payment_Account(models.Model):
    vendor=models.ForeignKey('projects.ContractMasterVendor',on_delete=models.CASCADE,blank=True, null=True)
    dateofsubmission=models.DateTimeField(editable=True,blank=True, null=True)
    upload_file=models.FileField(blank=True,null=True)
