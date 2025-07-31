from django.db import models


class LevelMasterManager(models.Manager):
    def get_all(self):
        return self.all()
    
    def createlevelmaster(self,level_name,company_id,):
        return self.create(level_name=level_name,company_id=company_id)
    
    def filter_company(self,company_id,status):
        return self.filter(company_id=company_id,status=status)
    
    def getlevel_byid(self,id):
        return self.filter(id=id)
    

class LevelMaster(models.Model):
    id = models.AutoField(primary_key=True)
    level_name=models.CharField(max_length=50,verbose_name="Level Type", blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=LevelMasterManager()