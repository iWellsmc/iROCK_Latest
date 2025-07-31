from django.db import models

class SettingsManager(models.Manager):
    def getcompany_settings(self,company_id):
        return self.filter(company_id=company_id).first()
    
    def get_company(self,company_id):
        """
        Return Multiple Objects of company in Settings Model
        """
        return self.filter(company=company_id)
  

class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    dateformat=models.CharField(max_length=255,blank=True, null=True)
    timeformat=models.CharField(max_length=255,blank=True, null=True)
    timezone=models.CharField(max_length=255,blank=True, null=True)
    currency=models.CharField(max_length=255,blank=True, null=True)
    urlfield=models.CharField(max_length=255,blank=True, null=True)
    unit=models.CharField(max_length=255,blank=True, null=True)
    vendor_invite_time=models.CharField(max_length=255,blank=True, null=True)
    vendor_invite_unit=models.CharField(max_length=255,blank=True, null=True)
    vendor_registartion_time=models.CharField(max_length=255,blank=True, null=True)
    bank_user=models.IntegerField(blank=True,null=True,default=0)
    objects=SettingsManager()
