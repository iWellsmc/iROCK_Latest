from django.db import models


class CostCodeMasterManager(models.Manager):
    def filter_by_status(self,status,company):
        return self.filter(status=status,company_id=company)
    
    def filter_by_company(self,company,level_id):
        return self.filter(status=True,company_id=company,level_type_id=level_id)
    
    def getnewlevel(self):
        return self.filter(leveltype='new')
    
    def get_by_id(self,master_id):
        return self.filter(id=master_id).first()
    
    def filter_by_id(self,id):
        return self.filter(id=id)

    def get_by_level_id(self,level_id):
        return self.get(level_type_id=level_id)
    
    def create_costcode_masternew(self,cost_code_format,digit,input,start,sequence,leveltype,newlevel,level_master_id,company_id):
        return self.create(cost_code_format=cost_code_format,no_digits=digit,input_type=input,start_with=start,sequence_gap=sequence,level_type_name=newlevel,leveltype=leveltype,level_type_id=level_master_id,company_id=company_id)

    
    def create_costcode_masterold(self,cost_code_format,level,digit,input,start,sequence,leveltype,company_id,level_name):
        return self.create(cost_code_format=cost_code_format,no_digits=digit,input_type=input,start_with=start,sequence_gap=sequence,level_type_id=level,leveltype=leveltype,company_id=company_id,level_type_name=level_name)
    
    
    def getfirst_level(self,company_id,status):
        return self.filter(company_id=company_id,status=status).first()
    
    def getsecond_level(self,company_id,status):
        return self.filter(company_id=company_id,status=status)[1:2].get()
    
    def getremaining_level(self,company_id,status):
        return self.filter(company_id=company_id,status=status).all()[2:]
    
    def update_costcode_master(self,cost_code_format,digit,input,start,sequence,id,level_type):
        return self.filter(id=id).update(cost_code_format=cost_code_format,no_digits=digit,input_type=input,start_with=start,sequence_gap=sequence,level_type_name=level_type)

    def filter_by_level_id(self,company,level_type):
        return self.filter(company=company,level_type_id=level_type).first()
    
    def getmaster_by_limit_offset(self,company_id,offset):
        return self.filter(company_id=company_id,status=1)[offset:offset+1].get()
    
    def getprevious_costcode_master(self,current_costcode_id,company_id):
        return self.filter(company_id=company_id,status=1,id__lt=current_costcode_id).order_by('-id').first()

  
    

class CostCodeMaster(models.Model):
    id = models.AutoField(primary_key=True)
    cost_code_format=models.CharField(max_length=50,verbose_name="No of Digits", blank=True, null=True)
    level_type=models.ForeignKey('LevelMaster',on_delete=models.CASCADE,blank=True,null=True)
    level_type_name=models.CharField(max_length=50,verbose_name="No of Digits", blank=True, null=True)
    leveltype=models.CharField(max_length=15,verbose_name="Level Type", blank=True, null=True)
    no_digits=models.CharField(max_length=50,verbose_name="No of Digits", blank=True, null=True)
    input_type=models.CharField(max_length=20,verbose_name="Input Type", blank=True, null=True)
    start_with=models.CharField(max_length=20,verbose_name="Start With", blank=True, null=True)
    sequence_gap=models.CharField(max_length=20,verbose_name="Sequence Gap", blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=CostCodeMasterManager()