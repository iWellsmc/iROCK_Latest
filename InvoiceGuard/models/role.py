from django.db import models
from .module import Module
class RoleManager(models.Manager):
    def filter_by_id(self,role_id):
        return self.filter(id__in=role_id)
    
    def get_by_id(self,id):
        return self.get(id=id)
    
    def delete_by_id(self,id,company_id):
        return self.get(id=id,company=company_id)
    
    def get_by_company(self,company_name,status):
        return self.filter(company=company_name,status=status)
    
    def filter_by_rolename(self,role_name,company,status):
        return self.filter(role_name__iexact=role_name,company=company,status=status)

    def filter_by_module_id(self,module_id,company):
        return self.filter(module_id=module_id,company=company,status=1)
    
    def create_role(self,role_name,company,module):
        return self.create(role_name=role_name,company=company,module=module)

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True,blank=True)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=RoleManager()

    # object = RoleManager()
    def __str__(self):
        return self.role_name