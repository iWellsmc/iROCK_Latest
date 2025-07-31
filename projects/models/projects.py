from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
import django.utils.timezone
class ProjectManager(models.Manager):
    def filter_by_company(self,company,status):
        return self.filter(company=company,status=status)

class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    name=models.CharField(max_length=255,verbose_name="Project Name", blank=True, null=True)
    country = models.ForeignKey("custom_auth.Countries",verbose_name="Country Name",on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_mosdified = models.DateTimeField(auto_now=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=0)
    project_status = models.IntegerField(blank=True, null=True,default=0)
    objects=ProjectManager()
    
    def __str__(self):
        """string representation"""
        return self.name