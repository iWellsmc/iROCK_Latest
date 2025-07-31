from django.db import models


class CostCodeVendorManager(models.Manager):
    def filter_by_comapny(self,company,status):
        return self.filter(company=company,status=status)
    
    def createCostCodeVendor(self,vendor_id,main,order,company_id ,contract_id=None):
        return self.create(vendor_id=vendor_id,costcode_main_id=main,order=order,company_id=company_id,contractid=contract_id)
    
    def get_vendor_data(self,vendor_id,status,costcode_main=None):
        vendor_costcode_queryset=self.filter(vendor_id=vendor_id,status=status)
        if costcode_main:
            vendor_costcode_queryset=vendor_costcode_queryset.filter(costcode_main_id__in=costcode_main)
        return vendor_costcode_queryset     
    
    def get_vendor_company(self,vendor_id,status,company):
        return self.filter(vendor_id=vendor_id,status=status,company=company)

    def get_match_data(self,vendor_id,main,order,company_id,contract_id=None):
        return self.filter(vendor_id=vendor_id,costcode_main_id=main,order=order,company_id=company_id,contractid=contract_id)
    # def filter_company(self,company_id,status):
    #     return self.filter(company_id=company_id,status=status)
    
    def get_by_id(self,id):
        return self.get(id=id)

    def getcostcodevendor_groupby_costcodemain(self,company_id):
        return self.filter(company_id=company_id,status=1).values('costcode_main_id').distinct()
    
    def getcostcodevendor_groupby_costcodemain_vendor(self,company_id,vendor_id):
        return self.filter(company_id=company_id,vendor_id=vendor_id,status=1).values('costcode_main_id').distinct()

    def getcostcode_vendor_bycostcodemain(self,costcode_main,company_id,vendor_id=None):
        queryset=self.filter(costcode_main_id=costcode_main,company_id=company_id,status=1)
        if vendor_id is not None:
            queryset=queryset.filter(vendor_id=vendor_id)
        return queryset

    def getcostcodevendor_bystatus_main_order(self,costcode_main_id,order,company_id,vendor_id=None,contract_id=None):
        queryset = self.filter(costcode_main_id=costcode_main_id,company_id=company_id,order=order,status=1)
        if vendor_id is not None:
            queryset=queryset.filter(vendor_id=vendor_id)
            if contract_id is not None:
                queryset=queryset.filter(contractid=contract_id)
        return queryset 
        


    

class CostCodeVendor(models.Model):
    id = models.AutoField(primary_key=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    costcode_main=models.ForeignKey('CostCodeMain',on_delete=models.CASCADE,blank=True,null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    order = models.CharField(max_length=100,verbose_name="Cost Code main Order", blank=True, null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    objects=CostCodeVendorManager()