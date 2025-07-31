from django.db import models
from projects.models import Projectcreation
class SignatoriesSettingsManager(models.Manager):
    def get_by_id(self,id):
        """
        Return Single Object by id from SignatoriesSettings Model
        """
        return self.get(pk=id)
    
    def get_by_company(self,company,status,signatory_type):
        """
        Return Multiple Objects by company from SignatoriesSettings Model
        """
        return self.filter(company=company,status=status,signatory_type=signatory_type)
    
    def get_by_company_type(self,company,status,type,signatory_type):
        """
        Return Multiple Objects by company and type from SignatoriesSettings Model
        """
        return self.filter(company=company,status=status,invoice_type=type,signatory_type=signatory_type)
    
    def filter_by_id(self,id):
        """
        Return Multiple Objects by id from SignatoriesSettings Model
        """
        return self.filter(id=id)

    def project_signatory(self,company,status,type,project_id):
        """
        Return Multiple Objects by company and type & project_id from SignatoriesSettings Model
        """
        if Projectcreation.objects.filter(id=project_id,signatory_type=1).exists():
            return self.filter(company=company,status=status,invoice_type=type)
        else:
            return self.filter(company=company,status=status,invoice_type=type,project_id=project_id)
    

    def filter_by_project(self,project,company,signatory,status):
        
        return self.filter(project_id=project,company_id=company,signatory_type=signatory,status=status)

class SignatoriesSettings(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    currency = models.ForeignKey('custom_auth.Basecountries', on_delete=models.CASCADE, null=True,blank=True)
    min_amount = models.BigIntegerField(blank=True, null=True)
    max_amount = models.BigIntegerField(blank=True, null=True)
    no_of_signatories = models.IntegerField(blank=True, null=True)
    invoice_type = models.CharField(choices=(('1', 'With Invoice'), ('2', 'Without Invoice')), max_length=1, blank=True, null=True)
    project = models.ForeignKey('projects.Projects',on_delete=models.CASCADE,blank=True,null=True)
    signatory_type = models.CharField(choices=(('1','Default Signatories'),('2','Project Signatories')),max_length=10,blank=True,null=True,default='1')
    status = models.BooleanField(blank=True, null=True, default=True)
    objects = SignatoriesSettingsManager()
    class Meta:
        managed = True
        db_table = 'signatories_settings'