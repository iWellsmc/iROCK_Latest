from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
from django.db.models import Q,F,Count
from django.core.exceptions import ObjectDoesNotExist



class ContractMasterVendorManager(models.Manager):
    def getvendor_byvin(self,vin,company):
        return self.filter(vin=vin,status=1,company=company).first()
    
    def getvendor_byid(self,id,companyid):
        return self.filter(id=id,company_id=companyid,status=1).first()
    
    def update_contractmastervendor(self,companyid,vendor_id,vendor_name,country_of_operation,country_of_incorporation,state,Address,website,Registernumber):
        return self.filter(company_id=companyid,id=vendor_id).update(vendor_name=vendor_name,country_of_operation_id=country_of_operation,country_of_incorporation_id=country_of_incorporation,state_id=state,Address=Address,website=website,RegisterNumber=Registernumber)
    
    def update_approvestatus(self,vendor_id,status):
        return self.filter(id=vendor_id).update(approver_status=status)
    
    def get_byid(self,id,companyid):
        return self.filter(id=id,company=companyid,status=1).first()
    
    def get_byvin(self,vin,companyid):
        return self.filter(vin=vin,company=companyid,status=1)

    def filter_company(self,company,status):
        return self.filter(company=company,status=status)

    
class ContractMasterVendor(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    set_vin_id=models.CharField(max_length=255,verbose_name="set vinid", blank=True, null=True)
    vin=models.CharField(max_length=255,verbose_name="Vin", blank=True, null=True)
    vendor_name=models.CharField(max_length=255,verbose_name="Vendor Name", blank=True, null=True)
    contactpersontitle=models.CharField(max_length=10,verbose_name="Title", blank=True, null=True)
    contactpersonname=models.CharField(max_length=255,verbose_name="Contact Person name", blank=True, null=True)
    contactpersonlastname=models.CharField(max_length=255,verbose_name="Contact Person name", blank=True, null=True)
    contactpersonemail=models.EmailField(max_length=100,blank=True, null=True)
    contact_primary_title=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_primary_first_name=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_primary_middle_name=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    contact_primary_last_name=models.CharField(max_length=50,verbose_name="secondary full name", blank=True, null=True)
    official_primary_email = models.EmailField(max_length=100,blank=True, null=True)
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
    country_of_operation= models.ForeignKey("custom_auth.BaseCountries",verbose_name="Country of operation",on_delete=models.CASCADE,blank=True, null=True)
    country_of_incorporation = models.ForeignKey("custom_auth.Countries",verbose_name="Country of incorporation",on_delete=models.CASCADE,blank=True, null=True)
    state=models.ForeignKey("custom_auth.States",verbose_name="State Name",on_delete=models.CASCADE,blank=True, null=True)
    official_secondary_email = models.EmailField(max_length=100,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    RegisterNumber=models.CharField(max_length=255,verbose_name="Registered number in the Country Of Incorporation", blank=True, null=True)
    Address=models.TextField(max_length=255,verbose_name="vendor Company official address", blank=True, null=True)
    website=models.CharField(max_length=50,verbose_name="Vendor Company Website", blank=True, null=True)
    created_at = models.CharField(max_length=255,verbose_name="Vendor Company Website", blank=True, null=True)
    approver_status=models.IntegerField(blank=True, null=True,default=0)
    active_status = models.IntegerField(blank=True, null=True,default=1)
    contact_primary_phone_number_extenstion=models.CharField(max_length=255,verbose_name="official primary extenstion", blank=True, null=True)
    contact_secondary_phone_number_extenstion=models.CharField(max_length=255,verbose_name="official secondary extenstion", blank=True, null=True)
    created_by = models.ForeignKey("custom_auth.User",verbose_name="ContractMasterVendor Created By",on_delete=models.CASCADE,blank=True, null=True, related_name="created_by_vendor")
    updated_by = models.ForeignKey("custom_auth.User",verbose_name="ContractMasterVendor Updated By",on_delete=models.CASCADE,blank=True, null=True,related_name="updated_by_vendor")
    objects=ContractMasterVendorManager()

    # def __str__(self):
    #     return self.contact_primary_first_name

class VendorTaxDetails(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("ContractMasterVendor",verbose_name="Contract Master Vendor",on_delete=models.CASCADE,blank=True, null=True)
    Tax_Name=models.CharField(max_length=255,verbose_name="Vendor Tax Name", blank=True, null=True)
    Tax_Number=models.CharField(max_length=255,verbose_name="Vendor Tax Number", blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)

class ContractMasterManager(models.Manager):
    def getcontractmaster(self,vendorid):
        return self.filter(contractvendor_id=vendorid,status=1).exclude(Q(name_service__exact = '') | Q(name_service__isnull=True) | Q(reference_number__exact='') | Q(reference_number__isnull=True) | Q(executed_date__isnull=True) | Q(amount__exact='') | Q(projects_id__isnull=True) | Q(projectdiscipline_id__isnull=True) | Q(projectdisciplinetype_id__isnull=True))
    
    def getcontract(self,contractid):
        """
        Return Single Object from ContractMaster Model
        """
        return self.filter(id=contractid,status=1).first()
    
    def get_by_id(self,id):
        """
        Return Multiple Objects from ContractMaster Model
        """
        return self.filter(id=id,status=1)
    
    def get_contract_project(self,project_id):
        """
        Return Multiple Objects from ContractMaster Model
        """
        return self.filter(projects_id=project_id,status=1)
    

    def gettotalcontracts(self,vendor_id):
        return self.filter(contractvendor_id=vendor_id,status=1)
    
    def gettotalcontracts_bystatus(self,vendor_id,status):
        return self.filter(contractvendor_id=vendor_id,status=1,projects__active_status=status)

    def getproject_bycountrywise(self,status,vendor_id=None,country_ids=[]):
        queryset=self.filter(status=1,projects__active_status=status)
        if vendor_id is not None:
            queryset=queryset.filter(contractvendor_id=vendor_id)
        if len(country_ids) > 0:
            queryset=queryset.filter(projects__country_id__in=country_ids)
        queryset=queryset.values(country=F('projects__country')).annotate(project_count=Count('id'))
        return queryset

    def getproject_bycountry(self,status,vendor_id=None,country_id=None):
        queryset=self.filter(status=1,projects__active_status=status)
        if vendor_id is not None:
            queryset = queryset.filter(contractvendor_id=vendor_id,)
        if country_id is not None:
            queryset = queryset.filter(projects__country_id=country_id)
        queryset = queryset.values('projects').annotate(Count('projects'))
        return queryset

    def getcontract_byid(self,contract_id,services):
        return self.filter(id=contract_id,types_service__in=services)

    def getprojectcount_by_vendor_status(self,vendor_id,status=None,country_ids=[]):
        queryset=self.filter(contractvendor_id=vendor_id)
        if status is not None:
            queryset=queryset.filter(projects__active_status=status)
        if len(country_ids) > 0:
            queryset=queryset.filter(projects__country_id__in=country_ids)

        queryset=queryset.values('projects_id').distinct()
        return queryset




class ContractMaster(models.Model):
    id = models.AutoField(primary_key=True)
    updated_by = models.ForeignKey('custom_auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='updated_by')
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    contractvendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    types_service=models.CharField(max_length=15,verbose_name="Types of Service", blank=True, null=True)
    name_service=models.CharField(max_length=255,verbose_name="name service", blank=True, null=True)
    projects=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    projectdiscipline=models.ForeignKey("ProjectDevelopmentDiscipline",verbose_name="Project Development Discipline",on_delete=models.CASCADE,null=True,blank=True)
    projectdisciplinetype=models.ForeignKey("ProjectDevelopmentSubType",verbose_name="ProjectDevelopmentSubType",on_delete=models.CASCADE,null=True,blank=True)
    reference_number=models.CharField(max_length=255,verbose_name="reference number", blank=True, null=True)
    executed_date=models.DateTimeField(editable=True,blank=True, null=True)
    currency=models.ForeignKey("custom_auth.BaseCountries",verbose_name="currency",on_delete=models.CASCADE,blank=True, null=True)
    amount=models.CharField(max_length=255,verbose_name="amount", blank=True, null=True)
    upload_contract=models.FileField(blank=True,null=True)
    contract_file_name=models.CharField(max_length=255,blank=True,null=True)
    upload_pricetable=models.FileField(blank=True,null=True)
    price_table_file_name=models.CharField(max_length=255,blank=True,null=True)
    # add created by field default to current user
    created_by = models.ForeignKey('custom_auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='created_by')
    status=models.IntegerField(blank=True, null=True,default=1)
    wcc=models.IntegerField(blank=True, null=True,default=0)
    #save_type =1 for save as draft and save_type =2 for submit
    save_type=models.IntegerField(blank=True, null=True,default=1)
    list_items=models.BooleanField(blank=True, null=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True , blank=True)
    objects=ContractMasterManager()

    class meta:
        # verbose_name = "Contract Master"
        # verbose_name_plural = "Contract Master"
        ordering = ('id','created_by','updated_by')


class VendorContractPriceTableManager(models.Manager):
    def uploadpricetablefile(self,file_name,company_id,vendor_id,contract_id,amendment_id=None):
        self.create(file_name=file_name,company_id=company_id,vendor_id=vendor_id,contract_id=contract_id,amendment_addendum_id=amendment_id)
    
    def checkpricetable_exists_by_contractid(self,contract_id,amendment_addendum_id=None):
        queryset=self.filter(contract_id=contract_id,status=1)
        if amendment_addendum_id is not None:
            queryset=queryset.filter(amendment_addendum_id=amendment_addendum_id)
        return queryset

    def getallprice_tablefiles_contractid(self,contract_id,file_type=None):
        return self.filter(contract_id=contract_id,status=1,file_type=file_type)

    def getallprice_tablefiles_amendment_addendum(self,amendment_addendum_id,file_type=None):
        return self.filter(amendment_addendum_id=amendment_addendum_id,status=1,file_type=file_type)
    
    def getfiles_byid(self,id):
        try:
            return self.get(id=id)
        except ObjectDoesNotExist:
            return ""

class VendorContractPriceTable(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    contract=models.ForeignKey("ContractMaster",on_delete=models.CASCADE,blank=True, null=True)
    amendment_addendum=models.ForeignKey("Amendment",on_delete=models.CASCADE,blank=True, null=True)
    file_name=models.FileField(blank=True,null=True)
    #file type=1 if contract file or file type=2 if price table
    file_type=models.IntegerField(blank=True, null=True,default=0)
    original_file_name=models.CharField(max_length=255,blank=True,null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    objects=VendorContractPriceTableManager()
