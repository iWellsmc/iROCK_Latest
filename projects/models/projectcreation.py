from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class ProjectCreationManager(models.Manager):
    def get_by_id(self,pk,status):
        return self.get(id=pk,status=status)
    
    def filter__by_company(self,company,status):
        return self.filter(company_id=company,status=status)
    
    def getproject_byid(self,pk):
        return self.get(id=pk)
    
class Projectcreation(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    entity=models.CharField(max_length=255,verbose_name="Entity Name", blank=True, null=True)
    projectname=models.ForeignKey("Projects",on_delete=models.CASCADE,blank=True, null=True)
    country = models.ForeignKey("custom_auth.Countries",verbose_name="Country Name",on_delete=models.CASCADE,blank=True, null=True)
    signatory_type = models.CharField(choices=(('1','Default Signatories'),('2','Project Signatories')),max_length=10,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=0)
    flow=models.ForeignKey("InvoiceGuard.Flow",on_delete=models.CASCADE,blank=True, null=True)
    flow_level=models.CharField(max_length=30,verbose_name="Levels", blank=True, null=True)
    flow_status = models.IntegerField(blank=True, null=True,default=0)
    projectcreation_status = models.IntegerField(blank=True, null=True,default=0)
    invoice_bank_user = models.IntegerField(blank=True,default=0)
    active_status=models.BooleanField(default=True,blank=True,null=True)
    objects=ProjectCreationManager()

    def __str__(self):
        """string representation"""
        return self.projectname.name