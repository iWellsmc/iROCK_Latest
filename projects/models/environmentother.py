from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class EnvironmentOther(models.Model):
    id=models.AutoField(primary_key=True)
    # field=models.ForeignKey("FieldName",verbose_name="Field Name",on_delete=models.CASCADE,null=True,blank=True)
    field_environment_other=models.CharField(max_length=25,null=True,blank=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    field_environment=models.ForeignKey("FieldEnvironment",verbose_name="Field Environment",on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(blank=True,default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)