from django.db import models

class countriesModel(models.Manager):
    def get_by_id(self,id):
        """
        Return Multiple Object of id in Basecountries Model
        """
        return self.filter(id__in=id)
    
    def getone_by_id(self,id):
        """
        Return Single Object of id in Basecountries Model
        """
        return self.get(id=id)
    
    def filter_by_id(self,id):
        return self.filter(id=id).first()

class Basecountries(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    iso3=models.CharField(max_length=255)
    numeric_code=models.CharField(max_length=255)
    iso2=models.CharField(max_length=255)
    phonecode=models.CharField(max_length=255)
    capital=models.CharField(max_length=255)
    currency=models.CharField(max_length=255)
    currency_name=models.CharField(max_length=255)
    currency_symbol=models.CharField(max_length=255)
    tld=models.CharField(max_length=255)
    native=models.CharField(max_length=255)
    region=models.CharField(max_length=255)
    subregion=models.CharField(max_length=255)
    timezones=models.TextField()
    translations=models.TextField()
    flag=models.IntegerField(blank=True, null=True,default=1)
    latitude=models.DecimalField(max_digits=10, decimal_places=8)
    longitude=models.DecimalField(max_digits=11, decimal_places=8)
    emoji=models.CharField(max_length=255)
    emojiU=models.CharField(max_length=255,blank=True, null=True)
    currency_unit = models.CharField(max_length=25,blank=True, null=True)
    fractional_unit = models.CharField(max_length=25,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now_add=True, editable=False)
    wikiDataId=models.CharField(max_length=255,blank=True, null=True)
    objects=countriesModel()
    
    def __str__(self):
        """stirng representation"""
        return self.name