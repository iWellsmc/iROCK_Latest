from django import template
from ..models import User
register = template.Library()
@register.simple_tag
def UserDepartment(DepartmentId):
    return True if  User.objects.filter(user_department_id=DepartmentId,status=1).exists() else False
@register.simple_tag
def UserGroup(GroupId):
    return True if  User.objects.filter(user_group_id=GroupId,status=1).exists() else False