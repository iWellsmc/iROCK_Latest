from django.db import models

class UserBankMasterManager(models.Manager):
    def filter_company(self,company):
        """
        Return Multiple Object of Company in UserBankMaster Model
        """
        return self.filter(company=company,status=1)
    def get_company(self,id,company):
        """
        Return Single Object of Company in UserBankMaster Model
        """
        return self.get(id=id,company=company,status=1)
    def getbank(self,pk,company):
        """
        Return Single Object of Bank in UserBankMaster Model
        """
        return self.get(id=pk,company=company,status=1)
    def delete_bankusers(self,pk):
        """
        Remove Single Object of BankUsers in UserBankMaster Model
        """
        return self.filter(id=pk).update(status=0)
   
    
    def update_bank(self,pk,company,bankname,currency,otherdetails):
        """
        Update Single Object of Bank in UserBankMaster Model
        """
        return self.filter(id=pk,company=company,status=1).update(bank_name=bankname,currency=currency,otherdetails=otherdetails)
    
class UserBankMaster(models.Model):
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    otherdetails = models.CharField(max_length=500, null=True, blank=True)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True) 
    status = models.BooleanField(default=True)
    objects = UserBankMasterManager()
    
