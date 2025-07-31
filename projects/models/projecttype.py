from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class ProjectType(models.Model):
    id=models.AutoField(primary_key=True)
    project_type=models.CharField(max_length=255,verbose_name="Project Type",blank=True,null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.project_type

class ProjectTypeCompany(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Project creation",on_delete=models.CASCADE,null=True,blank=True)
    project_type=models.CharField(max_length=255,verbose_name="Project Type",blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)