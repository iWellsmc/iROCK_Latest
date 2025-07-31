from django.db import models
from .role import Role
from .right import Right
from projectflow.models import ProjectFlowModules
from django.core.exceptions import ObjectDoesNotExist

class RoleRightManager(models.Manager):
    def filter_by_role(self,id,status):
        return self.filter(role_id=id,status=status)

    def filter_by_role_with_name(self,id,status):
        return self.filter(role_id=id,status=status).values('id','right_id__right_name')
    
    def filter_by_id(self,role,right,company):
        return self.filter(role=role,right__in=right,company=company)
    
    def filter_by_role1(self,role):
        return self.filter(role=role)

    def filter_by_right_slug(self,company,slug):
        return self.filter(company=company,right__slug=slug,status=1).exclude(role__module_id=8)

    def filter_by_role_ids(self,role_ids,slug):
        return self.filter(role_id__in=role_ids,right__slug=slug,status=1)
    
    def check_module_rights(self,role_id,right_name):
        try:
            return self.get(role_id=role_id,right__right_name=right_name,status=1)
        except ObjectDoesNotExist:
            return ""

class RoleRight(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)    
    right = models.ForeignKey(Right, on_delete=models.CASCADE)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=RoleRightManager()

    def __str__(self):
        return self.role.role_name + ' - ' + self.right.right_name