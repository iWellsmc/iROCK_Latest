from django.db import models


class CompleteReport(models.Model):
    id = models.AutoField(primary_key=True)
    reportname=models.CharField(max_length=255,blank=True, null=True)
    period=models.CharField(max_length=255,blank=True, null=True)
    gettodate=models.DateField(blank=True,null=True)
    getfromdate=models.DateField(blank=True,null=True)
    country=models.CharField(max_length=255,blank=True, null=True)
    project=models.CharField(max_length=255,blank=True, null=True)
    discipline=models.CharField(max_length=255,blank=True, null=True)
    service=models.CharField(max_length=255,blank=True, null=True)
    vendor=models.CharField(max_length=255,blank=True, null=True)
    currency=models.IntegerField(blank=True, null=True)
    approvalstatus=models.CharField(max_length=255,blank=True, null=True)
    paymentstatus=models.CharField(max_length=255,blank=True, null=True)
    ageingperiod=models.CharField(max_length=255,blank=True, null=True)
    invoiceid=models.CharField(max_length=255,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    reporttype=models.IntegerField(blank=True,null=True)
    ranklist=models.CharField(max_length=255,blank=True, null=True)
    exceptions=models.CharField(max_length=255,blank=True, null=True)
    amountfilter=models.CharField(max_length=255,blank=True, null=True)
    status=models.BooleanField(default=True) 
   
class starredreport(models.Model):
    reportname=models.CharField(max_length=255,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    starred=models.BooleanField(default=True)

class PaymentAccount(models.Model):
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    currency=models.ForeignKey("custom_auth.BaseCountries",verbose_name="currency",on_delete=models.CASCADE,blank=True, null=True)
    amount=models.FloatField(blank=True,null=True)
    remaining_amount=models.IntegerField(blank=True,null=True,default=0)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    paymentfile=models.FileField(upload_to ='payment_account/',blank=True,null=True,default=None)
    status=models.IntegerField(default=True) #1-Saved #0 - Deleted #2-Draft
   
class PaymentAccount_PaidInvoice(models.Model):
    invoice=models.ForeignKey("InvoiceCostInvoice",on_delete=models.CASCADE,blank=True, null=True)
    payment=models.ForeignKey("PaymentAccount",on_delete=models.CASCADE,blank=True, null=True)
    date=models.DateTimeField(editable=True,blank=True, null=True)
    status=models.BooleanField(default=True,blank=True, null=True) #Status=1 is Allocated


    



