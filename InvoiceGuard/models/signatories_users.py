from django.db import models
from .signatories_settings import SignatoriesSettings


class SignatoriesUsersManager(models.Manager):

    def get_by_id(self,id):
        """
        Return Single Object by id from SignatoriesUsers Model
        """
        return self.get(pk=id)
    
    def get_by_signatoryId(self,id):
        """
        Return Multiple Objects by signatory id from SignatoriesUsers Model
        """
        return self.filter(signatory_id=id)
    
    def get_by_signatory(self,id):
        """
        Return Multiple Objects by signatory id from SignatoriesUsers Model
        """
        return self.filter(signatory=id)
    
    def filter_by_signatoryIds(self,list_ids):
        """
        Return Multiple Objects by Multiple Signatory ids from SignatoriesUsers Model
        """
        return self.filter(signatory_id__in=list_ids)

class SignatoriesUsers(models.Model):
    id = models.AutoField(primary_key=True)
    signatory = models.ForeignKey(SignatoriesSettings, on_delete=models.CASCADE, null=True,blank=True)
    user = models.ForeignKey('custom_auth.User', on_delete=models.CASCADE, null=True,blank=True)
    usertype = models.IntegerField( default=1, null=True,blank=True)
    objects = SignatoriesUsersManager()
    class Meta:
        managed = True
        db_table = 'signatories_users'
