from django.db import models

class UserBankAccountnoManager(models.Manager):
    def create_actno(self,actno,bankid):
        """
        Create Multiple Object of Account Number in UserBankAccount Model
        """
        return self.create(accountno=actno,userbank_id=bankid)
    def update_by_id(self,id,actno):
        """
        Update Multiple Object of Account Number in UserBankAccount Model
        """
        return self.filter(id=id).update(accountno=actno)
  

    
class UserBankAccountno(models.Model):
    accountno = models.CharField(max_length=50, null=True, blank=True)
    userbank = models.ForeignKey('finance.UserBankMaster', on_delete=models.CASCADE, null=True,blank=True)
    objects = UserBankAccountnoManager()