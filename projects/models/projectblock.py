from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
import django.utils.timezone

class ProjectBlock(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    block=models.ForeignKey("BlockName",verbose_name="Block Name",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)
    # last_modified = models.DateTimeField(auto_now=True, null=True)