import ast
import re
from django.shortcuts import render,redirect
from django.views import View
from .models import *
from projects.models import *
from custom_auth.models import *
from cost_code.models import *
from django.http import JsonResponse
from django.views.generic import ListView,UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from invoice.helpers import *
from wcc.helpers import *
from django.db.models import Q
from django.utils import timezone
from notifications.signals import notify
from custom_auth.views import markas_read_status
from django.contrib import messages
from .utils import pdf_view,wcc_number_generate
from InvoiceGuard.models import *
from datetime import datetime,date,timedelta
import pytz
from tzlocal import get_localzone
from custom_auth.helpers import check_user_sign 
from projects.helpers import create_user_log
from .templatetags.wcc_custom_tags import check_wcc_invoice,checkpermission_WCC_approval
from invoice.templatetags.invoice_custom_tags import confulldate,split_by_newline
import json


class WccList(ListView):
    model=WorkCompletionCost
    template_name='wcclist.html'
    def get_context_data(self,**kwargs):
        markas_read_status(self.request.get_full_path())
        context = super().get_context_data(**kwargs)
        self.request.session['submenu'] = 'wcc_list'
        user=User.objects.filter(Q(is_primary=1) | Q(is_secondary=1),id=self.request.user.id).first()
        vendor_status = True if user else False
        vendorid=ContractMasterVendor.objects.filter(vin=self.request.user.cin_number).first()
        count=ContractMaster.objects.filter(contractvendor=vendorid.id,wcc=1,status=1).count() 
        # wcclist=WorkCompletionCost.objects.filter_all_data(vendorid.id,self.request.company).order_by('-id') if vendor_status == True else WorkCompletionCost.objects.filter_submiited_data(vendorid.id,self.request.company).order_by('-id')
        context['vendorid']=vendorid
        # context['wcclist']=wcclist
        context['vendor_status']=vendor_status
        context['count']=count
        # local_timezone = get_localzone()
        # print("Local timezone:", local_timezone)
        # server_timezone = pytz.timezone('Asia/Calcutta')

        # # Get the current UTC time
        # current_utc_time = datetime.datetime.utcnow()
        # print('current_utc_time',current_utc_time)
        # # Localize the UTC time to the server's timezone
        # server_time = server_timezone.localize(current_utc_time)
        return context


class CreateWccMaster(View):    
    def get(self,request):
        request.session['mainmenu'] = 'wcc_list'
        company=Settings.objects.getcompany_settings(request.user.company.id)
        vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        contractlist=ContractMaster.objects.getcontractmaster(vendorid.id)
                # Assuming contractlist is a queryset of ContractMaster instances
        # for contract in contractlist:
        #     print("wcc:", contract.wcc)

        cost_code_list = CostCodeVendor.objects.get_vendor_data(vendorid.id,1)
        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        if(getlastlevel != None):
            lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        else:
            lastlevel=None 
        allcontractlist=[]
        for contract in contractlist:
            if contract.wcc == 1:
                allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original','check_status':contract.projects.active_status})
                # get_amendmentlist = Amendment.objects.filter(service_id=contract.id)
                get_amendmentlist = Amendment.objects.filter(service_id=contract.id, wcc=1)
                for amendment in get_amendmentlist:
                    if amendment.amendment_type == 'Amendment':
                        allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment','check_status':amendment.service.projects.active_status})
                    else:
                        allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum','check_status':amendment.service.projects.active_status})
        data={'company':company,'allcontractlist':allcontractlist,'vendor':vendorid,'company':request.company,'lastlevel':lastlevel,'cost_code_list':cost_code_list}
        return render(request,'createwcc.html',data)
    
    def post(self,request):

        fromdate=request.POST.get('fromdate',None)
        todate=request.POST.get('todate',None)
        contract=request.POST.get('contractid')
        if (contract == ''):
            contractid=''
            contract_type=''
        else:
            split_contract=contract.split("-")
            contractid=split_contract[0]
            contract_type=split_contract[1]
        from_date = datetime.now()
        contractnameservice=request.POST.get('contractnameservice')
        contractservicetype=request.POST.get('contractservicetype')
        service_rendered=request.POST.get('service_rendered')
        location_service=request.POST.get('location_service')
        project=request.POST.get('project')
        block=request.POST.get('block',None)
        field=request.POST.get('field',None)
        well=request.POST.get('well',None)
        block_not=request.POST.get('block_not')
        field_not=request.POST.get('field_not')
        well_not=request.POST.get('well_not')
        costcode=request.POST.get('costcode',None)
        project_hdn=request.POST.get('project_hdn')
        # receipt_datetime_object = datetime.strptime(receiptdate,request.POST.get('companydateformat'))invoice_submit_date=receipt_datetime_object,
        if (fromdate != '' and fromdate != None):
            from_datetime_object = datetime.strptime(fromdate,"%d-%b-%Y")
        else:
            from_datetime_object=None
        if (todate != '' and todate != None):
            todate_datetime_object = datetime.strptime(todate,"%d-%b-%Y")
        else:
            todate_datetime_object=None
        vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        print(request.POST)
        create_wcc=WorkCompletionCost.objects.createworkcompletioncost(from_datetime_object,todate_datetime_object,contractid,contract_type,contractnameservice,contractservicetype,service_rendered,location_service,project,block,field,well,request.company,vendorid.id,block_not,field_not,well_not,costcode,project_hdn)
        request.session['contractid']=request.POST.get('contractid')
        submit_type=request.POST.get('submit_type')
        if (submit_type == "0"):
            return redirect('wcc:wcclist')
        else:
            return redirect('wcc:createwccsteptwo',pk=create_wcc.id)
        
class CreateWccFormTwo(View):    
    def get(self,request,pk):
        company=Settings.objects.getcompany_settings(request.user.company.id)
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        from_date = wcc_data.fromdate
        if (wcc_data.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(wcc_data.contractid)
            contract_amount = contract.amount if contract.amount == 'No Max Limit' else contract.amount.replace(',','')
            contract_reference = contract.reference_number
            contract_date=contract.executed_date.date()
            vendor_id = contract.contractvendor
            reference_number = contract.reference_number
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id)

        else:
            contract=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
            contract_amount = contract.amendment_amount if contract.amendment_amount == 'No Max Limit' else contract.amendment_amount.replace(',','')
            contract_reference = contract.amendment_reference_number
            contract_date=contract.amendment_executed_date.date()
            vendor_id = contract.contractvendor
            reference_number = contract.amendment_reference_number
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id)

        supports_docs=getsupportsdata()
        wcc_number = wcc_number_generate(vendor_id,reference_number)
        data={'contractmaster':contract,'wcc_data':wcc_data,'company':company,'total_value':contract_amount,'contract_reference':contract_reference,'contract_date':contract_date,'supports_docs':supports_docs,'wcc_number':wcc_number,'price_table_files':price_table_files,'from_date': from_date ,'pk':pk }
        return render(request,'createwccformtwo.html',data)
    
    def post(self,request,pk):
        dateformat=request.POST.get('dateformat')
        wcc_num=request.POST.get('wc_num')
        wcc_date=request.POST.get('wcc_date')
        wcc_file=request.FILES.get('wcc_file',None)
        totalvalue=request.POST.get('totalvalue')
        pattern = r'[^0-9.,]+'
        matches = re.sub(pattern, '', totalvalue)
        if (len(matches) > 0):
            get_total_value = matches
        else:
            get_total_value = ''
        convert_date=getinvoiceDate(dateformat,wcc_date)
        vendor=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        WorkCompletionValue.objects.create_wcc_value(vendor,pk,wcc_num,convert_date,get_total_value,wcc_file,request.company)
        checksupportfile=request.POST.getlist('checksupportfile')
        for support in checksupportfile:
            files=checksupportfile=request.FILES.getlist('file'+str(support))
            for file in files:
                WccFileUpload.objects.create_wcc_supportfile(vendor,pk,support,file,request.company)
        submit_type=request.POST.get('submit_type')
        if (submit_type == '2'):
            return redirect('wcc:wccpreview',pk=pk)
        elif (submit_type == '1'):
            messages.success(self.request, 'WCC Submitted Successfully')
            WorkCompletionCost.objects.update_by_id(pk,1)
            wcc_data=WorkCompletionCost.objects.get_by_id(pk)
            wcc_work=WorkCompletionValue.objects.filter_by_wcc(pk).first()
            # wcc_work=WorkCompletionValue.objects.get_by_wcc(pk)
            # wcc_work = WorkCompletionValue.objects.get(wcc_id=pk)
            wcc_work = WorkCompletionValue.objects.filter(wcc_id=pk).first()


            wcc_flow=WccFlow.objects.get_by_project(wcc_data.project_id)
            if wcc_data.contracttype == "original":
                contract_data = ContractMaster.objects.get(id=wcc_data.contractid)
            else:
                amendment_data = Amendment.objects.get_by_id(wcc_data.contractid, 1).first()
                contract_data = amendment_data.service if amendment_data else None

            if wcc_flow.level_type == "discipline":
                get_flow_level = WccFlowLevel.objects.filter_wcc_level("discipline", contract_data.projectdisciplinetype_id, wcc_flow.id, True).first()
            elif wcc_flow.level_type == "cluster":
                #check cluster
                get_flow_level=WccFlowLevel.objects.filter_wcc_level("cluster",contract_data.projectdiscipline.cluster_id,wcc_flow.id,True).first()
            elif (wcc_flow.level_type == "well"):
                if wcc_data.well_not_applicable == "id":
                    get_flow_level=WccFlowLevel.objects.filter_wcc_level("well",wcc_data.well_id,wcc_flow.id,True).first()
                else:
                    get_flow_level=WccFlowLevel.objects.filter_wcc_levelbased(contract_data.projectdisciplinetype_id,wcc_flow.id,True).first()
            if not get_flow_level:
                get_flow_level=WccFlowLevel.objects.filter(project_id=wcc_data.project_id,status=1,wcc_flow_id=wcc_flow.id,company_id=request.company.id).first()
            wcc_flow_level_station=WccPerStation.objects.filter_by_flow_level(get_flow_level.id,True).first()
            get_users=WccStationUsers.objects.filter_by_station(wcc_flow_level_station.id,1)
            
            # server_timezone = pytz.timezone('Asia/Kolkata')

            # # Get the current time on the server
            # server_time = datetime.now(server_timezone)

            # print("Server time (New York):", server_time)

            # # Get your local system's timezone
            # local_timezone = pytz.timezone('Asia/Kolkata')  # Replace with your local timezone

            # # Convert the server time to your local time
            # local_time = server_time.astimezone(local_timezone)

            # print("Local time:", local_time)

            # print("Server time:", server_time)
            now = datetime.now()
            # now = local_time
            calculate_time=add_time(now,request.company)
            print(calculate_time)
            for userdata in get_users:
                create_user=WccApproval.objects.create_data(wcc_data.id,userdata.wcc_flow.id,userdata.user_id,userdata.wcc_per_station_id,calculate_time,now) 
                #send email
                wcccreatedmail(request,userdata.user,wcc_data,wcc_work,vendor,'wcccreatedemail')
                # send notification
                url="wcc/approvalwcclist"
                verb="WCC Received"
                description=f'WCC received from {get_vendor_company_name(request.user.cin_number)} for {wcc_data.name_service}'
                notify_wcc(request,userdata,url,verb,description,"user")
            recipient = User.objects.filter(cin_number__iexact=request.user.cin_number,status=1)
            sender = User.objects.filter(company=request.company.id,roles_id=2).first() 
            today = date.today()
            date_today = today.strftime("%d-%b-%Y")
            for mails in allVendors:
                wccsubmissionmail(request,mails,wcc_data,wcc_work,'wccsubmissionmail',request.user.id,date_today,contract_data)
            for notifications in recipient:
                urls="wcc/approvalwcclist"
                notify.send(sender, recipient=notifications,data=urls, verb='WCC Received', description=f'WCC received by {sender.name} on {date_today} for {wcc_data.name_service} ')
            usercreate = request.user.roles_id   
            print(wcc_num,"WCC NUMBER")  
            create_user_log(request,wcc_num,'WCC','Create','WCC Submitted',usercreate)      
        return redirect('wcc:wcclist')
    
def add_time(now,company):
    get_company_invoice_time=WccTimeTrigger.objects.filter(company=company).first()
    if get_company_invoice_time.time_unit == 2:
        calculate_time=now+timedelta(minutes=get_company_invoice_time.time_allotted)
    elif get_company_invoice_time.time_unit == 0:
        calculate_time= now+timedelta(hours=get_company_invoice_time.time_allotted)
    else:
        calculate_time=now+timedelta(days=get_company_invoice_time.time_allotted)
    return calculate_time
class WccPreview(View):
    def get(self,request,pk):
        wccworkvalues=WorkCompletionValue.objects.filter_by_wcc(pk)
        if (wccworkvalues[0].wcc.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(wccworkvalues[0].wcc.contractid)
            currency_symbol=contract.currency.currency_symbol
        else:
            contract=Amendment.objects.get_by_id(wccworkvalues[0].wcc.contractid,1).first()
            currency_symbol=contract.amendment_currency.currency_symbol
        supports_docs=getsupportsdata()
        data={'wccworkvalues':wccworkvalues,'currency_symbol':currency_symbol,'pk':pk,'supports_docs':supports_docs}
        return render(request,'wccpreview.html',data)

def getsupportfiles(request):
    supportid=request.GET.get('supportid','')
    wcc_id=request.GET.get('wcc_id','')
    if (supportid == "9" or supportid == "10"):
        wcc_data=WorkCompletionCost.objects.get_by_id(wcc_id)
        if (wcc_data.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(wcc_data.contractid)
            contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,1).values()
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,2).values()
            data={'con_file':list(contract_table_files),'price_file':list(price_table_files),'contracttype':wcc_data.contracttype}
        else:
            contract=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
            original_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,1).values()
            original_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,2).values()
            amendment_addendum_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,1).values()
            amendment_addendum_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,2).values()
            confile=original_contract_table_files.union(amendment_addendum_contract_table_files)
            price_table_files=original_price_table_files.union(amendment_addendum_price_table_files)
            data={'con_file':list(confile),'price_file':list(price_table_files),'contracttype':wcc_data.contracttype}
        return JsonResponse(data,safe=False)
    else:
        getfiles=WccFileUpload.objects.get_by_support(wcc_id,True,supportid).values()
        data={'filecount':getfiles.count(),'files':list(getfiles)}
        return JsonResponse(data)

class WccView(View):    
    def get(self,request,pk):
        request.session['mainmenu'] = 'wcc_list'
        data = self.get_context_data(pk=pk)
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        submit_date_format=confulldate(wcc_data.wcc_submit_date,request.company.id)
        data['submit_date_format']=submit_date_format
        data['request']=request

        return render(request,'wccview.html',data)
    
    
    def get_context_data(self,**kwargs):
        pk = kwargs.get('pk')
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        costcodedata=CostCodeVendor.objects.get_by_id(wcc_data.costcodevendor.id) if wcc_data.costcodevendor else ''
        wccworkvalues=WorkCompletionValue.objects.filter_by_wcc(pk)
        wcc_number = wccworkvalues.values_list('wcc_number',flat=True)
        amendment=''
        contract_file_name=''
        price_table_file_name=''
        if (wcc_data.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(wcc_data.contractid)
            contract_number=contract.reference_number
            contract_file=contract.upload_contract
            price_table=contract.upload_pricetable
            contract_file_name=contract.contract_file_name
            price_table_file_name=contract.price_table_file_name
            currency_symbol=contract.currency.currency_symbol
            currency_data=contract.currency

            contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,1).values()
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,2).values()

        else:
            contract=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
            contract_number=contract.amendment_reference_number
            currency_symbol=contract.amendment_currency.currency_symbol
            # contract_file=contract.service.upload_contract
            # contract_file_name=contract.service.contract_file_name
            # amendment=contract.amendment_upload_contract
            # price_table=contract.amendment_upload_pricetable
            # # price_table_file_name=contract.price_table_file_name
            currency_data=contract.amendment_currency
            contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,1).values()
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,2).values()
            amendment_addendum_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,1).values()
            amendment_addendum_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,2).values()
            confile=contract_table_files.union(amendment_addendum_contract_table_files)
            price_table_files=price_table_files.union(amendment_addendum_price_table_files)
    
        wcc_approved_date= WccApproval.objects.filter_by_wcc(pk).exclude(approval_status=1).last()
        approved_by_user=None
        approved_users=WccApproval.objects.filter_by_wcc(pk).exclude(approval_status=1)
        wcc_approval = WccApproval.objects.filter_by_wcc(pk).exclude(approval_status=1)
        for approval in wcc_approval:
            approved_by_user = approval.user if wcc_approval else None
        supports_docs=getsupportsdata()
        seen_users = set()
        unique_approved_users = []
        approved_ids=[]
        for approval in wcc_approval:
            user_id = approval.user.id
    
            approved_ids.append(approval)
            if user_id not in seen_users:
                seen_users.add(user_id)
                unique_approved_users.append(approval)

        approved_users = unique_approved_users

        data= {'pk':pk,'wcc_data':wcc_data,
            #    'contract_file_name':contract_file_name,
            #    'price_table_file_name':price_table_file_name,
               'costcodedata':costcodedata,'wccworkvalues':wccworkvalues,'currency_symbol':currency_symbol,'contractmaster':contract, 'approved_by_user': approved_by_user,'wcc_approval':wcc_approval,'approved_ids':approved_ids,
            #    'contract_file':contract_file,
            #    'price_table':price_table,
            #    'amendment':amendment,
               'supports_docs':supports_docs,'contract_file_name': ", ".join([file['original_file_name'] for file in contract_table_files]),'contract_number':contract_number,'wcc_number':",".join(map(str,wcc_number)),  'price_table_file_name': ", ".join([file['original_file_name'] for file in price_table_files]),'currency_data':currency_data,'approved_users':approved_users,'price_table_files':price_table_files,'wcc_approved_date':wcc_approved_date}
        return data

class WccEditFormOne(View):
    def get(self,request,pk):
        request.session['mainmenu'] = 'wcc_list'
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        company=Settings.objects.getcompany_settings(request.user.company.id)
        vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        contractlist=ContractMaster.objects.getcontractmaster(vendorid.id)
        cost_code_list = CostCodeVendor.objects.get_vendor_data(vendorid.id,1)
        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        if(getlastlevel != None):
            lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        else:
            lastlevel=None 
        # allcontractlist=[]
        # for contract in contractlist:
        #     if contract.wcc == 1:
        #         allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original'})
        #     get_amendmentlist=Amendment.objects.getamendment(contract.id).exclude(wcc=0)
        #     for amendment in get_amendmentlist:
        #         if amendment.amendment_type == 'Amendment':
        #             allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment'})
        #         else:
        #             allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum'})
        allcontractlist=[]
        for contract in contractlist:
            if contract.wcc == 1:
                allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original','check_status':contract.projects.active_status})
            get_amendmentlist=Amendment.objects.getamendment(contract.id).exclude(wcc=0)
            for amendment in get_amendmentlist:
                if amendment.amendment_type == 'Amendment':
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment','check_status':amendment.service.projects.active_status})
                else:
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum','check_status':amendment.service.projects.active_status})
        if (wcc_data.contractid == ''):
            getprojectid=''
            projectid=''
        else:
            if (wcc_data.contracttype == 'original'):
                getprojectid=ContractMaster.objects.getcontract(wcc_data.contractid)
                projectid=getprojectid.projects.id
            else:
                getprojectid=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
                projectid=getprojectid.service.projects.id
        data={'company':company,'allcontractlist':allcontractlist,'vendor':vendorid,'company':request.company,'lastlevel':lastlevel,'cost_code_list':cost_code_list,'wcc_data':wcc_data,'getprojectid':projectid}
        return render(request,'wcceditformone.html',data)
    
    def post(self,request,pk):
        fromdate=request.POST.get('fromdate')
        todate=request.POST.get('todate')
        
        contractnameservice=request.POST.get('contractnameservice')
        contractservicetype=request.POST.get('contractservicetype')
        service_rendered=request.POST.get('service_rendered')
        location_service=request.POST.get('location_service')
        project=request.POST.get('project')
        block=request.POST.get('block',None)
        field=request.POST.get('field',None)
        well=request.POST.get('well',None)
        block_not=request.POST.get('block_not')
        field_not=request.POST.get('field_not')
        well_not=request.POST.get('well_not')
        costcode=request.POST.get('costcode',None)
        contract=request.POST.get('contractid')
        if contract == None or contract == '':
            contractid = ''
            contract_type = ''
        else:
            split_contract=contract.split("-")
            contractid = split_contract[0]
            contract_type = split_contract[1]
        if (fromdate != '' and fromdate != None):
            from_datetime_object = datetime.strptime(fromdate,"%d-%b-%Y")
        else:
            from_datetime_object=None
        if (todate != '' and todate != None):
            todate_datetime_object = datetime.strptime(todate,"%d-%b-%Y")
        else:
            todate_datetime_object=None
        # from_datetime_object = datetime.strptime(fromdate,'%d-%b-%Y')
        # todate_datetime_object = datetime.strptime(todate,'%d-%b-%Y')
        WorkCompletionCost.objects.updateworkcompletioncost(pk,from_datetime_object,todate_datetime_object,contractid,contract_type,contractnameservice,contractservicetype,service_rendered,location_service,project,block,field,well,block_not,field_not,well_not,costcode)
        submit_type=request.POST.get('submit_type')
        if (submit_type == "0"):
            return redirect('wcc:wcclist')
        else:
            return redirect('wcc:wcceditformtwo',pk=pk)

class WccEditFormTwo(View):
    def get(self,request,pk):
        company=Settings.objects.getcompany_settings(request.user.company.id)
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        from_date = wcc_data.fromdate
        wcc_values=WorkCompletionValue.objects.filter_by_wcc(pk)
        amendment=''
        contract_file_name=''
        price_table_file_name=''
        if (wcc_data.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(wcc_data.contractid)
            contract_amount = contract.amount if contract.amount == 'No Max Limit' else contract.amount.replace(',','')
            contract_reference = contract.reference_number
            contract_date=contract.executed_date.date()
            # contract_file=contract.upload_contract
            price_table=contract.upload_pricetable
            if contract.upload_contract:
                contract_file = contract.upload_contract
                contract_file_name = contract.contract_file_name
            else:
                contract_file = None
                contract_file_name = None

            # contract_file_name=contract.contract_file_name
            price_table_file_name=contract.price_table_file_name
            currency_symbol=contract.currency.currency_symbol
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id)

        else:
            contract=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
            contract_amount = contract.amendment_amount if contract.amendment_amount == 'No Max Limit' else contract.amendment_amount.replace(',','')
            contract_reference = contract.amendment_reference_number
            contract_date=contract.amendment_executed_date.date()
            currency_symbol=contract.amendment_currency.currency_symbol
            contract_file=contract.service.upload_contract
            amendment=contract.amendment_upload_contract
            price_table=contract.amendment_upload_pricetable
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id)

        if wcc_values.exists():
            wcc_number = wcc_values.values_list('wcc_number',flat=True).first()
        else:
            wcc_number = wcc_number_generate(wcc_data.vendor.id,contract_reference)
        supports_docs=getsupportsdata()
        data={'contractmaster':contract,'wcc_data':wcc_data,'contract_file_name':contract_file_name,'price_table_file_name':price_table_file_name,'company':company,'total_value':contract_amount,'contract_reference':contract_reference,'contract_date':contract_date,'pk':pk,'wcc_values':wcc_values.first(),'contract_file':contract_file,'price_table':price_table,'currency_symbol':currency_symbol,'amendment':amendment,'supports_docs':supports_docs,'wcc_number':wcc_number,'from_date': from_date ,'price_table_files':price_table_files}
        return render(request,'wcceditformtwo.html',data)

    def post(self,request,pk):
        dateformat=request.POST.get('dateformat')
        wcc_num=request.POST.get('wc_num')
        wcc_date=request.POST.get('wcc_date')
        wcc_file=request.FILES.get('wcc_file',None)
        totalvalue=request.POST.get('totalvalue')
        wccfilehdnid=request.POST.get('wccfilehdnid')
        getallfilehdnids=request.POST.getlist('hdnfileid')
        pattern = r'[^A-Za-z0-9.,]+'
        matches = re.sub(pattern, '', totalvalue)
        if (len(matches) > 0):
            get_total_value = matches
        else:
            get_total_value = ''
        get_date=getinvoiceDate(dateformat,wcc_date)
        convert_date = None if get_date == '' else get_date
        checksupportfile=request.POST.getlist('checksupportfile')
        vendor=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        if (WorkCompletionValue.objects.filter_by_wcc(pk).exists()):
            WorkCompletionValue.objects.update_data(pk,wcc_num,convert_date,get_total_value,wcc_file,wccfilehdnid)
        else:
            WorkCompletionValue.objects.create_wcc_value(vendor,pk,wcc_num,convert_date,get_total_value,wcc_file,request.company)
        for support in checksupportfile:
            files=checksupportfile=request.FILES.getlist('file'+str(support))
            for file in files:
                create_file=WccFileUpload.objects.create_wcc_supportfile(vendor,pk,support,file,request.company)
                getallfilehdnids.append(create_file.id)
        new_list = list(filter(None, getallfilehdnids))
        WccFileUpload.objects.update_file_status(pk,new_list)
        submit_type=request.POST.get('submit_type')
        if (submit_type == '2'):
            return redirect('wcc:wccpreview',pk=pk)
        elif (submit_type == '1'):
            messages.success(self.request, 'WCC Submitted Successfully')
            WorkCompletionCost.objects.update_by_id(pk,1)
            wcc_data=WorkCompletionCost.objects.get_by_id(pk)
            wcc_work=WorkCompletionValue.objects.get_by_wcc(pk)
            wcc_flow=WccFlow.objects.get_by_project(wcc_data.project_id)
            if (wcc_data.contracttype == "original"):
                contract_data=ContractMaster.objects.getcontract(wcc_data.contractid)
            else:
                amendment_data=Amendment.objects.get_by_id(wcc_data.contractid , 1 ).first()
                contract_data=ContractMaster.objects.getcontract(amendment_data.service.id)
            if (wcc_flow.level_type == "discipline"):
                get_flow_level=WccFlowLevel.objects.filter_wcc_level("discipline",contract_data.projectdisciplinetype_id,wcc_flow.id,True).first()
            elif (wcc_flow.level_type == "cluster"):
                get_flow_level=WccFlowLevel.objects.filter_wcc_level("cluster",contract_data.projectdiscipline.cluster_id,wcc_flow.id,True).first()
            elif (wcc_flow.level_type == "well"):
                if wcc_data.well_not_applicable == "id":
                    get_flow_level=WccFlowLevel.objects.filter_wcc_level("well",wcc_data.well_id,wcc_flow.id,True).first()
                else:
                    get_flow_level=WccFlowLevel.objects.filter_wcc_levelbased(contract_data.projectdisciplinetype_id,wcc_flow.id,True).first()
            if not get_flow_level:
                get_flow_level=WccFlowLevel.objects.filter(project_id=wcc_data.project_id,status=1,wcc_flow_id=wcc_flow.id,company_id=request.company.id).first()
            wcc_flow_level_station=WccPerStation.objects.filter_by_flow_level(get_flow_level.id,True).first()
            get_users=WccStationUsers.objects.filter_by_station(wcc_flow_level_station.id,1)
            server_timezone = pytz.timezone('Asia/Kolkata')
            # # Get the current time on the server
            # server_time = datetime.now(server_timezone)
            # print("Server time (New York):", server_time)
            # # Get your local system's timezone
            # local_timezone = pytz.timezone('Asia/Kolkata')  # Replace with your local timezone
            # # Convert the server time to your local time
            # local_time = server_time.astimezone(local_timezone)
            # print("Local time:", local_time)
            # print("Server time:", server_time)
            now = datetime.now()
            # now = local_time
            calculate_time=add_time(now,request.company)
            for userdata in get_users:
                create_user=WccApproval.objects.create_data(wcc_data.id,userdata.wcc_flow.id,userdata.user_id,userdata.wcc_per_station_id,calculate_time,now) 
                #send email
                wcccreatedmail(request,userdata.user,wcc_data,wcc_work,vendor,'wcccreatedemail')
                # send notification
                url="wcc/approvalwcclist"
                verb="WCC Submitted"
                description=f'{get_vendor_company_name(request.user.cin_number)} has Submitted WCC for {wcc_work.wcc_number}'
                notify_wcc(request,userdata,url,verb,description,"user")
            # wcc_flow_station=WccPerStation.objects.filter_by_project(wcc_data.project_id,1).first()
            # get_users=WccStationUsers.objects.filter_by_station(wcc_flow_station.id,1)
            # for userdata in get_users:
            #     create_user=WccApproval.objects.create_data(wcc_data.id,userdata.wcc_flow.id,userdata.user_id,userdata.wcc_per_station_id,now) 
            #     #send email
            #     wcccreatedmail(request,userdata.user,wcc_data,wcc_work,vendor,'wcccreatedemail')
            #     scheme=request.scheme
            #     gethost=request.get_host()
            #     url=f"{scheme}://{gethost}/wcc/approvalwcclist"
            #     url="wcc/approvalwcclist"
                    # verb="WCC Submitted"
                    # description=f'{get_vendor_company_name(request.user.cin_number)} has Submitted WCC for {wcc_work.wcc_number}'
                    # notify_wcc(request,userdata,url,verb,description)
        else:
             WorkCompletionCost.objects.update_by_id(pk,0)
        return redirect('wcc:wcclist')

def notify_wcc(request,userdata,url,verb,description,type):
    sender = request.user
    recipient=userdata.user if type == "user" else userdata
    scheme=request.scheme
    gethost=request.get_host()
    url=f"{scheme}://{gethost}/{url}"
    notify.send(sender, recipient=recipient,data=url, verb=verb, description=description)
    return

def notify_wcc_robust(request,userdata,url,verb,description,type):
    sender = request.user
    recipient=userdata.user if type == "user" else userdata
    scheme=request.scheme
    gethost=request.get_host()
    url=f"{scheme}://{gethost}/{url}"
    notify.send_robust(sender, recipient=recipient,data=url, verb=verb, description=description)
    return
def get_vendor_company_name(cin_number):
    vendor_company = ContractMasterVendor.objects.filter(vin=cin_number).first()
    return vendor_company.vendor_name

class CheckWccNumber(View):
    def post(self,request):
        wcc_number= request.POST.get('wcc_number')
        wcc_id=request.POST.get('wcc_id')
        check=list(WorkCompletionValue.objects.check_data(wcc_id=wcc_id,company=request.company,wcc_number=wcc_number))
        data={'status':True}
        if (len(check) > 0):
            data={'status':False}
        return JsonResponse(data)
    
class ProjectWccFlow(View):
    def get(self,request,project_id):
        get_project=Projectcreation.objects.get_by_id(project_id,0)
        users_list=ProjectUser.objects.getuser_byproject(project_id)
        # users_list=User.objects.filter(company_id=request.company,status=1).exclude(roles_id=4)
        level_types=['discipline','cluster',"well"]
        wcc_completion_data=WorkCompletionCost.objects.filter_by_project(project_id,0,1).count()
        wcc_roles=Role.objects.filter_by_module_id(8,request.company)
        data={'project':get_project,'users_list':users_list,'level_types':level_types,'wcc_completion_data':wcc_completion_data,'wcc_roles':wcc_roles}
        if WccFlow.objects.filter_by_project(project_id).exists():
            wcc_data=WccFlow.objects.get_by_project(project_id)
            wcc_station=WccPerStation.objects.filter_by_wcc(1,wcc_data.id)
            data.update({'wcc_data':wcc_data,'wcc_station':wcc_station})
        return render(request,'wccflow.html',data)

    def post(self,request,project_id):
        level_type=request.POST.get('level_type')
        level_list=request.POST.getlist('level')
        well_discipline=request.POST.getlist('well_discipline')
        print('asd',request.POST)
        if WccFlow.objects.filter_by_project(project_id).exists():
            wcc_data=WccFlow.objects.get_by_project(project_id)
            WccFlow.objects.update_data_project(wcc_data.id,level_type)
            if (level_type == "well"):
                flow_level_list=[]
                for well_based in well_discipline:
                    get_station=request.POST.get('station'+well_based)
                    if WccFlowLevel.objects.check_wcc_levelbased(well_based,wcc_data.id).exists():
                        WccFlowLevel.objects.update_levelbased(well_based,wcc_data.id,get_station)
                        flow_level=WccFlowLevel.objects.check_wcc_levelbased(well_based,wcc_data.id).first()
                        flow_level_list.append(flow_level.id)
                        flow_level_id=flow_level.id
                    else:
                        create_wcc_flow_level=WccFlowLevel.objects.create_well_based_data(request.company,project_id,wcc_data,well_based,get_station)
                        flow_level_list.append(create_wcc_flow_level.id)
                        flow_level_id=create_wcc_flow_level.id
                    per_station_list=[]
                    for value in range(int(get_station)):
                        hdn_per_station_user=request.POST.get('hdnstation_user'+well_based+'-'+str(value))
                        user_role=request.POST.get('station_role'+well_based+'-'+str(value))
                        per_station_user=request.POST.get('station_user'+well_based+'-'+str(value))
                        if (hdn_per_station_user):
                            WccPerStation.objects.update_wcc_per_station(hdn_per_station_user,per_station_user,user_role)
                            per_station_list.append(hdn_per_station_user)
                            per_station_id=hdn_per_station_user
                        else:
                            create_wcc_station=WccPerStation.objects.create_wcc_per_station(flow_level_id,per_station_user,wcc_data,project_id,user_role)
                            per_station_list.append(create_wcc_station.id)
                            per_station_id=create_wcc_station.id
                        station_user=request.POST.getlist('user'+well_based+'-'+str(value))
                        users_list=[]
                        for user in station_user:
                            if WccStationUsers.objects.check_by_user(per_station_id,user).exists():
                                WccStationUsers.objects.update_user_status(per_station_id,user)
                                user_data=WccStationUsers.objects.check_by_user(per_station_id,user).first()
                                users_list.append(user_data.id)
                            else:
                                create_station_users=WccStationUsers.objects.create_wcc_station_user(user,per_station_id,wcc_data.id,project_id,flow_level_id)
                                users_list.append(create_station_users.id)
                        WccStationUsers.objects.edit_station_users(per_station_id,users_list)
                    WccStationUsers.objects.update_other_status(wcc_data.id,flow_level_id,per_station_list)
                    WccPerStation.objects.update_all_per_station(wcc_data.id,flow_level_id,per_station_list)
                WccFlowLevel.objects.update_all_well_based(wcc_data.id,flow_level_list)
            # next
            flow_level_list=[]
            for level in level_list:
                get_station=request.POST.get('station'+level)
                if WccFlowLevel.objects.check_wcc_level(level_type,level,wcc_data.id).exists():
                    WccFlowLevel.objects.update_wcc_flowlevel(level,wcc_data.id,get_station,level_type)
                    print('asfc',level_type,level,wcc_data.id,True)
                    flow_level=WccFlowLevel.objects.filter_wcc_level(level_type,level,wcc_data.id,True).first()
                    flow_level_list.append(flow_level.id)
                    flow_level_id=flow_level.id
                else:
                    create_wcc_flow_level=WccFlowLevel.objects.create_flow_level(request.company,project_id,wcc_data,level_type,level,get_station)
                    flow_level_list.append(create_wcc_flow_level.id)
                    flow_level_id=create_wcc_flow_level.id

                per_station_list=[]
                for value in range(int(get_station)):
                    hdn_per_station_user=request.POST.get('hdnstation_user'+level+'-'+str(value))
                    user_role=request.POST.get('station_role'+level+'-'+str(value))
                    per_station_user=request.POST.get('station_user'+level+'-'+str(value))
                    if (hdn_per_station_user):
                        WccPerStation.objects.update_wcc_per_station(hdn_per_station_user,per_station_user,user_role)
                        per_station_list.append(hdn_per_station_user)
                        per_station_id=hdn_per_station_user
                    else:
                        create_wcc_station=WccPerStation.objects.create_wcc_per_station(flow_level_id,per_station_user,wcc_data,project_id,user_role)
                        per_station_list.append(create_wcc_station.id)
                        per_station_id=create_wcc_station.id
                    station_user=request.POST.getlist('user'+level+'-'+str(value))
                    users_list=[]
                    for user in station_user:
                        if WccStationUsers.objects.check_by_user(per_station_id,user).exists():
                            WccStationUsers.objects.update_user_status(per_station_id,user)
                            user_data=WccStationUsers.objects.check_by_user(per_station_id,user).first()
                            users_list.append(user_data.id)
                        else:
                            create_station_users=WccStationUsers.objects.create_wcc_station_user(user,per_station_id,wcc_data.id,project_id,flow_level_id)
                            users_list.append(create_station_users.id)
                    WccStationUsers.objects.edit_station_users(per_station_id,users_list)
                WccStationUsers.objects.update_other_status(wcc_data.id,flow_level_id,per_station_list)
                WccPerStation.objects.update_all_per_station(wcc_data.id,flow_level_id,per_station_list)
            WccFlowLevel.objects.update_all_flow_level(wcc_data.id,flow_level_list)
        else:
            create_wcc_flow=WccFlow.objects.create_flow(project_id,level_type,request.company)
            if (level_type == "well"):
                for well_based in well_discipline:
                    get_station=request.POST.get('station'+well_based)
                    create_wcc_flow_level=WccFlowLevel.objects.create_well_based_data(request.company,project_id,create_wcc_flow,well_based,get_station)
                    # WccFlowLevel.objects.filter(id=create_wcc_flow_level.id).update()
                    for value in range(int(get_station)):
                        user_role=request.POST.get('station_role'+well_based+'-'+str(value))
                        per_station_user=request.POST.get('station_user'+well_based+'-'+str(value))
                        create_wcc_station=WccPerStation.objects.create_wcc_per_station(create_wcc_flow_level.id,per_station_user,create_wcc_flow,project_id,user_role)
                        station_user=request.POST.getlist('user'+well_based+'-'+str(value))
                        for user in station_user:
                            create_station_users=WccStationUsers.objects.create_wcc_station_user(user,create_wcc_station.id,create_wcc_flow.id,project_id,create_wcc_flow_level.id)
            for level in level_list:
                get_station=request.POST.get('station'+level)
                create_wcc_flow_level=WccFlowLevel.objects.create_flow_level(request.company,project_id,create_wcc_flow,level_type,level,get_station)

                for value in range(int(get_station)):
                    user_role=request.POST.get('station_role'+level+'-'+str(value))
                    per_station_user=request.POST.get('station_user'+level+'-'+str(value))
                    create_wcc_station=WccPerStation.objects.create_wcc_per_station(create_wcc_flow_level.id,per_station_user,create_wcc_flow,project_id,user_role)
                    station_user=request.POST.getlist('user'+level+'-'+str(value))
                    for user in station_user:
                        create_station_users=WccStationUsers.objects.create_wcc_station_user(user,create_wcc_station.id,create_wcc_flow.id,project_id,create_wcc_flow_level.id)
            # 
            
        project_name =  request.POST.get('project_userlog')
        print(project_name,'wccworkflo.....')
        usercreate = request.user.roles_id
        create_user_log(request,project_name,' WCC Approval Workflow','Create','WCC Approval Workflow Created',usercreate)        
        return redirect('projects:projectwcc')

class WccProjectLevels(View):
    def post(self,request):
        project_id= request.POST.get('project_id')
        get_type=request.POST.get('type')
        if (get_type == "discipline"):
            get_data=list(ProjectDevelopmentSubType.objects.filter_by_project(project_id,1).values('discipline_subtype__discipline_subtype','project_discipline__project_discipline','id','project_discipline__cluster__clustersubname__cluster_subname'))
            data=change_key_name(get_data,"discipline_subtype__discipline_subtype","name")
        elif (get_type == "cluster"):
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
                #check above well in roshini sys
            # get_data=list(ProjectWellName.objects.filter_by_project(project_id,1).values('wellname__well_subname','id','welltype__discipline_type__discipline_subtype__discipline_subtype','welltype__discipline_type_id','welltype__discipline_type__project_discipline__project_discipline'))
                # data=change_key_name(get_data,"wellname__well_subname","name")
        data={'data':data}
        return JsonResponse(data)
    
class ApprovalWccList(View):
    def get(self,request):
        markas_read_status(request.get_full_path())
        request.session['submenu'] = 'wcc_list'
        wcclist=WorkCompletionCost.objects.filter_by_status(1,request.company.id).order_by('-id')
        sign_data=check_user_sign(self.request.user)
        data={'wcclist':wcclist,'sign_data':sign_data}
        return render(request,'approvalwcclist.html',data)
    
class WccApprovalView(View):
    def get(self,request,pk):
        wccworkvalues=WorkCompletionValue.objects.filter_by_wcc(pk)
        if (wccworkvalues[0].wcc.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(wccworkvalues[0].wcc.contractid)
            currency_symbol=contract.currency.currency_symbol
        else:
            contract=Amendment.objects.get_by_id(wccworkvalues[0].wcc.contractid,1).first()
            currency_symbol=contract.amendment_currency.currency_symbol
        supports_docs=getsupportsdata()
        sign_data=check_user_sign(self.request.user)
        get_role=WccApproval.objects.get_by_user_wcc(request.user.id,pk).last()
        wcc_rights=RoleRight.objects.filter_by_role(get_role.wcc_per_station.role,True) 
        data={'wccworkvalues':wccworkvalues,'currency_symbol':currency_symbol,'pk':pk,'supports_docs':supports_docs,'wcc_rights':wcc_rights ,'sign_data':sign_data}
        return render(request,'wccapprovalview.html',data)
    
    def post(self,request,pk):  
        submit_type=request.POST.get('submit_type')
        wcc_number_user_log = request.POST.get('wcc_userlog')
        today = date.today()
        date_today = today.strftime("%d-%b-%Y")
        # current_date=timezone.now()
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        wcc_work=WorkCompletionValue.objects.filter_by_wcc(pk)
        print(wcc_number_user_log,'wcc_number_user_log.......')
        if wcc_work.exists():
            wcc_work = wcc_work.first()  # Get the first object
            print(wcc_number_user_log, 'wcc_number_user_log.......')

        vendor=ContractMasterVendor.objects.get_byid(wcc_data.vendor_id,request.company)
        comments=request.POST.get('main_comments',None)
        recipient=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        url="wcc/wcclist"
        status=""
        current_date=datetime.now()
        #ahj
        if (submit_type == '1'):
            status="Approved"
            WccApproval.objects.update_user_data(request.user.id,pk,2,comments,current_date)
            get_data=WccApproval.objects.filter_by_user_wcc(pk,request.user.id).last()
            get_station=WccPerStation.objects.get_by_id(get_data.wcc_per_station_id)
            next_data = WccPerStation.objects.get_next_data(get_station.id,get_station.wcc_flow_level_id ).order_by('id')
            if (next_data.count() > 0):
                next_station = next_data.first()
                get_users=WccStationUsers.objects.filter_by_station(next_station.id,1)
                messages.success(self.request, 'WCC Submitted Successfully')
                now = datetime.now()
                calculate_time=add_time(now,request.company)
                print(calculate_time)
                # calculate_time= now+timedelta(hours=get_company_invoice_time.time_allotted) if get_company_invoice_time.time_unit == 0 else now+timedelta(days=get_company_invoice_time.time_allotted)
                for userdata in get_users:
                    create_user=WccApproval.objects.create_data(pk,userdata.wcc_flow.id,userdata.user_id,userdata.wcc_per_station_id,calculate_time,now) 
                    title = request.user.Title+'.' if request.user.Title != None else '' 
                    approver_name=f"{title} {request.user.name} {request.user.lastname}"
                    wcccreatedmail(request,userdata.user,wcc_data,wcc_work,vendor,'station_to_station',approver_name)
                    verb="WCC Approved"
                    url="wcc/approvalwcclist"
                    description=f'{get_vendor_company_name(vendor.vin)} has Submitted WCC for {wcc_work.wcc_number}'
                    notify_wcc(request,userdata,url,verb,description,"user")
                    verb='WCC '+status
                    description=f'WCC {status} by {request.company.first_name} on {date_today} for {wcc_data.name_service}'
                for notifications in allVendors:
                    notify_wcc(request,notifications,url,verb,description,"vendor")
            else:
                #approve wcc status 
                recipient=User.objects.filter(cin_number=vendor.vin)
                WorkCompletionCost.objects.approve_wcc(pk,1,current_date)
                get_byvin=ContractMasterVendor.objects.get_byvin(vendor.vin,request.company)
                wcc_approve_mail_robust(request,wcc_data,wcc_work,get_byvin)
                verb='WCC '+status
                description=f'WCC {status} by {request.company.first_name} on {date_today} for {wcc_data.name_service}'
                for notifications in allVendors:
                    notify_wcc(request,notifications,url,verb,description,"vendor")
                  
        elif (submit_type == '2'):
            get_exceptional = request.POST.getlist('exceptional')
            messages_json = request.POST.get('selected_messages')
    
            selected_messages = json.loads(messages_json)
            checklist=WccExceptional.objects.filter(wcc_id=pk).last()
            if checklist:
                return_status=int(checklist.return_status)+1
            else :
                return_status=1
            
            exceptional_list=[WccExceptional(wcc_id=pk,exceptional_type=i,return_status=return_status) for i in get_exceptional]
            WccExceptional.objects.bulk_create(exceptional_list)
            if selected_messages:
                ok=WccExceptional.objects.filter(wcc_id=pk)
                WccExceptional.objects.filter(wcc_id=pk,return_status=return_status).update(checked_messages=selected_messages)

            #return
            # status="Returned"
            # messages.success(self.request, 'WCC Returned Successfully')
            # WccApproval.objects.update_user_data(request.user.id,pk,3,comments,current_date)
            # WorkCompletionCost.objects.approve_wcc(pk,2,current_date)
            # wcc_status_mail(request,wcc_data,wcc_work,vendor,'returned',comments)
            # verb='WCC '+status
            # description=f'WCC {status} by {request.company.first_name} on {date_today} for {wcc_data.name_service}'
            # for notifications in allVendors:
            #     notify_wcc(request,notifications,url,verb,description,"vendor")

            wcc_return_flow(pk,8,submit_type,comments,request)
        elif (submit_type == '3'):
            #reject
            status="Rejected"
            messages.success(self.request, 'WCC Rejected')
            messages.success(self.request, 'WCC Rejected')
            WccApproval.objects.update_user_data(request.user.id,pk,0,comments,current_date)
            WorkCompletionCost.objects.approve_wcc(pk,3,current_date)
            get_exceptional = request.POST.getlist('exceptional')
            messages_json = request.POST.get('selected_messages')
    
            selected_messages = json.loads(messages_json)
            checklist=WccExceptional.objects.filter(wcc_id=pk).last()
            if checklist:
                return_status=int(checklist.return_status)+1
            else :
                return_status=1
            
            exceptional_list=[WccExceptional(wcc_id=pk,exceptional_type=i,return_status=return_status) for i in get_exceptional]
            WccExceptional.objects.bulk_create(exceptional_list)
            if selected_messages:
                ok=WccExceptional.objects.filter(wcc_id=pk)
                WccExceptional.objects.filter(wcc_id=pk,return_status=return_status).update(checked_messages=selected_messages)

            wcc_exceptional_instance = WccExceptional.objects.filter(wcc_id=pk, status=1).exclude(exceptional_type=5).last()
            if wcc_exceptional_instance:
                checked_messages = wcc_exceptional_instance.checked_messages
            else:
                checked_messages = None
            # wcc_status_mail(request,wcc_data,wcc_work,vendor,'returned',comments)
            return_reason_messages=split_by_newline(checked_messages)
            verb='WCC for '+status
            description=f'WCC {status} by {request.company.first_name} on {date_today} for {wcc_data.name_service}'
            for notifications in allVendors:
                notify_wcc(request,notifications,url,verb,description,"vendor")
                wccreturnrejectmail(request,notifications,wcc_data,wcc_work,request.user.id,date_today,status,return_reason_messages)

        print(wcc_number_user_log,'wcc_number_user_log1.......')        
        usercreate=request.user.roles_id
        create_user_log(request,wcc_number_user_log,'WCC','Create',f'WCC has been {status} ',usercreate)        
        return redirect('wcc:approvalwcclist')


class WccApprovalTrack(View):
    def get(self,request,pk):
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        wcc_flow=WccFlow.objects.get_by_project(wcc_data.project_id)
        contract=ContractMaster.objects.getcontract(wcc_data.contractid)
       
        if (wcc_data.contracttype == "original"):
            contract_data=ContractMaster.objects.getcontract(wcc_data.contractid)
            vendor_id = contract_data.contractvendor
            contract_reference = contract_data.reference_number
        else:
            amendment_data=Amendment.objects.get_by_id(wcc_data.contractid ,1).first()
            contract_data=ContractMaster.objects.getcontract(amendment_data.service.id)
            vendor_id = contract_data.contractvendor
            contract_reference = contract_data.reference_number
        wcc_number = wcc_number_generate(vendor_id,contract_reference)    
        data={'pk':pk,'contract_data':contract_data,'wcc_data':wcc_data}
        if (wcc_data.wcc_status == 0):
            get_approval_wcc_station=list(WccApproval.objects.filter(wcc_id=pk).values('wcc_per_station_id').annotate(dcount=Count('wcc_per_station_id')))
            get_station_ids=[i.get('wcc_per_station_id') for i in get_approval_wcc_station]
            if (wcc_flow.level_type == "discipline"):
                get_flow_level=WccFlowLevel.objects.filter_wcc_level("discipline",contract_data.projectdisciplinetype_id,wcc_flow.id,True).first()
            elif (wcc_flow.level_type == "cluster"):
                #check cluster
                get_flow_level=WccFlowLevel.objects.filter_wcc_level("cluster",contract_data.projectdiscipline.cluster_id,wcc_flow.id,True).first()
            elif (wcc_flow.level_type == "well"):
                if wcc_data.well_not_applicable == "id":
                    get_flow_level=WccFlowLevel.objects.filter_wcc_level("well",wcc_data.well_id,wcc_flow.id,True).first()
                else:
                    get_flow_level=WccFlowLevel.objects.filter_wcc_levelbased(contract_data.projectdisciplinetype_id,wcc_flow.id,True).first()
            if not get_flow_level:
                get_flow_level=WccFlowLevel.objects.filter(project_id=wcc_data.project_id,status=1,wcc_flow_id=wcc_flow.id,company_id=request.company.id).first()
            wcc_flow_level_station=WccPerStation.objects.filter_by_flow_level(get_flow_level.id,True)
            filter_wcc_station=wcc_flow_level_station.exclude(id__in=get_station_ids)
            previous_count=wcc_flow_level_station.count()
            userslist=WccApproval.objects.filter(wcc_per_station_id__in=wcc_flow_level_station.values_list('id'),wcc_id=pk).exclude(approval_status=1).count()
            total_approval=0
            
            print("yes",wcc_number)
            if(previous_count == userslist):
                total_approval=1
            data.update({'station_list':get_station_ids,'pending_station_data':filter_wcc_station,'total_approval':total_approval,'wcc_number': wcc_number})
        else:
            approved_users=WccApproval.objects.filter(wcc_id=pk).exclude(approval_status=1)
            data.update({'approved_users':approved_users,'wcc_number': wcc_number})
        return render(request,'wcc_approval_track.html',data)
    
class ProjectWccView(View):
    def get(self,request,project_id):
        get_project=Projectcreation.objects.get_by_id(project_id,0)
        users_list=ProjectUser.objects.getuser_byproject(project_id)
        level_types=['discipline','cluster',"well"]
        wcc_completion_data=WorkCompletionCost.objects.filter_by_project(project_id,0,1).count()
        wcc_roles=Role.objects.filter_by_module_id(8,request.company)
        data={'project':get_project,'users_list':users_list,'level_types':level_types,'wcc_completion_data':wcc_completion_data,'wcc_roles':wcc_roles}
        if WccFlow.objects.filter_by_project(project_id).exists():
            wcc_data=WccFlow.objects.get_by_project(project_id)
            wcc_station=WccPerStation.objects.filter_by_wcc(1,wcc_data.id)
            data.update({'wcc_data':wcc_data,'wcc_station':wcc_station})
        return render(request,'projectwccview.html',data) 

class WccPDFView(View):
    template_name='pdf/wccpdf.html'
    def get(self,request,pk):
        wcc_summary = WccView()
        context = wcc_summary.get_context_data(pk=pk)
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        submit_date_format=confulldate(wcc_data.wcc_submit_date,request.company.id)
        context['submit_date_format']=submit_date_format
        return pdf_view(request,self.template_name,context)

class CheckWccApprovalProcess(View):
    def get(self,request):
        wcc_list=ast.literal_eval(request.GET.get('wcc_ids'))
        get_company_user=User.objects.filter(company=request.user.company).first()
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
        current_timestamp = datetime.timestamp(parsed_datetime)
        for id in wcc_list:
            wcc_detail=WorkCompletionCost.objects.get_by_id(id)
            wcc_work_value=WorkCompletionValue.objects.get_by_wcc(wcc_detail.id)       
            calculate_time=add_time(now,request.company)
            get_wcc_flow=WccApproval.objects.filter(wcc_id=wcc_detail.id).last()
            formatted_datetime = get_wcc_flow.notification_at.strftime("%Y-%m-%d %H:%M:%S")
            parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
            get_notify_timestamp = datetime.timestamp(parsed_datetime)
            if (current_timestamp >= get_notify_timestamp):
                print('send Notify')
                get_flow_users=WccApproval.objects.filter(wcc_id=wcc_detail.id,wcc_per_station_id=get_wcc_flow.wcc_per_station.id,invoice_override=0)
                for flow_user in get_flow_users:
                    sender = get_company_user
                    recipient=flow_user.user
                    scheme=request.scheme
                    gethost=request.get_host()
                    url=f"{scheme}://{gethost}/wcc/approvalwcclist"
                    notify.send(sender, recipient=recipient,data=url, verb='Indication Mail', description=f'Please Approve these {wcc_work_value.wcc_number} Wcc')
                wcc_per_station_data=WccPerStation.objects.filter(project_id=wcc_detail.project.id,status=1,wcc_flow_level_id=get_wcc_flow.wcc_per_station.wcc_flow_level.id)
                for station_data in wcc_per_station_data:
                    check_right=RoleRight.objects.filter(role_id=station_data.role_id,right__slug="wcc-override",status=1).first()
                    if (check_right):
                        get_override_users=WccStationUsers.objects.filter(wcc_per_station_id=station_data.id,status=1)
                        for over_ride_user in get_override_users:
                            if (WccApproval.objects.filter(wcc_id=id,wcc_per_station_id=get_wcc_flow.wcc_per_station.id,user_id=over_ride_user.user.id).exists()):
                                print('sa',over_ride_user.user)
                            else:
                                print('no',over_ride_user.user)
                                #create override user
                                WccApproval.objects.create_override_user(wcc_detail.id,over_ride_user.wcc_flow.id,over_ride_user.user.id,get_wcc_flow.wcc_per_station.id,calculate_time)
                            sender = get_company_user
                            recipient=over_ride_user.user
                            scheme=request.scheme
                            gethost=request.get_host()
                            url=f"{scheme}://{gethost}/wcc/approvalwcclist"
                            notify.send(sender, recipient=recipient,data=url, verb='Indication Mail', description=f'Wcc {wcc_work_value.wcc_number} Still Pending')
                WccApproval.objects.filter(wcc_id=wcc_detail.id,wcc_per_station_id=get_wcc_flow.wcc_per_station.id).update(notification_at=calculate_time)
            else:
                print('wait for wcc time')
        return JsonResponse({'data':'success'})

class WccAssignUsers(View):
    def get(self,request,pk):
        wcc_detail=WorkCompletionCost.objects.get_by_id(pk)
        get_wcc_current_flow=WccApproval.objects.filter(wcc_id=wcc_detail.id).last()
        get_flow_users=WccApproval.objects.filter(wcc_id=wcc_detail.id,wcc_per_station_id=get_wcc_current_flow.wcc_per_station.id).values_list('user_id',flat=True)
        users_list=list(ProjectUser.objects.getuser_byproject(wcc_detail.project_id).exclude(user__id__in=get_flow_users))
        data={'users_list':users_list}
        return render(request,'wcc_assign_users.html',data) 
    
    def post(self,request,pk):
        get_users=request.POST.getlist('users')
        wcc_detail=WorkCompletionCost.objects.get_by_id(pk)
        get_wcc_current_flow=WccApproval.objects.filter(wcc_id=wcc_detail.id).last()
        get_company_invoice_time=WccTimeTrigger.objects.filter(company=request.company).first()
        now = datetime.now()
        calculate_time= add_time(now,request.company)
        for user in get_users:
            WccApproval.objects.create_data(wcc_detail.id,get_wcc_current_flow.wcc_flow.id,user,get_wcc_current_flow.wcc_per_station.id,get_wcc_current_flow.notification_at,now)
        return redirect('wcc:approvalwcclist')


def get_wcc_details(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    user=User.objects.filter(Q(is_primary=1) | Q(is_secondary=1),id=request.user.id).first()
    vendor_status = True if user else False
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    if search_value:
        wcc_value = WorkCompletionValue.objects.filter(Q(wcc__vendor_id=vendorid.id ,wcc__company_id=request.company.id) & Q( wcc_number__icontains=search_value,wcc__vendor_id=vendorid.id ,wcc__company_id=request.company.id)).order_by('-wcc__id').distinct() if vendor_status == True else WorkCompletionValue.objects.filter(Q(wcc__vendor_id=vendorid.id ,wcc__company_id=request.company.id ,wcc__status=1,wcc__wcc_status=2) & Q( wcc_number__icontains=search_value,wcc__vendor_id=vendorid.id ,wcc__company_id=request.company.id ,wcc__status=1,wcc__wcc_status=2)).order_by('-id').distinct()
    else :
        wcc_value = WorkCompletionCost.objects.filter(Q(vendor_id=vendorid.id ,company_id=request.company.id) & Q(vendor_id=vendorid.id ,company_id=request.company.id)).order_by('-id').distinct() if vendor_status == True else WorkCompletionCost.objects.filter(vendor_id=vendorid.id ,company_id=request.company.id ,status=1,wcc_status=2).order_by('-id').distinct()
    full_wcc_value=wcc_value[start:start+length]
    all_Wcc_invoice=[]
    s_no=start+1
    for wcc in full_wcc_value:
        if search_value :
            wcc_invoice_number=WorkCompletionValue.objects.filter(id=wcc.id).first()
        else : 
            wcc_invoice_number=WorkCompletionValue.objects.filter_by_wcc(wcc.id).first()

        wcc_inv_num=None
        if wcc_invoice_number == None :
            wcc_inv_num="---"
        else :
            wcc_inv_num=wcc_invoice_number.wcc_number
        
        if search_value :
            wcc=WorkCompletionCost.objects.filter(id=wcc.wcc_id).first()
            return_query = wcc.wcc_query_status
        else :
            wcc=wcc
            return_query = wcc.wcc_query_status

        if wcc.fromdate == None or wcc.todate == None  :
            from_date_month = "---"
            from_date_year = "---"
            to_date_month = "---"
            to_date_year = "---"
            period_date ="---"
        else:    
            from_date_month = wcc.fromdate.strftime('%b') 
            from_date_year = wcc.fromdate.year 
            to_date_month = wcc.todate.strftime('%b')  
            to_date_year = wcc.todate.year 
            period_date = f"{from_date_month}-{from_date_year} to {to_date_month}-{to_date_year}"
        wcc_submit_date=confulldate(wcc.wcc_submit_date,request.company.id)
        approve_status=""
        wcc_invoice_status = ""
        wcc_status=""
        if wcc.wcc_status == 0 :
            approve_status="Awaiting approval"
        elif wcc.wcc_status == 1:
             approve_status="Approved"
        elif wcc.wcc_status == 2 :
             approve_status="Returned"
        else :
             approve_status="Rejected"
        wcc_approve_date=confulldate( wcc.wcc_status_date,request.company.id)
        if wcc_approve_date == None :
            wcc_approve_date="---"
        else :
            wcc_approve_date=wcc_approve_date
  

        wcc_data_count=check_wcc_invoice(wcc.id)
        if wcc_data_count == 0:
             wcc_invoice_status="Not Mapped to Invoice"
        else :
            wcc_invoice_status="Mapped to Invoice"

        if wcc.status == 1:
            wcc_status="Submitted"
        else :
            wcc_status="Draft"


        all_Wcc_invoice.append({
            's_no':s_no,
            'id':wcc.id,
            'wcc_num':wcc_inv_num,
            'period_Service':period_date,
            'submit_date': wcc_submit_date,
            'approval_status':approve_status,
            'approval_date':wcc_approve_date,
            'invoice_status':wcc_invoice_status,
            'status':wcc_status,
            'vendorid':vendorid.id,
            'vendorid_active_status':vendorid.active_status,
            'vendor_status':vendor_status,
            'wcc_status':wcc.status,
            'wcc_wcc_status':wcc.wcc_status,
            'wcc_data_count':wcc_data_count,
            'return_query_stataus':return_query,
        })
        s_no+=1                       
        
    response = {
        'draw': draw,
        'recordsTotal': wcc_value.count(),
        'recordsFiltered': wcc_value.count(),
        'data': all_Wcc_invoice
    }
    return JsonResponse(response)



import pytz
def wcc_return_flow(wcc_id,module_id,submit_type,comments,request):
    print(f'module_id ,{module_id}')
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    current_date=datetime.now()
    wcc_data=WorkCompletionCost.objects.get_by_id(wcc_id)
    wcc_work=WorkCompletionValue.objects.filter_by_wcc(wcc_id)
    vendor=ContractMasterVendor.objects.get_byid(wcc_data.vendor_id,request.company)
    allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
    if wcc_work.exists():
        wcc_work = wcc_work.first()  
   
    WccApproval.objects.update_user_data(request.user.id,wcc_id,3,comments,current_date)
    WorkCompletionCost.objects.approve_wcc(wcc_id,2,current_date)
    returnCheck=WccReturnTrack.objects.filter(wcc_id=wcc_id).count()
    
    wcc_exceptional_instance = WccExceptional.objects.filter(wcc_id=wcc_id, status=1).exclude(exceptional_type=5).last()
    if wcc_exceptional_instance:
        checked_messages = wcc_exceptional_instance.checked_messages
    else:
        checked_messages = None
    # wcc_status_mail(request,wcc_data,wcc_work,vendor,'returned',comments)
    return_reason_messages=split_by_newline(checked_messages)
    url=f"wcc/wccqueryhistory/{wcc_id}"
    verb='WCC for Returned'
    description=f'WCC Returned by {request.company.first_name} on {date_today} for {wcc_data.name_service}'
    for notifications in allVendors:
       notify_wcc(request,notifications,url,verb,description,"vendor")
       wccreturnrejectmail(request,notifications,wcc_data,wcc_work,request.user.id,date_today,'Returned',return_reason_messages)
    
    if returnCheck== 0:
        WccReturnTrack.objects.create(user_id=request.user.id,wcc_id=wcc_id,stage=1,created_at=current_date,module_id=module_id)
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        vendor=ContractMasterVendor.objects.get_byid(wcc_data.vendor_id,request.company)
        WccQuery.objects.reason_for_wcc(wcc_id,comments,request.user,time_stamp,vendor.id,module_id,1)
    else:
        main_url="wcc/wcclist"
        get_prev_user=WccQuery.objects.filter(wcc_id=wcc_id).last()
        
        try:
            returned_counting=get_prev_user.returned_count+1
        except:
            returned_counting=0
        # notify_invoice_flow(request,get_prev_user.user,main_url,main_verb,content)
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        vendor=ContractMasterVendor.objects.get_byid(wcc_data.vendor_id,request.company)
        WccQuery.objects.reason_for_wcc(wcc_id,comments,request.user,time_stamp,vendor.id,module_id,returned_counting)
        BackTowccQuery.objects.reason_for_wcc(wcc_id,comments,request.user,time_stamp,vendor.id,module_id)
    return


def CloseWccQuery(request,pk):
    query=WorkCompletionCost.objects.get_by_id(pk)
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
    
    wcc_number=list(WorkCompletionValue.objects.filter(wcc=pk,status=1).values_list('wcc_number',flat=True))
    all_wcc=', '.join(str(e) for e in wcc_number)
    accepted_member=f'Credit Note No.{all_wcc} query has been accepted by {request.user.name} {request.user.lastname}'
    utc_timezone = pytz.utc
    utc_time = datetime.now(utc_timezone)
    time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    wcc_id=''
    get_wcc=WorkCompletionCost.objects.filter(id=pk,status=1).first()
    if get_wcc:
        wcc_id=get_wcc.name_service
    file=request.FILES.get('file')  
    get_dispute=WccQuery.objects.create_wccdisputed_query(pk,accepted_member,request.user,time_stamp,vendor.id,file)
    get_invoice=WorkCompletionCost.objects.filter(id=pk).update(dispute_status=1)
    WccReturnTrack.objects.create(stage=2,wcc_id=pk,status=True,user=request.user,created_at=datetime.now())
    
    
    if request.user.roles.id == 3 or request.user.roles.id == 2:
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        main_url=f"wcc/wccqueryhistory/{pk}"
        main_verb=f'Wcc NO.{all_wcc} Accepted for Approval Flow '
        content=f'Wcc NO.{all_wcc} Accepted for Approval by {request.user.name} on {date_today} for {wcc_id} '
        now = datetime.now()
        for notifications in allVendors:
            notify_wcc(request,notifications,main_url,main_verb,content,"vendor")
    else:
        main_url=f"wcc/wccqueryhistory/{pk}"
        main_verb=f'Wcc NO.{all_wcc} Accepted by {request.user.name} {request.user.lastname} '
        content=f'Wcc NO.{all_wcc} Accepted for Approval by {request.user.name} on {date_today} for {wcc_id} '
        get_user=WccQuery.objects.filter(wcc_id=pk).first()
        # notify_invoice_flow(request,get_user.user,main_url,main_verb,content)
    return redirect('wcc:wccqueryhistory', pk=pk)

class WccQueryHistory(View):
    def get(self,request,pk):
        # query=Invoice.objects.get_by_id(pk)
        wcc_data=WorkCompletionCost.objects.get_by_id(pk)
        ref_num=ContractMaster.objects.filter(id=wcc_data.contractid).first()  
        vendor=ContractMasterVendor.objects.get_byid(wcc_data.vendor_id,request.company)
        check_wccExceptional=WccExceptional.objects.filter(wcc_id=pk,status=1).exclude(exceptional_type=5).count()

        wcc_exceptional_instance = WccExceptional.objects.filter(wcc_id=pk, status=1).exclude(exceptional_type=5).last()
        if wcc_exceptional_instance:
            checked_messages = wcc_exceptional_instance.checked_messages
        else:
            checked_messages = None  
        # checked_messages = WccExceptional.objects.filter(wcc_id=pk, status=1).exclude(exceptional_type=5).values_list('checked_messages', flat=True)
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=13,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights).count()
        # print(f'wcc_files {wcc_files}')
        wcc_files=other_documents()
        get_status=WccReturnTrack.objects.filter(wcc_id=pk,stage=4).first()
        querylist=WccQuery.objects.filter(wcc_id=pk)
        closed_query_count=list(querylist.filter(query_status=1).order_by('returned_count').values_list('returned_count',flat=True).distinct())

        data={'querylists':querylist,'query':wcc_data,'pk':pk,'contact_person':vendor,'ref_num':ref_num,'get_status':get_status,'get_dispute_users':get_dispute_users,'check_wccExceptional':check_wccExceptional,'checked_messages':checked_messages,'wcc_files':wcc_files, 'closed_query_count':closed_query_count}
        return render(request,'wccquerylist.html',data)



    def post(self,request,pk):
        print(f' reqe {request.POST}')
        today = date.today()
        current_date=datetime.now()
        date_today = today.strftime("%d-%b-%Y")
        query=WorkCompletionCost.objects.get_by_id(pk)
        wcc_id_number=None
        get_wcc=WorkCompletionCost.objects.filter(id=pk,status=1).first()
        if get_wcc:
            wcc_id_number=get_wcc.name_service
        wcc_number=list(WorkCompletionValue.objects.filter(wcc=pk,status=1).values_list('wcc_number',flat=True))
        all_wcc=', '.join(str(e) for e in wcc_number)
        print(f'query {query}')
        get_submit=request.POST.get('submit_type')
        print(f'get_submit {get_submit}')
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=13,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights)
        
        if(get_submit):
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            get_user=request.user
            print(f'submit_type {submit_type}, submit_name {submit_name}, comments {comments}')
            wcc_detail = WorkCompletionCost.objects.get_by_id(pk)
            vendor=ContractMasterVendor.objects.get_byid(wcc_detail.vendor_id,request.company)
            
            if submit_type == '8':
                file=request.POST.get('file')
                get_exceptional=request.POST.getlist('exceptional')
                exceptional_list=[WccExceptional(wcc_id=pk,exceptional_type=i,confirm_dispute=1) for i in get_exceptional]
                WccExceptional.objects.bulk_create(exceptional_list)
                WorkCompletionCost.objects.filter(id=pk).update(dispute_status=2)
                WccReturnTrack.objects.create(wcc_id=pk,stage=3,status=True,user=request.user,created_at=datetime.now(),reason=comments)
                main_url="wcc/approvalwcclist"
                subject=f"Recommendation for Wcc Dispute"
                reason=f'Wcc {all_wcc} has been recommended for Dispute for {vendor.vendor_name} on {date_today} for {wcc_id_number}'
                # for user in get_dispute_users:
                #     url='https://irockinfo.mo.vc/'
                #     moved_as_dispute_mail(request,user,all_wcc,url,wcc_detail,vendor,comments)
                #     notify_invoice_flow(request,user,main_url,subject,reason)
                WccQuery.objects.create_wccdisputed_query(pk,reason,request.user,time_stamp,vendor.id,file)
                return redirect("wcc:approvalwcclist")
            
            else:
                get_module=WccQuery.objects.filter(wcc_id=pk).first()
                check_possiblity=BackTowccQuery.objects.filter(wcc_id=pk).count()
                if(check_possiblity>0):
                    get_module=BackTowccQuery.objects.filter(wcc_id=pk).first()
                WccReturnTrack.objects.create(wcc_id=pk,stage=5,status=True,user=request.user,created_at=datetime.now(),reason=comments)
                WorkCompletionCost.objects.approve_wcc(pk,1,current_date)
                WccQuery.objects.filter(wcc_id=pk).update(query_status=1)
                get_data=WccApproval.objects.filter(wcc_id=pk,user_id=request.user.id).last()
                get_data.approval_status=1
                get_data.save()
                print(f'pk {pk},comments {comments},submit_type {submit_type},submit_name {submit_name}')
                if request.user.roles_id == 2 or request.user.roles_id ==3:
                    return redirect("wcc:wccapprovalview", pk)
                else:
                    return redirect("wcc:wccapprovalview" ,pk)

        else:
            deniedreason=request.POST.get('message')
            files_upload=request.POST.get('files_upload')
            document_type=request.POST.get('document_type')
            document_name=request.POST.get('document_name')
            vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
            allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            check_wccExceptional=WccExceptional.objects.filter(wcc_id=pk,exceptional_type=1,status=1).count()
            main_url=f"wcc/wccqueryhistory/{pk}"
            verb=f"Response to Wcc Returned Clarification."
            reason=f'Wcc {all_wcc} has been received response for returned Wcc from {request.user.name} on {date_today} for {wcc_id_number}'
            if request.user.roles_id == 4:
                url='https://irockinfo.mo.vc/' 
                team=f'The Invoice Approval Process System'
                # if query.invoice_status == 6:
                #     for users in get_dispute_users:
                #         notify_invoice_flow(request,users,main_url,verb,reason)
                #         response_to_vendor_mail(request,users,all_wcc,url,query,team)
                # else:
                #     returned_user=AddNewDisputedQuery.objects.filter(query_id=pk).first()
                #     if returned_user.user:
                #         notify_invoice_flow(request,returned_user.user,main_url,verb,reason)
                #         response_to_vendor_mail(request,returned_user.user,all_wcc,url,query,team)
            else:
                url='https://irockinfo.mo.vc/vendorlogin' 
                team=f'The Finance Team'
                # for vendor_data in allVendors:
                #     notify_invoice_flow(request,vendor_data,main_url,verb,reason)
                #     response_to_vendor_mail(request,vendor_data,all_wcc,url,query,team)

            print(f'check_wccExceptional---- {check_wccExceptional}')
            if check_wccExceptional > 0 and request.user.roles_id == 4:
                files=request.FILES.getlist('file')
                print(f'files {files}')
                if len(files) > 0:
                    get_dispute=WccQuery.objects.create_wccdisputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None)
                    for file in files:
                        WccFileUpload.objects.create_wcc_supportfile(vendor,pk,document_type,file,request.company)   
                        WccQueryFiles.objects.create(disputedquery=get_dispute,file=file,document_name=document_name,document_type=document_type)
                else:
                    get_dispute=WccQuery.objects.create_wccdisputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None)
            else:
                file=request.FILES.get('file')
                if (file != None): 
                    fs = FileSystemStorage()
                    file = fs.save(file.name, file)
                get_dispute=WccQuery.objects.create_wccdisputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,file)
            scheme=request.scheme
            gethost=request.get_host()
            if request.user.roles_id == 4:
                sender = User.objects.get_by_id(request.user.id)
                url=f"{scheme}://{gethost}/wcc/wccqueryhistory/{pk}"
                description=f'Reply received from {vendor.vendor_name}'
                # getCompanyUserlist(request,sender,url,'Reply Received for Disputed Invoice',description)
            else:
                print('To Vendor')
                sender = User.objects.filter(id=request.user.id).first()
                recipients = User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
                print('recipients',recipients)
                url=f"{scheme}://{gethost}/wcc/wccqueryhistory/{query.id}"
                notify.send(sender, recipient=recipients,data=url, verb='Reply Received for Disputed Wcc', description=f'Reply received from {sender.name} {sender.lastname if sender.lastname != None else ""}')
            return redirect('wcc:wccqueryhistory',pk=pk) 
        
