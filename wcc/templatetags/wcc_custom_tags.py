from django import template
from wcc.models import *
from invoice.models import *
from projects.models import *
from wcc.helpers import *
register = template.Library()


@register.simple_tag
def getwccsupportfile(wcc_id,supportid):
    files=WccFileUpload.objects.get_by_support(wcc_id,1,supportid)
    return files,files.count()

@register.simple_tag
def getwccvalues(pk):
    wccvalues=WorkCompletionValue.objects.filter_by_wcc(pk).first()
    return wccvalues

@register.simple_tag
def wcc_approval_check(wcc_id,user_id):
    return WccApproval.objects.filter_by_user_wcc(wcc_id,user_id).count()

@register.simple_tag
def checkapproveaccess(wcc_id,user_id):
        data=WccApproval.objects.filter_by_user_wcc(wcc_id,user_id).last()
        return WccApproval.objects.filter_by_station_not_approve(wcc_id,data.wcc_per_station_id).count(),data


@register.simple_tag
def checkreturndata(wcc_id):
    data=WccApproval.objects.filter(wcc_id=wcc_id,approval_status=3).count()
    return data


@register.simple_tag
def checkapproveaccess_admin(wcc_id,user_id):
    data=WccApproval.objects.filter_by_user_wcc(wcc_id,user_id).last()
    if (data):
        return WccApproval.objects.filter_by_station_not_approve(wcc_id,data.wcc_per_station_id).count(),data
    else:
        return 1,0
    

def check_wcc_invoice(wcc_id):
    return Invoice.objects.filter_by_wcc(wcc_id).count()

def get_station_users(station_id):
    return WccStationUsers.objects.filter_by_station(station_id,1)

@register.simple_tag
def get_wcc_data(wcc_level_type,wcc_id,project_id):
    
    if (wcc_level_type == "discipline"):
        get_data=list(ProjectDevelopmentSubType.objects.filter_by_project(project_id,1).values('discipline_subtype__discipline_subtype','project_discipline__project_discipline','id','project_discipline__cluster__clustersubname__cluster_subname'))
        data=change_key_name(get_data,"discipline_subtype__discipline_subtype","name")
    elif (wcc_level_type == "cluster"):
        get_data=list(ProjectCluster.objects.filter_by_project(project_id,1).values('clustersubname__cluster_subname','id'))
        data=change_key_name(get_data,"clustersubname__cluster_subname","name")
    else:
        data=[]
        get_discipline=list(ProjectWellName.objects.filter_by_project(project_id,1).values('welltype__discipline_type__discipline_subtype__discipline_subtype','welltype__discipline_type_id','welltype__discipline_type__project_discipline__project_discipline','welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname'))
        new_list=[dict(t) for t in {tuple(d.items()) for d in reversed(get_discipline)}]
        for discipline in new_list:
            project_discipline=""
            if discipline['welltype__discipline_type__project_discipline__project_discipline'] == "1":
                project_discipline="Green Field Development"
            elif discipline['welltype__discipline_type__project_discipline__project_discipline'] == "2":
                project_discipline="Brown Field Development"    
            else:
                project_discipline="Others"
            data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
            get_well_type=ProjectWellType.objects.filter_by_discipline(project_id,discipline['welltype__discipline_type_id'],1)
            well_array=[]
            for well_type in get_well_type:
                well_data=list(ProjectWellName.objects.filter_by_well_type(project_id,well_type.id,1).values('wellname__well_subname','id'))
                well_array.extend(well_data)
            data_obj['well_datas']=well_array
            data.append(data_obj)
            # data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
            # get_well_type=ProjectWellType.objects.get_by_discipline(project_id,discipline['welltype__discipline_type_id'],1)
            # well_data=list(ProjectWellName.objects.filter_by_well_type(project_id,get_well_type.id,1).values('wellname__well_subname','id'))
            # data_obj.update({'well_datas':well_data})
            # data.append(data_obj)
    return data

@register.simple_tag
def check_wcc_flowdata(level_type,level_id,wcc_flow_id):
    if level_type == '' or level_id == '' or wcc_flow_id == '':
        return 0,[]
    data = WccFlowLevel.objects.filter_wcc_level(level_type,level_id,wcc_flow_id,True)
    return data.count(),data.first()

@register.simple_tag
def check_wcc_wellbased(level_id,wcc_flow_id):
    print('level_id',level_id,'wcc_flow_id',wcc_flow_id)
    data = WccFlowLevel.objects.filter_wcc_levelbased(level_id,wcc_flow_id,True)
    print('data',data)
    return data.count(),data.first()


@register.simple_tag
def get_station_data(flow_level_id,status):
    wccstationdata = WccPerStation.objects.filter_by_flow_level(flow_level_id,status)
    return wccstationdata

@register.simple_tag
def get_station_users(station_id,status):
    userslist=WccStationUsers.objects.filter_by_station(station_id,status)
    return userslist

@register.simple_tag
def trackstation(wcc_id,station_id):
    userslist=WccApproval.objects.track_station_data(wcc_id,station_id)
    return userslist

@register.simple_tag
def unapprovedtrackstation(wcc_id,station_id):
    userslist=WccApproval.objects.station_data_app_status(wcc_id,station_id,1)
    return userslist



def convert_wcc_date(value,companyid):
    if (value != None and value !=""):
        # convert_date=datetime.strptime(value ,"%Y-%m-%d").date()
        company_generalsetting=Settings.objects.filter(company_id=companyid).first()
        all_dateformat = {'dd-M-yy':"%d-%b-%Y",'dd-mm-yy':"%d-%m-%Y",'dd/mm/yy':"%d/%m/%Y",'mm-dd-yy':'%m-%d-%Y','mm/dd/yy':'%m/%d/%Y','yy-mm-dd':'%Y-%m-%d','yy/mm/dd':'%Y/%m/%d'}
        try:
            for key,values in all_dateformat.items():
                if (key == company_generalsetting.dateformat):
                    return value.strftime(values)
        except:
            return ''
    else:
        return ''

register.filter('check_wcc_invoice',check_wcc_invoice)
register.filter('get_station_users',get_station_users)
register.filter('convert_wcc_date',convert_wcc_date)

@register.simple_tag
def checkpermission_WCC_approval(wcc_id, user_id):
    dispute_track=WccReturnTrack.objects.filter(wcc=wcc_id,user_id=user_id).first()
    dispute_track_count=0
    if dispute_track:
        dispute_track_count=1
    elif UserRights.objects.filter(module_id=13,user_id=user_id).first():
        if UserRights.objects.filter(module_id=13,user_id=user_id).first().create == '1':
                dispute_track_count=1

    if dispute_track_count == 1 :
        WorkCompletionCost.objects.filter(id=wcc_id).update(wcc_query_status=1)

    return dispute_track_count


@register.simple_tag
def get_wcc_committee_member(request,wcc):
    dispute_member=0
    if(wcc.wcc_status == 2):
        if UserRights.objects.filter(module_id=13,user_id=request.user.id).first():
            if UserRights.objects.filter(module_id=13,user_id=request.user.id).first().create == '1':
                dispute_member=1
    elif(wcc.wcc_status == 3):
        if UserRights.objects.filter(module_id=13,user_id=request.user.id).first():
            if UserRights.objects.filter(module_id=13,user_id=request.user.id).first().create == '1':
                dispute_member=1
    return dispute_member


@register.simple_tag
def query_closed_by_wcc_user(stage,wcc):
    # print(f'pk {invoice}, stage {stage}, credit {credit}')
    if wcc:
        current_user=WccReturnTrack.objects.filter(stage=stage,wcc_id=wcc,status=True).last()
        return current_user
    else:
        return
    

@register.simple_tag
def wcc_get_files(id, request):
    get_files = WccQueryFiles.objects.filter(disputedquery_id=id)
    return get_files



@register.simple_tag
def get_wcc_originalcontract_price_files(contract,contracttype,file_type):
    if contracttype == 'original':
        contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,file_type).values()
        file_count=contract_table_files.count()
        return contract_table_files,file_count
    else:
        contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,file_type).values()
        file_count=contract_table_files.count()
        return contract_table_files,file_count
    
@register.simple_tag
def getwccamendmentcontract_price_files(contract,contracttype,file_type):
    contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,file_type).values()
    file_count=contract_table_files.count()
    # print(f"contract_table_files {contract_table_files}")
    return contract_table_files,file_count

@register.simple_tag
def reasonfor_wccqueryhistory(pk,status):
    wcc_exceptional_instance = WccExceptional.objects.filter(wcc_id=pk,return_status=status).first()
    if wcc_exceptional_instance:
        checked_messages = wcc_exceptional_instance.checked_messages
    else:
        checked_messages = None  
        
    return checked_messages
@register.simple_tag
def get_Wcc_previous_histories(count,wcc):
    return WccQuery.objects.filter(wcc_id=wcc.id,returned_count=count)
