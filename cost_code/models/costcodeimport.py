from django.db import models

class CostCodeImportLevel(models.Model):
    id = models.AutoField(primary_key=True)
    level=models.CharField(max_length=25,verbose_name="Level1 Cost Code", blank=True, null=True)
    level_name=models.CharField(max_length=100,verbose_name="Level1 Cost Code", blank=True, null=True)


class CostCodeImportLevelData(models.Model):
    id = models.AutoField(primary_key=True)
    costcodeimportlevel_id=models.IntegerField(blank=True, null=True)
    name=models.CharField(max_length=250,verbose_name="Level1 Cost Code", blank=True, null=True)
