from django.db import models

class CompanyBankUserManager(models.Manager):
   def create_company_bankuser(self,company,users):
        """
        Return Multiple Objects by id from CompanyBank Model
        """
        return self.create(companybank_id=company,user_id=users)
   
   def filter_by_company(self,bankdetailsid):
        """
        Return Multiple Objects by id from CompanyBank Model
        """
        return self.filter(companybank_id=bankdetailsid)
   
   def updatecompanybank(self,pk,otherdetails):
        """
        Update Multiple Objects by id from CompanyBank Model
        """
        return self.filter(id=pk).update(bankdetails=otherdetails)
   
   def delete_company_bankuser(self,user_id,pk):
        """
        Delete Multiple Objects by id from CompanyBank Model
        """
        return self.filter(user_id=user_id,companybank_id=pk).delete()
   
    

class CompanyBankUser(models.Model):
    companybank = models.ForeignKey('finance.CompanyBank',on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey('custom_auth.User',on_delete=models.CASCADE,null=True,blank=True)
    status = models.BooleanField(default=True)
    objects = CompanyBankUserManager()