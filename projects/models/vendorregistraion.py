from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
from django.db.models import Q


class VendorRegistraion(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    invite_vendor= models.ForeignKey("VendorInvitationModel",verbose_name="Vendor Invitation Model",on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    contact_primary_title=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_primary_first_name=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_primary_middle_name=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_primary_last_name=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_secondary_title=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_secondary_first_name=models.CharField(max_length=50,verbose_name="primary full name", blank=True, null=True)
    contact_secondary_middle_name=models.CharField(max_length=50,verbose_name="primary full name", blank=True, null=True)
    contact_secondary_last_name=models.CharField(max_length=50,verbose_name="primary full name", blank=True, null=True)
    primary_designation=models.CharField(max_length=50,verbose_name="primary designation", blank=True, null=True)
    secondary_designation=models.CharField(max_length=50,verbose_name="secondary designation", blank=True, null=True)
    contact_primary_phone_code=models.CharField(max_length=255,verbose_name="official primary landline", blank=True, null=True)
    contact_primary_phone=models.CharField(max_length=255,verbose_name="official primary landline", blank=True, null=True)
    contact_primary_area_code=models.CharField(max_length=50,verbose_name="official secondary landline", blank=True, null=True)
    contact_secondary_area_code=models.CharField(max_length=50,verbose_name="official secondary landline", blank=True, null=True)
    contact_secondary_phone_code=models.CharField(max_length=50,verbose_name="official secondary landline", blank=True, null=True)
    contact_secondary_phone=models.CharField(max_length=50,verbose_name="official secondary landline", blank=True, null=True)
    contact_primary_mobile_code=models.CharField(max_length=50,verbose_name="official  pprimary mobile", blank=True, null=True)
    contact_primary_mobile=models.CharField(max_length=50,verbose_name="official  pprimary mobile", blank=True, null=True)
    contact_secondary_mobile_code=models.CharField(max_length=50,verbose_name="official secondary mobile", blank=True, null=True)
    contact_secondary_mobile=models.CharField(max_length=50,verbose_name="official secondary mobile", blank=True, null=True)
    vendor_name=models.CharField(max_length=255,verbose_name="Vendor Name", blank=True, null=True)
    country_of_operation= models.ForeignKey("custom_auth.BaseCountries",verbose_name="Country of operation",on_delete=models.CASCADE,blank=True, null=True)
    country_of_incorporation = models.ForeignKey("custom_auth.Countries",verbose_name="Country of incorporation",on_delete=models.CASCADE,blank=True, null=True)
    state=models.ForeignKey("custom_auth.States",verbose_name="State Name",on_delete=models.CASCADE,blank=True, null=True)
    official_primary_email = models.EmailField(max_length=100)
    official_secondary_email = models.EmailField(max_length=100)
    status = models.IntegerField(blank=True, null=True,default=0)
    RegisterNumber=models.CharField(max_length=255,verbose_name="Registered number in the Country Of Incorporation", blank=True, null=True)
    Address=models.TextField(max_length=255,verbose_name="vendor Company official address", blank=True, null=True)
    website=models.CharField(max_length=50,verbose_name="Vendor Company Website", blank=True, null=True)
    created_at = models.CharField(max_length=255,verbose_name="Vendor Company Website", blank=True, null=True)
    approver_status=models.IntegerField(blank=True, null=True,default=0)

class Vendorcompanyserviceinfo(models.Model):
    id = models.AutoField(primary_key=True)
    vendor=models.ForeignKey("VendorRegistraion",verbose_name="VendorRegistraion",on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    type_services=models.CharField(verbose_name="services",max_length=50, blank=True)
    nameofcontract=models.TextField(max_length=255,verbose_name="Name of contract", blank=True, null=True)
    abrigdge_scope_service=models.TextField(max_length=1000,verbose_name="abrigdge scope service", blank=True, null=True)
    contract_reference_number=models.TextField(max_length=255,verbose_name="Vendor Tax Name", blank=True, null=True)
    contract_date= models.DateTimeField(editable=True)
    status = models.IntegerField(blank=True, null=True,default=1)

class VendorFileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    vendor=models.ForeignKey("VendorRegistraion",verbose_name="VendorRegistraion",on_delete=models.CASCADE,blank=True, null=True)
    contract=models.ForeignKey("Vendorcompanyserviceinfo",verbose_name="Vendor company serviceinfo",on_delete=models.CASCADE,blank=True, null=True)
    files=models.FileField(blank=True)
    status = models.IntegerField(blank=True, null=True,default=1)

class VendorInvitationModel(models.Model):
    id=models.AutoField(primary_key=True)
    # created_at=UnixTimeStampField(auto_now_add=True)
    created_at=models.CharField(max_length=255,verbose_name="created", blank=True, null=True)
    vendorcompany=models.CharField(max_length=255,verbose_name="vendorCompanyName", blank=True, null=True)
    title=models.CharField(max_length=75,verbose_name="tile", blank=True, null=True)
    contact_person_email=models.EmailField(max_length=100)
    contactpersonname=models.CharField(max_length=255,verbose_name="CompanyName", blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    invite_link_status=models.IntegerField(blank=True, null=True,default=1)


class VendorInvoiceSplitManager(models.Manager):
    def getvendor_split_invoice(self,vendor_id,contract_id,company):
        return self.filter(vendor_id=vendor_id,contract_id=contract_id,company=company,status=1)
    
    def getvendor_split_invoiceamendment(self,vendor_id,contract_id,company):
        return self.filter(vendor_id=vendor_id,amendment_id=contract_id,company=company)
    
    def get_split_invoice(self,contract_id,company,status):
        """
        Return Multiple Objects from VendorInvoiceSplit Model
        """
        return self.filter(contract_id=contract_id,company=company,status=status)
    
    def get_split_amendment(self,amendment_id,company,status):
        """
        Return Multiple Objects from VendorInvoiceSplit Model
        """
        return self.filter(amendment_id=amendment_id,company=company,status=status)

class VendorInvoiceSplit(models.Model):
    id = models.AutoField(primary_key=True)
    no_invoice=models.CharField(max_length=255, blank=True, null=True)
    currency=models.ForeignKey("custom_auth.BaseCountries",verbose_name="currency",on_delete=models.CASCADE,blank=True, null=True)
    percentage=models.CharField(max_length=255,verbose_name="percentage", blank=True, null=True)
    exchange_rate=models.CharField(max_length=255, blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("ContractMasterVendor",verbose_name="Contract Master Vendor",on_delete=models.CASCADE,blank=True, null=True)
    contract=models.ForeignKey("ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment=models.ForeignKey("Amendment",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    draft_status = models.IntegerField(blank=True, null=True,default=0)
    objects=VendorInvoiceSplitManager()

class VendorPaymentTermsManager(models.Manager):
    def getvendor_paymentterms(self,vendor_id,contract_id,company):
        return self.filter(vendor_id=vendor_id,contract_id=contract_id,company=company,status=1)
    def getvendor_paymenttermsamendment(self,vendor_id,contract_id,company):
        return self.filter(vendor_id=vendor_id,amendment_id=contract_id,company=company,status=1)

class VendorPaymentTerms(models.Model):
    id = models.AutoField(primary_key=True)
    payment_type=models.CharField(max_length=255, blank=True, null=True)
    payment_name=models.CharField(max_length=255, blank=True, null=True)
    payment_day=models.CharField(max_length=255, blank=True, null=True)
    payment_percentage=models.CharField(max_length=255, blank=True, null=True)
    contract=models.ForeignKey("ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment=models.ForeignKey("Amendment",on_delete=models.CASCADE,blank=True, null=True) 
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("ContractMasterVendor",verbose_name="Contract Master Vendor",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    draft_status = models.IntegerField(blank=True, null=True,default=0)
    objects=VendorPaymentTermsManager()



class AmendmentManager(models.Manager):
    def getamendment(self,contract_id):
        return self.filter(service_id=contract_id,status=1).exclude(Q(amendment_reference_number__exact='') | Q(amendment_executed_date__isnull=True) | Q(amendment_amount__exact='') | Q(amendment_amount__isnull=True) | Q(amendment_upload_contract__exact='') | Q(amendment_upload_contract__isnull=True) | Q(amendment_upload_pricetable__exact='') | Q(amendment_upload_pricetable__isnull=True) | Q(amendment_currency_id__isnull=True))
    
    def get_by_id(self,id,status):
        """
        Return Multiple Objects from Amendment Model
        """
        return self.filter(id=id,status=status)
   
class Amendment(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    contractvendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    service=models.ForeignKey("ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment_type=models.CharField(max_length=255,verbose_name="Type", blank=True, null=True)
    amendment_reference_number=models.CharField(max_length=255,verbose_name="reference number", blank=True, null=True)
    amendment_executed_date=models.DateTimeField(editable=True,blank=True, null=True)
    amendment_currency=models.ForeignKey("custom_auth.BaseCountries",verbose_name="currency",on_delete=models.CASCADE,blank=True, null=True)
    amendment_amount=models.CharField(max_length=255,verbose_name="amount", blank=True, null=True)
    amendment_upload_contract=models.FileField(blank=True,null=True)
    amendment_upload_pricetable=models.FileField(blank=True,null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    updated_by = models.ForeignKey('custom_auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='amendment_updated_by')
    wcc=models.IntegerField(blank=True, null=True,default=0)
    #save_type =1 for save as draft and save_type =2 for submit
    save_type=models.IntegerField(blank=True, null=True,default=1)
    reference_type=models.CharField(max_length=255, blank=True, null=True)
    reference_id=models.CharField(max_length=255, blank=True, null=True)
    objects=AmendmentManager()
    created_at = models.DateTimeField(auto_now_add=True, null=True , blank=True)

    class meta:
        ordering = ('id','created_by','updated_by')
    def __str__(self):
        return self.amendment_reference_number

class CheckVendorContract(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    refnum=models.CharField(max_length=255,verbose_name="Contract Reference Number", blank=True, null=True)
    reason=models.CharField(max_length=1000,verbose_name="Type", blank=True, null=True)
    c_file=models.FileField(blank=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    vendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    close_status=models.IntegerField(blank=True, null=True,default=1)
    contract_type=models.CharField(max_length=255,verbose_name="Type", blank=True, null=True)
    contract=models.ForeignKey("ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment=models.ForeignKey("Amendment",on_delete=models.CASCADE,blank=True, null=True)
    contractfile=models.ForeignKey("VendorContractPriceTable",on_delete=models.CASCADE,blank=True, null=True)
    file_name=models.CharField(max_length=255,verbose_name="Type", blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.c_file and not self.file_name:  
            self.file_name = self.c_file.name  # Save full file path
        super().save(*args, **kwargs)
class CheckVendorContractHistory(models.Model):
    id = models.AutoField(primary_key=True)
    query=models.ForeignKey("CheckVendorContract",on_delete=models.CASCADE,blank=True, null=True)
    reason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    file=models.FileField(blank=True)
    vendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    date=models.CharField(max_length=255)
    query_status=models.IntegerField(blank=True, null=True,default=0)
    original_file_name = models.CharField(max_length=255,blank=True, null=True)