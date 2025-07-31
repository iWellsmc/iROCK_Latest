from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class Modules(models.Model):
    id = models.AutoField(primary_key=True)
    module_name=models.CharField(max_length=75,verbose_name="Module Name", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
