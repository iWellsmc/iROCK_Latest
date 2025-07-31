from django import template
from ..models import RoleRight
from ..models import *
from ..models import SignatoriesUsers
from custom_auth.models import UserDepartment
from projects.models import Projectcreation
register = template.Library()

@register.simple_tag
def RightStatus(right_id,role_id):
    return True if RoleRight.objects.filter(right_id=right_id,role_id=role_id,status=True).exists() else False


def get_related_roles(module_id,company_id):
    datas=Role.objects.filter_by_module_id(module_id,company_id)
    return datas
register.filter('get_related_roles',get_related_roles)

@register.filter(name='get_dept_name')
def get_dept_name(id):
    if id!=None: 
        value=UserDepartment.objects.get(id=id)
        return value
    else:
        return None


@register.filter
def add_seperator(val):
    if (val != None):
        final_value='{:,}'.format(val)
        return final_value  
    else:
        return val

@register.filter
def SignatoryUser(signatory_id):

    return SignatoriesUsers.objects.filter(signatory_id=signatory_id)

@register.filter
def no_of_users(signatory_id):
    return SignatoriesUsers.objects.filter(signatory_id=signatory_id).count()


@register.simple_tag
def get_related_flow(pk,request):
    flow = Flow.objects.get(id=pk)
    process = Process.objects.filter(company=request.company)
    flow_process = FlowProcess.objects.filter(flow_id=pk, flow__company=request.company.id)
    return {'flow':flow,'process':process,'flow_process':flow_process}

@register.simple_tag
def get_related_modules(pk,request):
    process=Process.objects.get(id=pk)
    get_modules = Module.objects.filter(processmodule__process_id=pk)
    return {'modules_in':get_modules,'process_id':process}

@register.filter
def isProcessUsed(process_id):
    status = False if FlowProcess.objects.filter(process_id=process_id,status=True).exists() else True
    return status

@register.simple_tag
def project_signatory(project_id,company,invoice_type):
    return SignatoriesSettings.objects.project_signatory(company,True,invoice_type,project_id)


@register.filter
def signatory_type(project_id):
    return Projectcreation.objects.get(id=project_id).get_signatory_type_display()