from django.db import models

class States(models.Model):

    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    country=models.ForeignKey("Basecountries",on_delete=models.CASCADE,related_name="states",blank=True, null=True)
    country_code=models.CharField(max_length=255)
    fips_code=models.CharField(max_length=255)
    iso2=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    latitude=models.DecimalField(max_digits=10, decimal_places=8)
    longitude=models.DecimalField(max_digits=11, decimal_places=8)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now_add=True, editable=False)
    flag=models.IntegerField(blank=True, null=True,default=1)
    wikiDataId=models.CharField(max_length=255)