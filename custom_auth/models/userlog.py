from django.db import models
from datetime import datetime 

class userlog(models.Model):
    id = models.AutoField(primary_key=True)
    source_id= models.CharField(max_length=255,blank=True, null=True)
    source_type=models.CharField(max_length=255,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    Action=models.CharField(max_length=255,blank=True, null=True)
    username=models.ForeignKey('User',on_delete=models.CASCADE,blank=True, null=True)
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    created = models.DateTimeField(default=datetime.now, editable=False)
    message= models.CharField(max_length=255,blank=True, null=True)
    roleId=models.ForeignKey("Roles",on_delete=models.CASCADE,blank=True, null=True)
 