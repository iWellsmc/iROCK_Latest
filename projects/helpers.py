from custom_auth.models import *

from projects.models import *
import re

def generatecin(companyid):
    if (ContractMasterVendor.objects.filter(company_id=companyid).exists()):
        # company=Companies.objects.filter(id=companyid).first()
        max_id = ContractMasterVendor.objects.filter(company_id=companyid).last()
        if(max_id):
            next_id=int(max_id.set_vin_id)+1
    else:
        next_id=1
    company=Companies.objects.filter(id=companyid).first()
    addcompany=str(company.id).zfill(3)
    max_id_str=str((next_id))
    max_id_str=max_id_str.zfill(4)
    return [addcompany+"-V"+max_id_str,next_id]


    # if (ContractMaster.objects.filter(company_id=companyid,vendor_name__iexact=companyname).exists()):
    #     print('exists')
    #     vin_number=ContractMaster.objects.filter(company_id=companyid,vendor_name__iexact=companyname).last()
    #     return vin_number.vin
    # else:
    #     if (ContractMaster.objects.filter(company_id=companyid).exists()):
    #         lastcontract=ContractMaster.objects.filter(company_id=companyid).last()
    #         next_id =int(lastcontract.set_vin_id)+1
    #     else:
    #         next_id=1
    #     max_id_str=str(next_id)
    #     companyname=re.sub('[^A-Za-z0-9]+', '', companyname)
    #     companynameshort=companyname[:3].upper()
    #     max_id_str=max_id_str.zfill(3)
    #     return companynameshort+"-"+max_id_str

# source_id= models.CharField(max_length=255,blank=True, null=True)
#     source_type=models.CharField(max_length=255,blank=True, null=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     Action=models.CharField(max_length=255,blank=True, null=True)
#     username=models.ForeignKey('User',on_delete=models.CASCADE,blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     message= models.CharField(max_length=255,blank=True, null=True)
#     role_id=models.ForeignKey("Roles",on_delete=models.CASCADE,blank=True, null=True)
from datetime import datetime
from custom_auth.models import userlog
from custom_auth.models import Companies
from projects.models import *



def create_user_log(request,source_id,source_type,action_type,message,usercreate,company=None):
    now = datetime.now()
    company=None
    if request.company:
        company_id = request.company
        # company_instance = Companies.objects.filter(id=company_id).first()
    else:
        company=None


   
    # print(company.company_name,'company....')
    users= userlog.objects.create(source_id=source_id,source_type=source_type,company=company_id,Action=action_type,username_id=request.user.id,created=now,message=message,roleId_id=usercreate)
    userlog.objects.create(source_id=source_id,source_type=source_type,company=company_id,Action=action_type,username_id=request.user.id,created=now,message=message,roleId_id=usercreate)

def getvendorcontracts(vendor_id):
    contracts=ContractMaster.objects.gettotalcontracts_bystatus(vendor_id,1)
    allcontract=[]
    for contract in contracts:
        if contract.projectdisciplinetype_id != None :
            projectdevelopmentdiscipline=ProjectDevelopmentDiscipline.objects.getdevelopment_details(contract.projectdiscipline_id)
            development_type=projectdevelopmentdiscipline.project_discipline
            if development_type == "1":
                developmenttype='Green Field Development'
            elif development_type == "2":
                developmenttype='Brown Field Development'
            else:
                developmenttype='Others'

            if projectdevelopmentdiscipline.development_type.development.development_type == 'Oil_Development':
                development_name='Oil Development'
            elif projectdevelopmentdiscipline.development_type.development.development_type == 'Gas_Development':
                development_name='Gas Development'
            elif projectdevelopmentdiscipline.development_type.development.development_type == 'Unconventional_Oil':
                development_name='Unconventional Oil'
            else:
                development_name='Unconventional Gas'
            
            discipline=ProjectDevelopmentSubType.objects.getdetails_byid(contract.projectdisciplinetype_id)
            disciplinename=discipline.discipline_subtype.discipline_subtype
            allcontract.append({
                'id':contract.id,
                'contract_name':contract.name_service,
                'field_type':developmenttype,   
                'development_type':development_name,
                'disciplinename':disciplinename,
                'reference_number':contract.reference_number
            })
    return allcontract
    
    
