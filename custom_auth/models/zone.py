from django.db import models

class zone(models.Model):
    id= models.AutoField(primary_key=True)
    country_code=models.CharField(max_length=255,blank=True, null=True)
    zone_name =models.CharField(max_length=255,blank=True, null=True)
    created_by =models.CharField(max_length=255,blank=True, null=True)
    updated_by =models.CharField(max_length=255,blank=True, null=True)
    deleted_by =models.CharField(max_length=255,blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now_add=True, editable=False)
    deleted_at =models.DateTimeField(auto_now_add=True, editable=False)
    lock =models.IntegerField(blank=True, null=True,default=1)