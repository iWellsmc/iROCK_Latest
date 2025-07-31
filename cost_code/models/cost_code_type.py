from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class CostCodeTypeManager(models.Manager):
    def filter_by_status(self,status):
        return self.filter(status=status)
    
    def create_costcode_type(self,comp_name,comp_cost_code,cost_code,company,costcode_main_id=None):
        return self.create(component_name=comp_name,component_cost_code=comp_cost_code,cost_code=cost_code,company=company,costcode_main_id=costcode_main_id)
    
    def filter_by_codemaster(self,cost_code,status,company):
        return self.filter(cost_code=cost_code,status=status,company=company)
    
    def get_by_id(self,pk,status):
        return self.get(id=pk,status=status)
    
    def check_data(self,pk,data,status):
        return self.filter(Q(component_name=data)|Q(component_cost_code=data),status=status,cost_code_id=pk)
    
    def check_data_costtypeid(self,pk,data,status,id):
        return self.filter(Q(component_name=data)|Q(component_cost_code=data),status=status,cost_code_id=pk).exclude(id=id)
    
    def update_data(self,comp_name,comp_cost,pk):
        return self.filter(id=pk).update(component_name=comp_name,component_cost_code=comp_cost)

    def getcostcodetype_bymasterid(self,cost_code_id,status):
        return self.filter(cost_code_id=cost_code_id,status=status)

    def getcostcodetype_id(self,id):
        return self.filter(id=id)
    
    def getcostcodetype_name_masterid(self,name,cost_code_id):
        return self.filter(component_name=name,cost_code_id=cost_code_id).first()
    
    def getcostcodecontains(self,status,component_name):
        return self.filter(component_name__icontains=component_name,status=1)
    
    def filter_by_company(self,status,company):
        return self.filter(status=status,company=company)
    
    def check_component_exist(self,cost_code_id,company,component_name):
        try:
            return self.get(status=1,company=company,component_name=component_name,cost_code_id=cost_code_id)
        except ObjectDoesNotExist:
            return ""


    def check_component_exist_new(self,cost_code_id,company,component_name,costcode_main_id):
        try:
            return self.get(status=1,company=company,component_name=component_name,cost_code_id=cost_code_id,costcode_main_id=costcode_main_id)
        except ObjectDoesNotExist:
            return ""

    def getcostcodetype_bymasterid_table(self,cost_code_id,status,offset,limit,search_value):
        return self.filter(Q(cost_code_id=cost_code_id) & Q(status=status) & Q(component_name__icontains=search_value))[offset:offset+limit]

    def getallcostcodetype_bymasterid(self,cost_code_id,status,search_value):
        return self.filter(Q(cost_code_id=cost_code_id) & Q(status=status) & Q(component_name__icontains=search_value))
    # def create_costcode_masterold(self,cost_code_format,level,digit,input,start,sequence,leveltype):
    #     return self.create(cost_code_format=cost_code_format,no_digits=digit,input_type=input,start_with=start,sequence_gap=sequence,level_type_id=level,leveltype=leveltype)


class CostCodeType(models.Model):
    id = models.AutoField(primary_key=True)
    cost_code=models.ForeignKey('CostCodeMaster',on_delete=models.CASCADE,blank=True,null=True)
    component_name=models.CharField(max_length=255,verbose_name="Component Name", blank=True, null=True)
    component_cost_code=models.CharField(max_length=100,verbose_name="Component Cost Code", blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    # level_type=models.ForeignKey('LevelMaster',on_delete=models.CASCADE,blank=True,null=True)
    costcode_main=models.ForeignKey('CostCodeMain',on_delete=models.CASCADE,blank=True,null=True)
    objects=CostCodeTypeManager()

    