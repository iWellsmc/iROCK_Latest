from django import template
from cost_code.models import CostCodeType,CostCodeSub,CostCodeMaster,LevelMaster,CostCodeVendor,CostCodeMain
from projects.models import ProjectDiscipline,DisciplineSubtype,ContractMasterVendor,DevelopmentType
from cost_code.helpers import getcostcode_format_type
from django.core.paginator import Paginator
from django.db.models import IntegerField, Value
from django.db.models.functions import Cast
from cost_code.helpers import getlevel1_level2,getlevel1_level2_components

register = template.Library()


@register.simple_tag
def get_component_details(company,component_data,counter):
    get_level=LevelMaster.objects.filter_company(company,1)
    comp_data = str(component_data)
    component=comp_data.strip() if (comp_data) else ""
    for i,level in zip(range(counter+1),get_level):
        if i == counter:
            get_ccomponent=CostCodeType.objects.filter(cost_code__level_type_id=level.id,company_id=company,component_name=component,status=1).first()
        else:
            get_ccomponent=0
            # print('get_ccomponent',get_ccomponent)
            # myval = CostCodeMaster.objects.filter(id=get_ccomponent.cost_code_id)
            # for i in myval:
            #  print('myval',i.start_with)
    return get_ccomponent

@register.simple_tag
def check_data_add_class(company_id,list_data):
    counter = 0
    for i,data in enumerate(list_data):
        get_data=get_component_details(company_id,data,i)
        # print("get_data",get_data)
        if (get_data  == None or get_data  == 0):
            counter +=1
    return counter

@register.simple_tag
def get_component_details_step_one(company,component_data,counter):
    get_level=LevelMaster.objects.filter_company(company,1)
    comp_data = str(component_data)
    component=comp_data.strip() if (comp_data) else ""
    for i,level in zip(range(counter+1),get_level):
        if i == counter:
            get_ccomponent=CostCodeType.objects.filter(cost_code__level_type_id=level.id,company_id=company,component_name=component,status=1).first()
            level_id=level.id
        else:
            get_ccomponent=None
            level_id=level.id
    return get_ccomponent,level_id

@register.filter
def pdfserialnumber(request):
    prevalue = request.session.get('serialno', 0)
    value = request.session['serialno'] = 1 + prevalue
    return value

@register.simple_tag
def clearpdfserial(request):
    request.session['serialno'] = 0
    return ''


@register.filter
def get_costcode_subtype(id):
    subtype=CostCodeType.objects.filter(cost_code_id=id,status=1)
    return subtype

@register.simple_tag
def getcost_type_by_masterid(remaining_level):
    costcodetype=CostCodeType.objects.getcostcodetype_bymasterid(remaining_level.id,1)
    return costcodetype

@register.simple_tag
def getLastValue(level_id,company):
    level = CostCodeMaster.objects.get_by_level_id(level_id)
    data=CostCodeType.objects.filter_by_codemaster(level,1,company).order_by('-component_cost_code').first()
    if (data != None):
        set_val = int(data.component_cost_code)+int(level.sequence_gap)+1
        data = str(set_val).zfill(int(level.no_digits))
    return data,level

@register.simple_tag
def getcostcode_sub(costcode_main,company):
    costcodesub=CostCodeSub.objects.getgroup_costcode_sub(costcode_main)
    getdiscipline=ProjectDiscipline.objects.get(id=costcode_main.level1_discipline_id)
    getdevelopmenttype=DevelopmentType.objects.get(id=costcode_main.level1_developmenttype_id)
    getlevel2discipline=DisciplineSubtype.objects.get(id=costcode_main.level2_discipline_id)
    costcode_type=getcostcode_format_type(company)
    costcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
    allcost_code=[]
    for costcode in costcodesub:
        allcostcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
        allcostcode_string=getdiscipline.name+'('+getdevelopmenttype.development_type+')'+'/'+getlevel2discipline.discipline_subtype+'/'
        allcostcodesub_order=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order'])
        allcostcodesub_value=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order']).last()
        type_name=CostCodeType.objects.get(id=allcostcodesub_value.cost_type_id)
        lastcategory=CostCodeType.objects.get(id=allcostcodesub_value.cost_type_id)
        for index, costcodesub_order in enumerate(allcostcodesub_order):
           allcostcode +=costcodesub_order.cost_code
           if index != len(allcostcodesub_order) - 1:
            allcostcode +=costcode_type
            costtype=CostCodeType.objects.getcostcodetype_id(costcodesub_order.cost_type_id).first()
            allcostcode_string +=costtype.component_name
            allcostcode_string +='/'
        allcost_code.append({
            'allcostcode':allcostcode.rstrip(costcode_type),
            'allcostcode_string':allcostcode_string.rstrip('/'),
            'order':costcode['order'],
            'type_name':type_name,
            'lastcategory':lastcategory,
            'main_costcode_id':costcode_main.id,
        })
    return allcost_code

@register.simple_tag
def Check_generate(order,main_id):
    status = False if CostCodeVendor.objects.filter(costcode_main_id=main_id,status=True,order=order).exists() else True
    return status

@register.simple_tag
def getcostcode_category(maincostcode,order,company):
    costcodesub=CostCodeSub.objects.get_by_company_main_id(maincostcode.id,order,company)
    return costcodesub
    
@register.simple_tag
def get_sub_type(order,main):
    get_sub=CostCodeSub.objects.get_by_main_id(order,main,1)
    return get_sub.costcode_preview

@register.filter
def get_cost_vendors(id):
    vendors_list=CostCodeVendor.objects.get_vendor_data(id,1)
    return vendors_list

@register.simple_tag
def getoldcostcode(order,maincostcode_id,index):
    costcodesub=CostCodeSub.objects.getcostcodesub_with_components_order_index(order,maincostcode_id,index)
    return costcodesub

def get_by_Levels(count):
    count= count+2
    return count

register.filter('get_by_Levels',get_by_Levels)

@register.simple_tag
def getcostcode_preview(maincostcode,order,company):
    try:
        print(f"maincostcode {maincostcode}")
        costcodesub=CostCodeSub.objects.getallcostcodesub_order(maincostcode,order)
        costcode_type=getcostcode_format_type(company)
        cost_code=maincostcode.level1_cost_code+costcode_type+maincostcode.level2_cost_code+costcode_type
        for subcode in costcodesub:
            cost_code +=subcode.cost_code
            cost_code +=costcode_type
        return cost_code.rstrip(costcode_type)   
    except ValueError:
        return ''
    else:
        return ''

@register.simple_tag
def getcostcode_string(maincostcode,order,company):
    try:
        costcodesub=CostCodeSub.objects.getgroup_costcode_sub(maincostcode)
        getdiscipline=ProjectDiscipline.objects.get(id=maincostcode.level1_discipline_id)
        getlevel2discipline=DisciplineSubtype.objects.get(id=maincostcode.level2_discipline_id)
        getdevelopmenttype=DevelopmentType.objects.get(id=maincostcode.level1_developmenttype_id)
        allcostcode_string=getdiscipline.name+'('+ getdevelopmenttype.development_type +')' + '/'+getlevel2discipline.discipline_subtype+'/'
        cost_sub_list = CostCodeSub.objects.getallcostcodesub_order(maincostcode,order)
        for index,costcodesub_order in enumerate(cost_sub_list):
            if index != len(cost_sub_list) - 1:
                costtype=CostCodeType.objects.getcostcodetype_id(costcodesub_order.cost_type_id).first()
                allcostcode_string +=costtype.component_name
                if index != len(cost_sub_list) - 1:
                    allcostcode_string +='/'
        return allcostcode_string.rstrip('/')
    except AttributeError:
        return ''
    else:
        return ''

@register.simple_tag
def getlevelcount(index):
    return index+2

@register.simple_tag
def getallcostcodemaster(company,status):
    if(company): 
        costcodemaster=CostCodeMaster.objects.filter_by_status(status,company)
        data={
            'costcodemaster':costcodemaster,
            'count':costcodemaster.count()
        }
        return data
    else:
        return ''

@register.simple_tag
def checkcostcodetype(company,costcodemaster):
    return CostCodeType.objects.getcostcodetype_bymasterid(costcodemaster.id,1).count()


@register.simple_tag
def checkcostcodetypeexists(costtypeid,company,component_name):
    costcodesub=CostCodeSub.objects.checkcostcodetypeexists(costtypeid,company,component_name)
    return costcodesub.count()
    


@register.simple_tag
def checkempty(request,value):
    value = request.session['cost_code_value'] = value
    return value

@register.simple_tag
def getsession(request):
    return request.session['cost_code_value']
@register.simple_tag
def clearvalue(request):
    del request.session['cost_code_value']
    return 

@register.simple_tag
def get_discipline_name(discipline,development):
    set_disciple=f'{discipline}_{development}'
    return set_disciple


@register.simple_tag
def getaddicon(costtypeid,company,cost_code,levelid,costcodemaster):
    getsequence = CostCodeMaster.objects.filter(company_id=company.id,id=costcodemaster.id).first()
    newcostcode = int(cost_code)+1
    lennewcostcode = len(str(newcostcode))
    noofdigit=int(getsequence.no_digits)
    if(lennewcostcode < noofdigit):
        newcostcode = str(newcostcode).rjust(noofdigit, '0')
    nxtcostcodeexit = CostCodeType.objects.filter(company=company,status=1,component_cost_code=newcostcode).exclude(id=costtypeid).exists()
    return nxtcostcodeexit
    

@register.simple_tag
def get_level_name(pk,request):
    get_level=LevelMaster.objects.getlevel_byid(pk).first()
    get_count=LevelMaster.objects.filter_company(request.company.id,1)
    level_name=''
    for count,level in zip(range(3,get_count.count()+3),get_count):
        if get_level.id == level.id:
            level_name += str(count)
    return level_name

@register.simple_tag
def increment_value_func(component_code,sequence_gap,digits,counter):
    convert_value=int(component_code)
    if convert_value == 0:
        if counter == 1 :
            add_value = component_code
        else:
            minus_counter = counter - 1
            increment_value=int(sequence_gap) * minus_counter + minus_counter
            add_value=convert_value + increment_value
            if len(str(add_value)) < int(digits):
                add_value=str(add_value).zfill(int(digits))
    else:
        increment_value=int(sequence_gap) * counter + counter
        add_value=convert_value + increment_value
        if len(str(add_value)) < int(digits):
            add_value=str(add_value).zfill(int(digits))
    return add_value

@register.simple_tag
def getcode_from_dict(code,level_index):
    # print(f"code {code}")
    data={
        'code':code['level'+str(level_index)+'_code'],
        'name':code['level'+str(level_index)]
    }
    return data

@register.simple_tag
def getcode_format(total_length,code,cost_code_format):
    allcode=''
    for i in range(1,total_length+1):
        if(i==total_length):
            allcode +=code['level'+str(i)+'_code']
        else:

            allcode +=code['level'+str(i)+'_code']+cost_code_format
    return allcode
  
@register.simple_tag
def sum_costcode(costcode,sequence_gap):
    new_costcode = str(int(costcode) + int(sequence_gap))
    return new_costcode.zfill(len(costcode))

@register.simple_tag
def getdatafrom_allcostcode(costcode,index):
    data={
        'name':costcode['level'+str(index)],
        'code':costcode['level'+str(index)+'_code']
    }
    return data

@register.simple_tag
def checklimit_exist(index,company_id,cost_code):
    costcode_master=list(CostCodeMaster.objects.filter_by_status(1,company_id))
    length_start_with=len(costcode_master[index-1].start_with)
    highest_number = 10 ** length_start_with - 1
    if(int(cost_code) <= highest_number):
        return False
    else:
        return True


@register.simple_tag
def check_code_exist(costcode,company):
    cost_code_exist=CostCodeSub.objects.getcostcodesub_codecode(costcode,company)
    if(cost_code_exist.count()>0):
        return True
    else:
        return False

@register.simple_tag
def checkcomponent_exist(index,company,level_data,level1_discipline,level1_development,level2_id):
    costcode_master=CostCodeMaster.objects.getmaster_by_limit_offset(company.id,index-1)
    costcode_main=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_development,level1_discipline,level2_id,company)
    # print(f"costcode_main {costcode_main}")
    if(costcode_main):
        costcode_type=CostCodeType.objects.check_component_exist_new(costcode_master.id,company,level_data['name'],costcode_main.id)
        if(not costcode_type):
            return True
        else:
            return False
    else:
        return True


@register.simple_tag
def getcostcodemaster_details(index,company):
    costcode_master=CostCodeMaster.objects.getmaster_by_limit_offset(company.id,index-1)
    print(f"costcode_master {costcode_master}")
    # return costcode_master
    return costcode_master

   


@register.simple_tag
def check_sequence_gap(order,costcode_main_id,company):
    allsubcode=CostCodeSub.objects.getallcostcodesub_order(costcode_main_id,order)
    nextcode_count=0
    for subcode in allsubcode:
        sub_cost_code=int(subcode.cost_code)
        master_codes = list(CostCodeSub.objects.getallcode_by_masterid(company.id, subcode.costcode_master_id).annotate(cost_code_int=Cast('cost_code', IntegerField())).values_list('cost_code_int', flat=True).distinct())
        next_costcode = None
        for cost_code in sorted(master_codes):
            if cost_code > sub_cost_code:
                next_costcode = cost_code
                break
        if(next_costcode):
            nextcode_count +=1
    
    if(nextcode_count > 0):
        return True
    else:
        return None


@register.simple_tag 
def getcostcode_contract_forreport(company,vendor_id=None , contract_id=None):
    if(vendor_id):
        costcodevendor=CostCodeVendor.objects.getcostcodevendor_groupby_costcodemain_vendor(company.id,vendor_id).filter(contractid=contract_id)
        print(f"costcodevendor {costcodevendor}")
    else:
        costcodevendor=CostCodeVendor.objects.getcostcodevendor_groupby_costcodemain(company.id)
    allcodes_data=[]
    costcode_type=getcostcode_format_type(company.id)

    for costcode_vendor in costcodevendor:
        if(vendor_id):
            costcode_vendor_bycostcodemain=CostCodeVendor.objects.getcostcode_vendor_bycostcodemain(costcode_vendor['costcode_main_id'],company.id,vendor_id).filter(contractid=contract_id)
        else:
            costcode_vendor_bycostcodemain=CostCodeVendor.objects.getcostcode_vendor_bycostcodemain(costcode_vendor['costcode_main_id'],company.id)
        allcost_code=[]

        costcode_main_details=getlevel1_level2(costcode_vendor['costcode_main_id'],company.id)
        for costcodemain in costcode_vendor_bycostcodemain:
            allcostcode=costcode_main_details['level1_2_code']

            vendor_details=ContractMasterVendor.objects.get_byid(costcodemain.vendor_id,company.id)
            # print(f"vendor_details {vendor_details}")
            getcostcode_sub_by_order_main=CostCodeSub.objects.getallcostcodesub_order(costcodemain.costcode_main_id,costcodemain.order)
            # print(f"getcostcode_sub_by_order_main {getcostcode_sub_by_order_main[0].status}")
            if getcostcode_sub_by_order_main[0].status == 1:
                remaining_levels=[]
                index=0
                for index, costcodesub in enumerate(getcostcode_sub_by_order_main):
                    if costcodesub.costcode_master is not None:
                        remaining_levels.append({costcodesub.costcode_master.level_type_name:costcodesub.cost_type.component_name})
                        allcostcode +=costcodesub.cost_code
                        if index != len(getcostcode_sub_by_order_main) - 1:
                            allcostcode +=costcode_type
                            print(f"allcostcode {allcostcode}")
                
                allcost_code.append({
                    'allcostcode':allcostcode.rstrip(costcode_type),
                    'remaining_levels':remaining_levels,
                    'level1':costcode_main_details['level1'],
                    'level2':costcode_main_details['level2'],
                    'vin':vendor_details.vin,
                    'vendor_name':vendor_details.vendor_name,
                })
        allcodes_data.append(allcost_code)
    
    return allcodes_data 


