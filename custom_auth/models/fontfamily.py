from django.db import models

class FontFamily(models.Model):  
    id = models.AutoField(primary_key=True)
    font_name = models.CharField(max_length=50,blank=True,null=True)
    status = models.BooleanField(blank=True,default=True)
    def __str__(self):
        """stirng representation"""
        return self.font_name