from django.db import models

class CountriesManager(models.Manager):
    def getcountry_by_id(self,id):
        return self.get(id=id)



class Countries(models.Model):  
    id = models.AutoField(primary_key=True)
    iso= models.CharField(max_length=255)
    name= models.CharField(max_length=255)
    nicename= models.CharField(max_length=255)
    iso3= models.CharField(max_length=255)
    numcode= models.CharField(max_length=255)
    phonecode= models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    objects=CountriesManager()

    def __str__(self):
        """stirng representation"""
        return self.nicename