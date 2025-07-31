from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
from django.db.models import F


class AddNewContracts(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    contract_type=models.CharField(max_length=1000,verbose_name="Contract Type", blank=True, null=True)
    name_service=models.CharField(max_length=255,verbose_name="Name Service", blank=True, null=True)
    contract_refnum=models.CharField(max_length=255,verbose_name="Contract Reference Number", blank=True, null=True)
    amendment_refnum=models.CharField(max_length=255,verbose_name="Amendment Contract Reference Number", blank=True, null=True)
    c_file=models.FileField(blank=True)
    vendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    original_file_name = models.CharField(max_length=255,blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.c_file and not self.original_file_name:  # Check if c_file is uploaded and original_file_name is not set
            self.original_file_name = self.c_file.name
        super().save(*args, **kwargs)

class AddNewContractsHistory(models.Model):
    id = models.AutoField(primary_key=True)
    query=models.ForeignKey("AddNewContracts",on_delete=models.CASCADE,blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    date=models.CharField(max_length=255)
    file=models.FileField(blank=True)
    vendor=models.ForeignKey("ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    original_file_name = models.CharField(max_length=255,blank=True, null=True)

class ProjectUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def getuser_byproject(self,project_id):
        return self.filter(project=project_id,status=1).select_related('user').values('id',user_name=F('user__name'),user_lastname=F('user__lastname'),user_designation_role=F('user__designation_role'),user_uid=F('user__id'))
    
    def getprojectuser_byid(self,id):
        return self.get(id=id)
    
    def getprojectuser_byuserid(self,user_id):
        return self.filter(user_id=user_id,status=1)
    
    def getnewuser_byproject(self,project_id,users_list):
        return self.filter(project=project_id,status=True).select_related('user').values('id','user_id',user_name=F('user__name'),user_lastname=F('user__lastname'),user_designation_role=F('user__designation_role')).exclude(user_id__in=users_list)
    
    def getuser_byproject_userid(self,project_id,user_id):
        return self.get(project_id=project_id,user_id=user_id)

    def getuser_byproject_ids(self,project_list):
        return self.filter(project_id__in=project_list,status=1)
class ProjectUser(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    project=models.ForeignKey("Projectcreation",on_delete=models.CASCADE,blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=True)
    objects=ProjectUserManager()
