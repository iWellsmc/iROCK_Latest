from django.db import models

class CompanyBankManager(models.Manager):

    def get_by_id(self,id):
        """
        Return Single Object by id from CompanyBank Model
        """
        return self.get(id=id)
    
    def get_by_company(self,company):
        """
        Return Multiple Objects by id from CompanyBank Model
        """
        return self.filter(company=company,status=1)
    
    def create_companybank(self,company,currency,accountno,instructortitle,instructorfirstname,instructorlastname,bankname):
        """
        Create Multiple Objects by id from CompanyBank Model
        """
        return self.create(company=company,currency_id=currency,account_number_id=accountno,instructortitle=instructortitle,instructorfirstname=instructorfirstname,instructorlastname=instructorlastname,bank_name_id=bankname)
    
    def filter_for_search(self,company,search_query):
        """
        Return Single Object by id from CompanyBank Model
        """
        return self.filter(company=company,status=True,bank_name__icontains=search_query).order_by('-id')
       
    def updatecompanybank(self,pk,otherdetails):
        """
        Update Multiple Objects by id from CompanyBank Model
        """
        return self.filter(id=pk).update(bankdetails=otherdetails)


class CompanyBank(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    currency = models.ForeignKey('custom_auth.Basecountries', on_delete=models.CASCADE, null=True,blank=True)
    bank_name = models.ForeignKey('finance.UserBankMaster', on_delete=models.CASCADE, null=True,blank=True)
    account_number = models.ForeignKey('finance.UserBankAccountno', on_delete=models.CASCADE, null=True,blank=True)
    instructortitle = models.CharField(max_length=5, null=True, blank=True)
    instructorfirstname = models.CharField(max_length=50, null=True, blank=True)
    instructorlastname = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True)
    objects = CompanyBankManager()
    def __str__(self):
        return f'{self.company} - {self.bank_name} - {self.account_number}'