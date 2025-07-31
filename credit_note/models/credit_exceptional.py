from django.db import models

class CreditExceptional(models.Model):
    id = models.AutoField(primary_key=True)
    credit=models.ForeignKey("CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    exceptional_type = models.IntegerField(blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    confirm_dispute=models.IntegerField(blank=True, null=True,default=0)
    checked_messages=models.TextField(blank=True, null=True,default=0)
