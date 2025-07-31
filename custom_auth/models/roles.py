from django.db import models

class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    roles=models.CharField(max_length=75,verbose_name="Roles", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)