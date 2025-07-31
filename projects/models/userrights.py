from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class ProcessManager(models.Manager):
    def get_by_module(self,process,company):
        """
        Get Single Object by id from UserRights model 
        """
        return self.get(user_id=process,module_id=company)
    
    def get_by_moduleid(self,userid,moduleid):
        """
        Get Single Object by id from UserRights model 
        """
        return self.get(user_id=userid,module_id=moduleid)

class UserRights(models.Model):
    id = models.AutoField(primary_key=True)
    module=models.ForeignKey("Modules",verbose_name="Modules",on_delete=models.CASCADE,blank=True, null=True)
    create=models.CharField(max_length=75,verbose_name="create", blank=True, null=True)
    view=models.CharField(max_length=75,verbose_name="view", blank=True, null=True)
    edit=models.CharField(max_length=75,verbose_name="edit", blank=True, null=True)
    delete=models.CharField(max_length=75,verbose_name="delete", blank=True, null=True)
    lock=models.CharField(max_length=75,verbose_name="delete", blank=True, null=True)
    unlock=models.CharField(max_length=75,verbose_name="vendor approve", blank=True, null=True)
    vendor_invite=models.CharField(max_length=75,verbose_name="vendor invite", blank=True, null=True)
    vendor_approve=models.CharField(max_length=75,verbose_name="vendor approve", blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    objects=ProcessManager()

class ProjectRights(models.Model):
    id = models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    