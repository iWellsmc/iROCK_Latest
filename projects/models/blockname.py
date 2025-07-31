from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
# from django.utils import timezone
import django.utils.timezone
#Multiple block name#
class BlockName(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    block_name=models.CharField(max_length=255,verbose_name="Block Name", blank=True, null=True)
    status=models.IntegerField(blank=True,default=0)
    # created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    # last_modified = models.DateTimeField(auto_now=True, null=True)

    # def save(self, *args, **kwargs):

    #     self.last_modified = timezone.now()
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return self.block_name