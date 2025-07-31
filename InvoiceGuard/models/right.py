from django.db import models
class RightModule(models.Manager):
    def filter_by_companyId(self,company):
        return self.filter(company=company)
    
    def filter_only_wcc(self,company):
        return self.filter(company=company,slug__startswith='wcc')
    
    def filter_without_wcc(self,company):
        return self.filter(company=company).exclude(slug__startswith='wcc')


class Right(models.Model):
    id = models.AutoField(primary_key=True)
    right_name = models.CharField(max_length=50)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=50,blank=True,null=True)
    objects=RightModule()

    def __str__(self):
        return self.right_name