from django.db import models
from datetime import datetime

class PaymentReceiptManager(models.Manager):
    current_date=datetime.now()
    def create_data(self,company_id,invoice,invoice_cost,user,current_date=current_date):
        return self.create(company_id=company_id,invoice_id=invoice,invoice_cost_id=invoice_cost,created_at=current_date,user_id=user)
    
    def get_by_invcost(self,invcost_id):
        return self.filter(invoice_cost_id=invcost_id)
    
    def get_by_payment(self,payment_instruct):
        return self.filter(payment_instruct_id=payment_instruct)
    
    def filter_by_inv_user(self,inv_id,user_id):
        return self.filter(invoice_id=inv_id,user_id=user_id)
    
class PaymentReceipt(models.Model):
    id = models.AutoField(primary_key=True)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    invoice_cost=models.ForeignKey('InvoiceCostInvoice',on_delete=models.CASCADE,blank=True,null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    created_at=models.DateTimeField(editable=True,null=True)
    status=models.BooleanField(default=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    payment_instruct=models.ForeignKey('PaymentInstruction',on_delete=models.CASCADE,blank=True,null=True)
    objects=PaymentReceiptManager()


class PaymentReceiptFileManager(models.Manager):
    current_date=datetime.now()
    def create_file_data(self,payment_receipt,payment_percentage,payment_receipt_file ,current_date):
        return self.create(payment_receipt_id=payment_receipt,payment_percentage=payment_percentage,payment_receipt_file=payment_receipt_file,original_file_name=payment_receipt_file.name,created_at=current_date)
    
class PaymentReceiptFile(models.Model):
    id = models.AutoField(primary_key=True)
    payment_percentage=models.CharField(max_length=50, null=True, blank=True)
    payment_receipt=models.ForeignKey("PaymentReceipt",on_delete=models.CASCADE,blank=True, null=True)
    payment_receipt_file = models.FileField(upload_to='payment_receipt/',blank=True,null=True)
    original_file_name = models.CharField(max_length=255, blank=True, null=True)
    created_at=models.DateTimeField(editable=True,null=True)
    status=models.BooleanField(default=True)
    objects=PaymentReceiptFileManager()