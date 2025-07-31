from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

#Multiple field name#
class FieldName(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    block=models.ForeignKey("BlockName",verbose_name="Block Name",on_delete=models.CASCADE,null=True,blank=True)
    field_name=models.CharField(max_length=255,verbose_name="Field Name",null=True,blank=True)
    status = models.IntegerField(blank=True,default=1)
    def __str__(self):
        return self.field_name