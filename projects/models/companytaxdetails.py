from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class CompanyTaxDetails(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    Tax_Type=models.CharField(max_length=255,verbose_name="Vendor Tax Name", blank=True, null=True)
    Tax_Name=models.CharField(max_length=255,verbose_name="Vendor Tax Name", blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)

class BankDetailsManager(models.Manager):
    def getbankdetails_byvendor_company(self,companyid,vendor_id):
        return self.filter(company_id=companyid,vendor_id=vendor_id,status=1)
    def update_bankdetails(self,bankdetailid,companyid,vendor_id,bankdetails,currencybank,bankname,accno):
        return self.filter(id=bankdetailid).update(company_id=companyid,vendor=vendor_id,bankdetails=bankdetails,bankcurrency_id=currencybank,bankname=bankname,accountnumber=accno)
    def create_bankdetails(self,companyid,vendor_id,bankdetails,currencybank,bankname,accno):
        return self.create(company_id=companyid,vendor_id=vendor_id,bankdetails=bankdetails,bankcurrency_id=currencybank,bankname=bankname,accountnumber=accno)
    def updateinactive_bankdetails(self,companyid,vendor_id,currentbankids):
        return self.filter(company_id=companyid,vendor_id=vendor_id).exclude(id__in=currentbankids).update(status=0)
   
class BankDetails(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("ContractMasterVendor",verbose_name="Contract Master Vendor",on_delete=models.CASCADE,blank=True, null=True)
    bankcurrency=models.ForeignKey("custom_auth.BaseCountries",verbose_name="currency",on_delete=models.CASCADE,blank=True, null=True)
    bankname=models.CharField(max_length=255,verbose_name="Bank Name", blank=True, null=True)
    accountnumber=models.CharField(max_length=255,verbose_name="Account Number", blank=True, null=True)
    bankdetails=models.CharField(max_length=1000,verbose_name="Bank Details", blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=BankDetailsManager()

class VendorCompanyTaxDetailsManager(models.Manager):
    def getvendortaxdetails_by_contract(self,vendor_id,contract_id,company):
        return self.filter(vendor_id=vendor_id,contract_id=contract_id,company=company,status=1)
    def getvendortaxdetails_by_amendment(self,vendor_id,contract_id,company):
        return self.filter(vendor_id=vendor_id,amendment_id=contract_id,company=company,status=1)
    def getvendortaxdetails(self,companyid,vendor_id):
        return self.filter(company_id=companyid,vendor_id=vendor_id,status=1)
    

    def getvendortax_by_contract(self,vendor_id,contract_id,company,Tax_Type):
        """
        Return Multiple Objects from VendorCompanyTaxDetails Model
        """
        return self.filter(vendor_id=vendor_id,contract_id=contract_id,company=company,status=1,Tax_Type=Tax_Type)
    
    def getvendortax_by_amendment(self,vendor_id,amendment_id,company,Tax_Type):
        """
        Return Multiple Objects from VendorCompanyTaxDetails Model
        """
        return self.filter(vendor_id=vendor_id,amendment_id=amendment_id,company=company,status=1,Tax_Type=Tax_Type)
    
    def getcontracttax_by_contract_taxtype(self,contract_id,tax_type):
        return self.filter(contract_id=contract_id,Tax_Type__in=tax_type)


class VendorCompanyTaxDetails(models.Model):
    id = models.AutoField(primary_key=True)
    Tax_Type=models.CharField(max_length=255,verbose_name="Vendor Tax Name", blank=True, null=True)
    tax=models.ForeignKey("CompanyTaxDetails",on_delete=models.CASCADE,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("ContractMasterVendor",verbose_name="Contract Master Vendor",on_delete=models.CASCADE,blank=True, null=True)
    contract=models.ForeignKey("ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment=models.ForeignKey("Amendment",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    draft_status = models.IntegerField(blank=True, null=True,default=0)
    objects=VendorCompanyTaxDetailsManager()


class CompanyTaxManager(models.Manager):
    def vendorTax(self,vendortax):
        """
        Return Multiple Objects from VendorCompanyTaxPercentage Model
        """
        return self.filter(vendortax__in=vendortax,status=1)
    
    def getinclusivetaxes_bycontractid(self,contract_id):
        return self.filter(vendortax__contract_id=contract_id,vendortax__Tax_Type='Inclusive')
    
    def getinclusivetaxes_byammendment(self,amendment_id):
        return self.filter(vendortax__amendment_id=amendment_id,vendortax__Tax_Type='Inclusive')


class VendorCompanyTaxPercentage(models.Model):
    id = models.AutoField(primary_key=True)
    taxpercentage=models.CharField(max_length=255,verbose_name="Vendor Tax Number", blank=True, null=True)
    vendortax=models.ForeignKey("VendorCompanyTaxDetails",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=CompanyTaxManager()