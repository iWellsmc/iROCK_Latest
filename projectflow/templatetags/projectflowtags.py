from django import template
from invoice.models import InvoiceCostInvoice
from projectflow.models import *
from InvoiceGuard.models import *
from projects.models import *

register = template.Library()

@register.simple_tag
def checkflowavailable(level_id,flow_level,project_id):
    projectflowlevel=ProjectFlowlevel.objects.checklevel(level_id,flow_level,project_id)
    # print(level_id,flow_level,project_id,'asfd',projectflowlevel)
    return projectflowlevel.count()

@register.simple_tag
def checkwellbasedflowavailable(level_id,flow_level,project_id):
    projectflowlevel=ProjectFlowlevel.objects.checkwellbasedlevel(level_id,flow_level,project_id)
    # print(level_id,projectflowlevel)
    return projectflowlevel.count()


@register.simple_tag
def getprojectflowlevel(process_id,level_id,project_id):
    projectflowlevel=ProjectFlowlevel.objects.getprojectflowlevel(process_id,level_id,project_id)
    return projectflowlevel

@register.simple_tag
def getmodule_byprocess(process_id):
    modules=ProcessModule.objects.getmodule_byprocess(process_id)
    return modules

@register.filter(name='times') 
def times(number):
    if(number):
        return range(number)
    
@register.filter(name='no_of_range') 
def no_of_range(number):
    if(number):
        return range(0, int(number))

@register.simple_tag
def getprojectflowmodule(projectflow_level_id,offset):
    if(projectflow_level_id):
        projectflowmodules=ProjectFlowModules.objects.getprojectmodules_by_levelid(projectflow_level_id,offset)
        return projectflowmodules

@register.simple_tag
def getroleandusers(module_id,company,project_id):
    if module_id != '' and module_id != None:
        process_module=ProcessModule.objects.getmodule_byid(module_id)
        roles=Role.objects.filter_by_module_id(process_module.module_id,company)
        projectusers=ProjectUser.objects.getuser_byproject(project_id)
        data={
            'roles':roles,
            'projectusers':projectusers
        }
        return data

@register.simple_tag
def getflowusers(flowmodule_id,offset):
    projectflowusers=ProjectFlowModuleUsers.objects.getflowusers(flowmodule_id,offset)
    return projectflowusers

@register.simple_tag
def get_related_roles(projectid,userid,companyid,request):
    role_name=[]
    projectuser=ProjectUser.objects.get(user=userid,project=projectid,company=companyid)
    projectflowmodulesuser=ProjectFlowModuleUsers.objects.filter(company=companyid,project_id=projectid,user_id=projectuser).values_list('ProjectFlowModules',flat=True)
    for i in projectflowmodulesuser:
        rolename = Role.objects.filter(company=companyid, projectflowmodules__id=i).first()
        role_name.append(rolename)
    return role_name

@register.simple_tag
def show_signatories(project_id,request):
    get_project_signatories=SignatoriesSettings.objects.filter_by_project(project_id,request.company.id,2,1)
    if (get_project_signatories.count() > 0):
        filtered_ids=get_project_signatories.values_list('id',flat=True)
    else:
        get_project_signatories=SignatoriesSettings.objects.filter_by_project(None,request.company.id,1,1)
        filtered_ids=get_project_signatories.values_list('id',flat=True)
    users_list=list(SignatoriesUsers.objects.filter_by_signatoryIds(filtered_ids).select_related('user').annotate(user__id=F('signatory__currency__currency_symbol')).values('id','user__name','user__lastname','user__designation_role','signatory__currency__currency_symbol'))
    return users_list

@register.simple_tag
def show_signatories_track(pk,project_id,request):
    new_list=[]
    contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
    get_project_signatories=SignatoriesSettings.objects.filter_by_project(project_id,request.company.id,2,1)
    if (get_project_signatories.count() > 0):
        filtered_data=get_project_signatories
    else:
        filtered_data=SignatoriesSettings.objects.filter_by_project(None,request.company.id,1,1)
    for costinvoice in contractcostinvoice:
        data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=2)
        if (data.count() > 0):
            sign_data=data.first()
        else:
            get_value=costinvoice.invoice_total_amount
            split_val=get_value.split(' ')
            convert_val=float(split_val[1].replace(',',''))
            sign_data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=1).filter(Q(min_amount__lte=convert_val) & Q(max_amount__gte=convert_val)).first()
        if sign_data:
            sign_users=SignatoriesUsers.objects.get_by_signatoryId(sign_data.id)
            new_list.extend(sign_users)
    if len(new_list) == 0:
        new_list.append(None)
    return new_list

register.filter('checkflowavailable',checkflowavailable)
register.filter('getprojectflowlevel',getprojectflowlevel)
register.filter('times',times)
register.filter('getprojectflowmodule',getprojectflowmodule)
