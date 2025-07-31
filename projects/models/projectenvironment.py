from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class ProjectEnvironment(models.Model):
    id=models.AutoField(primary_key=True)
    block=models.ForeignKey("ProjectBlock",verbose_name="Block Name",on_delete=models.CASCADE,null=True,blank=True)
    field=models.ForeignKey("ProjectField",verbose_name="Project Field",on_delete=models.CASCADE,null=True,blank=True)
    field_environment=models.ForeignKey("FieldEnvironment",verbose_name="Field Environment",on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)