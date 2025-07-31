from django.db import models


class PaymentManager(models.Manager):
    def get_by_payment(self,id):
        """
        Return Multiple Objects from generate_payment Model
        """
        return self.filter(invoicecost__invoice_id=id,status=True)
    
    def get_by_payment_id(self,invoice_id,pk):
        """
        Return Multiple Objects from generate_payment Model
        """
        return self.filter(id=pk,invoicecost__invoice_id=invoice_id,status=True)
    def get_by_id(self,id):
        """
        Return Single Object from generate_payment Model
        """
        return self.get(id=id)
    
    def update_verification_status(self,id,verified_status):
        return self.filter(id=id).update(verified_status=verified_status)
    
    def sequence_number_exists(self,sequence):
        return self.filter(pi_number=sequence).exists()
    
    def get_all_inv_cost(self,invoicecost):
        return self.filter(invoicecost_id__in=invoicecost,status=True)
    
    def get_verified_instruction(self,invoice_id,verified_status):
        return self.filter(invoicecost__invoice_id=invoice_id,verified_status=verified_status,status=True)
    
    def get_by_invcostid(self,inv_cost_id,id):
        return self.filter(invoicecost_id=inv_cost_id,status=True,id__in=id).first()

    def check_verification_code(self,id,verification_code):
        return self.filter(id=id,verification_code=verification_code).first()

# class BaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True,related_name="%(app_label)s_%(class)s_created_by",auto_created=True)
#     updated_by=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True,related_name="%(app_label)s_%(class)s_updated_by")

#     class Meta:
#         abstract = True 

class PaymentInstruction(models.Model):
    """Payment Instruction Model"""
    id = models.AutoField(primary_key=True)
    invoicecost=models.ForeignKey('InvoiceCostInvoice',on_delete=models.CASCADE,blank=True,null=True)
    companybank=models.ForeignKey('finance.CompanyBank',on_delete=models.CASCADE,blank=True,null=True)
    masterbank=models.ForeignKey('finance.UserBankMaster',on_delete=models.CASCADE,blank=True,null=True)
    # companyuserstatus=1 default ,companyuserstatus = 2 bankuser present , companyuserstatus=3 bankuser not present
    companyuserstatus=models.IntegerField(blank=True,null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    pi_number = models.CharField(max_length=20,unique=True,blank=True,null=True)
    pi_file = models.FileField(upload_to='payment_instruction/',blank=True,null=True)
    payment_percentage = models.IntegerField(blank=True,null=True)
    payable_amount = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    pending_amount = models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_editable=models.BooleanField(default=True)
    status=models.BooleanField(default=True)
    verified_status=models.IntegerField(blank=True,null=True,default=0)
    invoice_type=models.IntegerField(blank=True,null=True,default=0)
    bankuser_verification=models.IntegerField(blank=True,null=True,default=0)
    payment_count=models.IntegerField(blank=True,null=True,default=1)
    percentage_confirm=models.BooleanField(default=False)
    verification_code=models.CharField(max_length=10,verbose_name="verification_code", blank=True, null=True)
    verified_bank_user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    #payment_status = 1 if unpaid, payment_status = 2 confirmed for payment , payment_status = 3 for paid
    payment_status=models.IntegerField(blank=True,null=True,default=1)
    new_payment_status=models.IntegerField(blank=True,null=True,default=1)
    objects=PaymentManager()
    original_file_name=models.CharField(max_length=100,blank=True,null=True)
    def save(self, *args, **kwargs):
        if self.pi_file:
            self.original_file_name = self.pi_file.name
        super(PaymentInstruction, self).save(*args, **kwargs)