from django.db import models

class Enquiryusers(models.Model):
    id= models.AutoField(primary_key=True)
    title=models.CharField(max_length=255,blank=True, null=True)
    username=models.CharField(max_length=255,blank=True, null=True)
    email_id=models.CharField(max_length=255,blank=True, null=True)
    message=models.TextField(blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    proposalstatus=models.IntegerField(blank=True, null=True,default=0)