from django.db import models
from django.db.models import Count,Sum,DecimalField
from django.db.models.functions import Cast


class InvoiceCostInvoiceManager(models.Manager):
    def create_invoicecost(self,pk,invoiceid,invoicesplit,num,get_convert_date,per,base,payment,exchange,final,bank,todaydate,vendor_id,invoicecurrency,contractid):
        return self.create(invoice_id=pk,vendor_invoice_id=invoiceid,invoice_payment=invoicesplit,invoice_number=num,invoice_date=get_convert_date,invoice_percentage=per,invoice_base_amount=base,invoice_currency=payment,invoice_exchange_rate=exchange,invoice_total_amount=final,invoice_bank_id=bank,invoice_submission_date=todaydate,vendor_id=vendor_id,currency_id=invoicecurrency,contractid=contractid)
    
    def get_invoice_id(self,id,status):
        """
        Return Multiple Objects 
        """
        return self.filter(invoice_id=id,status=status)
    
    def get_id(self,id):
        return self.get(id=id)
    
    def update_verification_code(self,id,verification_code):
        return self.filter(id=id).update(verification_code=verification_code)
    def check_verification_code(self,id,verification_code):
        return self.filter(id=id,verification_code=verification_code).first()
    
    def groupinvoice_by_currency(self,vendor_id):
        return self.filter(vendor_id=vendor_id,invoice__approval_status=1).values('invoice_currency').annotate(currency_count=Count('invoice_currency'))

    def groupawaitinginvoice_by_currency(self,vendor_id):
        return self.filter(vendor_id=vendor_id,invoice__approval_status=0,invoice__invoice_status=2,approval_status=1).values('invoice_currency').annotate(currency_count=Count('invoice_currency'))
    
    def groupdisputedinvoice_by_currency(self,vendor_id):
        return self.filter(vendor_id=vendor_id,invoice__invoice_status=6,approval_status=6).values('invoice_currency').annotate(currency_count=Count('invoice_currency'))
    
    def getinvoice_by_currency(self,vendor_id,currency,project_id=None):
        query=self.filter(vendor_id=vendor_id,invoice__approval_status=1,invoice_currency=currency)
        if project_id:
            query = query.filter(invoice__project_id=project_id)
        return query
    
    def getallawaiting_invoice_by_currency_and_projectid(self,vendor_id,currency,project_id):
        return self.filter(vendor_id=vendor_id,invoice__approval_status=0,invoice__invoice_status=2,approval_status=1,invoice_currency=currency,invoice__project_id=project_id)
    
    def getalldisputed_invoice_by_currency_and_projectid(self,vendor_id,currency,project_id):
        return self.filter(vendor_id=vendor_id,invoice__invoice_status=6,approval_status=6,invoice_currency=currency,invoice__project_id=project_id)
    
    def getallcurrencies_by_vendor(self,vendor_id):
        return self.filter(vendor_id=vendor_id).values('invoice_currency').annotate(currency_count=Count('invoice_currency'))

    def getallinvoice_by_currency_vendor(self,vendor_id,currencies,project_id,country_ids,default_currency):
        queryset=self.filter(vendor_id=vendor_id)
        if len(currencies) > 0:
            queryset=queryset.filter(invoice_currency__in=currencies)
        if len(project_id) > 0:
            queryset=queryset.filter(invoice__project_id__in=project_id)
        if len(country_ids) > 0:
            queryset=queryset.filter(invoice__project__country_id__in=country_ids)
        if len(currencies) == 0:
            queryset=queryset.filter(invoice_currency=default_currency)

        return queryset 

class InvoiceCostInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    vendor_invoice=models.ForeignKey("projects.VendorInvoiceSplit",on_delete=models.CASCADE,blank=True, null=True)
    invoice_payment=models.CharField(max_length=255,blank=True, null=True)
    invoice_number=models.CharField(max_length=255,blank=True, null=True)
    invoice_date=models.CharField(max_length=255,blank=True, null=True)
    invoice_percentage=models.CharField(max_length=255,blank=True, null=True)
    invoice_base_amount=models.CharField(max_length=255,blank=True, null=True)
    invoice_currency=models.CharField(max_length=255,blank=True, null=True)
    currency=models.ForeignKey("custom_auth.BaseCountries",verbose_name="currency",on_delete=models.CASCADE,blank=True, null=True)
    invoice_exchange_rate=models.CharField(max_length=255,blank=True, null=True)
    invoice_total_amount=models.CharField(max_length=255,blank=True, null=True)
    invoice_bank=models.ForeignKey("projects.BankDetails",on_delete=models.CASCADE,blank=True, null=True)
    invoice_submission_date=models.DateTimeField(editable=True,blank=True, null=True)
    invoice_resubmission_date=models.DateTimeField(editable=True,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    approval_status=models.IntegerField(blank=True, null=True,default=1)
    approval_date=models.DateTimeField(editable=True,blank=True, null=True)
    disputed_date=models.DateTimeField(editable=True,blank=True, null=True)
    payment_status=models.IntegerField(blank=True, null=True,default=1)#payment status =2 paid
    payment_date=models.DateTimeField(editable=True,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True, blank=True,null=True)
    verification_code=models.CharField(max_length=10,verbose_name="verification_code", blank=True, null=True)
    payment_account=models.IntegerField(default=False,blank=True, null=True)#1Allocated to payment on Account #2Draft for payment on Account
    paid_inbetween=models.BooleanField(default=False,blank=True,null=True)
    verified_bank_user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    new_netpayable=models.CharField(max_length=255,blank=True, null=True)
    partial_status=models.IntegerField(blank=True, null=True,default=1)
    total_inclusive_percentage=models.CharField(max_length=255,blank=True, null=True)
    total_inclusive_amount=models.CharField(max_length=255,blank=True, null=True)
    objects=InvoiceCostInvoiceManager()


class InvoiceExceptionalManager(models.Manager):
    def get_by_invoice(self,invoice_id):
        return
class InvoiceExceptional(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    exceptional_type = models.IntegerField(blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    confirm_dispute=models.IntegerField(blank=True, null=True,default=0)
    checked_messages = models.TextField(blank=True, null=True)
    query_status=models.IntegerField(blank=True, null=True,default=0)
    return_status=models.IntegerField(blank=True, null=True,default=0)
    objects=InvoiceExceptionalManager()