from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class CostCodeMainManager(models.Manager):
    def create_costcode_main(self,discipline_id,development_id,level2,level1_costcode,level2_costcode,company):
        return self.create(level1_cost_code=level1_costcode,level2_cost_code=level2_costcode,company=company,level1_developmenttype_id=discipline_id,level1_discipline_id=development_id,level2_discipline_id=level2)
   
    def getcostcode_bydevelopment_discipline(self,discipline_id,development_id,company):
        return self.filter(company=company,level1_developmenttype_id=development_id,level1_discipline_id=discipline_id).first()
    
    def getcostcode_level1_level2(self,discipline_id,development_id,company,level2):
        return self.filter(company=company,level1_developmenttype_id=development_id,level1_discipline_id=discipline_id,level2_discipline_id=level2).first()
    
    def getallcostcode(self,company):
        return self.filter(company=company,status=1)
    
    def getcostcode_discipline(self,discipline_id,company):
        return self.filter(company=company,level2_discipline_id=discipline_id).first()
    
    def getmaincostcode_byid(self,id):
        return self.filter(id=id).first()
    
    def updatemain_costcode(self,level1_cost_code,level2_cost_code,level1_developmenttype_id,level1_discipline_id,level2_discipline_id,id):
        return self.filter(id=id).update(level1_cost_code=level1_cost_code,level2_cost_code=level2_cost_code,level1_developmenttype_id=level1_developmenttype_id,level1_discipline_id=level1_discipline_id,level2_discipline_id=level2_discipline_id)
    
    def get_by_development_discipline(self,levl1,level1_sub,status,company,level2):
        return self.filter(level1_discipline=levl1,level1_developmenttype=level1_sub,status=status,company_id=company,level2_discipline__in=level2)
    
    def filter_by_development(self,level1_discipline,level1_developmenttype,status,company):
        return self.filter(level1_discipline=level1_discipline,level1_developmenttype=level1_developmenttype,status=status,company_id=company)
        
    def filter_by_discipline(self,status,company,level2_discipline):
        return self.filter(status=status,company_id=company,level2_discipline__in=level2_discipline)
    
    def getallcostcode_by_level1_level2(self,level1_discipline,level1_development,level2_discipline,company):
        try:
            return self.filter(status=1,company=company,level1_discipline_id=level1_discipline,level1_developmenttype_id=level1_development,level2_discipline_id=level2_discipline).first()
        except ObjectDoesNotExist:
            return ""

    def getcostcodemain_byid(self,id):
        try:
            return self.get(id=id)
        except ObjectDoesNotExist:
            return ""

class CostCodeMain(models.Model):
    id = models.AutoField(primary_key=True)
    # (oil,gas,unconventional oil,unconventional gas)
    level1_discipline=models.ForeignKey('projects.ProjectDiscipline',on_delete=models.CASCADE,blank=True,null=True) 
    level1_cost_code=models.CharField(max_length=25,verbose_name="Level1 Cost Code", blank=True, null=True)
    # (green,brown.others)
    level1_developmenttype=models.ForeignKey('projects.DevelopmentType',on_delete=models.CASCADE,blank=True,null=True)
    level2_discipline=models.ForeignKey('projects.DisciplineSubtype',on_delete=models.CASCADE,blank=True,null=True) 
    level2_cost_code=models.CharField(max_length=25,verbose_name="Level1 Cost Code", blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=CostCodeMainManager()
