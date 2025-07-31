from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from InvoiceGuard.models import *
from custom_auth.models import *
from credit_note.models import *
from projects.models import *
import re
from custom_auth.views import *
from projects.views import *
from django.core.files.storage import FileSystemStorage
from invoice.models import *
from finance.models import CompanyBank
from credit_note.views import get_vendor_company_name
# from datetime import date 
import pathlib
from django.template.loader import get_template
from .utils.utils import *
from easy_pdf.views import PDFTemplateView
from invoice.helpers import *
# import weasyprint
from weasyprint import HTML, CSS
from io import BytesIO
from django.template import RequestContext, Template
import base64
# from django.conf import settings
from django.core.files import File
from PIL import Image
from django.template.loader import render_to_string
from num2words import num2words
from decimal import Decimal
from wcc.models import *
from wcc.views import add_time
from wcc.helpers import change_key_name
from django.db.models import Q
from projectflow.models import ProjectFlowlevel,ProjectFlowModules,ProjectFlowModuleUsers
from InvoiceGuard.models import ProcessModule
from projects.helpers import create_user_log

from django.db.models import Sum,QuerySet
from custom_auth.views import markas_read_status
from datetime import datetime,date,timedelta,timezone
from finance.models import *
from django.db.models import F
import random
from datetime import datetime

from django.utils import timezone
from django.utils import timezone
from django.core import serializers
from .templatetags.invoice_custom_tags import getpaidamount,gettotalgrossamountint,getprojectname_only,statusvalue,getinvoicecount,rankinglisttotalamount,getdaysforunpaid,getdaysforpayment,invoicegrossamount,invoicetaxamount,replacecommaid,addvalues,getprojectname,amount_convertion,confulldate,get_payment_detail,get_payment_percentage,checkpermission_bankuser,checkpermission_invoiceapproval_dispute,check_query_history,check_for_balance_invoice,checkpermission_invoiceoverride,checkpermission_invoicerecipt,checkreturned_documents,get_credit_notes,check_get_invoicecost,check_invoice_receiptfile_upload,check_bank_users,check_bank_user_currencies,get_dispute_committee_member,resolution_team_approval,checkpermission_invoicerecipt_upload,checkdynamic_flow,get_returned_invoice_count,partial_payment_percentage,check_payment_spit_module,get_project_id , check_invoice_receiptfile_upload_by_payment_id ,get_new_payment_percentage,find_fully_paid,get_confirm_payment_percentage ,find_signatories_user,fetbankaccountnumber,withoutbankuserapproval,new_round_of_two_values,round_of_two_values,remove_symbol
import calendar
from custom_auth.helpers import check_user_sign 
from credit_note.helpers import credit_applied_mail
from operator import attrgetter
from projects.templatetags.custom_tags import checkcreate,checkforbankuser
from custom_auth.models import Settings

# Local application/library-specific imports
from cost_code.helpers import getcostcode_component_path,getcostcode_format_type
from cost_code.models import CostCodeMaster
from django.db.models import Sum
from custom_auth.helpers import getcompany_iamge
from cost_code.templatetags.cost_code_tags import getcostcode_string,getcostcode_preview,getcostcode_category



def getCompanyUserlist(request,sender,url,verb,description):
    clinet_admin_id=User.objects.filter(company_id=request.company.id).first()
    company_users=User.objects.filter(company_id=request.company.id,roles_id=3,status=1).values_list('id',flat=True)
    check_rights_list=list(UserRights.objects.filter(user_id__in=company_users,module_id=4).filter(Q(create=1) | Q(view=1) | Q(edit=1) | Q(delete=1)).values_list('user_id',flat=True))
    # check_rights_list.append(clinet_admin_id.id)
    for user_id in check_rights_list:
        recipient=User.objects.get(id=user_id) 
        send_url=url
        notify.send(sender, recipient=recipient,data=send_url, verb=verb, description=description)
    return True

# Create your views here.
def createinvoice(request):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    wcc_id=request.GET.get('wcc_id',None)
    company=Settings.objects.getcompany_settings(request.user.company.id)
    vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    bankcount=BankDetails.objects.getbankdetails_byvendor_company(request.company,vendorid.id)
    contractlist=ContractMaster.objects.getcontractmaster(vendorid.id).exclude(wcc=0) if wcc_id else ContractMaster.objects.getcontractmaster(vendorid.id).exclude(wcc=1)
    cost_code_list = CostCodeVendor.objects.get_vendor_data(vendorid.id,1)
    getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
    if(getlastlevel != None):
        lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
    else:
        lastlevel=None
    # print('contractlist',wcc_id)
    allcontractlist=[]
    if (wcc_id):
        for contract in contractlist:
            if contract.wcc == 1:
                allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original','check_status':contract.projects.active_status})
            # get_amendmentlist=Amendment.objects.getamendment(contract.id).exclude(wcc=0)
            get_amendmentlist=Amendment.objects.filter( service_id=contract.id,status=1,save_type=2).exclude(wcc=0)
            for amendment in get_amendmentlist:
                if amendment.amendment_type == 'Amendment':
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment','check_status':amendment.service.projects.active_status})
                else:
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum','check_status':amendment.service.projects.active_status})
    else:
        for contract in contractlist:
            allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original','check_status':contract.projects.active_status})
            # get_amendmentlist=Amendment.objects.getamendment(contract.id).exclude(wcc=1)
            get_amendmentlist=Amendment.objects.filter( service_id=contract.id,status=1,save_type=2).exclude(wcc=1)
            for amendment in get_amendmentlist:
                if amendment.amendment_type == 'Amendment':
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment','check_status':amendment.service.projects.active_status})
                else:
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum','check_status':amendment.service.projects.active_status})
    if (request.POST):
        invoicetype=request.POST.get('invoicetype')
        fromdate=request.POST.get('fromdate',None)
        todate=request.POST.get('todate',None)
        contract=request.POST.get('contractid')
        project_hdn=request.POST.get('project_hdn')
        if (contract == ''):
            contractid=''
            contract_type=''
        else:
            split_contract=contract.split("-")
            contractid=split_contract[0]
            contract_type=split_contract[1]
        
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
        costcode=request.POST.get('costcode')
        # receipt_datetime_object = datetime.strptime(receiptdate,request.POST.get('companydateformat'))invoice_submit_date=receipt_datetime_object,
        if (fromdate != '' and fromdate != None):
            from_datetime_object = datetime.strptime(fromdate,'%d-%b-%Y')
        else:
            from_datetime_object=None
        if (todate != '' and todate != None):
            todate_datetime_object = datetime.strptime(todate,'%d-%b-%Y')
        else:
            todate_datetime_object=None

        if (project_hdn == '' or project_hdn == None):
            project_hdn =get_project_id(contractid ,contract_type)

        vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        create_invoice=Invoice.objects.createinvoice(invoicetype,from_datetime_object,todate_datetime_object,
        contractid,contract_type,contractnameservice,contractservicetype,service_rendered,location_service,
        project,block,field,well,request.company,vendorid.id,block_not,field_not,well_not,costcode,project_hdn,wcc_id)
       
        request.session['contractid']=request.POST.get('contractid')
        submit_type=request.POST.get('submit_type')
        if (submit_type == "0"):
            return redirect('invoice:invoicelist')
        else:
            if (wcc_id):
                # redirect_url = '/invoice/createinvoicesteptwo/{}?wcc_id={}'.format(create_invoice.id,wcc_id)
                redirect_url = '/invoice/editinvoicesteptwo/{}/{}?wcc_id={}'.format(create_invoice.id,1,wcc_id)
                return redirect(redirect_url)
            else:
                # return redirect('invoice:createinvoicesteptwo',pk=create_invoice.id)
                return redirect('invoice:editinvoicesteptwo',pk=create_invoice.id,status=1)
        
    data={'company':company,'allcontractlist':allcontractlist,'bankcount':bankcount,'vendor':vendorid,'company':request.company,'lastlevel':lastlevel,'cost_code_list':cost_code_list,'wcc_id':wcc_id}
    if (wcc_id):
        wcc_data=WorkCompletionCost.objects.get_by_id(wcc_id)
        if (wcc_data.contracttype == 'original'):
            getprojectid=ContractMaster.objects.getcontract(wcc_data.contractid)
            projectid=getprojectid.projects.id
        else:
            getprojectid=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
            projectid=getprojectid.service.projects.id
        wcc_obj={'wcc_data':wcc_data,'getprojectid':projectid}
        data.update(wcc_obj)
    return render(request,'createinvoice.html',data)
    

def contractdetails(request):
    contractid=request.GET.get('contractid',None)
    vendor_id=request.GET.get('vendor_id',None)
    type=request.GET.get('type',None)
    formname=request.GET.get('formname',None)
    invoicediscilpline= False
    invoicecluster = False
    Flowdisciplinecluster = False
    invoicewell = False
    vendor_query=False
    data={}
   
    if (type == 'original'):
        contract=ContractMaster.objects.filter(id=contractid,status=1).first()
        # print('contract----',contract)
        querylist=CheckVendorContract.objects.filter(contract_id=contract.id , status=1).count()
        draft_count=VendorCompanyTaxDetails.objects.filter(contract_id=contract.id,status=1,draft_status=1).count() + VendorInvoiceSplit.objects.filter(contract_id=contract.id,status=1,draft_status=1).count() + VendorPaymentTerms.objects.filter(contract_id=contract.id,status=1,draft_status=1).count()
        invoices=VendorInvoiceSplit.objects.filter(contract_id=contract.id,status=1).count()
        invoiceflowlevel = Projectcreation.objects.filter(id=contract.projects_id,company_id=request.company).first()
        if (contract.types_service == 'service_supply'):
            convert_data=(contract.types_service).replace("_"," & ")
        else:
            convert_data=(contract.types_service).replace("_"," ")
        change_title=convert_data.title()
        # print('draft_count---',draft_count)
        if formname == 'Wcc':
            wccdiscilpline=WccFlowLevel.objects.filter(discipline_id=contract.projectdisciplinetype_id,status=1,company=request.company).exists()
            wcccluster=WccFlowLevel.objects.filter(cluster_id=contract.projectdiscipline.cluster_id,status=1,company=request.company).exists()
            wccwell=WccFlowLevel.objects.filter(project_id=invoiceflowlevel.id,status=1,company=request.company).exists()
            if wccdiscilpline == True or wcccluster == True or wccwell == True:
                 Flowdisciplinecluster = True    
        elif formname == 'Invoice':
            if invoiceflowlevel.flow_level == 'discipline':
                invoicediscilpline = ProjectFlowlevel.objects.filter(level_id=contract.projectdisciplinetype_id,status=1,company=request.company).exists()
            elif  invoiceflowlevel.flow_level == 'clusters':   
                invoicecluster = ProjectFlowlevel.objects.filter(level_id=contract.projectdiscipline.cluster_id,status=1,company=request.company).exists()
            elif invoiceflowlevel.flow_level =='well':
                invoicewell = ProjectFlowlevel.objects.filter(project_id=invoiceflowlevel.id,status=1,company=request.company).exists()
            if invoicediscilpline == True or invoicecluster == True or invoicewell == True:
                Flowdisciplinecluster = True
        data={'contractname':contract.name_service,'contractservice':change_title,'contractid':contract.id,'invoices_count':invoices,'draft_count':draft_count,'contract_date':contract.executed_date,'Flowdisciplinecluster':Flowdisciplinecluster , 'vendor_query':querylist}
    
    else:
        amendmentdata=Amendment.objects.filter(id=contractid,status=1).first()
        querylist=CheckVendorContract.objects.filter(amendment_id=amendmentdata.id , status=1).count()
        draft_count=VendorCompanyTaxDetails.objects.filter(amendment_id=amendmentdata.id,status=1,draft_status=1).count() + VendorInvoiceSplit.objects.filter(amendment_id=amendmentdata.id,status=1,draft_status=1).count() + VendorPaymentTerms.objects.filter(amendment_id=amendmentdata.id,status=1,draft_status=1).count()
        invoices=VendorInvoiceSplit.objects.filter(amendment_id=amendmentdata.id,status=1).count()
        contract=ContractMaster.objects.filter(status=1,id=amendmentdata.service_id).first()
        invoiceflowlevel = Projectcreation.objects.filter(id=contract.projects_id,company_id=request.company).first()
        if (contract.types_service == 'service_supply'):
            convert_data=(contract.types_service).replace("_"," & ")
        else:
            convert_data=(contract.types_service).replace("_"," ")
        change_title=convert_data.title()
        if formname == 'Wcc':
            wccdiscilpline=WccFlowLevel.objects.filter(discipline_id=contract.projectdisciplinetype_id,status=1,company=request.company).exists()
            wcccluster=WccFlowLevel.objects.filter(cluster_id=contract.projectdiscipline.cluster_id,status=1,company=request.company).exists()
            wccwell=WccFlowLevel.objects.filter(project_id=invoiceflowlevel.id,status=1,company=request.company).exists()
            if wccdiscilpline == True or wcccluster == True or wccwell == True:
                Flowdisciplinecluster = True    
        elif formname == 'Invoice':
            if invoiceflowlevel.flow_level == 'discipline':
                invoicediscilpline = ProjectFlowlevel.objects.filter(level_id=contract.projectdisciplinetype_id,status=1,company=request.company).exists()
            elif  invoiceflowlevel.flow_level == 'clusters':   
                invoicecluster = ProjectFlowlevel.objects.filter(level_id=contract.projectdiscipline.cluster_id,status=1,company=request.company).exists()
            elif invoiceflowlevel.flow_level =='well':
                invoicewell = ProjectFlowlevel.objects.filter(project_id=invoiceflowlevel.id,status=1,company=request.company).exists()
            if invoicediscilpline == True or invoicecluster == True or invoicewell == True:
                Flowdisciplinecluster = True
        data={'contractname':contract.name_service,'contractservice':change_title,'contractid':amendmentdata.id,'invoices_count':invoices,'draft_count':draft_count,'contract_date':contract.executed_date,'Flowdisciplinecluster':Flowdisciplinecluster,'vendor_query':querylist}
   
    return JsonResponse({'data':data})

def getproject(request):
    contractid=request.GET.get('contractid')
    type=request.GET.get('type')
    data={}
    if (type  == 'original'):
        if (contractid != ''):
            contractmasterdata=ContractMaster.objects.filter(id=contractid).first()
            data={'id':contractmasterdata.projects.id,'projectname':contractmasterdata.projects.projectname.name}
    else:
        if (contractid != ''):
            amendmentdata=Amendment.objects.filter(id=contractid,status=1).first()
            data={'id':amendmentdata.service.projects.id,'projectname':amendmentdata.service.projects.projectname.name}
    return JsonResponse({'data':data})


def getcostcodeval(request):
    contract_id=request.GET.get('contract_id')
    vendor_id=request.GET.get('vendor_id')
    contracttype=request.GET.get('contracttype')
    if (contracttype == "original"):
        contractmaster=ContractMaster.objects.filter(id=contract_id).first()
        con_id=contractmaster.id
    else:
        ammendment=Amendment.objects.filter(id=contract_id).first()
        con_id=ammendment.service.id
    vendors_list=CostCodeVendor.objects.filter(vendor_id=vendor_id,status=1 ,contractid=con_id)
    all_costcode_data=[]
    for costcode in vendors_list :
        costcode_preview=getcostcode_preview(costcode.costcode_main ,costcode.order ,request.company.id)
        costcode_string=getcostcode_string(costcode.costcode_main ,costcode.order, request.company.id)
        costcode_category=getcostcode_category(costcode.costcode_main ,costcode.order, request.company.id)
        cost_value=f'{costcode_string}/{costcode_category.cost_type.component_name}'
        datas={ "id": costcode.id, "costcode_preview": costcode_preview, "costcode_string":cost_value }
        all_costcode_data.append(datas)
    
    json_data={'data':all_costcode_data}
    return JsonResponse(json_data)

def getprojectblock(request):
    projectid=request.GET.get('projectid')
    datalist=[]
    if (projectid != ''):
        allblocks=ProjectBlock.objects.filter(project_id=projectid,status=1)
        for blocks in allblocks:
            if (blocks.block.block_name != 'Not Applicable'):
                datalist.append({'id':blocks.id,'blockname':blocks.block.block_name})
    else:
        data={'data':'data'}
    return JsonResponse({'data':datalist})

def getallwell(request):
    projectid=request.GET.get('projectid')
    fieldid=request.GET.get('fieldid')
    blockid=request.GET.get('blockid')
    if (fieldid == "Not Applicable" or fieldid == "" and blockid == "Not Applicable"):
        fields=ProjectField.objects.filter(project_id=projectid,status=1).values_list('id',flat=True)
        getallfieldenvironment=ProjectEnvironment.objects.filter(project_id=projectid,field__id__in=fields,status=1).values_list('id',flat=True)
        getallcluster=ProjectCluster.objects.filter(project_id=projectid,environment__id__in=getallfieldenvironment,status=1).values_list('id',flat=True)
        getalldevelopmentype=ProjectDevelopmentType.objects.filter(project_id=projectid,cluster__id__in=getallcluster,status=1).values_list('id',flat=True)
        getalldiscipline=ProjectDevelopmentDiscipline.objects.filter(project_id=projectid,development_type__id__in=getalldevelopmentype,status=1).values_list('id',flat=True)
        getalldisciplinetype=ProjectDevelopmentSubType.objects.filter(project_id=projectid,project_discipline__id__in=getalldiscipline,status=1).values_list('id',flat=True)
        getallwelltype=ProjectWellType.objects.filter(project_id=projectid,discipline_type__id__in=getalldisciplinetype,status=1).values_list('id',flat=True)
        getallwellname=ProjectWellName.objects.filter(project_id=projectid,welltype__id__in=getallwelltype,status=1)
        welllist=[]
        for well in getallwellname:
            welllist.append({'id':well.id,'wellname':well.wellname.well_subname})
        return JsonResponse({'data':welllist})
    elif (fieldid == "Not Applicable" or fieldid == "" and blockid !="Not Applicable" and blockid != ""):
        fields=ProjectField.objects.filter(project_id=projectid,block_id=blockid,status=1).values_list('id',flat=True)
        getallfieldenvironment=ProjectEnvironment.objects.filter(project_id=projectid,field__id__in=fields,status=1).values_list('id',flat=True)
        getallcluster=ProjectCluster.objects.filter(project_id=projectid,environment__id__in=getallfieldenvironment,status=1).values_list('id',flat=True)
        getalldevelopmentype=ProjectDevelopmentType.objects.filter(project_id=projectid,cluster__id__in=getallcluster,status=1).values_list('id',flat=True)
        getalldiscipline=ProjectDevelopmentDiscipline.objects.filter(project_id=projectid,development_type__id__in=getalldevelopmentype,status=1).values_list('id',flat=True)
        getalldisciplinetype=ProjectDevelopmentSubType.objects.filter(project_id=projectid,project_discipline__id__in=getalldiscipline,status=1).values_list('id',flat=True)
        getallwelltype=ProjectWellType.objects.filter(project_id=projectid,discipline_type__id__in=getalldisciplinetype,status=1).values_list('id',flat=True)
        getallwellname=ProjectWellName.objects.filter(project_id=projectid,welltype__id__in=getallwelltype,status=1)
        welllist=[]
        for well in getallwellname:
            welllist.append({'id':well.id,'wellname':well.wellname.well_subname})
        return JsonResponse({'data':welllist})
    else:
        getallfieldenvironment=ProjectEnvironment.objects.filter(project_id=projectid,field_id=fieldid,status=1).values_list('id',flat=True)
        getallcluster=ProjectCluster.objects.filter(project_id=projectid,environment__id__in=getallfieldenvironment,status=1).values_list('id',flat=True)
        getalldevelopmentype=ProjectDevelopmentType.objects.filter(project_id=projectid,cluster__id__in=getallcluster,status=1).values_list('id',flat=True)
        getalldiscipline=ProjectDevelopmentDiscipline.objects.filter(project_id=projectid,development_type__id__in=getalldevelopmentype,status=1).values_list('id',flat=True)
        getalldisciplinetype=ProjectDevelopmentSubType.objects.filter(project_id=projectid,project_discipline__id__in=getalldiscipline,status=1).values_list('id',flat=True)
        getallwelltype=ProjectWellType.objects.filter(project_id=projectid,discipline_type__id__in=getalldisciplinetype,status=1).values_list('id',flat=True)
        getallwellname=ProjectWellName.objects.filter(project_id=projectid,welltype__id__in=getallwelltype,status=1)
        welllist=[]
        for well in getallwellname:
            welllist.append({'id':well.id,'wellname':well.wellname.well_subname})
        return JsonResponse({'data':welllist})

def createinvoicesteptwo(request,pk):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    company=Settings.objects.getcompany_settings(request.company.id)
    getcurrencylist=ast.literal_eval(company.currency)
    companycurrency=Basecountries.objects.filter(id__in=getcurrencylist)
    contractid=Invoice.objects.get_by_id(pk)
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.getvendor_byvin(getvin,request.company)
    wcc_id=request.GET.get('wcc_id',None)
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.getcontract(contractid.contractid)
        invoice_totalvalue = []
        contract_amount = contract.amount if contract.amount == 'No Max Limit' else contract.amount.replace(',','')
        contract_reference = contract.reference_number
        currency_symbol=contract.currency.currency_symbol
        vendortax=VendorCompanyTaxDetails.objects.getvendortaxdetails_by_contract(getvendordetails.id,contract.id,request.company)
        vendorinvoice=VendorInvoiceSplit.objects.getvendor_split_invoice(getvendordetails.id,contract.id,request.company)
        # print('vendorinvoice1',vendorinvoice)
        vendorpayment=VendorPaymentTerms.objects.getvendor_paymentterms(getvendordetails.id,contract.id,request.company)
        if (vendorinvoice.count() > 0):
            get_vendor_invoice=list(vendorinvoice.values('no_invoice').distinct())
            no_vendor_invoice=get_vendor_invoice[0]['no_invoice']
        else:
            no_vendor_invoice='1'
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        invoice_totalvalue = []
        contract_amount = contract.amendment_amount if contract.amendment_amount == 'No Max Limit' else contract.amendment_amount.replace(',','')
        contract_reference = contract.amendment_reference_number
        currency_symbol=contract.amendment_currency.currency_symbol
        vendortax=VendorCompanyTaxDetails.objects.getvendortaxdetails_by_amendment(getvendordetails.id,contract.id,request.company)
        vendorinvoice=VendorInvoiceSplit.objects.getvendor_split_invoiceamendment(getvendordetails.id,contract.id,request.company)
        # print('vendorinvoice2',vendorinvoice)
        vendorpayment=VendorPaymentTerms.objects.getvendor_paymenttermsamendment(getvendordetails.id,contract.id,request.company)
        vendorpaymentlist=vendorpayment.values_list()
        if (vendorinvoice.count() >0):
            get_vendor_invoice=list(vendorinvoice.values('no_invoice').distinct())
            no_vendor_invoice=get_vendor_invoice[0]['no_invoice']
        else:
            no_vendor_invoice='1' 
    inclusivetaxlist=vendortax.filter(Tax_Type="Inclusive").values_list('id',flat=True)
    getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=inclusivetaxlist,status=1)
    exclusivetaxlist=vendortax.filter(Tax_Type="Exclusive").values_list('id',flat=True)
    getexclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=exclusivetaxlist,status=1)
    bankdetails=BankDetails.objects.getbankdetails_byvendor_company(request.company,getvendordetails.id)
    todaydate = datetime.now().date() 
    if (request.POST):
        postvalues=request.POST
        tax_types=postvalues.get('tax_type')
        # print(f'tax_types {tax_types}')
        Invoice.objects.filter(id=pk).update(tax_type=tax_types)
        hdninvcost=postvalues.get('hdninvcost')
        total_invoice=postvalues.get('totalvalue')
        pattern = r'[^A-Za-z0-9.,]+'
        matches = re.sub(pattern, '', total_invoice)
        if (len(matches) > 0):
            get_total_value = matches
        else:
            get_total_value = ''
        grossamountwithdis=postvalues.get('grossamountwithdis')
        grossamountafterother=postvalues.get('grossamountwithother')
        totalexclusivetax=postvalues.get('totalexclusivetax')
        totalalltax=postvalues.get('totalalltax')
        paymentterm=postvalues.get('paymentterm')
        create_cost_information=InvoiceCostInformation.objects.create_invoicecostinformation(pk,get_total_value,grossamountwithdis,totalexclusivetax,totalalltax,paymentterm,getvendordetails.id,contractid.contractid,grossamountafterother)

        discountname=postvalues.getlist('discountname')
        discounttype=postvalues.getlist('discounttype')
        discountamount=postvalues.getlist('discountamount')
        discount_value=postvalues.getlist('discount_value')
        for name,type,amount,value in zip(discountname,discounttype,discountamount,discount_value):
            create_discount=InvoiceDiscount.objects.create(invoice_id=pk,discount_name=name,discount_type=type,discount_value=amount,discount_calculated_value=value,vendor_id=getvendordetails.id,contractid=contractid.contractid)

        hdninvother=postvalues.getlist('hdninvother')
        others_name=postvalues.getlist('others_name')
        others_amount=postvalues.getlist('others_amount')
        for hdndis,name,amount in zip(hdninvother,others_name,others_amount):
            if name:
                create_otherdata=InvoiceOthersAmount.objects.create(invoice_id=pk,description=name,amount=amount,vendor_id=getvendordetails.id)

        exclusive_list=postvalues.getlist('exclusive')
        exclusive_value=postvalues.getlist('exclusive_value')
        exclusive_percentage=postvalues.getlist('exclusive_percentage')
        # print(f'exclusive_percentage {exclusive_percentage}, exclusive_value {exclusive_value}')
        for exclusive,value,tax_percent in zip(exclusive_list,exclusive_value,exclusive_percentage):
            # print(f'exclusive {exclusive}, value {value}')
            if exclusive:
                create_exclusive=InvoiceExclusive.objects.create(invoice_id=pk,exclusive_id=exclusive,exclusive_calculated_value=value,vendor_id=getvendordetails.id,contractid=contractid.contractid,tax_percentage=tax_percent)

        contractinvoiceid=postvalues.getlist('contractinvoiceid')
        invoicecurrencyid=postvalues.getlist('invoicecurrencyid')
        splitinvoice=postvalues.getlist('splitinvoice')
        invoicenum=postvalues.getlist('invoicenum')
        invoicedate=postvalues.getlist('invoicedate')
        percentage=postvalues.getlist('percentage')
        basecurrencyamount=postvalues.getlist('basecurrencyamount')
        paymentcurrency=postvalues.getlist('paymentcurrency')
        exchangerate=postvalues.getlist('exchangerate')
        finalamount=postvalues.getlist('amount')
        banks=postvalues.getlist('bank')

        companydateformat=postvalues.get('dateformat')
        for invoiceid,invoicesplit,num,date,per,base,payment,exchange,final,bank,invoicecurrency in zip(contractinvoiceid,splitinvoice,invoicenum,invoicedate,percentage,basecurrencyamount,paymentcurrency,exchangerate,finalamount,banks,invoicecurrencyid):
            get_convert_date=getinvoiceDate(companydateformat,date)
            create_contract_invoice=InvoiceCostInvoice.objects.create_invoicecost(pk,invoiceid,invoicesplit,num,get_convert_date,per,base,payment,exchange,final,bank,todaydate,getvendordetails.id,invoicecurrency,contractid.contractid)
        submit_type=request.POST.get('submit_type')
        if (submit_type == "0"):
            return redirect('invoice:invoicelist')
        else:
            if (wcc_id):
                redirect_url = '/invoice/addinvoicefile/{}?wcc_id={}'.format(pk,wcc_id)
                return redirect(redirect_url)
            else:
                return redirect('invoice:createinvoicestepthree',pk=pk)
    # print(f'exclusivetaxlist {vendortax.filter(Tax_Type="Exclusive")}')
    data={'company':company,'contractmaster':contract,'contracttype':contractid.contracttype,'inclusivetaxlist':getinclusivewithpercentage,'inclusivetaxcount':getinclusivewithpercentage.count(),'exclusivetaxlist':getexclusivewithpercentage,'exclusivetaxcount':vendortax.filter(Tax_Type="Exclusive").count(),'range':range(1, 61),'bankdetails':bankdetails,'pk':pk,'companycurrency':companycurrency,'vendorinvoice':vendorinvoice,'vendorinvoicecount':vendorinvoice.count(),'no_invoice':int(no_vendor_invoice),'vendorpayment':list(vendorpayment),'vendorpaymentcount':vendorpayment.count(),'total_value':contract_amount,'contract_reference':contract_reference,'invoice':contractid,'wcc_id':wcc_id,'currency_symbol':currency_symbol}
    return render(request,'createinvoiceform2.html',data)

def checkvendorinvoice(request):
    invoice_num=request.GET.get('invoice_num')
    vendorId = request.GET.get('vendorId', None)
    if (InvoiceCostInvoice.objects.filter(invoice_number__exact=invoice_num,vendor=vendorId).exists()):
        data={'data':'exists'}
    else:
        data={'data':'success'}
    return JsonResponse(data)

def createinvoicestepthree(request,pk):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    wcc_id=request.GET.get('wcc_id',None)
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.filter(vin=getvin,company=request.company,status=1).first()
    allVendors=User.objects.filter(cin_number__iexact=getvendordetails.vin,status=1)
    contractid=Invoice.objects.get(id=pk)
    wcc_id=request.GET.get('wcc_id',None)
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        contract_data=contract
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1).count()
        price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id)

    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        contract_data=ContractMaster.objects.filter(id=contract.service.id ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1).count()
        price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id)

        
    
    invoicecostinformation=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
    totalinvoicevalue=invoicecostinformation.total_invoice_value
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)

    getworkcompletion=workcompletionvalues.objects.filter(invoice_id=pk,status=1)
    if (request.POST):
        # print('asdd',request.POST)
        workcompletevalue=request.POST.getlist('workcomplete')
        checksupport=request.POST.getlist('checksupportfile')
        getinvoicefiles=request.FILES.getlist('files')
        invoicecostinvoice=request.POST.getlist('invoicecostinvoice')

        for invfile,invoicecostid in zip(getinvoicefiles,invoicecostinvoice):
            create_file=InvoiceFileUpload.objects.create(work_completion=workcompletevalue,invoice_id=pk,support=1,support_file=invfile,invoicecostinvoice_id=invoicecostid,vendor_id=getvendordetails.id,contractid=contractid.contractid,file_name=invfile)
        for support in checksupport:
            getfiles=request.FILES.getlist('file'+support+'')
            for file in getfiles:
                create_file=InvoiceFileUpload.objects.create(work_completion=workcompletevalue,invoice_id=pk,support=support,support_file=file,vendor_id=getvendordetails.id,contractid=contractid.contractid,file_name=file)
                
        for value in workcompletevalue:
            if (value):
                create_workcompletion=workcompletionvalues.objects.create(workcompletion=value,invoice_id=pk) 
        # if (contractid.contracttype == 'original'):
        #     contract=ContractMaster.objects.filter(id=contractid,status=1).first()
        # else:
        #     contract=Amendment.objects.filter(id=contractid,status=1).first()
        # vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1).count()
        list_cost_ids=list(contractcostinvoice.values_list('id',flat=True))
        cost_count=contractcostinvoice.count()
        invoicesupportfile=InvoiceFileUpload.objects.filter(invoice_id=pk,invoicecostinvoice_id__in=list_cost_ids,status=1).count()
        # print(vendorinvoice,cost_count,invoicesupportfile)
        # if (vendorinvoice == cost_count  and vendorinvoice == invoicesupportfile):
        #     Invoice.objects.filter(id=pk).update(invoice_status=2)
        submit_type=request.POST.get('submit_type')
        if (submit_type == "0"):

            return redirect('invoice:invoicelist')
        elif (submit_type == "3"):
            #update here invoice
            if (vendorinvoice == cost_count  and vendorinvoice == invoicesupportfile):
                now = datetime.now()
                calculate_time=add_time(now,request.company)
                scheme=request.scheme
                gethost=request.get_host()  
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
                all_invoice=', '.join(str(e) for e in invoice_number)
                Invoice.objects.filter(id=pk).update(invoice_status=2,created_at=calculate_time)
                invoice_type=Invoice.objects.filter(id=pk)
                invoice_id=invoice_type.first()
                sender = User.objects.get(id=request.user.id)
                if (contract_data.projects.flow_level == "discipline"):
                    checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdisciplinetype_id,'discipline',request.company,contract_data.projects_id)
                elif (contract_data.projects.flow_level == "clusters"):
                    checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdiscipline.cluster_id,'clusters',request.company,contract_data.projects_id)
                else:
                    if contractid.well_not_applicable == "id":
                        checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contractid.well_id,'well',request.company,contract.projects_id)
                        print('well ')
                    else:
                        print('well based discipline')
                        #use wellbased field to get data
                        checkflow=ProjectFlowlevel.objects.projectflow_bywellbasedlevel_main(contract_data.projectdisciplinetype_id,'well',request.company,contract_data.projects_id)
                if not checkflow:
                    checkflow=ProjectFlowlevel.objects.filter(project_id=invoice_id.project_id,company_id=request.company.id,status=1).first()
                flowlevelmodules=ProjectFlowModules.objects.getactiveflow_level(checkflow.id)
                flowlevelusers=ProjectFlowModuleUsers.objects.getflowusers_active(flowlevelmodules.id,checkflow.id)
                user_pro=ProjectUser.objects.filter(id__in=flowlevelusers.values_list('user_id',flat=True)).first()
                getmodules=ProcessModule.objects.getmodule_byid(flowlevelmodules.module_id)
                now = datetime.now()
                get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
                get_invoice_date=get_payment_term.payment_terms.payment_day
                get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
                calculate_time=add_invoice_time(now,get_company_invoice_time)
                invoiceflow_modules=Invoiceflowmodules.objects.createinvoiceflowmodules(contract_data.projects_id,request.company,checkflow.id,flowlevelmodules.id,pk,getmodules.module_id,now,calculate_time)
                urls=getInvoiceModule(getmodules.module_id,pk)
                usercreate = request.user.roles_id
                create_user_log(request,all_invoice,'Invoice','Create','Invoice Created',usercreate)
                for user in flowlevelusers:
                    projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                    Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(contract_data.projects_id,projectusers.id,invoiceflow_modules.id,user.id,projectusers.user_id)
                    recipientuser = User.objects.get(id=projectusers.user_id)
                    print(f"recipientuser {recipientuser}")
                    # notify.send(sender, recipient=recipientuser,data=urls, verb='Invoice Raised', description=f'{get_vendor_company_name(request.user.cin_number)} has raised Invoice for Invoice No: {all_invoice}')
                    notify_invoice_flow(request,recipientuser,urls,'Invoice Received',f'Invoice received from {get_vendor_company_name(request.user.cin_number)} for {contractid.name_service}')
                    # notify.send(sender, recipient=recipientuser,data=urls, verb='Invoice Received', description=f'Invoice received from {get_vendor_company_name(request.user.cin_number)} for {contractid.name_service}')
                    invoice_submission_fpoc(request.company,recipientuser,invoice_type.first(),getvendordetails,request)
                today = date.today()
                date_today = today.strftime("%d-%b-%Y")
                sender = User.objects.get(id=request.user.id)
                recipient = User.objects.filter(company=request.company.id,roles_id=2).first()
                # notify.send(sender, recipient=recipient,data=urls, verb='Invoice Submitted', description=f'{get_vendor_company_name(request.user.cin_number)} has submitted Invosubmission_fpocice for Invoice No: {all_invoice}')
                recipient = User.objects.filter(cin_number__iexact=getvin,status=1)
                print('recipient',recipient)
                sender = User.objects.filter(company=request.company.id,roles_id=2).first() 
                
                urls=f"{scheme}://{gethost}/invoice/invoicelist"
                for notifications in recipient:     
                    notify.send(sender, recipient=notifications,data=urls, verb='Invoice Received', description=f'Invoice received by {request.company.company_name} on {date_today} for {contractid.name_service} ')
                    invoive_submission_mail(request,request.company,notifications)
                # user_receiver = User.objects.get(id=user_pro.user_id)
                # notify.send(sender, recipient=user_receiver,data=urls, verb='Invoice for Approval', description=f'Invoice {all_invoice} for Vendor {get_vendor_company_name(request.user.cin_number)} for services {contractid.name_service}')
                messages.success(request, 'Invoice Submitted Successfully')
                # for vendors in allVendors:
                #     invoive_submission_mail(request,request.company,vendors)

            return redirect('invoice:invoicelist')
        else:
            # Invoice.objects.filter(id=pk).update(invoice_status=2)
            if (wcc_id):
                redirect_url = '/invoice/invoicepreview/{}?wcc_id={}'.format(pk,wcc_id)
                return redirect(redirect_url)
            else:       
                return redirect('invoice:invoicepreview',pk=pk)
    wcc_files=other_documents()
    data={'vendorinvoice':vendorinvoice,'created_inv_count':contractcostinvoice.count(),'contractcostinvoice':contractcostinvoice,'contracttype':contractid.contracttype,'contract':contract,'invoicecostinformation':invoicecostinformation,'totalinvoicevalue':totalinvoicevalue,'pk':pk,'all_work_completion':getworkcompletion,'wcc_id':wcc_id,'wcc_files':wcc_files,'price_table_files':price_table_files}
    # if (wcc_id):

        # data.update({'wcc_files':wcc_files})
    return render(request,'createinvoiceform3.html',data)



def invoicepreview(request,pk):
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.filter(vin=getvin,company=request.company,status=1).first()
    contractid=Invoice.objects.get_by_id(pk)
    wcc_id=request.GET.get('wcc_id',None)
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1)
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1)
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    invoicedetail=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
    if (invoicedetail == None):
        invoicedetail=""
    invoicefiles=InvoiceFileUpload.objects.filter(invoice_id=pk,status=1)
    get_document_data=getDocumentlist()
    get_document_data.pop(0)
    data={'contractcostinvoice':contractcostinvoice,'invoicefiles':invoicefiles,'pk':pk,'vendor_id':getvendordetails.id,'contract_id':contract.id,'contract_type':contractid.contracttype,'maininvoices':vendorinvoice,'invoicedetail':invoicedetail,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'wcc_id':wcc_id,'support_dcouments':get_document_data}
    return render(request,'invoicepreview.html',data) 


def getsupportfiles(request):
    supportid=request.GET.get('supportid','')
    invoiceid=request.GET.get('invoiceid','')
    wcc_id=request.GET.get('wcc_id','')
    get_wcc_files=[]
    
    if (supportid == "9" or supportid == "10"):
        contractid=Invoice.objects.get_by_id(invoiceid)
        print(f"contractid.contracttype {contractid.contracttype}")
        if (contractid.contracttype == 'original'):
            print(f"contractid.contractid {contractid.contractid}")
            contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
            confile=str(contract.upload_contract)
            contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,1).values()
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,2).values()

            print(f"price_table_files {price_table_files}")
            price_file=str(contract.upload_pricetable)
            data={'con_file':list(contract_table_files),'price_file':list(price_table_files),'contracttype':contractid.contracttype}
        else:
            print(f"ontractid.contractid {contractid.contractid}")
            contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()

            original_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,1).values()
            original_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,2).values()

            amendment_addendum_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,1).values()
            amendment_addendum_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,2).values()
            confile=original_contract_table_files.union(amendment_addendum_contract_table_files)
            price_table_files=original_price_table_files.union(amendment_addendum_price_table_files)
            data={'con_file':list(confile),'price_file':list(price_table_files),'contracttype':contractid.contracttype}

        return JsonResponse(data,safe=False)
    else:
        if (wcc_id):
            if (supportid == "2"):
                get_wcc_files=list(WorkCompletionValue.objects.filter_by_wcc(wcc_id).values())
                print(get_wcc_files)
            else:
                files_data=list(WccFileUpload.objects.get_by_support(wcc_id,1,supportid).values())
                get_wcc_files=change_key_name(files_data,"wcc_support_file","support_file")
        getfiles=list(InvoiceFileUpload.objects.filter(invoice_id=invoiceid,support=supportid,status=1).values())
        query_files=DisputedQueryFiles.objects.filter(disputedquery__query_id=invoiceid ,document_type=supportid).values()
        get_wcc_files.extend(getfiles)
        get_wcc_files.extend(query_files)
        data={'filecount':len(get_wcc_files),'files':get_wcc_files}
 
        return JsonResponse(data)

def invoicelist(request):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    markas_read_status(request.get_full_path())
    user=User.objects.filter(Q(is_primary=1) | Q(is_secondary=1),id=request.user.id).first()
    vendor_status = True if user else False
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    # allinvoices=Invoice.objects.filter(vendor_id=vendorid.id,status=1).exclude(invoice_status=6).order_by('-id') if vendor_status == True else Invoice.objects.filter(vendor_id=vendorid.id,status=1,invoice_status__in=[2,4]).order_by('-id')
    # count=allinvoices.count()
    data={'vendor_status':vendor_status,'vendorid':vendorid}
    return render(request,'invoicelist.html',data)

def invoiceview(request,pk):

    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    
    invoicedetail=Invoice.objects.get_by_id_status(pk,1)
    invoicecostinformation=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
    invoicedisount=InvoiceDiscount.objects.get_invoice_id(pk,1)
    contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
    invoicesupportfile=InvoiceFileUpload.objects.get_invoice_id(pk,1,None)
    getvendordetails=ContractMasterVendor.objects.get_byid(invoicedetail.vendor.id,request.company)
    invoicedetails=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
    invoice_id = Invoice.objects.get_by_id_status(pk, 1)
    split_invoices = InvoiceCostInvoice.objects.filter(invoice_id=invoice_id, status=1)
    if (invoicedetails == None):
        invoicedetails=""
    try:
        if (invoicedetail.contracttype == 'original'):
            getinclusivetax=VendorCompanyTaxDetails.objects.getvendortax_by_contract(invoicedetail.vendor.id,invoicedetail.contractid,request.company,"Inclusive").values_list('id',flat=True)
            contract=ContractMaster.objects.getcontract(invoicedetail.contractid)
            vendorinvoice=VendorInvoiceSplit.objects.getvendor_split_invoice(getvendordetails.id,contract.id,request.company)
        else:
            getinclusivetax=VendorCompanyTaxDetails.objects.getvendortax_by_amendment(invoicedetail.vendor.id,invoicedetail.contractid,request.company,"Inclusive").values_list('id',flat=True)
            contract=Amendment.objects.get_by_id(invoicedetail.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.getvendor_split_invoiceamendment(getvendordetails.id,contract.id,request.company)
        getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.vendorTax(getinclusivetax)
        getexclusivetax=InvoiceExclusive.objects.get_by_id(pk)
        
        listdata = unique_list(list(vendorinvoice.values_list('currency__id',flat=True)))
        costcodedata=CostCodeVendor.objects.get_by_id(invoicedetail.costcodevendor.id) if invoicedetail.costcodevendor else ''
        get_document_data=getDocumentlist()
        get_document_data.pop(0)
        get_document_data.pop(0)
        check_settlement=SettlementInvoice.objects.filter(invoice_id=pk)
        mapped_creditnote=CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True)
        payment_receipt=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True)
        get_used_creditnotes=list(mapped_creditnote.values_list('credit_note_id',flat=True).distinct())
        module_value=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
       

        data={'invoicedetail':invoicedetail,'invoicecostinformation':invoicecostinformation,'invoicedisount':invoicedisount,'contractcostinvoice':contractcostinvoice,'invoicesupportfile':invoicesupportfile,'pk':pk,'invoicedetails':invoicedetails,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency',flat=True).last(),'listdata':listdata,'costcodedata':costcodedata,'support_documents':get_document_data,'check_settlement':check_settlement.count(),'check_creditnote':mapped_creditnote.count(),'get_used_creditnotes':get_used_creditnotes ,'get_used_creditnotes_count':len(get_used_creditnotes),'payment_receipt':payment_receipt,'payment_count':payment_receipt.count(),'status':True,'contract':contract ,"module_value":module_value ,"module_count":len(module_value),'split_invoices':split_invoices,'basecurreccy_symbol':vendorinvoice.values_list('currency__currency_symbol',flat=True).first()}
    except:
        data={'pk':pk}
    return render(request,'invoiceview.html',data)

def invoicefile(request,id,type,pk):
    if (type == "invfile"):
        invoice=InvoiceFileUpload.objects.get(invoicecostinvoice_id=id,invoice_id=pk,status=1)
        # filepath=request.scheme+'://'+request.gethost()+'/'+invoice.support_file.url
        getfilename=invoice.support_file.path
        getextension=pathlib.Path(getfilename).suffix
        if (getextension == ".pdf"):
        # return render(request,'invoicelist.html') 
            with open(getfilename, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                return response
        else:
            image_data = open(getfilename, "rb").read()
            return HttpResponse(image_data, content_type="image/jpeg")
    else:
        # invoice_details=Invoice.objects.get_by_id(id)
        # print(f"invoice_details {invoice_details.contractid}")

        # files = VendorContractPriceTable.objects.getfiles_byid(pk)
        # file_path = os.path.join(settings.MEDIA_ROOT, str(files.file_name))
        
        # with open(file_path, 'rb') as f:
        #     # Prepare an HTTP response with the file contents
        #     response = HttpResponse(f.read(), content_type='application/octet-stream')
        #     # Set the Content-Disposition header to force download
        #     response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        #     return response


        invoice=InvoiceFileUpload.objects.get(id=pk,status=1)
        # filepath=request.scheme+'://'+request.gethost()+'/'+invoice.support_file.url
        getfilename=invoice.support_file.path
        getextension=pathlib.Path(getfilename).suffix
        if (getextension == ".pdf"):
        # return render(request,'invoicelist.html') 
            with open(getfilename, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                return response
        else:
            image_data = open(getfilename, "rb").read()
            return HttpResponse(image_data, content_type="image/jpeg") 

def getcontractfile(request,contractid,type,filetype):
    if (filetype == "contract"):
        if (type == 'original'):
            contract=ContractMaster.objects.filter(id=contractid ,status=1).first()
            getfilename=contract.upload_contract.path
            getextension=pathlib.Path(getfilename).suffix
            if (getextension == ".pdf"):
            # return render(request,'invoicelist.html') 
                with open(getfilename, 'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                    return response
            else:
                image_data = open(getfilename, "rb").read()
                return HttpResponse(image_data, content_type="image/jpeg") 
        else:
            contract=Amendment.objects.filter(id=contractid,status=1).first()
            getfilename=contract.amendment_upload_contract.path
            getextension=pathlib.Path(getfilename).suffix
            if (getextension == ".pdf"):
            # return render(request,'invoicelist.html') 
                with open(getfilename, 'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                    return response
            else:
                image_data = open(getfilename, "rb").read()
                return HttpResponse(image_data, content_type="image/jpeg") 
            
    else:
        if (type == 'original'):
            contract=ContractMaster.objects.filter(id=contractid ,status=1).first()
            getfilename=contract.upload_pricetable.path
            getextension=pathlib.Path(getfilename).suffix
            if (getextension == ".pdf"):
                with open(getfilename, 'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                    return response
            else:
                image_data = open(getfilename, "rb").read()
                return HttpResponse(image_data, content_type="image/jpeg") 
        else:
            contract=Amendment.objects.filter(id=contractid,status=1).first()
            getfilename=contract.amendment_upload_pricetable
            getextension=pathlib.Path(getfilename).suffix
            if (getextension == ".pdf"):
            # return render(request,'invoicelist.html') 
                with open(getfilename, 'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline;filename=some_file.pdf'
                    return response
            else:
                image_data = open(getfilename, "rb").read()
                return HttpResponse(image_data, content_type="image/jpeg") 

def editinvoiceform(request,pk,status):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    wcc_id=request.GET.get('wcc_id',None)
    invoice=Invoice.objects.get_by_id(pk)
    company=Settings.objects.filter(company_id=request.company.id).first()
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    cost_code_list = CostCodeVendor.objects.filter(vendor_id=vendorid.id,status=1 ,contractid=invoice.contractid)
    getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()

    cost_Contract_id=invoice.contractid
    cost_Contract_type=invoice.contracttype
    if(getlastlevel != None):
        lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
    else:
        lastlevel=None 
    contractlist=ContractMaster.objects.getcontractmaster(vendorid.id).exclude(wcc=1) if wcc_id == '' or wcc_id ==None else ContractMaster.objects.getcontractmaster(vendorid.id).filter(wcc=1)
    # contractlist=ContractMaster.objects.filter(contractvendor_id=vendorid.id,status=1).exclude(Q(name_service__exact = '') | Q(name_service__isnull=True) | Q(reference_number__exact='') | Q(reference_number__isnull=True) | Q(executed_date__isnull=True) | Q(amount__exact='') | Q(amount__isnull=True) | Q(upload_contract__exact='') | Q(upload_contract__isnull=True) | Q(upload_pricetable__exact='') | Q(upload_pricetable__isnull=True) | Q(projects_id__isnull=True) | Q(projectdiscipline_id__isnull=True) | Q(projectdisciplinetype_id__isnull=True)).exclude(wcc=0) if wcc_id  else ContractMaster.objects.filter(contractvendor_id=vendorid.id,status=1).exclude(Q(name_service__exact = '') | Q(name_service__isnull=True) | Q(reference_number__exact='') | Q(reference_number__isnull=True) | Q(executed_date__isnull=True) | Q(amount__exact='') | Q(amount__isnull=True) | Q(upload_contract__exact='') | Q(upload_contract__isnull=True) | Q(upload_pricetable__exact='') | Q(upload_pricetable__isnull=True) | Q(projects_id__isnull=True) | Q(projectdiscipline_id__isnull=True) | Q(projectdisciplinetype_id__isnull=True)).exclude(wcc=1)
    allcontractlist=[]
    if (wcc_id):
        for contract in contractlist:
            if contract.wcc == 1:
                allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original','check_status':contract.projects.active_status})
            get_amendmentlist=Amendment.objects.getamendment(contract.id).exclude(wcc=0)
            for amendment in get_amendmentlist:
                if amendment.amendment_type == 'Amendment':
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment','check_status':amendment.service.projects.active_status})
                else:
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum','check_status':amendment.service.projects.active_status})
    else:
        for contract in contractlist:
            allcontractlist.append({'id':contract.id,'contractrefnum':contract.reference_number+' (Original Contract)','type':'original','check_status':contract.projects.active_status})
            get_amendmentlist=Amendment.objects.getamendment(contract.id).exclude(wcc=1)
            for amendment in get_amendmentlist: 
                if amendment.amendment_type == 'Amendment':
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Amendment)','type':'amendment','check_status':amendment.service.projects.active_status})
                else:
                    allcontractlist.append({'id':amendment.id,'contractrefnum':amendment.amendment_reference_number+' (Addendum)','type':'addendum','check_status':amendment.service.projects.active_status})
    if (invoice.contractid == ''):
        getprojectid=''
        projectid=''
    else:
        if (invoice.contracttype == 'original'):
            getprojectid=ContractMaster.objects.filter(id=invoice.contractid).first()
            projectid=getprojectid.projects.id
            
        else:
            getprojectid=Amendment.objects.filter(id=invoice.contractid).first()
            projectid=getprojectid.service.projects.id
        
    if (request.POST):
        invoicetype=request.POST.get('invoicetype')
        # receiptdate=request.POST.get('receiptdate')
        fromdate=request.POST.get('fromdate')
        todate=request.POST.get('todate')
        contract=request.POST.get('contractid')
        split_contract=contract.split("-")
        contractnameservice=request.POST.get('contractnameservice')
        contractservicetype=request.POST.get('contractservicetype')
        service_rendered=request.POST.get('service_rendered')
        location_service=request.POST.get('location_service')
        project=request.POST.get('project')
        block=request.POST.get('block')
        field=request.POST.get('field')
        well=request.POST.get('well')
        block_not=request.POST.get('block_not')
        field_not=request.POST.get('field_not')
        well_not=request.POST.get('well_not')
        costcode=request.POST.get('costcode')
        # receipt_datetime_object = datetime.strptime(receiptdate,request.POST.get('companydateformat'))
        if (fromdate != '' and fromdate != None):
            from_datetime_object = datetime.strptime(fromdate,'%d-%b-%Y')
        else:
            from_datetime_object=None
        if (todate != '' and todate != None):
            todate_datetime_object = datetime.strptime(todate,'%d-%b-%Y')
        else:
            todate_datetime_object=None
        # from_datetime_object = datetime.strptime(fromdate,'%b-%Y')
        # todate_datetime_object = datetime.strptime(todate,'%b-%Y')
        vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number,status=1).first()
        current_date_time = datetime.now(timezone.utc)
        print(current_date_time,'tttlll......')
        create_invoice=Invoice.objects.filter(id=pk).update(invoice_type=invoicetype,fromdate=from_datetime_object,todate=todate_datetime_object,contractid=split_contract[0],contracttype=split_contract[1],name_service=contractnameservice,types_service=contractservicetype,description_service=service_rendered,location_service=location_service,project_name=project,block_id=block,field_id=field,well_id=well,block_not_applicable=block_not,field_not_applicable=field_not,well_not_applicable=well_not,costcodevendor_id=costcode , project_id=projectid)
        submit_type=request.POST.get('submit_type')
        if (submit_type == "0"):
            return redirect('invoice:invoicelist')
        else:
            request.session['contractid']=request.POST.get('contractid')
            if status == 1:
                if (wcc_id):
                    print('if--condition')
                    redirect_url = '/invoice/editinvoicesteptwo/{}/{}?wcc_id={}'.format(pk,1,wcc_id)
                    return redirect(redirect_url)
                else:
                    print('else--condition')
                    return redirect('invoice:editinvoicesteptwo',pk=pk,status=1)
            else:
                if (wcc_id):
                    redirect_url = '/invoice/createinvoicesteptwo/{}?wcc_id={}'.format(pk,wcc_id)
                    return redirect(redirect_url)
                else: 
                    return redirect('invoice:createinvoicesteptwo',pk=pk)
    # return render (request,'backcreateinvoice1.html',data)
    data={'invoice':invoice,'company_date':company,'allcontractlist':allcontractlist,'getprojectid':projectid,'status_type':status,'company':request.company,'lastlevel':lastlevel,'cost_code_list':cost_code_list,'wcc_id':wcc_id,'vendor':vendorid ,'cost_Contract_id':cost_Contract_id ,'cost_Contract_type':cost_Contract_type}
    if (wcc_id):
        wcc_data=WorkCompletionCost.objects.get_by_id(wcc_id)
        if (wcc_data.contracttype == 'original'):
            getprojectid=ContractMaster.objects.getcontract(wcc_data.contractid)
            projectid=getprojectid.projects.id
        else:
            getprojectid=Amendment.objects.get_by_id(wcc_data.contractid,1).first()
            projectid=getprojectid.service.projects.id
        wcc_obj={'wcc_data':wcc_data,'getprojectid':projectid}
        data.update(wcc_obj)
    return render(request,'editinvoiceform1.html',data)


def safe_float(value, default=0.0):
    try:
        return float(value)
    except ValueError:
        return default

def editinvoicesteptwo(request,pk,status):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list' 
    company=Settings.objects.filter(company_id=request.company.id).first()
    if not company:
        pass
    getcurrencylist=ast.literal_eval(company.currency)
    companycurrency=Basecountries.objects.filter(id__in=getcurrencylist)
    contractid=Invoice.objects.get_by_id(pk)
    wcc_id=request.GET.get('wcc_id',None)
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.filter(vin=getvin,company=request.company,status=1).first()
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        contract_amount = contract.amount if contract.amount == 'No Max Limit' else contract.amount.replace(',','')
        contract_reference = contract.reference_number
        vendortax=VendorCompanyTaxDetails.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1)
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1)
        print('vendorinvoice1',vendorinvoice)
        vendorpayment=VendorPaymentTerms.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1)
        if (vendorinvoice.count() >0):
            get_vendor_invoice=list(vendorinvoice.values('no_invoice').distinct())
            no_vendor_invoice=get_vendor_invoice[0]['no_invoice']
        else:
            no_vendor_invoice='1'
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        contract_amount = contract.amendment_amount if contract.amendment_amount == 'No Max Limit' else contract.amendment_amount.replace(',','')
        contract_reference = contract.amendment_reference_number
        vendortax=VendorCompanyTaxDetails.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1)
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1)
        print('vendorinvoice2',vendorinvoice)
        vendorpayment=VendorPaymentTerms.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1)
        vendorpaymentlist=vendorpayment.values_list()
        if (vendorinvoice.count() >0):
            get_vendor_invoice=list(vendorinvoice.values('no_invoice').distinct())
            no_vendor_invoice=get_vendor_invoice[0]['no_invoice']
        else:
            no_vendor_invoice='1' 
    getexchangetype=vendorinvoice.first()
    inclusivetaxlist=vendortax.filter(Tax_Type="Inclusive").values_list('id',flat=True)
    getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=inclusivetaxlist,status=1)
    exclusivetaxlist=vendortax.filter(Tax_Type="Exclusive").values_list('id',flat=True)
    getexclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=exclusivetaxlist,status=1)
    # mylist = json.dumps(list(vendorinvoice.values()))
    # mylist = list(vendorinvoice)
    bankdetails=BankDetails.objects.filter(vendor_id=getvendordetails.id,company=request.company,status=1)
    todaydate = datetime.now().date()
    # created invoice details #
    invoicedetail=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1)
    otherdetails=InvoiceOthersAmount.objects.filter(invoice_id=pk,status=1)
    print('invoicedetail',invoicedetail)
    # Check if invoicedetail is not empty before accessing its attributes
    if invoicedetail.exists():
        # Assuming total_invoice_value is a field in the InvoiceCostInformation model
        totalvalueofinvoice = invoicedetail.first().total_invoice_value
    else:
        invoicedetail = ""  # Set invoicedetail to an empty string if it's None or empty
        totalvalueofinvoice = ''

    invoice_discount=InvoiceDiscount.objects.filter(invoice_id=pk,status=1)
    invoice_exclusive_tax=InvoiceExclusive.objects.filter(invoice_id=pk,status=1)
    created_invoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    invoice_numbers=list(created_invoice.values_list('invoice_number',flat=True))
    get_created_invoice=list(created_invoice.values_list('vendor_invoice',flat=True))
    balance_vendorinvoice=vendorinvoice.exclude(id__in=get_created_invoice)
    # ends here created invoice details#
    # print("sftagba",created_invoice)
    exchange_type = None  # Initialize with a default value

    try:
        if getexchangetype is not None:
            exchange_type = getexchangetype.exchange_rate
    except AttributeError:
        # Handle the AttributeError here, such as assigning a default value
        pass  # No need to do anything here as exchange_type already has a default value

    print(request.POST)
    if (request.POST):
        print("Form data received:", request.POST)
        postvalues=request.POST
        tax_types=postvalues.get('tax_types')
        print(f'tax_types {tax_types}')
        Invoice.objects.filter(id=pk).update(tax_type=tax_types)
        hdninvcost=postvalues.get('hdninvcost')
        # total_invoice=postvalues.get('totalvalue')
        # total_invoice1 = (''.join(e for e in total_invoice if e.isalnum()).replace(',',''))
        # get_total_value1=re.findall(r'[0-9][0-9,.]+', total_invoice1)
        # get_total_value = get_total_value1[0]
        total_invoice = postvalues.get('totalvalue')
        pattern = r'[^A-Za-z0-9.,]+'
        matches = re.sub(pattern, '', total_invoice)

        # Remove commas from numeric values
        matches = matches.replace(',', '')

        # Check if the string is not empty before converting to float
        # if matches:
        #     try:
        #         get_total_value = float(matches)
        #     except ValueError:
        #         # Handle the case where total_invoice is not a valid float
        #         get_total_value = 0.0  # or any default value you prefer
        # else:
        #     # Handle the case where total_invoice is an empty string
        #     get_total_value = 0.0  # or any default value you prefer
        get_total_value = matches

        # if len(get_total_value) > 0:
        #     get_total_value = get_total_value[0]
        # else:
        #     get_total_value = ''
        grossamountwithdis=postvalues.get('grossamountwithdis')
        grossamountafterother=postvalues.get('grossamountwithother')
        totalexclusivetax=postvalues.get('totalexclusivetax')
        totalalltax=postvalues.get('totalalltax')
        paymentterm=postvalues.get('paymentterm')
        if (hdninvcost):
            InvoiceCostInformation.objects.filter(id=hdninvcost).update(total_invoice_value=get_total_value,total_discount_value=grossamountwithdis,total_exclusive_value=totalexclusivetax,finalvalue=totalalltax,payment_terms_id=paymentterm,total_after_otherdetails=grossamountafterother)
            invoice_cost_info=hdninvcost
        else:
            invoice_cost_info=InvoiceCostInformation.objects.create(total_invoice_value=get_total_value,total_discount_value=grossamountwithdis,total_exclusive_value=totalexclusivetax,finalvalue=totalalltax,payment_terms_id=paymentterm,invoice_id=pk,vendor_id=getvendordetails.id,contractid=contractid.contractid,total_after_otherdetails=grossamountafterother)
            invoice_cost_info=invoice_cost_info.id
        InvoiceCostInformation.objects.filter(invoice_id=pk).exclude(id=invoice_cost_info).update(status=0)
        hdninvdis=postvalues.getlist('hdninvdis')
        discountname=postvalues.getlist('discountname')
        discounttype=postvalues.getlist('discounttype')
        discountamount=postvalues.getlist('discountamount')
        discount_value=postvalues.getlist('discount_value')
        discountidlist=[]

        for hdndis,name,type,amount,value in zip(hdninvdis,discountname,discounttype,discountamount,discount_value):
            if (hdndis):
                InvoiceDiscount.objects.filter(id=hdndis).update(discount_name=name,discount_type=type,discount_value=amount,discount_calculated_value=value)
                discountidlist.append(hdndis)
            else:
                create_discount=InvoiceDiscount.objects.create(invoice_id=pk,discount_name=name,discount_type=type,discount_value=amount,discount_calculated_value=value,vendor_id=getvendordetails.id)
                discountidlist.append(create_discount.id)
        InvoiceDiscount.objects.filter(invoice_id=pk).exclude(id__in=discountidlist).update(status=0)

        hdninvother=postvalues.getlist('hdninvother')
        # hdninvdis=['']
        others_name=postvalues.getlist('others_name')
        others_amount=postvalues.getlist('others_amount')
        othersidlist=[]
        # print(f'hdninvdis {hdninvdis},others_name {others_name},')
        for hdndis,name,amount in zip(hdninvother,others_name,others_amount):
            if (hdndis):
                InvoiceOthersAmount.objects.filter(id=hdndis).update(description=name,amount=amount)
                othersidlist.append(hdndis)
            else:
                if name:
                    create_otherdata=InvoiceOthersAmount.objects.create(invoice_id=pk,description=name,amount=amount,vendor_id=getvendordetails.id)
                    othersidlist.append(create_otherdata.id)
        InvoiceOthersAmount.objects.filter(invoice_id=pk).exclude(id__in=othersidlist).update(status=0)

        hdninvexcl=postvalues.getlist('hdninvexcl')
        exclusive_list=postvalues.getlist('exclusive')
        exclusive_value=postvalues.getlist('exclusive_value')
        exclusive_percentage=postvalues.getlist('exclusive_percentage')
        excluiveidlist=[]
        print(f'hdninvexcl {hdninvexcl} ,exclusive_list {exclusive_list},exclusive_value {exclusive_value},exclusive_percentage {exclusive_percentage}')
        for hdnexcl,exclusive,value,tax_percent in zip(hdninvexcl,exclusive_list,exclusive_value,exclusive_percentage):
            if (hdnexcl):
                InvoiceExclusive.objects.filter(id=hdnexcl).update(exclusive_id=exclusive,exclusive_calculated_value=value,tax_percentage=tax_percent)
                excluiveidlist.append(hdnexcl)
            else:
                if exclusive != '':
                    create_exclusive=InvoiceExclusive.objects.create(invoice_id=pk,exclusive_id=exclusive,exclusive_calculated_value=value,vendor_id=getvendordetails.id,tax_percentage=tax_percent)
                    excluiveidlist.append(create_exclusive.id)
        InvoiceExclusive.objects.filter(invoice_id=pk).exclude(id__in=excluiveidlist).update(status=0)

        hdnveninv=postvalues.getlist('hdnveninv')   
        contractinvoiceid=postvalues.getlist('contractinvoiceid')
        invoicecurrencyid=postvalues.getlist('invoicecurrencyid')
        splitinvoice=postvalues.getlist('splitinvoice')
        invoicenum=postvalues.getlist('invoicenum')
        invoicedate=postvalues.getlist('invoicedate')
        percentage=postvalues.getlist('percentage')
        basecurrencyamount=postvalues.getlist('basecurrencyamount')
        print("this is base",basecurrencyamount)
        paymentcurrency=postvalues.getlist('paymentcurrency')
        exchangerate=postvalues.getlist('exchangerate')
        finalamount=postvalues.getlist('amount')
        banks=postvalues.getlist('bank')     
        grs_amount=postvalues.getlist('totalsumcls')     
        companydateformat=postvalues.get('dateformat')
        veninvidlist=[]
        # inclusive_tax=postvalues.get('incpercentage')
        grossamount =postvalues.get('grossamout', '0.0')
        if grossamount == "":
            grossamount=0
        else :
            grossamount=grossamount
        inclusive_tax = postvalues.get('incpercentage', '0.0')
        
        if inclusive_tax == "":
            inclusive_tax=0
        else :
            inclusive_tax=inclusive_tax
        print('total_invoice',(total_invoice))
        print('grossamount',grossamount)
        for hdninv, invoiceid, invoicesplit, num, date, per, base, payment, exchange, final, bank, invoicecurrency in zip(hdnveninv, contractinvoiceid, splitinvoice, invoicenum, invoicedate, percentage, basecurrencyamount, paymentcurrency, exchangerate, finalamount, banks, invoicecurrencyid):
            # Safely convert variables involved in calculations
            grossamount =float(grossamount)  # Ensure this is done if not already
            inclusive_tax=int(inclusive_tax)
            per=float(per)
            get_convert_date=getinvoiceDate(companydateformat,date)
            # Calculations with safe conversions
            testtax1 = (grossamount * per) / 100
            testtax2 =float(round_of_two_values((testtax1 * inclusive_tax) / 100))
            netpayableamount = round_of_two_values(testtax1 - testtax2)
            print("acfgvhsaujw",base)
            if (hdninv):
                InvoiceCostInvoice.objects.filter(id=hdninv).update(vendor_invoice_id=invoiceid,invoice_payment=invoicesplit,invoice_number=num,invoice_date=get_convert_date,invoice_percentage=per,invoice_base_amount=base,invoice_currency=payment,invoice_exchange_rate=exchange,invoice_total_amount=final,invoice_bank_id=bank,invoice_submission_date=todaydate,invoice_resubmission_date=todaydate,currency_id=invoicecurrency, new_netpayable=netpayableamount , total_inclusive_percentage=inclusive_tax , total_inclusive_amount=testtax2)
                veninvidlist.append(hdninv)
            else:
                create_contract_invoice=InvoiceCostInvoice.objects.create(invoice_id=pk,vendor_invoice_id=invoiceid,invoice_payment=invoicesplit,invoice_number=num,invoice_date=get_convert_date,invoice_percentage=per,invoice_base_amount=base,invoice_currency=payment,invoice_exchange_rate=exchange,invoice_total_amount=final,invoice_bank_id=bank,invoice_resubmission_date=todaydate,vendor_id=getvendordetails.id,currency_id=invoicecurrency,invoice_submission_date=todaydate,new_netpayable=netpayableamount, total_inclusive_percentage=inclusive_tax , total_inclusive_amount=testtax2)
                veninvidlist.append(create_contract_invoice.id)
        InvoiceCostInvoice.objects.filter(invoice_id=pk).exclude(id__in=veninvidlist).update(status=0)
        # print("bhba",request.POST) 
        submit_type=request.POST.get('submit_type')
        print("hey hello",submit_type)
       
        # The rest of yo
        print("status",status)
        if submit_type == "0":
            return redirect('invoice:invoicelist')
        else:
            if status == 1:
                if (wcc_id):
                    print('if-condition')
                    redirect_url = '/invoice/editinvoicestepthree/{}/{}?wcc_id={}'.format(pk,1,wcc_id)
                    return redirect(redirect_url)
                else: 
                    print('else-condition')
                    return redirect('invoice:editinvoicestepthree',pk=pk,status=1)
            else:
                if (wcc_id):
                    redirect_url = '/invoice/addinvoicefile/{}?wcc_id={}'.format(pk,wcc_id)
                    return redirect(redirect_url)
                else: 
                    return redirect('invoice:createinvoicestepthree',pk=pk)
    try:
        invoicedetail=invoicedetail.last()
    except:
        invoicedetail=None
    invoicebase_amounts = created_invoice.values_list('invoice_base_amount', flat=True)

    # Print or process the invoicebase amounts
    for invoicebase_amount in invoicebase_amounts:
        print("invoicebase_amount",invoicebase_amount)
    data={'company':company,'contractmaster':contract,'contracttype':contractid.contracttype,'inclusivetaxlist':getinclusivewithpercentage,'inclusivetaxcount':getinclusivewithpercentage.count(),'exclusivetaxlist':getexclusivewithpercentage,'exclusivetaxcount':vendortax.filter(Tax_Type="Exclusive").count() ,'exclusivetaxValues': getexclusivewithpercentage.count() ,'range':range(1, 61),'bankdetails':bankdetails,'pk':pk,'companycurrency':companycurrency,'vendorinvoice':vendorinvoice,'vendorinvoicecount':vendorinvoice.count(),'no_invoice':int(no_vendor_invoice),'vendorpayment':list(vendorpayment),'vendorpaymentcount':vendorpayment.count(),'invoicedetail':invoicedetail,'totalvalueofinvoice':totalvalueofinvoice,'invoice_discount':invoice_discount,'invoice_exclusive_tax':invoice_exclusive_tax,'tax_count':invoice_exclusive_tax.count(),'added_taxes':invoice_exclusive_tax,'created_invoice':created_invoice,'created_invoice_count':created_invoice.count(),'exchangetype':exchange_type,'status_type':status,'maininvoices':vendorinvoice,'invoice_numbers':invoice_numbers,'total_value':contract_amount,'contract_reference':contract_reference,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'invoice':contractid,'wcc_id':wcc_id,'otherdetails':otherdetails,'other_data_count':otherdetails.count(),'discount_check':invoice_discount.count()}
    return render(request,'editinvoicesteptwo.html',data)

def editinvoicestepthree(request,pk,status):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.filter(vin=getvin,company=request.company,status=1).first()
    allVendors=User.objects.filter(cin_number__iexact=getvendordetails.vin,status=1)
    contractid=Invoice.objects.get_by_id(pk)
    wcc_id=request.GET.get('wcc_id',None)
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        contract_data=contract
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1).count()
        price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id)
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        contract_data=ContractMaster.objects.filter(id=contract.service.id ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1).count()
        price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id)

    invoicecostinformation=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
    totalinvoicevalue=invoicecostinformation.total_invoice_value
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    getworkcompletion=workcompletionvalues.objects.getworkcompletion(pk)
    if (request.POST):
        print(f'request.POST {request.POST}')
        gethdnfilesid=request.POST.getlist('hdnfileid')
        workcompletionvalues_id=request.POST.getlist('workcompletionid')
        workcompletevalue=request.POST.getlist('workcomplete')
        checksupport=request.POST.getlist('checksupportfile')   
        invoicecostinvoice=request.POST.getlist('invoicecostinvoice')
        for invoiceid in invoicecostinvoice:
            getinvoicefiles=request.FILES.get('files'+str(invoiceid),None)
            if (getinvoicefiles != None):
                file_name = getinvoicefiles
                create_file=InvoiceFileUpload.objects.upload_invoice_files(workcompletevalue,pk,getinvoicefiles,invoiceid,getvendordetails.id,1,getinvoicefiles)
                gethdnfilesid.append(create_file.id)

            i=0
            workcompletevalueids=[]
            while i < len(workcompletionvalues_id):
                if (workcompletionvalues_id[i]):
                    work=workcompletionvalues.objects.filter(id=workcompletionvalues_id[i]).update(workcompletion=workcompletevalue[i])
                    workcompletevalueids.append(workcompletionvalues_id[i])
                else:
                    if (workcompletevalue[i]):
                        create_work=workcompletionvalues.objects.create(workcompletion=workcompletevalue[i],invoice_id=pk)
                        workcompletevalueids.append(create_work.id)
                i +=1
            workcompletionvalues.objects.filter(invoice_id=pk).exclude(id__in=workcompletevalueids).update(status=0)

        for support in checksupport:
            getfiles=request.FILES.getlist('file'+support+'')
            for file in getfiles:
                create_file=InvoiceFileUpload.objects.create(work_completion=workcompletevalue,invoice_id=pk,support=support,support_file=file,vendor_id=getvendordetails.id,file_name=file.name)
                gethdnfilesid.append(create_file.id)
        new_list = list(filter(None, gethdnfilesid))
        InvoiceFileUpload.objects.update_status(pk,new_list)
        submit_type=request.POST.get('submit_type')    
        list_cost_ids=list(contractcostinvoice.values_list('id',flat=True))
        cost_count=contractcostinvoice.count()
        invoicesupportfile=InvoiceFileUpload.objects.getuploaded_files(pk,list_cost_ids).count()
        if (submit_type == "0"):
            return redirect('invoice:invoicelist')
        elif (submit_type == "3"):
            if (vendorinvoice == cost_count  and vendorinvoice == invoicesupportfile):
                now = datetime.now()
                calculate_time=add_time(now,request.company)
                Invoice.objects.filter(id=pk).update(invoice_status=2,created_at=calculate_time)
                scheme=request.scheme
                gethost=request.get_host()  
                sender = User.objects.get(id=request.user.id)
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
                invoice_type=Invoice.objects.filter(id=pk)
                invoice_id=invoice_type.first()
                all_invoice=', '.join(str(e) for e in invoice_number)
                if (contract_data.projects.flow_level == "discipline"):
                    checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdisciplinetype_id,'discipline',request.company,contract_data.projects_id)
                elif (contract_data.projects.flow_level == "clusters"):
                    checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdiscipline.cluster_id,'clusters',request.company,contract_data.projects_id)
                else:
                    if contractid.well_not_applicable == "id":
                        checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contractid.well_id,'well',request.company,contract_data.projects_id)
                        print('well')
                    else:
                        print('well based discipline')
                        #use wellbased field to get data
                        checkflow=ProjectFlowlevel.objects.projectflow_bywellbasedlevel_main(contract_data.projectdisciplinetype_id,'well',request.company,contract_data.projects_id)
                if not checkflow:
                    checkflow=ProjectFlowlevel.objects.filter(project_id=invoice_id.project_id,company_id=request.company.id,status=1).first()
                flowlevelmodules=ProjectFlowModules.objects.getactiveflow_level(checkflow.id)
                flowlevelusers=ProjectFlowModuleUsers.objects.getflowusers_active(flowlevelmodules.id,checkflow.id)
                getmodules=ProcessModule.objects.getmodule_byid(flowlevelmodules.module_id)
                now = datetime.now()
                get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
                get_invoice_date=get_payment_term.payment_terms.payment_day
                get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
                calculate_time=add_invoice_time(now,get_company_invoice_time)
                for costinvoice in contractcostinvoice:
                    invoiceflow_modules=Invoiceflowmodules.objects.createinvoiceflowmodules(contract_data.projects_id,request.company,checkflow.id,flowlevelmodules.id,pk,getmodules.module_id,now,calculate_time)
                    invoiceflow_modules.invoicecost_id=costinvoice.id
                    invoiceflow_modules.save()
                    for user in flowlevelusers:
                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(contract_data.projects_id,user.user_id,invoiceflow_modules.id,user.id,projectusers.user_id)
                urls=getInvoiceModule(getmodules.module_id,pk)
                user_pro=ProjectUser.objects.filter(id__in=flowlevelusers.values_list('user_id',flat=True)).first()
                for user in flowlevelusers:
                    print(f"user {user}")
                    projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                    # Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(contract_data.projects_id,user.user_id,invoiceflow_modules.id,user.id,projectusers.user_id)
                    recipientuser = User.objects.get(id=projectusers.user_id)
                    notify_invoice_flow(request,recipientuser,urls,'Invoice Received',f'Invoice received from {get_vendor_company_name(request.user.cin_number)} for {contractid.name_service}')
                    invoice_submission_fpoc(request.company,recipientuser,invoice_type.first(),getvendordetails,request)
                today = date.today()
                date_today = today.strftime("%d-%b-%Y")
                sender = User.objects.get(id=request.user.id)
                recipient = User.objects.filter(company=request.company.id,roles_id=2).first()
                urls=f"{scheme}://{gethost}/invoice/invoicelist"
                recipient = User.objects.filter(cin_number__iexact=getvin,status=1)
                print('recipient',recipient)
                sender = User.objects.filter(company=request.company.id,roles_id=2).first() 
                for notifications in recipient:
                    notify.send(sender, recipient=notifications,data=urls, verb='Invoice Received', description=f'Invoice received by {request.company.company_name} on {date_today} for {contractid.name_service} ')
                    invoive_submission_mail(request,request.company,notifications)
                messages.success(request, 'Invoice Submitted Successfully')
            return redirect('invoice:invoicelist')

        else:
            if status == 1:
                if (wcc_id):
                    redirect_url = '/invoice/editinvoicepreview/{}?wcc_id={}'.format(pk,wcc_id)
                    return redirect(redirect_url)
                else: 
                    return redirect('invoice:editinvoicepreview',pk=pk)
            else:
                if (wcc_id):
                    redirect_url = '/invoice/invoicepreview/{}?wcc_id={}'.format(pk,wcc_id)
                    return redirect(redirect_url)
                else: 
                    return redirect('invoice:invoicepreview',pk=pk)
    wcc_files=other_documents()
    wcc_files.pop(0)
    data={'vendorinvoice':vendorinvoice,'created_inv_count':contractcostinvoice.count(),'contractcostinvoice':contractcostinvoice,'contracttype':contractid.contracttype,'contract':contract,'invoicecostinformation':invoicecostinformation,'totalinvoicevalue':totalinvoicevalue,'pk':pk,'status_type':status,'all_work_completions':getworkcompletion,'wcc_id':wcc_id,'wcc_files':wcc_files,'price_table_files':price_table_files}
    return render(request,'editinvoicestepthree.html',data)


def editinvoicepreview(request,pk):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu']='invoice_list'
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.filter(vin=getvin,company=request.company,status=1).first()
    contractid=Invoice.objects.get_by_id(pk)
    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1)
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1)
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    invoicefiles=InvoiceFileUpload.objects.filter(invoice_id=pk,status=1)
    invoicedetail=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
    if (invoicedetail == None):
        invoicedetail=""
    get_document_data=getDocumentlist()
    get_document_data.pop(0)
    wcc_id=request.GET.get('wcc_id',None)
    data={'contractcostinvoice':contractcostinvoice,'invoicefiles':invoicefiles,'pk':pk,'vendor_id':getvendordetails.id,'contract_id':contract.id,'contract_type':contractid.contracttype,'invoicedetail':invoicedetail,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'support_dcouments':get_document_data,'wcc_id':wcc_id}
    return render(request,'editinvoicepreview.html',data) 


def invoicecompleted(request):
    vendor_id=request.GET.get('vendor_id')
    invoice_id=request.GET.get('invoiceid')
    contract_id=request.GET.get('contract_id')
    contract_type=request.GET.get('contract_type')
    if (contract_type == 'original'):
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=vendor_id,contract_id=contract_id,company=request.company,status=1).count()
    else:
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=vendor_id,amendment_id=contract_id,company=request.company,status=1).count()
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1)
    list_cost_ids=list(contractcostinvoice.values_list('id',flat=True))
    cost_count=contractcostinvoice.count()
    invoicesupportfile=InvoiceFileUpload.objects.filter(invoice_id=invoice_id,invoicecostinvoice_id__in=list_cost_ids,status=1).count()
    if (vendorinvoice == cost_count  and vendorinvoice == invoicesupportfile):
        Invoice.objects.filter(id=invoice_id).update(invoice_status=2)
    data={'status':'success'}
    return JsonResponse(data)

class InvoicePDFView(PDFTemplateView):
    template_name = 'invoice_pdf.html'
    footer_template = 'footer.html'
    pagination = True
    def get(self, request,pk, *args, **kwargs):
        companyImage= Companies.objects.filter(id=request.company.id).first()
        # company_image=getcompany_iamge(request.company.id)
        # encoded_image=company_image['encoded_image']
        # imageurl=company_image['imageurl']
        company_image=Companies.objects.filter(id=request.company.id).first()
        if company_image.image:
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')  # Convert the image to RGB mode
            image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
           
        imageurl= company_image.image.url
        invoicedetail=Invoice.objects.get_by_id_status(pk,1)
        invoicecostinformation=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
        invoicedisount=InvoiceDiscount.objects.filter(invoice_id=pk,status=1)
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        invoicesupportfile=InvoiceFileUpload.objects.filter(invoice_id=pk,status=1,invoicecostinvoice=None)
        getvin=request.user.cin_number
        payment_receipt=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True)
        split_invoices = InvoiceCostInvoice.objects.filter(invoice_id=invoicedetail, status=1)
        getvendordetails=ContractMasterVendor.objects.filter(id=invoicedetail.vendor.id,company=request.company,status=1).first()
        check_settlement=SettlementInvoice.objects.filter(invoice_id=pk)
        module_value=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
        try:
            if (invoicedetail.contracttype == 'original'):
                getinclusivetax=VendorCompanyTaxDetails.objects.filter(vendor_id=invoicedetail.vendor.id,contract_id=invoicedetail.contractid,company=request.company,status=1,Tax_Type="Inclusive").values_list('id',flat=True)
                contract=ContractMaster.objects.filter(id=invoicedetail.contractid ,status=1).first()
                vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company=request.company,status=1)
            else:
                getinclusivetax=VendorCompanyTaxDetails.objects.filter(vendor_id=invoicedetail.vendor.id,amendment_id=invoicedetail.contractid,company=request.company,status=1,Tax_Type="Inclusive").values_list('id',flat=True)
                contract=Amendment.objects.filter(id=invoicedetail.contractid).first()
                vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,amendment_id=contract.id,company=request.company,status=1)
            getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=getinclusivetax,status=1)
            getexclusivetax=InvoiceExclusive.objects.filter(invoice_id=pk,status=1)
            invoicedetails=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
            invoicedetails = "" if invoicedetails == None else invoicedetails
            cur = list(Basecountries.objects.all().values('name','currency_symbol'))
            listdata = unique_list(list(vendorinvoice.values_list('currency__id',flat=True)))
            vendor_name = ContractMasterVendor.objects.filter(id=invoicedetail.vendor.id).first()
            if (invoicedetail.contracttype == 'original'):
                contract_number = ContractMaster.objects.filter(id=invoicedetail.contractid).first().reference_number
            else:
                contract_number = Amendment.objects.filter(id=invoicedetail.contractid).first().amendment_reference_number
            invoice_number = InvoiceCostInvoice.objects.filter(invoice_id=pk).values_list('invoice_number',flat=True)
            costcodedata=CostCodeVendor.objects.get_by_id(invoicedetail.costcodevendor.id)
            mapped_creditnote=CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True)
            get_used_creditnotes=list(mapped_creditnote.values_list('credit_note_id',flat=True).distinct())
            get_document_data=getDocumentlist()
            get_document_data.pop(0)
            get_document_data.pop(0)
            data={'invoicedetail':invoicedetail,'invoicecostinformation':invoicecostinformation,'invoicedisount':invoicedisount,'inclusivetax':getinclusivewithpercentage,'exclusivetax':getexclusivetax,'contractcostinvoice':contractcostinvoice,'invoicesupportfile':invoicesupportfile,'contract':contract,'pk':pk,'invoicedetails':invoicedetails,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency',flat=True).last(),'company':request.company.id,'cur':cur,'imageurl':imageurl,'comapnyname':companyImage,'listdata':listdata,'costcodedata':costcodedata,'request':request,'vendor_name':vendor_name,'contract_number':contract_number,'invoice_number':", ".join(map(str,invoice_number)),'support_documents':get_document_data,'check_creditnote':mapped_creditnote.count(),'get_used_creditnotes':get_used_creditnotes,'check_settlement':check_settlement.count() ,'split_invoices':split_invoices ,"module_value":module_value ,"module_count":len(module_value),'payment_receipt':payment_receipt,'payment_count':payment_receipt.count()}
        except AttributeError:
            data={'invoicedetail':invoicedetail,'pk':pk,'request':request}
        # else:
        #     data={'pk':pk,'request':request}
        # get contract number from contract master and amendment
        #  get all invoice number from invoice table
        # encoded_image = base64.b64encode(companyImage.image.url).decode('utf-8')
        # encoded_image = f'{companyImage.image.url}'
        table_style = '''
        table {
        width: 100%;
        border-collapse: collapse;
        }
        .head-inv-pre {
    color: #AF2B50 !important;
    font-weight: 600 !important;
    font-size: 18px; !important;
}
            @page {
                    size: A4 portrait; /* can use also 'landscape' for orientation */
                    margin-right:1cm !important;
                    margin-left:1cm !important;
                    margin-bottom:150px !important;
                    margin-top:110px !important;
            }

            @page {
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10px;
                    
                }
                @top-center{
                    content: element(header);
                    align-items: center;
                    padding-left: 50px;
                    
                    /*line-height: 1.3;
                    font-size: 20px; 
                    margin-left:30px !important;
                    color: #AF2B50; 
                    font-weight: 600;*/
                }
                 @top-left {
            margin-top:100px !important;
            ''' + (f"content: url('data:image/png;base64,{encoded_image}');" if encoded_image else "") + '''
            margin-bottom:50px !important;         
        }
                @bottom-left{
                    margin-top:35px !important;
                    content: element(footer);
                    margin-bottom: 30px !important;
                }

            }
            *{
            font-family:arial,helvetica,sans-serif !important;
            }
       
        footer {
            position: running(footer);
            /*height: 150px;*/
        }
        header{
                position: running(header);
                font-size:10px !important;
            }
    .display_val{
        display:flex;
    }
    .summary_heading{
        color: #AF2B50 !important;
    }

     .from-head {
        color: #AF2B50;
        font-weight: 600;
        font-size:20px;
          
        text-align: center;
        margin: 10px 150px 0px 0px;
        width: 100% !important;
    }
    .invoice_no{
        margin-left:1000px !important;
    }
    .from-sub-head{
        color: #006e80;
        font-weight: 600 !important;
        font-size:18px;
        
        text-align: center !important;
        margin: 0px 120px 0px 0px;
    }

    .from-sub-head1{
        color: #006e80;
        font-weight: 600 !important;
        font-size:18px;
        
        text-align: center;
        margin: 0px 0px 25px 0px !important;
    }
    .invoice_info{  
        margin-top:20px !important;
        margin-bottom: 15px !important;
    }
    @page land{
                size:landscape;
          }
     .invoice-info {
        width:100%; 
        margin: 0 auto; border: 1px solid #c7c7c7;
    }
    
    /* @media print {
    .page-break { page-break-after: auto; }
   } */

    .invoice-info th, .invoice-info td { 
        border-bottom: 1px solid #c7c7c7 !important;
        padding: 4px 0px 0px 4px;
        font-size:14px !important;
        
        text-align:left;
    }
    .header_text{
        font-size:10px !important;
        display: inline-block; 
        width:110px;
        margin-right:5px !important;
        font-weight:600 !important;
    }
    .inv_name{
        padding-right:2px !important;
        padding-left:2px !important;
    }
    .header_val{
        font-size:10px !important;
        width: 300px !important;
    }
    .invoice-info th {
        width: 50%;
        border-right: 1px solid #c7c7c7 !important;
    }
    .invoice-info a{
         color:#96183a;
    }
    /* table { page-break-inside:auto }
   tr    { page-break-inside:avoid; page-break-after:auto } */
    .inv-pretbl {
        border: 1px solid #9f9f9f94;
        width:100%;
        margin:10px auto;
        page-break-inside: auto;
    }
    .inv-pretbl tr{
        page-break-inside: avoid;
        page-break-after: auto;
     }
     .inv-pretbl th, .inv-pretbl td {
        border:1px solid #9f9f9f94 !important;
        padding: 4px 0px 0px 0px;
        text-align:center;
}
    
    .inv-pretbl th {
        color: #007480;
        font-size: 14px;
        
        
        font-weight: 600;
        /* color:#000; */
    }
    
    .inv-pretbl td {
        color: #000000;
        font-size:14px;
        
        font-weight: 400;
        overflow-wrap: break-word !important;
        word-break: break-all !important; 
    }
    
    .inv-txt{
        overflow-wrap: break-word !important;
        word-break: break-all !important;
    }

    .dont-break-out {
      color:#96183a;
    font-size: 14px !important;
  
    /* These are technically the same, but use both */
    overflow-wrap: break-word;
    word-wrap: break-word;

    -ms-word-break: break-all;
    /* This is the dangerous one in WebKit, as it breaks things wherever */
    word-break: break-all;
    /* Instead use this non-standard one: */
    word-break: break-word;

    /* Adds a hyphen where the word breaks, if supported (No Blink) */
    -ms-hyphens: auto;
    -moz-hyphens: auto;
    -webkit-hyphens: auto;
    hyphens: auto;
    display:block;
    }

    /* .inv-file {
        width:20%;
    } */

    .widt-sno {
        width:5% ;
    }
    a {
        /* width:20%; */
        word-break: break-word !important;
        word-wrap: break-word;
    }

    .call-instr {
        width:20% !important;
    }
    .Invoice-Information-pdf tbody tr td:last-child {
        text-align: left !important;
    }

    .Invoice-Information-pdf tbody tr td {
        padding: 3px 3px;
    }

    .pdf-heading-section {
        text-align: center !important;
        width:85%;
    }

    .companyname-text { 
        text-align: center !important;    
        font-size: 20px;
        color: #AF2B50; 
        font-weight: 600;
        margin-right: 150px;
    }

    .from-sub-head-Invoice {
        color: #006e80;
        font-weight: 600 !important;
        font-size:18px;
        text-align: center;  
        margin-top: 30px; 
    }

    #invoicefile-td-left {
        width:15% !important;
        text-align: left !important;
        padding-left: 5px !important;
    }

    #invoicefile-td-left a{
        color: #96183a;
    }

    .img-pdf {
        width: 90px;
        height: 90px;
        }

    /* .img-pdf{
        width:100% !important;
        max-width:100px !important;
        height: 200px !important;
        object-fit: cover;
    } */
    
    .pdf-total-vv{
        color:#000 !important;
        font-weight: 900 !important;
        margin:0px;
    }

    .doll-val{
        color:#000 !important;
        font-weight: 900 !important;
        margin:0px;
    }
    
    .pre-vvalue{
        color:#000 !important;
        font-weight: 600 !important;
        margin:0px;
    }

    .Invoice-Summary-table-wid thead tr .table-sn-wid {
        width: 4%;
    }

    .Invoice-Summary-table-wid thead tr th {
        font-size: 10px !important;  
    }

    .Invoice-Summary-table-wid tbody tr td {
        font-size: 10px;
    }

    .table-heading-font tbody tr th{
        font-size: 10px !important;
    }

    .table-heading-font tbody tr td{
        font-size: 10px !important;
    }

    table {
        page-break-inside: avoid;
    }

    .inv-date-wid {
        width:8% !important;
    }

    .company-details {
        margin: auto;
        text-align: center;
        width: 100% !important;
    }

    .company-details h4 {
        margin-bottom: 5px;
    }
    
    .company-details p {
        color: #000;
        font-size: 10px;
        font-weight: 500;
        margin-top: 0px;
        display: inline-block !important;
    }

    /********** Applied Credit Note Summary Details **********/
    .text-center {
        text-align: center;
    }

    .credit_subhead {
        color: #006e80;
        font-weight: 600 !important;
        font-size:16px;
    }

    .creditnote_table {
        width: 100%;
        border-collapse: collapse; 
        border: 1px solid #9f9f9f94;
    }

    .creditnote_table th {
        color: #007480;
        font-size: 10px;
        border: 1px solid #9f9f9f94;
        padding: 5px 5px;
        text-align: center;
    }

    .creditnote_table td {
        color: #000;
        font-size: 10px;
        border: 1px solid #9f9f9f94;
        padding: 5px 5px;
        text-align: center;
    }

    .creditnote_table td a {
        color: #AF2B50;
        text-decoration: none;
    }
    

    /********** Applied Credit Note Summary Details **********/



        '''

        '''<header>multiline<br>header<br>lots<br>of<br>lines<br>here<br></header>

        <footer>multiline<br>footer{table_htmls}<br>lots<br>of<br>lines<br>here</footer>

        <table><thead><tr><th>Column 1</th><th>Column 2</th><th>Column 3</th></tr></thead><tbody>'''
        
        html_output = render_to_string('invoice_pdf.html', data)

        # print(html_output)
        # t = Template(table_html)
        # table_htmll = t.render(context)
        # Define the WeasyPrint CSS object with the style
        css = CSS(string=table_style)

        # Generate the PDF with WeasyPrint
        pdf_buffer = BytesIO()
        HTML(string=html_output).write_pdf(pdf_buffer, stylesheets=[css])

        # Create the Django response object with the PDF content
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')

        # Set the Content-Disposition header to force a download
        #attachment
        response['Content-Disposition'] = 'inline; filename="Invoice PDF.pdf"'

        # Return the response
        return response
        # return self.render_to_response(data)
    
    # def get_context_data(self, **kwargs):
          
    #     context = super().get_context_data(**kwargs)
    #     # Add any other context data here
    #     return context
    # def get_pdf_filename(self):
    #     return 'Invoice PDF.pdf'


class listCompanyInvoice(ListView):
    model = Invoice
    template_name = 'companyinvoicelist.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        markas_read_status(self.request.get_full_path())
        context['invoice_service_type'] = Invoice.objects.filter(company=self.request.company).values('name_service').distinct()
        invoicetype = Invoice.objects.filter(company=self.request.company).values('vendor').distinct()
        context['Vendor']=invoicetype
        context['sign_data']=check_user_sign(self.request.user)
        context['userid'] = self.request.user.id
        context['request']=self.request
        context['payment_type']=1
        return context
    
    
    def post(self, request):
        print('asd',request.POST)
        current_date=datetime.now()
        invoice_id=request.POST.get('invoice')
        payment_id=request.POST.get('payment_id')
        invoice_cost_list=request.POST.getlist('invoice_cost')
        payment_instrction =[]
        for inv_cost in invoice_cost_list:
            payment_split=request.POST.get('get_paymentcount_'+str(inv_cost))
            payment_instruct=PaymentInstruction.objects.filter(invoicecost_id=inv_cost,payment_count=payment_id,status=True).first()
            payment_instruct_li=list(PaymentInstruction.objects.filter(invoicecost_id=inv_cost,payment_count=payment_id,status=True).values_list('id',flat=True))
            PaymentInstruction.objects.filter(invoicecost_id=inv_cost,payment_count=payment_id,status=True).update(payment_status=3)
            pay_id=PaymentReceipt.objects.create_data(request.company.id,invoice_id,inv_cost,request.user.id)
            pay_id.payment_instruct=payment_instruct
            pay_id.save()
            payment_percentage=request.POST.getlist('payment_percentage_'+str(inv_cost))
            files=request.FILES.getlist('file_'+str(inv_cost)+'[]')
            payment_instrction.append(payment_instruct_li[0])
            for percentage in payment_percentage:
                for file in files :
                    PaymentReceiptFile.objects.create_file_data(pay_id.id,percentage,file,current_date)
            # update invoicecost data
            # InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1,id=inv_cost).update(approval_status=3,payment_status=2,payment_date=current_date,approval_date=current_date)
        # complete process
        payemnt_check=True
        if Invoiceflowmodules.objects.filter(module_id=4,status=0,invoice_id=invoice_id).exists():
            payemnt_check=False
        total_payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,status=True).count()
        paid_count=PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,status=True,payment_status=3).count()
        overall_count=PaymentInstruction.objects.get_by_payment(invoice_id).filter(payment_count=payment_id).exclude(payable_amount=0).count()
        verified_count=PaymentInstruction.objects.get_verified_instruction(invoice_id,1).filter(payment_count=payment_id).exclude(payable_amount=0).count()
        if (overall_count == verified_count):
            PaymentInstruction.objects.filter(id__in=payment_instrction,status=True).update(new_payment_status = 2)
            invoiceflow_modules=Invoiceflowmodules.objects.filter(invoice_id=invoice_id,module_id=7,payment_instruct_id__in=payment_instrction , status=0)
            InvoiceCostInvoice.objects.filter(id__in=invoice_cost_list,status=1).update(payment_date=current_date,approval_date=current_date )
            invoice_flow_func(invoice_id,7,request,None,"1","Approved",payment_id,payment_instrction)
            Invoiceflowmodules.objects.filter(invoice_id=invoice_id,module_id=7,payment_instruct_id__in=payment_instrction , status=0).update(status=1)
            print('invoiceflow_modules',invoiceflow_modules)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=invoiceflow_modules,user=request.user.id).update(status=1,comments=None,created_at=current_date)
            if payemnt_check:
                if total_payment == paid_count:
                    Invoice.objects.filter(id=invoice_id).update(invoice_status=3)
                    # InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1,id=inv_cost).update(approval_status=3,payment_status=2,payment_date=current_date,approval_date=current_date)
                    InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1).update(approval_status=3,payment_status=2 , payment_date=current_date)
                    return redirect(reverse_lazy("invoice:paidinvoicelist"))
            else:
                return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else: 
            invoiceflow_modules=Invoiceflowmodules.objects.filter(invoice_id=invoice_id,module_id=7,payment_instruct_id__in=payment_instruct_li)
            Invoiceflowmodules.objects.filter(invoice_id=invoice_id,module_id=7,payment_instruct_id__in=payment_instruct_li).update(status=1)
            print(invoiceflow_modules)
            InvoiceCostInvoice.objects.filter(id__in=invoice_cost_list,status=1).update(payment_date=current_date,approval_date=current_date )
            PaymentInstruction.objects.filter(id__in=payment_instrction,status=True).update(new_payment_status = 2)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=invoiceflow_modules,user=request.user.id).update(status=1,comments=None,created_at=current_date)
        return redirect(reverse_lazy("invoice:vendorbasedinvoice"))

class ListPaidInvoice(ListView):
    model = Invoice
    template_name = 'paidinvoicelist.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        markas_read_status(self.request.get_full_path())
        context['invoice_service_type']= Invoice.objects.filter(company=self.request.company , status=1,invoice_status=3).values('name_service').distinct()
        context['Vendor']= Invoice.objects.filter(company=self.request.company , status=1,invoice_status=3).values('vendor').distinct()
        context['userid'] = self.request.user.id
        context['payment_type']=2
        cost_paid=[]
        invoice_paid=Invoice.objects.filter_by_company(1,3,self.request.company).order_by('-id')
        try:
            for invoice in invoice_paid:
                invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=invoice.id,status=1)
                for cost in  invoice_cost:
                    payment=PaymentInstruction.objects.filter(invoicecost_id=cost.id,invoicecost__invoice_id=invoice.id,status=True).first()
                    if payment != None:
                        cost_paid.append(payment.payment_percentage)
            unique_values = list(set(cost_paid))
            context['paid_percentage']=unique_values
        except :
            pass

        return context
    
class CheckInvoiceApprovalProcess(View):
    def get(self,request):
        invoice_list=ast.literal_eval(request.GET.get('invoice_ids'))
        get_company_user=User.objects.filter(company=request.user.company).first()
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
        current_timestamp = datetime.timestamp(parsed_datetime)
        for id in invoice_list:
            invoice_detail = Invoice.objects.get_by_id(id)
            vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
            get_invoice_flow=Invoiceflowmodules.objects.filter(invoice_id=id).last()
            if (get_invoice_flow):
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=id,status=1).values_list('invoice_number',flat=True))
                get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=id).first()
                get_invoice_date=get_payment_term.payment_terms.payment_day
                get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
                all_invoice=', '.join(str(e) for e in invoice_number)
                formatted_datetime = get_invoice_flow.notification_at.strftime("%Y-%m-%d %H:%M:%S")
                parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
                get_notify_timestamp = datetime.timestamp(parsed_datetime)
                if (current_timestamp >= get_notify_timestamp):
                    # print('send notification')
                    # print(f'time {now},asdd,{get_invoice_flow.notification_at}')
                    get_users=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_invoice_flow.id,invoice_override=0)
                    for user in get_users:
                        recipient_user=User.objects.get(id=user.user)
                        sender = get_company_user
                        recipient=recipient_user
                        scheme=request.scheme
                        gethost=request.get_host()
                        url=f"{scheme}://{gethost}/invoice/vendorbasedinvoice"
                        notify.send(sender, recipient=recipient,data=url, verb='Action Required: Invoice Override Approval Needed', description=f'Assign personnel for Invoice approval for Invoice {all_invoice} for Vendor {vendor.vendor_name}  for services {invoice_detail.name_service}')
                    
                    #once confirm remove bloe code
                    #signatory primary secondary user create starts here
                    # if (get_invoice_flow.flowlevel_module.module.module.id == 5):
                    #     print('module 5')
                    #     if (invoice_detail.contracttype == 'original'):
                    #         contract=ContractMaster.objects.filter(id=invoice_detail.contractid ,status=1).first()
                    #         contract_data=contract
                    #         get_curreny=contract.currency
                    #     else:
                    #         contract=Amendment.objects.filter(id=invoice_detail.contractid ,status=1).first()
                    #         get_curreny=contract.amendment_currency
                    #         contract_data=ContractMaster.objects.filter(id=contract.service.id ,status=1).first()
                    #     if (contract_data.projects.signatory_type == '1'):
                    #         filter_company_signatory=SignatoriesSettings.objects.filter(company=request.company,signatory_type=contract_data.projects.signatory_type,currency_id=get_curreny.id,status=1)
                    #     else:
                    #         filter_company_signatory=SignatoriesSettings.objects.filter(company=request.company,project_id=contract_data.projects.projectname_id,signatory_type=contract_data.projects.signatory_type,currency_id=get_curreny.id,status=1)
                    #     remove_commas=get_payment_term.total_invoice_value
                    #     convert_val=int(remove_commas.replace(',',''))
                    #     check_data=filter_company_signatory.first()
                    #     if (check_data.invoice_type == '1'):
                    #         #with invoice amount
                    #         get_sig_data=filter_company_signatory.filter(Q(min_amount__lte=convert_val) & Q(max_amount__gte=convert_val)).first()
                    #     else:
                    #         #without invoice amount
                    #         get_sig_data=filter_company_signatory.first()
                    #     sig_users=SignatoriesUsers.objects.get_by_signatoryId(get_sig_data.id).first()
                    #     if (Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_invoice_flow.id,user=sig_users.user_id).exists()):
                    #         last_sig_users=SignatoriesUsers.objects.get_by_signatoryId(get_sig_data.id).last()
                    #         print('primary yes',last_sig_users.user)
                    #         if (Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_invoice_flow.id,user=last_sig_users.user_id).exists()):
                    #             print('secondary yes')
                    #             get_all_modules=ProjectFlowModules.objects.filter(project_id=get_invoice_flow.project_id,status=0)
                    #             for flow_module in get_all_modules:
                    #                 check_right=RoleRight.objects.filter(role_id=flow_module.role_id,right__right_name="Override Invoice Approval",status=1).first()
                    #                 if (check_right):
                    #                     module_users=ProjectFlowModuleUsers.objects.filter(ProjectFlowModules_id=flow_module.id,status=0)
                    #                     for user in module_users:
                    #                         if (Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_invoice_flow.id,user=user.user.user.id).exists()):
                    #                             print('exists')
                    #                         else:
                    #                             print('new')
                    #                             Invoiceflowmodulesusers.objects.createoverrideinvoiceusers(get_invoice_flow.project_id,user.user.id,get_invoice_flow.id,user.user.user.id,1)
                    #                         recipient_user=user.user.user
                    #                         print(check_right,'recipient_user',get_invoice_flow.project_id,user.user,get_invoice_flow.id,user.id,user.user.user.id)
                    #                         sender = get_company_user
                    #                         recipient=recipient_user
                    #                         scheme=request.scheme
                    #                         gethost=request.get_host()
                    #                         url=f"{scheme}://{gethost}/invoice/vendorbasedinvoice"
                    #                         notify.send(sender, recipient=recipient,data=url, verb='Indication Mail', description=f'Invoice {all_invoice} Still Pending')
                    #         else:
                    #             print('secondary No')
                    #             Invoiceflowmodulesusers.objects.createoverrideinvoiceusers(get_invoice_flow.project_id,None,get_invoice_flow.id,last_sig_users.user_id,0)
                    #     else:
                    #         print('primary no',sig_users)
                    #         Invoiceflowmodulesusers.objects.createoverrideinvoiceusers(get_invoice_flow.project_id,None,get_invoice_flow.id,sig_users.user_id,0)
                    #     #update notification time
                    #     calculate_time=add_invoice_time(now,get_company_invoice_time) 
                    #     # calculate_time= now+timedelta(hours=get_company_invoice_time.time_allotted) if get_company_invoice_time.time_unit == 0 else now+timedelta(days=get_company_invoice_time.time_allotted)
                    #     print('calculate_time',calculate_time)
                    #     Invoiceflowmodules.objects.filter(id=get_invoice_flow.id).update(notification_at=calculate_time)
                    #     #signatory orimary secondary user create ends here
                    # else:
                    #end here remove below code

                    # print('module other module')
                    flow_level=ProjectFlowlevel.objects.getprojectflowlevel_by_project_id(project_id=get_invoice_flow.project_id)
                    get_all_modules=ProjectFlowModules.objects.filter(project_id=get_invoice_flow.project_id,status=0).filter(projectflow_level_id__in=flow_level.values_list('id',flat=True))
                    for flow_module in get_all_modules:
                        check_right=RoleRight.objects.filter(role_id=flow_module.role_id,right__right_name="Override Invoice Approval",status=1).first()
                        if (check_right):
                            module_users=ProjectFlowModuleUsers.objects.filter(ProjectFlowModules_id=flow_module.id,status=0)
                            for user in module_users:
                                if (not Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_invoice_flow.id,user=user.user.user.id).exists()):
                                     Invoiceflowmodulesusers.objects.createoverrideinvoiceusers(get_invoice_flow.project_id,user.user.id,get_invoice_flow.id,user.user.user.id,1)
                               
                                recipient_user=user.user.user
                                # print(check_right,'recipient_user',get_invoice_flow.project_id,user.user,get_invoice_flow.id,user.id,user.user.user.id)
                                sender = get_company_user
                                recipient=recipient_user
                                scheme=request.scheme
                                gethost=request.get_host()
                                url=f"{scheme}://{gethost}/invoice/vendorbasedinvoice"
                                notify.send(sender, recipient=recipient,data=url, verb='Action Required: Invoice Override Approval Needed', description=f'Assign personnel for Invoice approval for Invoice {all_invoice} for Vendor {vendor.vendor_name}  for services {invoice_detail.name_service}')
                                # notify.send(sender, recipient=recipient,data=url, verb='Indication Mail', description=f'Invoice {all_invoice} Still Pending')
                    #update notification time 
                    calculate_time=add_invoice_time(now,get_company_invoice_time)
                    # print('calculate_time',calculate_time)
                    # for overdue i commented below line
                    # Invoiceflowmodules.objects.filter(id=get_invoice_flow.id).update(notification_at=calculate_time)
               
        return JsonResponse({'data':'success'})

import requests
class invoiceChecklist(View):
    def get(self, request,pk):
        url = 'https://ipapi.com/api/check?format=json'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            city = data['city']
            lat = data['latitude']
            lon = data['longitude']
        else:
            print('Error:', response.status_code)
        invoice_detail = Invoice.objects.filter_by_id(pk).get()
        document_list=getDocumentlist()
        invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,1)
        print(f"invoiceflow_modulestest {invoice_detail.invoice_status}")
        check_for_committe=InvoiceExceptional.objects.filter(invoice_id=pk,confirm_dispute=1).count()
        sign_data=check_user_sign(self.request.user)
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        costcode_format=getcostcode_format_type(self.request.company)
        try:
            costcode_data = getcostcode_component_path(invoice_detail.costcodevendor.order, self.request.company.id, invoice_detail.costcodevendor.costcode_main_id, get_remaining_level, costcode_format)
        except AttributeError:
            costcode_data = None  # or any other default value or error handling# or any other default value
        vendor_costcodes=getvendorcostcode_bycontracts(invoice_detail.contractid,request,invoice_detail.vendor_id , invoice_detail.contracttype)
        
        
        context={'invoice':invoice_detail,'pk':pk,'document_list':document_list,'check_for_committe':check_for_committe,'sign_data':sign_data,'costcode_data':costcode_data,'vendor_costcodes':vendor_costcodes,'order':invoice_detail.costcodevendor.order,'conform_costcode':invoice_detail.is_conform_costcode}
        try:
            if invoice_detail.wcc.id is not None :
                context["wcc_id"]=invoice_detail.wcc.id
        except :
            pass
        if invoiceflow_modules:
            get_role_id=invoiceflow_modules.flowlevel_module.role  
            print(f"get_role_id {get_role_id}")
            roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
            confirm_costcode_rights=getrights_by_name('Confirm Cost Code',get_role_id)
            context['get_role_id']=get_role_id
            context['roles_rights']=roles_rights
            context['confirm_costcode_rights']=confirm_costcode_rights
        else:
            if not invoice_detail.invoice_status == 4:
                if not invoice_detail.invoice_status == 6:
                    return redirect(reverse_lazy("invoice:vendorbasedinvoice"))

        return render(request, "checklist.html",context)
 

    def post(self, request, pk):
        if request.POST:
            print('r', request.POST)
            comments = request.POST.get('main_comments', None)
            submit_type = request.POST.get('submit_type')
            submit_name = request.POST.get('submit_name')

            current_date=datetime.now()
            messages = None  # Initialize messages variable
            if (submit_type == "3" or submit_type == "4"):
                get_exceptional = request.POST.getlist('exceptional')
                messages_json = request.POST.get('selected_messages')
                checklist=InvoiceExceptional.objects.filter(invoice_id=pk).last()
                if checklist:
                    return_status=int(checklist.return_status)+1
                else :
                    return_status=1
                exceptional_list = [InvoiceExceptional(invoice_id=pk, exceptional_type=i ,return_status=return_status) for i in get_exceptional]
                invoice_receipt = InvoiceExceptional.objects.bulk_create(exceptional_list)
                if submit_type=='3':
                    InvoiceExceptional.objects.filter(invoice_id=pk).update(query_status=1)
                if messages_json:
                    ok=InvoiceExceptional.objects.filter(invoice_id=pk)
                    InvoiceExceptional.objects.filter(invoice_id=pk,return_status=return_status).update(checked_messages=messages_json)


            invoice_number = list(
                InvoiceCostInvoice.objects.filter(invoice_id=pk, status=1).values_list('invoice_number', flat=True))
            all_invoice = ', '.join(str(e) for e in invoice_number)
            usercreate = request.user.roles_id
            create_user_log(request, all_invoice, 'Invoice', 'Create', f'Invoice Receipt has been {submit_name}', usercreate)
            document_list = getDocumentlist()
            for val in document_list:
                confirm_status = request.POST.get('confirmlist-' + str(val.get('data')))
                val_comments = request.POST.get('comment-' + str(val.get('data')))
                InvoiceFlowChecklist.objects.createinvoicechecklist(pk, val.get('data'), confirm_status, val_comments)
            invoice_number = list(
                InvoiceCostInvoice.objects.filter(invoice_id=pk, status=1).values_list('invoice_number', flat=True))
            all_invoice = ', '.join(str(e) for e in invoice_number)
            usercreate = request.user.roles_id
            create_user_log(request, all_invoice, 'Invoice', 'Create', f'Invoice Receipt has been {submit_name}',
                            usercreate)
            if (submit_type != "3"):
                InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_date=current_date )
                invoice_flow_func(pk, 1, request, comments, submit_type, submit_name)
            if (submit_type == '3'):
                invoice_return_flow(pk, 1, submit_type, comments, request, submit_name)
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))



# def invoice_flow_func(pk,module,request,comments,submit_type,submit_name):
#     current_date=datetime.now()
#     today = date.today()
#     date_today = today.strftime("%d-%b-%Y")
#     invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,module)
#     bank_usercheck=0
#     try:
#         check_for_user=Settings.objects.get(company_id=request.company.id)
#         bank_usercheck=check_for_user.bank_user
#     except:
#         bank_usercheck=0
#     print(f'bank_usercheck {bank_usercheck}')
#     if (invoiceflow_modules):
#         Invoiceflowmodules.objects.updateinvoiceflowmodules(invoiceflow_modules.id)
#         Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,submit_type,comments)
#     invoice_detail = Invoice.objects.get_by_id(pk)
#     invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
#     all_invoice=', '.join(str(e) for e in invoice_number)
#     vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
#     vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
#     allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
#     main_url="invoice/invoicelist"
#     main_verb='Invoice '+submit_name
#     main_description=f' Invoice for Payment Approval'
#     content=f'Invoice {submit_name} by {request.user.name} on {date_today} for {invoice_detail.name_service} '
#     now = datetime.now()
#     get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
#     get_invoice_date=get_payment_term.payment_terms.payment_day
#     get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
#     calculate_time=add_invoice_time(now,get_company_invoice_time)
#     if (submit_type == '3' or submit_type == '4'):
#         main_url=f"invoice/invoiceview/{pk}" 
#         print(f'main_url {main_url}')
        
#         Invoice.objects.filter(id=pk).update(invoice_status=4) if submit_type == '3' else Invoice.objects.filter(id=pk).update(invoice_status=5) 
#         InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=4,approval_date=current_date) if submit_type == '3' else InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=5,approval_date=current_date)
#         # notify_invoice_flow(request,vendor_data,main_url,main_verb,main_description) 
#         if(submit_type == '3'):
#             Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=invoiceflow_modules.id,user=request.user.id).update(returned=1,returned_date=current_date)


#         if module == 1 or module == 2:
#             for notifications in allVendors:
#                 invoive_return_mail(request,notifications,vendor,submit_name,invoice_detail,comments,all_invoice,submit_type)
#                 notify_invoice_flow(request,notifications,main_url,main_verb,content)
#     else:
#         print('1 0r 2')
#         if (invoice_detail.contracttype == 'original'):
#             contract=ContractMaster.objects.get_by_id(invoice_detail.contractid).first()
#             contract_data=contract
#         else:
#             contract=Amendment.objects.get_by_id(invoice_detail.contractid ,1).first()
#             contract_data=contract.service
#         if True:
#             if (module == None):
#                 invoiceflow_modules=Invoiceflowmodules.objects.get_by_module_id(pk,1,6)
#             print(f'invoiceflow_modules {invoiceflow_modules}')
#             getnextlevel=ProjectFlowModules.objects.getnextactivelevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.flowlevel_module_id)
#             print(f'getnextlevel {getnextlevel},bank_usercheck')
#             if(getnextlevel):
#                 print(f'next module id {getnextlevel.module.module.id}')
#                 getmodules=ProcessModule.objects.getmodule_byid(getnextlevel.module_id)
#                 projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnextlevel.id,invoiceflow_modules.flowlevel_id)
#                 if (getnextlevel.module.module.id == 7 and module == 6):
#                     if bank_usercheck == 1:
#                         PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).update(verified_status=0)
#                             #create invoiceflowmodule bank user
#                         invoiceflow=Invoiceflowmodules.objects.createbankinvoiceflowmodules(contract_data.projects.id,request.company,invoiceflow_modules.flowlevel_id,None,pk,None,now,calculate_time)
#                         invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('id',flat=True)
#                         get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost).exclude(payable_amount=0)
#                         print(f'get_payment_instruction {get_payment_instruction}')
#                         for instruction in get_payment_instruction:
#                             get_bank_uers=CompanyBankUser.objects.filter(companybank_id=instruction.companybank_id)
#                             for bank_user in get_bank_uers:
#                                 Invoiceflowmodulesusers.objects.creatbankinvoiceusers(contract_data.projects.id,invoiceflow.id,bank_user.user_id,instruction.id,bank_user.id,1)
#                                 verb=f'Approved Payment Instructions'
#                                 description=f'Payment Instruction No {instruction.pi_number} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been approved for payment by {request.user.name} {request.user.lastname}'
#                                 urls="invoice/vendorbasedinvoice"
#                                 notify_invoice_flow(request,bank_user.user,urls,verb,description)
#                                 bank_user_approvalmail(request,bank_user.user,instruction.pi_number,vendor,invoice_detail,all_invoice,comments)
#                                 print(f'getnextlevel.module.module.id == 7 and module == 6 ')
#                     else:
#                         invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,invoiceflow_modules.flowlevel_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
#                 else:
#                     invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,invoiceflow_modules.flowlevel_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
#                 if (getnextlevel.module.module.id == 5 ):
#                     signatory_func(pk,invoice_detail.project.projectname.id,request,getnextlevel,invoiceflow,invoice_detail,all_invoice,vendor,1)
#                 elif(getnextlevel.module.module.id == 7 and module == 6):
#                     if bank_usercheck == 0:
#                         for user in projectflow_modules_users:
#                             projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
#                             Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
#                             recipientuser = User.objects.get(id=projectusers.user_id)
#                             get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
#                             print('get_users2',get_users)
#                             approved_users=User.objects.filter(id__in=get_users)
#                             urls=getInvoiceModule(getnextlevel.module.module.id,pk)
#                             module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
#                 else:
#                     for user in projectflow_modules_users:
#                         projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
#                         # command 
#                         Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
#                         recipientuser = User.objects.get(id=projectusers.user_id)
#                         if getnextlevel.module.module.id == 4 or module == 3 and getnextlevel.module.module.id == 3:
#                             get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4]).values_list('user',flat=True)
#                         elif getnextlevel.module.module.id == 5:
#                             get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
#                         elif getnextlevel.module.module.id == 6 or getnextlevel.module.module.id == 5 and module == 5:
#                             get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
#                         else:
#                             get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
#                         print('get_users2',get_users)
#                         approved_users=User.objects.filter(id__in=get_users)
#                         urls=getInvoiceModule(getnextlevel.module.module.id,pk)
#                         module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
#             else:
#                 print(2)
#                 if (module == None):
#                     invoiceflow_modules=Invoiceflowmodules.objects.get_by_module_id(pk,1,6)
#                 getnexprocesstlevel=ProjectFlowModules.objects.getnxtprocessactlevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.project_id,invoiceflow_modules.flowlevel.level_id)
#                 if (getnexprocesstlevel):
#                     print(f'next process module id {getnexprocesstlevel.module.module.id}')
#                     getmodules=ProcessModule.objects.getmodule_byid(getnexprocesstlevel.module_id)
#                     print(3,'next process module')
#                     projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnexprocesstlevel.id,getnexprocesstlevel.projectflow_level_id)
#                     if (getnexprocesstlevel.module.module.id == 7 and module == 6):
#                         if bank_usercheck == 1:
#                             PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).update(verified_status=0)
#                                 #create invoiceflowmodule bank user
#                             invoiceflow=Invoiceflowmodules.objects.createbankinvoiceflowmodules(contract_data.projects.id,request.company,invoiceflow_modules.flowlevel_id,None,pk,None,now,calculate_time)
#                             invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('id',flat=True)
#                             get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost).exclude(payable_amount=0)
#                             print(f'get_payment_instruction {get_payment_instruction}')
#                             for instruction in get_payment_instruction:
#                                 get_bank_uers=CompanyBankUser.objects.filter(companybank_id=instruction.companybank_id)
#                                 for bank_user in get_bank_uers:
#                                     Invoiceflowmodulesusers.objects.creatbankinvoiceusers(contract_data.projects.id,invoiceflow.id,bank_user.user_id,instruction.id,bank_user.id,1)
#                                     print(f'getnextlevel.module.module.id == 7 and module == 6 ')
#                                     verb=f'Approved Payment Instructions'
#                                     description=f'Instruction No {instruction.pi_number} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been approved for payment by {request.user.name} {request.user.lastname}'
#                                     urls="invoice/vendorbasedinvoice"
#                                     notify_invoice_flow(request,bank_user.user,urls,verb,description)
#                                     bank_user_approvalmail(request,bank_user.user,instruction.pi_number,vendor,invoice_detail,all_invoice,comments)
#                         else:
#                             invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
#                     else:
#                         invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
#                     if (getnexprocesstlevel.module.module.id == 5):
#                         signatory_func(pk,invoice_detail.project.projectname.id,request,getnexprocesstlevel,invoiceflow,invoice_detail,all_invoice,vendor,1)
#                     elif(getnexprocesstlevel.module.module.id == 7 and module == 6):
#                         print(f'v invoiceflow {invoiceflow}')
#                         if bank_usercheck == 0:
#                             for user in projectflow_modules_users:
#                                 projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
#                                 Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
#                                 recipientuser = User.objects.get(id=projectusers.user_id)
#                                 get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
#                                 approved_users=User.objects.filter(id__in=get_users)
#                                 urls=getInvoiceModule(getnexprocesstlevel.module.module.id,pk)
#                                 module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnexprocesstlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
                                
#                     else:
#                         for user in projectflow_modules_users:
#                             projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
#                             Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
#                             recipientuser = User.objects.get(id=projectusers.user_id)
#                             if getnexprocesstlevel.module.module.id == 4 or module == 3 and getnexprocesstlevel.module.module.id == 3:
#                                 get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3]).values_list('user',flat=True)
#                             elif getnexprocesstlevel.module.module.id == 5:
#                                 get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
#                             elif getnexprocesstlevel.module.module.id == 6 or getnexprocesstlevel.module.module.id == 5 and module == 5:
#                                 get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
#                             else:
#                                 get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
#                             approved_users=User.objects.filter(id__in=get_users)
#                             urls=getInvoiceModule(getnexprocesstlevel.module.module.id,pk)
#                             module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnexprocesstlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
#                 else:
#                     module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,7,all_invoice)
#     return

def module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,next_module,all_invoice=None,recipientuser=None,urls=None,approved_users=None,comments=None,inv_approval_notification=None , payment_count=None):
    if module:
        if module == 1 or next_module == 1 or next_module == 2:
            verb="Invoice for Approval"
            user_data=f''
            if approved_users:
                for name in approved_users:
                    if name:
                        user_data+=f'{name.name} {name.lastname}, '
            description=f'Invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been reviewed by {user_data} and passed for your approval'
            notify_invoice_flow(request,recipientuser,urls,verb,description)
            invoive_approval_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,invoiceflow_modules)

        if module == 2 and next_module == 3 or module == 1 and next_module == 3:
            Invoice.objects.filter(id=pk).update(approval_status=1)
            verb="Invoice for Payment Approval"
            # print('invoiceflow_modules 2',invoiceflow_modules.flowlevel_module.role.role_name)
            description=f'Invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been approved for payment processing'
            if inv_approval_notification == 1 :
                notify_invoice_flow(request,recipientuser,urls,verb,description)
                invoive_approval_mail_step2(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,invoiceflow_modules)

        elif module == 3 and next_module == 3:
            user_data=f''
            if approved_users:
                for name in approved_users:
                    if name:
                        user_data+=f'{name.name} {name.lastname}, '
            print(f'approved_users {approved_users}')
            verb="Invoice for Payment Approval"
            # print('invoiceflow_modules 3',invoiceflow_modules.flowlevel_module.role.role_name)
            description=f'Invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service}  has been reviewed by {user_data} and passed for payment processing'
            notify_invoice_flow(request,recipientuser,urls,verb,description)            
            tax_confirmation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users)

        elif module < 4 and next_module == 4:

            # Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).values_list('pi_number',flat=True)
            # pi_number=",".join(map(str,Payment))
            verb="Generate Payment Instructions for payment processing"
            description=f'Invoice no {all_invoice} for Vendor {vendor.vendor_name}  for service {invoice_detail.name_service}.'
            if inv_approval_notification == 1 :
                notify_invoice_flow(request,recipientuser,urls,verb,description)
                payment_generation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users)

        elif module == 4 and next_module == 4:
            user_data=f''
            if approved_users:
                for name in approved_users:
                    if name:
                        user_data+=f'{name.name} {name.lastname}, '
            verb="Generation of Payment Instructions for payment processing"
            description=f'Invoice no {all_invoice} for Vendor {vendor.vendor_name}  for service {invoice_detail.name_service} has been reviewed by {user_data} for payment processing. Please generate payment instructions.'
            notify_invoice_flow(request,recipientuser,urls,verb,description)
            payment_generation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users)

        elif next_module == 5:
            # print('invoiceflow_modules 5',invoiceflow_modules.flowlevel_module.role.role_name)
            Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).values_list('pi_number',flat=True)
            pi_number=",".join(map(str,Payment))
            verb="Instructions for Payment Approval"
            description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been  sent for approval for payment processing'
            # notify_invoice_flow(request,recipientuser,urls,verb,description)
            # payment_confirmation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,pi_number)

        #payment confirmation user approve the invoice.no notification for payment receipt.
        elif next_module == 6:
            print('invoiceflow_modules 6',approved_users)
            Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).last()
            # pi_number=",".join(map(str,Payment.pi_number))
            pi_number=str(Payment.pi_number)
            verb="Approved Payment Instructions"
            description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been approved for payment'
            notify_invoice_flow(request,recipientuser,urls,verb,description)
            invoice_payment_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,comments,pi_number)


        # elif module == None:
        #     Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).values_list('pi_number',flat=True)
        #     pi_number=",".join(map(str,Payment))
        #     verb="Payment Instruction Received"
        #     description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service}  has been received by {request.user.name} {request.user.lastname}. Verification code - XXXXXX by Bank User' 

        elif module == 7:
            
            paid_status=find_fully_paid(pk)
            # print('invoiceflow_modules 7',invoiceflow_modules.flowlevel_module.role)
            Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).values_list('pi_number',flat=True)
            pi_number=",".join(map(str,Payment))
            
            if paid_status:
                verb="Payment on Invoices"
                description=f'Invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service}  has been paid and closed on {date_today}'

            else :
                verb="Partial Payment on Invoices"
                description=f'Invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service}  has been partially paid on {date_today}'
            # description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service}  has been paid and closed on {date_today}'
            allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            for notification_user in allVendors:
                notify_invoice_flow(request,notification_user,"invoice/invoicelist",verb,description)
                payment_receipt_vendor(request,notification_user,invoice_detail,all_invoice,pk,payment_count)
            get_invoice_flow=Invoiceflowmodules.objects.getinvoiceflowmodules_by_invoice_id(pk).values_list('id',flat=True)
            get_all_users=list(Invoiceflowmodulesusers.objects.getusers_by_invoiceflow_ids(get_invoice_flow).values_list('user',flat=True))
            remove_duplicate_ids=list(set(get_all_users))
            for inv_user in remove_duplicate_ids:
                get_user=User.objects.get(id=inv_user)
                notify_invoice_flow(request,get_user,"invoice/paidinvoicelist",verb,description)
                payment_receipt_confirmation(request,get_user,vendor,invoice_detail,all_invoice,pk ,payment_count)
            
    

        # check after notification given remove module != 6 condition
        # if (module != 6):
        #     if (module != 7 and module != None):
        #         Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).values_list('pi_number',flat=True)
        #         pi_number=",".join(map(str,Payment))
        #         verb="Approved Payment Instructions"
        #         description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been approved for payment'
        #         notify_invoice_flow(request,recipientuser,urls,verb,description)

    return

def notify_invoice_flow(request,userdata,url,verb,description):
    sender = request.user
    recipient=userdata
    scheme=request.scheme
    gethost=request.get_host()
    url=f"{scheme}://{gethost}/{url}"
    notify.send(sender, recipient=recipient,data=url, verb=verb, description=description)
    return

def signatory_func(pk,project_id,request,next_module,invoiceflow,invoice_detail,all_invoice,vendor,user_type,payment_count=None,paymentinstruct=None,notification_count=None, cost_id=None ):

    urls=getInvoiceModule(5,pk,payment_count)
    # contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    get_project_signatories=SignatoriesSettings.objects.filter_by_project(project_id,request.company.id,2,1)
    if (get_project_signatories.count() > 0):
        filtered_data=get_project_signatories
    else:
        filtered_data=SignatoriesSettings.objects.filter_by_project(None,request.company.id,1,1)
    
    for costinvoice in contractcostinvoice:
        if costinvoice.approval_status != 3 :
            data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=2)
            if (data.count() > 0):
                sign_data=data.first()
            else:
                get_value=costinvoice.invoice_total_amount
                split_val=get_value.split(' ')
                convert_val=float(split_val[1].replace(',',''))
                sign_data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=1).filter(Q(min_amount__lte=convert_val) & Q(max_amount__gte=convert_val)).first()
            sign_users=SignatoriesUsers.objects.get_by_signatoryId(sign_data.id)
            if sign_users:
                for user_data in sign_users:
                    project_user, created = ProjectUser.objects.update_or_create(
                                    project_id=invoice_detail.project_id,
                                    user_id=user_data.user_id,
                                    defaults={'company': request.company,'status':True},
                                    )
                    UserRights.objects.filter(user_id=user_data.user_id,module__module_name='Projects').update(view=1)
            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=next_module.project_id,status=1,
            Invoiceflowmodules__invoice_id=pk,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
            approved_users=User.objects.filter(id__in=get_users)
            Payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,payment_count=payment_count ,invoicecost_id=costinvoice.id).values_list('pi_number',flat=True)
            pi_number=",".join(map(str,Payment))
            
            if approved_users:
                verb="Instructions for Payment Approval"
                description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been  sent for approval for payment processing'
            if cost_id:
                pay_instruction_data=PaymentInstruction.objects.get_by_invcostid(cost_id.id,paymentinstruct)
            else :
                pay_instruction_data=PaymentInstruction.objects.get_by_invcostid(costinvoice.id,paymentinstruct)
            for user in sign_users:
                Invoiceflowmodulesusers.objects.createinvflowsignuser(next_module.project_id,invoiceflow.id,user.user.id,pay_instruction_data.id)
                if notification_count == 1:
                    notify_invoice_flow(request,user.user,urls,verb,description)   
                    payment_confirmation_mail(request,user.user,vendor,invoice_detail,all_invoice,approved_users,pi_number)           
            
            

    return

class invoiceApprovalProcess(View):
    def get(self, request,pk):
        document_list=getDocumentlist()
        contractid=Invoice.objects.get_by_id(pk)
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(contractid.contractid)
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        if (invoicedetail == None):
            invoicedetail=""
        invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,2)
        check_for_committe=InvoiceExceptional.objects.filter(invoice_id=pk,confirm_dispute=1).count()
        settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True,acceptance_status=2)

        # dispute_user=DisputedInvoiceTrack.objects.filter(invoice_id=pk,stage=1,status=True)
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        costcode_format=getcostcode_format_type(self.request.company)
        costcode_data=getcostcode_component_path(contractid.costcodevendor.order,self.request.company.id,contractid.costcodevendor.costcode_main_id,get_remaining_level,costcode_format)
        # vendor_costcodes=CostCodeVendor.objects.get_vendor_company(contractid.vendor_id,1,self.request.company)
        vendor_costcodes=getvendorcostcode_bycontracts(contractid.contractid,request,contractid.vendor_id , contractid.contracttype)

        sign_data=check_user_sign(self.request.user)
        
        context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,'check_for_committe':check_for_committe,'sign_data':sign_data,'vendor_costcodes':vendor_costcodes,'costcode_data':costcode_data,'order':contractid.costcodevendor.order,'settlement_invoice':settlement_invoice,'check_settlement':settlement_invoice.count(),'invoice_details':contractid}
        try:
            if contractid.wcc.id is not None :
                context["wcc_id"]=contractid.wcc.id
        except :
            pass
  
        if invoiceflow_modules:
            get_role_id=invoiceflow_modules.flowlevel_module.role
            roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
            confirm_costcode_rights=getrights_by_name('Confirm Cost Code',get_role_id)
            context['roles_rights']=roles_rights
            context['get_role_id']=get_role_id
            context['confirm_costcode_rights']=confirm_costcode_rights
        else:
            if not contractid.invoice_status == 4: 
                if not contractid.invoice_status == 6:
                    return redirect(reverse_lazy("invoice:vendorbasedinvoice"))

        return render(request, "invoiceapproval.html",context)

        
    def post(self, request,pk):
        if request.POST:
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            messages_json = request.POST.get('selected_messages')
            messages = json.loads(messages_json)
            if (submit_type == "3" or submit_type == "4" or submit_type == "5"):
                checklist=InvoiceExceptional.objects.filter(invoice_id=pk).last()
                if checklist:
                    return_status=int(checklist.return_status)+1
                else :
                    return_status=1
                get_exceptional=request.POST.getlist('exceptional')
               
                exceptional_list=[InvoiceExceptional(invoice_id=pk,exceptional_type=i,return_status=return_status) for i in get_exceptional]
                InvoiceExceptional.objects.bulk_create(exceptional_list)
                if messages:
                    ok=InvoiceExceptional.objects.filter(invoice_id=pk)
                    print("jisdhids",ok)
                    InvoiceExceptional.objects.filter(invoice_id=pk,return_status=return_status).update(checked_messages=messages_json)
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
                all_invoice=', '.join(str(e) for e in invoice_number)
                usercreate=request.user.roles_id
                create_user_log(request,all_invoice,'Invoice','Create',f'Invoice approval has been {submit_name}',usercreate)
            print(f'submit_type {submit_type}')
            if submit_type == "3":
                invoice_return_flow(pk,2,submit_type,comments,request,submit_name)
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
                all_invoice=', '.join(str(e) for e in invoice_number)
                usercreate=request.user.roles_id
                create_user_log(request,all_invoice,'Invoice','Create',f'Invoice approval has been {submit_name}',usercreate)
            # if(submit_type == '5'):
            #     current_date=datetime.now()
            #     today = date.today()
            #     date_today = today.strftime("%d-%b-%Y")
            #     invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,2)
            #     if (invoiceflow_modules):
            #         Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,submit_type,comments)
            #     invoice_detail = Invoice.objects.get_by_id(pk)
            #     invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
            #     all_invoice=', '.join(str(e) for e in invoice_number)
            #     Invoice.objects.filter(id=pk).update(invoice_status=6)
            #     InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=6,approval_date=current_date)
            #     utc_timezone = pytz.utc
            #     utc_time = datetime.now(utc_timezone)
            #     time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
            #     get_inv=Invoice.objects.filter(id=pk).first()
            #     data_to_create = [
            #         {'user': request.user, 'invoice_id': get_inv.id,'created_at':current_date,'reason':comments,'stage':1},
            #         {'invoice_id': get_inv.id, 'stage': 2},
            #         {'invoice_id': get_inv.id, 'stage': 3},
            #         {'invoice_id': get_inv.id, 'stage': 4},
            #         {'invoice_id': get_inv.id, 'stage': 5},
            #         # Add more dictionaries with different parameter values
            #     ]
            #     # DisputedInvoiceTrack.objects.create(user=request.user,invoice_id=pk,created_at=datetime.now(),stage=2)
            #     # Use the bulk_create method to insert the records into the database
            #     DisputedInvoiceTrack.objects.bulk_create([DisputedInvoiceTrack(**data) for data in data_to_create])
            #     # DisputedInvoiceTrack.objects.create(user=request.user,invoice_id=get_inv.id,created_at=current_date,reason=comments)
            #     get_url=f'invoice/invoicequeryhistory/{get_inv.id}'
            #     content =f'Invoice {all_invoice} has been {submit_name} by {request.user.name} on {date_today} for {invoice_detail.name_service} '
            #     vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
            #     allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            #     main_verb='Invoice '+submit_name
            #     AddNewDisputedQuery.objects.reason_for_dispute(get_inv.id,comments,request.user,time_stamp,vendor.id)
            #     for vendors in allVendors:
            #             disputed_invoice_mail(request,vendors,submit_name,invoice_detail,comments,all_invoice,vendor)
            #             notify_invoice_flow(request,vendors,get_url,main_verb,content)
            #     return redirect(reverse_lazy("invoice:listdisputeinvoices"))
            else:
                invoice_flow_func(pk,2,request,comments,submit_type,submit_name)
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            return render(request, "invoiceapproval.html",context)


class taxConfirmation(View):
    def get(self, request,pk):
        document_list=getDocumentlist()
        contractid=Invoice.objects.get_by_id(pk)
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(contractid.contractid).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        if (invoicedetail == None):
            invoicedetail=""
        context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail}
        return render(request, "taxconfirmation.html",context)
    def post(self, request,pk):
        if request.POST:
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            return render(request, "taxconfirmation.html",context)

class exchangeRateConfirmation(View):
    def get(self, request,pk):
        document_list=getDocumentlist()     
        contractid=Invoice.objects.get_by_id(pk)
        general=Settings.objects.get_company(request.company).first()
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(contractid.contractid ).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
            get_submit_type=list(vendorinvoice.values_list('exchange_rate',flat=True))
            currency_name=contract.currency
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
            get_submit_type=list(vendorinvoice.values_list('exchange_rate',flat=True))
            currency_name=contract.service.currency
        submit_type = 1
        if '2' in get_submit_type:
            submit_type=2
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        invoice_currency=list(contractcostinvoice.values_list('currency_id',flat=True))
        basecurrency_check=0
        if currency_name and invoice_currency:
            currency_update=[1 if i == currency_name.id else 2 for i in invoice_currency]
            if 2 in currency_update:
                basecurrency_check=1
        print(f'contractcostinvoice {contractcostinvoice}, currency_update {currency_update} basecurrency_check {basecurrency_check}' )
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        if invoicedetail is None:
            invoicedetail = ""

        invoiceflow_modules = Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk, 3)

        if invoiceflow_modules is not None and hasattr(invoiceflow_modules, 'flowlevel_module'):
            get_role_id = invoiceflow_modules.flowlevel_module.role
        else:
            # Handle the case where invoiceflow_modules is None or does not have flowlevel_module
            get_role_id = None  # Or handle this scenario accordingly, e.g., set get_role_id to a default value or raise an exception

        roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
        sign_data=check_user_sign(self.request.user)
        settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True)
        invoice_percentage=settlement_invoice.first()
        if get_role_id is not None:
            confirm_costcode_rights = getrights_by_name('Confirm Cost Code', get_role_id)
        else:
            # Handle the case where get_role_id is None
            confirm_costcode_rights = None  # Or handle this case according to your requirements

        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        costcode_format=getcostcode_format_type(self.request.company)
        costcode_data=getcostcode_component_path(contractid.costcodevendor.order,self.request.company.id,contractid.costcodevendor.costcode_main_id,get_remaining_level,costcode_format)
        # vendor_costcodes=CostCodeVendor.objects.get_vendor_company(contractid.vendor_id,1,self.request.company)
        vendor_costcodes=getvendorcostcode_bycontracts(contractid.contractid,request,contractid.vendor_id , contractid.contracttype)
        
        context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,'general':general,'get_role_id':get_role_id,'roles_rights':roles_rights,'submit_type':submit_type,'contract':currency_name,'invoiceflow_modules':invoiceflow_modules,'sign_data':sign_data,'basecurrency_check':basecurrency_check,'confirm_costcode_rights':confirm_costcode_rights,'vendor_costcodes':vendor_costcodes,'costcode_data':costcode_data,'Invoice_details':contractid,'order':contractid.costcodevendor.order,'invoice_percentage':invoice_percentage,'check_settlement':settlement_invoice.count(),'settlement_invoice':settlement_invoice }
        try:
            if contractid.wcc.id is not None :
                context["wcc_id"]=contractid.wcc.id
        except :
            pass
        return render(request, "exchangerate.html",context)
       
    def post(self, request,pk):
        if request.POST:
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            invoice_flow_func(pk,3,request,comments,submit_type,submit_name)
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            usercreate=request.user.roles_id
            create_user_log(request,all_invoice,'Invoice','Create',f'Tax Confirmation has been {submit_name}',usercreate)
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            return render(request, "exchangerate.html",context)

class generatepaymentInstruction(View):
    def get(self, request,pk):
        try:
            document_list=getDocumentlist()
            contractid=Invoice.objects.get_by_id(pk)
            get_credit=CreditNoteInvoice.objects.filter(invoice_id=contractid.id,status=1)
            payment_split = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
            # get_credit=CreditNoteInvoice.objects.filter(credit__contract_id=contractid.contractid,status=1,credit__usage_status__in=[1,2],credit__approval_status=4)
            print(f'get_credit {get_credit.count()}')
            bankdetails=CompanyBank.objects.get_by_company(request.company)
            if (contractid.contracttype == 'original'):
                contract=ContractMaster.objects.get_by_id(contractid.contractid).first()
                vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
            else:
                contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
                vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
            contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
            invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
            instuctionscount=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).count()
            payment_generate_count=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).last()
            payment_generate_count_value=1
            if payment_generate_count == None:
                payment_generate_count_value=1
            else  :
                payment_generate_count_value=payment_generate_count.payment_count
            payment_count=1
            if instuctionscount > 0:
                pi_count=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True,percentage_confirm=True).last()
                if pi_count:
                    payment_count+=pi_count.payment_count
            payment_details=PaymentInstruction.objects.get_by_payment(pk).filter(payment_count=payment_count)
            print(f'payment_details {payment_details}')
            check_creditnote=list(payment_details.values_list('invoice_type',flat=True))
            print(f'check_creditnote {check_creditnote}')
            credit_value=False
            if 2 in check_creditnote:
                credit_value=True
            credit_mapped_data=list(CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True).values_list('credit_note_id',flat=True).distinct())
            get_credit_notes=CreditNote.objects.filter(id__in=credit_mapped_data)
            numbers_credit=[]
            for i in get_credit_notes:
                credit_data=list(CreditNoteContractInvoice.objects.filter(credit_id=i.id).values_list('credit_note_no',flat=True))
                credit_data=', '.join(str(e) for e in credit_data)
                numbers_credit.append(credit_data)
            all_company_bank = CompanyBank.objects.get_by_company(request.company)
            if (invoicedetail == None):
                invoicedetail=""
            invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,4)
            get_role_id=invoiceflow_modules.flowlevel_module.role
            roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
            contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
            get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
            try:
                costcode_format=getcostcode_format_type(self.request.company)
                costcode_data=getcostcode_component_path(contractid.costcodevendor.order,self.request.company.id,contractid.costcodevendor.costcode_main_id,get_remaining_level,costcode_format)
                vendor_costcodes=getvendorcostcode_bycontracts(contractid.contractid,request,contractid.vendor_id ,contractid.contracttype)
            except:
                costcode_format=costcode_data=vendor_costcodes=None
            # vendor_costcodes=CostCodeVendor.objects.get_vendor_company(contractid.vendor_id,1,self.request.company)
            

            try:
                projectname=contractid.project.projectname.id
            except:
                projectname=None
            get_project_signatories=SignatoriesSettings.objects.filter_by_project(projectname,request.company.id,2,1)
            len_sign=[]
            if (get_project_signatories.count() > 0):
                filtered_data=get_project_signatories
            else:
                filtered_data=SignatoriesSettings.objects.filter_by_project(None,request.company.id,1,1)
            for costinvoice in contractcostinvoice:
                data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=2)

                if (data.count() > 0):
                    sign_data=data.count()
                    len_sign.append(sign_data)
                else:
                    get_value=costinvoice.invoice_total_amount
                    split_val=get_value.split(' ')
                    convert_val=float(split_val[1].replace(',',''))
                    sign_data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=1).filter(Q(min_amount__lte=convert_val) & Q(max_amount__gte=convert_val)).count()
                    len_sign.append(sign_data)
            print(f'len_sign {len_sign}')
            sign_data=check_user_sign(self.request.user)
            settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True,acceptance_status=2)
            context={'contractcostinvoice':contractcostinvoice,'bankdetails':bankdetails,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,'payment_details':list(payment_details),'all_company_bank':all_company_bank,'bankdetails':bankdetails,'get_role_id':get_role_id,'roles_rights':roles_rights,'credit_count':get_credit.count(),'credit_value':credit_value,'contractid':contractid,'len_sign':len_sign,'instuctionscount':instuctionscount,'sign_data':sign_data,'costcode_data':costcode_data,'vendor_costcodes':vendor_costcodes,'order':contractid.costcodevendor.order,'invoice_details':contractid,'settlement_invoice':settlement_invoice,'check_settlement':settlement_invoice.count(),'payment_count':payment_count , 'payment_split_count':len(payment_split) , 'payment_generate_count':payment_generate_count_value}


            return render(request, "generatepayment.html",context)
        except Exception as e:
            print(f'error {e}')
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
    
       
    def post(self, request,pk):
        invoice_detail=Invoice.objects.get_by_id(pk)
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk).values_list('invoice_number',flat=True))
        # credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
        invoice_number=', '.join(str(e) for e in invoice_number)
        credit_mapped_data=list(CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True).values_list('credit_note_id',flat=True).distinct())
        get_credit_notes=CreditNote.objects.filter(id__in=credit_mapped_data)
        numbers_credit=[]
        for i in get_credit_notes:
            credit_data=list(CreditNoteContractInvoice.objects.filter(credit_id=i.id).values_list('credit_note_no',flat=True))
            credit_data=', '.join(str(e) for e in credit_data)
            numbers_credit.append(credit_data)
        creditnote_number= ', '.join(str(e) for e in numbers_credit)
        print('ooo',numbers_credit)
        all_company_bank = CompanyBank
        postvalues=request.POST
        comments=request.POST.get('main_comments',None)
        submit_type=request.POST.get('submit_type')
        submit_name=request.POST.get('submit_name')
        payment_id=request.POST.getlist('payment_id')
        print(f'payment_id {payment_id}')
        # PaymentInstruction.objects.filter(id__in=payment_id,invoicecost__invoice_id=pk,status=True).update(percentage_confirm=True)
        payment_count=request.POST.get('payment_count')
        print(f'payment_count {payment_count}')
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
        all_invoice=', '.join(str(e) for e in invoice_number)
        usercreate=request.user.roles_id
        create_user_log(request,all_invoice,'Invoice','Create',f'Payment Generation has been {submit_name}',usercreate)
        
        if postvalues.get('confirm_button') == 'confirm':
            PaymentInstruction.objects.filter(id__in=payment_id,invoicecost__invoice_id=pk,is_editable=True).update(is_editable=False,verified_status=1)
            get_payment_instructions=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,is_editable=False,verified_status=1).values_list('payable_amount',flat=True))
            payment_details=PaymentInstruction.objects.get_by_payment(pk)
            check_creditnote=list(payment_details.values_list('invoice_type',flat=True))
            credit_value=False
            scheme=request.scheme
            gethost=request.get_host()
            url=f"{scheme}://{gethost}/dashboard/dashboard"
            today = date.today()
            date_today = today.strftime("%d-%b-%Y")
            if 2 in check_creditnote:
                credit_value=True
            get_submission_date=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).first()
            if credit_value:
                for user in allVendors:
                    notify.send(request.user, recipient=user,data=url, verb='Credit Note applied to Invoice', description=f'Credit Note {creditnote_number} Applied to Invoice Number {invoice_number}')
                    credit_applied_mail(request,user,all_invoice,creditnote_number,date_today,get_submission_date)
            net_payable=sum([float(i) for i in get_payment_instructions])
            if net_payable == 0:
                current_date=datetime.now()
                InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=3,payment_status=2,payment_date=current_date,approval_date=current_date)
                Invoice.objects.filter(id=pk).update(invoice_status=3)
                invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,4)
                print(f'invoiceflow_modules {invoiceflow_modules}')
                if (invoiceflow_modules):
                    Invoiceflowmodules.objects.updateinvoiceflowmodules(invoiceflow_modules.id)
                    Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,submit_type,comments)
                invoice_detail = Invoice.objects.get_by_id(pk)
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
                all_invoice=', '.join(str(e) for e in invoice_number)
                vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
                invoicecost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
                for i in invoicecost:
                    if InvoiceCostInvoice.objects.filter(id=i.id,payment_account=1):
                        InvoiceCostInvoice.objects.filter(id=i.id).update(payment_status=2,payment_date=datetime.now())
                module_based_data(pk,request,7,vendor,invoice_detail,date_today,invoiceflow_modules,7,all_invoice,None,None,None,None,None,payment_count)
            else:
                get_payment_instructions=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).values_list('payable_amount',flat=True))
                paid_split=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,payable_amount=0).values_list('invoicecost_id',flat=True))
                InvoiceCostInvoice.objects.filter(id__in=paid_split).update(approval_status=3,paid_inbetween=True)
                invoicecost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
                for i in invoicecost:
                    if InvoiceCostInvoice.objects.filter(id=i.id,payment_account=1):
                        InvoiceCostInvoice.objects.filter(id=i.id).update(payment_status=2,payment_date=datetime.now())
                if request.POST:
                    invoice_flow_func(pk,4,request,comments,submit_type,submit_name,payment_count,payment_id)
                    return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
                
        
        return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        # else:
        #     return render(request, "generatepayment.html",context)
        

class GetPaymentInstruction(View):
    def post(self,request,pk):
        data={}
        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')  # Convert the image to RGB mode
            image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        pi_id = request.POST.get('payment_instruction')
        paycount = request.POST.get('payment_count')

        generate_payment = PaymentInstruction.objects.get_by_id(pi_id)
        generate_payment.pi_file.delete()
        generaterated_pi_number = generate_payment.pi_number
        val = generate_payment.payable_amount
        number_to_word = num2words(val)
        if float(val).is_integer():
            number_to_word = f'{number_to_word} {generate_payment.invoicecost.currency.currency_unit}'
        else:
            integer_part = f'{val}'.split('.')[0]
            fractional_part = f'{val}'.split('.')[1]
            word_representation_integral = num2words(integer_part)
            word_representation_fractional  = num2words(fractional_part)
            number_to_word = f'{word_representation_integral} {generate_payment.invoicecost.currency.currency_unit} and {word_representation_fractional} {generate_payment.invoicecost.currency.fractional_unit}'
        numto_word = f'{number_to_word.title()}'
        vendor_name = f'{generate_payment.invoicecost.vendor.vendor_name}'
       
        if generate_payment.companybank:
            if generate_payment.companybank.instructorfirstname == '':
                get_users=CompanyBankUser.objects.filter(companybank=generate_payment.companybank).select_related('user').values(user_name=F('user__name'),user_lastname=F('user__lastname'),user_designation_role=F('user__designation_role'))
                user_full_name=[f"{i.get('user_name')} {i.get('user_lastname')}" for i in get_users] 
                contact_personnel=', '.join(user_full_name)
                contact_personnel_title='user'
            else:
                contact_personnel=generate_payment.companybank.instructortitle+' '+generate_payment.companybank.instructorfirstname+' '+generate_payment.companybank.instructorlastname 
                contact_personnel_title=generate_payment.companybank.instructortitle
            if generate_payment.companybank.bank_name:
                bank_name=generate_payment.companybank.bank_name.bank_name
                bank_address=generate_payment.companybank.bank_name.otherdetails
                account_no=generate_payment.companybank.account_number.accountno
            data={'bank_address':bank_address,'account_no':account_no,'bank_name':bank_name,'contact_personnel':contact_personnel,'contact_personnel_title':contact_personnel_title,'paycount':paycount}



        elif generate_payment.masterbank:
            if generate_payment.masterbank:
                bank_name=generate_payment.masterbank.bank_name
                bank_address=generate_payment.masterbank.otherdetails
                account_no=fetbankaccountnumber(generate_payment.masterbank.id)
            data={'bank_address':bank_address,'account_no':account_no,'bank_name':bank_name,'paycount':paycount}
       
        updated_at_date = generate_payment.updated_at.date()
        day = updated_at_date.day
        suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        formatted_date = f"{day}{suffix} {updated_at_date.strftime('%b')}, {updated_at_date.year}"          
        data.update({'name':request.company,'invoice_cost':generate_payment.invoicecost,'pi_number':generaterated_pi_number,'updated_at':formatted_date,'numto_word':numto_word,'vendor_name':vendor_name,'vendor_bank_name':generate_payment.invoicecost.invoice_bank.bankname,'vendor_bank_acno':generate_payment.invoicecost.invoice_bank.accountnumber,'invoice_no':generate_payment.invoicecost.invoice_number,'payment_percentage':generate_payment.payment_percentage,'payable_amount':f'{generate_payment.invoicecost.currency.currency_symbol} {val:,}'})
        html_output = render_to_string('payment_instruction_pdf.html', data,request)
        # Define the WeasyPrint CSS object with the style
        pdf_style = payment_instruction_pdfstyle(encoded_image)
        css = CSS(string=pdf_style)
        # Generate the PDF with WeasyPrint
        pdf_buffer = BytesIO()
        HTML(string=html_output).write_pdf(pdf_buffer, stylesheets=[css])
        pdf_file = File(pdf_buffer)
        generate_payment.pi_file.save('generated_pi.pdf', pdf_file)
        pdf_file_url = generate_payment.pi_file.url
        return JsonResponse({'success': True,'pdf_file_url':pdf_file_url})
    
class signatoryUserForm(View):
    
    def get(self, request,pk,pay_id):
        document_list=getDocumentlist()

        contractid=Invoice.objects.get_by_id(pk)
        payment_split = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(contractid.contractid ).first()
            project=contract.projects
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            project=contract.service.projects
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        if (invoicedetail == None):
            invoicedetail=""
        invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,5)
        invoiceflowapproval_modules=Invoiceflowmodules.objects.filter_by_module_id(pk,0,5)
        get_specific_pay_ids=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_byuser(request.user.id,invoiceflow_modules.project_id)
        get_specific_pay_ids=get_specific_pay_ids.filter(Invoiceflowmodules_id__in=list(invoiceflowapproval_modules.values_list('id',flat=True)))
        mapped_creditnote=CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True)
        get_used_creditnotes=list(mapped_creditnote.values_list('credit_note_id',flat=True).distinct())
        get_role_id=invoiceflow_modules.flowlevel_module.role
        roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
        filing=find_signatories_user(pk,project.projectname_id, request , request.user.email)

        payment_details=PaymentInstruction.objects.get_by_payment(pk).filter(id__in=get_specific_pay_ids.values_list('payment_instruction_id'),invoicecost__in=filing )
        if pay_id:
            payment_details=payment_details.filter(payment_count=pay_id)        
        sign_data=check_user_sign(self.request.user)
        settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True,acceptance_status=2)
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        costcode_format=getcostcode_format_type(self.request.company)
        costcode_data=getcostcode_component_path(contractid.costcodevendor.order,self.request.company.id,contractid.costcodevendor.costcode_main_id,get_remaining_level,costcode_format)
        # vendor_costcodes=CostCodeVendor.objects.get_vendor_company(contractid.vendor_id,1,self.request.company)
        vendor_costcodes=getvendorcostcode_bycontracts(contractid.contractid,request,contractid.vendor_id , contractid.contracttype)

        confirm_costcode_rights=getrights_by_name('Confirm Cost Code',get_role_id)
        

        context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,'get_role_id':get_role_id,'roles_rights':roles_rights,'payment_details':payment_details,'sign_data':sign_data,'check_creditnote':mapped_creditnote.count(),'get_used_creditnotes':get_used_creditnotes,'settlement_invoice':settlement_invoice,'check_settlement':settlement_invoice.count(),'confirm_costcode_rights':confirm_costcode_rights,'vendor_costcodes':vendor_costcodes,'costcode_data':costcode_data,'order':contractid.costcodevendor.order,'invoice_details':contractid , 'pay_id':pay_id,'payment_split_count':len(payment_split)}
        try:
            if contractid.wcc.id is not None :
                context["wcc_id"]=contractid.wcc.id
        except :
            pass
        return render(request, "signatoryuser.html",context)
       

    def post(self, request,pk,pay_id):
        current_date=datetime.now()
        if request.POST:
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            invoice_cost_invoice_id = request.POST.getlist('invoice_cost_id')
            payment_id=request.POST.getlist('payment_id')
            pay_id=request.POST.get('pay_id')
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            usercreate=request.user.roles_id
            create_user_log(request,all_invoice,'Invoice','Create',f'Payment Approval has been {submit_name}',usercreate)
            invoiceflow_modules_id=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,5)
            invoiceflow_muliplemodules=list(Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoiceids(pk,5).filter(payment_instruct__in=payment_id).values_list('id',flat=True))

            Invoiceflowmodulesusers.objects.updatemultipleinvoiceflowusers(invoiceflow_muliplemodules,request.user.id,current_date,1,comments)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=invoiceflow_muliplemodules,user=request.user.id).update(invoice_costinvoice = invoice_cost_invoice_id)

            pay_app_ids=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=invoiceflow_muliplemodules).values_list('payment_instruction_id',flat=True)
            remove_dup_ids=list(set(pay_app_ids))
            
            invoiceflow=Invoiceflowmodules.objects.filter_by_module_id(pk,1,5).filter(payment_instruct__payment_count=pay_id)
            checkingflow=list(Invoiceflowmodules.objects.filter_by_module_id(pk,0,5).filter(payment_instruct__payment_count=pay_id).values_list('id',flat=True))
            updatestatus=list(Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=5,payment_instruct__payment_count=pay_id).values_list('id',flat=True))

            check_data=Invoiceflowmodulesusers.objects.get_payins_ids(invoiceflow_muliplemodules,remove_dup_ids).values('payment_instruction_id').distinct().count()
            # check_data=Invoiceflowmodulesusers.objects.get_payins_ids(invoiceflow_modules_id.id,remove_dup_ids).count()
            print(f'pay_app_ids {pay_app_ids}, remove_dup_ids {remove_dup_ids}')
            print(f'check_data {check_data}, remove_dup_ids {len(remove_dup_ids)}')
            invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoiceids(pk,5)
            
            
            payment_instrcut_id=[]
            invoiceflowpayment_id=Invoiceflowmodules.objects.filter(invoice_id=pk,status=1,module_id=5,payment_instruct__payment_count=pay_id)
            if invoiceflowpayment_id :
                payment_instrcut_id=list(set(invoiceflowpayment_id.values_list('payment_instruct_id',flat=True)))

            flow_module_id=list(invoiceflowpayment_id.values_list('id',flat=True))
            flow_module_id=flow_module_id+invoiceflow_muliplemodules
            current_date=datetime.now()
            module =5
            
            if set(invoiceflow_muliplemodules) == set(updatestatus) or set(invoiceflow_muliplemodules)== set(checkingflow):
                payment_id=payment_id+payment_instrcut_id
                # Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_module_id,user=request.user.id).update(status=submit_type)
                Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=updatestatus ,user=request.user.id).update(user_status=1 ,created_at=current_date)
                    
                invoice_flow_func(pk,5,request,comments,submit_type,submit_name,pay_id,payment_id)
                return redirect(reverse_lazy("invoice:vendorbasedinvoice"))

            else :
                if payment_id and module == None or module > 4:
                    with_instructions=invoiceflow_modules.filter(payment_instruct__in=payment_id)
                    if (invoiceflow_modules.count() > 0):
                        flow_modules=list(invoiceflow_modules.values_list('id',flat=True))
                        try:
                            with_instructionsmodule=list(with_instructions.values_list('id',flat=True))
                        except:
                            with_instructionsmodule=[]
                        if module == None:
                            print(11)
                            invoice_singleId=Invoiceflowmodules.objects.filter(invoice_id=pk,status=1,module_id=6,payment_instruct__payment_count=pay_id,payment_instruct__in=payment_id).last()
                        elif payment_id and module > 4:
                            print(12)
                            invoice_singleId=Invoiceflowmodules.objects.filter(invoice_id=pk,status=0,module_id=module,payment_instruct__in=payment_id).first()
                        else:
                            print(13)
                            invoice_singleId=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,module)
                        if module and  module < 5:
                            print(1)
                            Invoiceflowmodules.objects.filter(id__in=list(invoiceflow_modules.values_list('id',flat=True))).update(status=1)
                            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_modules,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date)
                            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=updatestatus,user=request.user.id).update(user_status=1)
                        else:
                            print(2)
                            Invoiceflowmodules.objects.filter(id__in=list(with_instructions.values_list('id',flat=True))).update(status=1)
                            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=with_instructionsmodule,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date)
                            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=updatestatus,user=request.user.id).update(user_status=1)
                        if (submit_type == '3' or submit_type == '4'): 
                            Invoice.objects.filter(id=pk).update(invoice_status=4) if submit_type == '3' else Invoice.objects.filter(id=pk).update(invoice_status=5) 
                            InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=4,approval_date=current_date) if submit_type == '3' else InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=5,approval_date=current_date)
                            if(submit_type == '3'):
                                Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_modules,user=request.user.id).update(returned=1,returned_date=current_date)
                return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
            # else :
            #     if (len(remove_dup_ids) == check_data): 
            #         payment_id=payment_id+payment_instrcut_id
            #         print('(((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))')
            #         print('(((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))')
            #         print('move to next module')
            #         print(f'payment_instrcut_id {payment_instrcut_id}')
            #         print(f'payment_id {payment_id}')
            #         Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_module_id,user=request.user.id).update(status=submit_type)
            #         Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=updatestatus ,user=request.user.id).update(user_status=1)
                    
            #         invoice_flow_func(pk,5,request,comments,submit_type,submit_name,pay_id,payment_id)
            #     return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            return render(request, "signatoryuser.html",context)

class accountPayableOffical(View):

    def get(self, request,pk,pay_id):
        try:
            document_list=getDocumentlist()
            mapped_creditnote=CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True)
            get_used_creditnotes=list(mapped_creditnote.values_list('credit_note_id',flat=True).distinct())
            contractid=Invoice.objects.get_by_id(pk)
            payment_split = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
            if (contractid.contracttype == 'original'):
                contract=ContractMaster.objects.get_by_id(contractid.contractid ).first()
                vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)

            else:
                contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
                vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
            contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
            invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
            if (invoicedetail == None):
                invoicedetail=""
            invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,6)
            get_role_id=invoiceflow_modules.flowlevel_module.role
            roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
            payment_details=PaymentInstruction.objects.get_by_payment(pk).filter(payment_count=pay_id)
            settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True,acceptance_status=2)
            sign_data=check_user_sign(self.request.user)

            get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
            costcode_format=getcostcode_format_type(self.request.company)
            costcode_data=getcostcode_component_path(contractid.costcodevendor.order,self.request.company.id,contractid.costcodevendor.costcode_main_id,get_remaining_level,costcode_format)
            # vendor_costcodes=CostCodeVendor.objects.get_vendor_company(contractid.vendor_id,1,self.request.company)
            vendor_costcodes=getvendorcostcode_bycontracts(contractid.contractid,request,contractid.vendor_id , contractid.contracttype)

            confirm_costcode_rights=getrights_by_name('Confirm Cost Code',get_role_id)




            print(f'sign_data {sign_data}')
            context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,'get_role_id':get_role_id,'roles_rights':roles_rights,'payment_details':payment_details,'sign_data':sign_data,'check_creditnote':mapped_creditnote.count(),'get_used_creditnotes':get_used_creditnotes,'settlement_invoice':settlement_invoice,'check_settlement':settlement_invoice.count(),'confirm_costcode_rights':confirm_costcode_rights,'costcode_data':costcode_data,'vendor_costcodes':vendor_costcodes,'order':contractid.costcodevendor.order,'invoice_details':contractid ,'pay_id':pay_id, 'payment_split_count':len(payment_split)}
            try:
                if contractid.wcc.id is not None :
                    context["wcc_id"]=contractid.wcc.id
                print(" accountpayable wcc_id ",contractid.wcc.id)
            except :
                pass
            return render(request, "accountpayable.html",context)
        except:
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
    # def get(self, request,pk):
    #     contractid=Invoice.objects.get_by_id(pk)
    #     if (contractid.contracttype == 'original'):
    #         contract=ContractMaster.objects.get_by_id(contractid.contractid ).first()
    #         contract_data=contract
    #         vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
    #     else:
    #         contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
    #         contract_data=contract
    #         vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
    #     contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
    #     invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
    #     if (invoicedetail == None):
    #         invoicedetail=""
    #     invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,6)
    #     get_role_id=invoiceflow_modules.flowlevel_module.role
    #     roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)  
    #     payment_details=PaymentInstruction.objects.get_by_payment(pk)
    #     context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'invoicedetail':invoicedetail,'invoice':contractid,'get_role_id':get_role_id,'roles_rights':roles_rights,'payment_details':payment_details}
    #     return render(request, "accountpayable.html",context)
    def post(self, request,pk,pay_id):
        if request.POST:
            invoice_detail=Invoice.objects.get_by_id(pk)
            if (invoice_detail.contracttype == 'original'):
                contract=ContractMaster.objects.get_by_id(invoice_detail.contractid).first()
                contract_data=contract
            else:
                contract=Amendment.objects.get_by_id(invoice_detail.contractid ,1).first()
                contract_data=contract
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            payment_id=request.POST.getlist('payment_id')

            paycount_id=request.POST.get('pay_id')
            invoice_flow_func(pk,6,request,comments,submit_type,submit_name,pay_id,payment_id)
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            usercreate=request.user.roles_id
            create_user_log(request,all_invoice,'Invoice','Create',f'Payment Confirmation has been {submit_name}',usercreate)
            # nextlevel_users(pk,request,6)
            return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            return render(request, "accountpayable.html",context)


def nextlevel_users(pk,request,module_id):
    invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,module_id)
    Invoiceflowmodules.objects.updateinvoiceflowmodules(invoiceflow_modules.id)
    Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id)
    getnextlevel=ProjectFlowModules.objects.getnextactivelevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.flowlevel_module_id)
    if(getnextlevel):
        getmodules=ProcessModule.objects.getmodule_byid(getnextlevel.module_id)
        projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnextlevel.id,invoiceflow_modules.flowlevel_id)
        scheme=request.scheme
        gethost=request.get_host()  
        invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,invoiceflow_modules.flowlevel_id,getnextlevel.id,pk,getmodules.module_id)
        sender = User.objects.get(id=request.user.id)
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
        all_invoice=', '.join(str(e) for e in invoice_number)
        sender = User.objects.get(id=request.user.id)
        urls=f"{scheme}://{gethost}/invoice/vendorbasedinvoice"
        for user in projectflow_modules_users:
            projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
            Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,user.id,invoiceflow.id,user.user_id,projectusers.user_id)
            recipientuser = User.objects.get(id=projectusers.user_id)
            notify.send(sender, recipient=recipientuser,data=urls, verb='Invoice Raised', description=f'Invoice Raised for Invoice No: {all_invoice}')
    else:
        print('next process')
        getnexprocesstlevel=ProjectFlowModules.objects.getnxtprocessactlevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.project_id)
        if (getnexprocesstlevel):
            getmodules=ProcessModule.objects.getmodule_byid(getnexprocesstlevel.module_id)
            projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnexprocesstlevel.id,getnexprocesstlevel.projectflow_level_id)
            scheme=request.scheme
            gethost=request.get_host()  
            invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id)
            sender = User.objects.get(id=request.user.id)
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            sender = User.objects.get(id=request.user.id)
            urls=f"{scheme}://{gethost}/invoice/vendorbasedinvoice"
            for user in projectflow_modules_users:
                projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,user.id,invoiceflow.id,user.user_id,projectusers.user_id)
                recipientuser = User.objects.get(id=projectusers.user_id)
                notify.send(sender, recipient=recipientuser,data=urls, verb='Invoice Raised', description=f'Invoice Raised for Invoice No: {all_invoice}')
        else:
            print('process fully completed')

def paymentInstructionData(request,pk):
    invoicedata=Invoice.objects.get_by_id(pk)
    if (invoicedata.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=invoicedata.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(contract_id=contract.id,company=request.company,status=1)
    else:
        contract=Amendment.objects.filter(id=invoicedata.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(amendment_id=contract.id,company=request.company,status=1)
    contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    invoicedetail=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
    if (invoicedetail == None):
        invoicedetail=""
    payment_details=PaymentInstruction.objects.get_by_payment(pk)
    context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'invoicedetail':invoicedetail,'invoice':invoicedata,'payment_details':payment_details}
    return render(request,'paymentinstructiondata.html',context)

def getallInvoiceFiles(request):
    file_type=request.GET.get('file_type')
    invoice_id=request.GET.get('invoice_id')
    if (file_type == 'document'):
        contractid=Invoice.objects.get_by_id_status(invoice_id,1)
        if (contractid.contracttype == 'original'):
            contract_file=VendorContractPriceTable.objects.filter(contract_id=contractid.contractid  ,status=1 ,file_type=1 ).values()
            price_file=VendorContractPriceTable.objects.filter(contract_id=contractid.contractid  ,status=1 ,file_type=2 ).values()
            file_data=[{'support_file':list(contract_file)},{'support_file':list(price_file)}]
        else:
            contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
            amendment_file=VendorContractPriceTable.objects.filter(amendment_addendum_id=contract.id,status=1 ).values()
            contract_file=VendorContractPriceTable.objects.filter(contract_id=contract.service.id  ,status=1 ).values()
            file_data=[{'support_file':list(contract_file)},{'support_file':list(amendment_file)}]
        getfiles=list(InvoiceFileUpload.objects.filter(invoice_id=invoice_id,status=1).exclude(support=1).values())
        file_data.extend(getfiles)
        data={'files':file_data,'supporting_doc':True}
        return JsonResponse(data,safe=False)
    else:
        getfiles=InvoiceFileUpload.objects.filter(invoice_id=invoice_id,support=1,status=1).values()
        data={'files':list(getfiles),'supporting_doc':False}
        return JsonResponse(data)

class invoiceCoverSheet(View):
    def get(self,request,pk):
        
        context = self.get_context_data(request,pk)
        return render(request, "coversheet.html",context)
    
    def get_context_data(self, request, pk):
        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')  # Convert the image to RGB mode
            image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            imageurl = None
        invoice_data = Invoice.objects.get_by_id(pk)
        invoice_exclusive_type=InvoiceExclusive.objects.filter(invoice_id=pk,status=1)
        Check_for_settlement=SettlementInvoice.objects.filter(invoice_id=pk,status=True,acceptance_status=2)
        invoice_number = InvoiceCostInvoice.objects.filter(invoice_id=pk).values_list('invoice_number',flat=True)
        invoice_cost = InvoiceCostInformation.objects.filter(invoice_id=pk, status=1).first()
        split_invoices = InvoiceCostInvoice.objects.filter(invoice_id=pk, status=1)
        get_date=PastExchangeRate.objects.filter(invoice__invoice_id=pk).last()
        if get_date != None:
            get_date=get_date
        else:
            get_date=InvoiceCostInvoice.objects.filter(invoice_id=pk, status=1).last()
        try:
            if invoice_data.contracttype == "original":
                contract=ContractMaster.objects.filter(id=invoice_data.contractid ,status=1).first()
                vendorpayment = VendorPaymentTerms.objects.filter(vendor_id=invoice_data.vendor.id, contract_id=invoice_data.contractid, company=request.company, status=1)
                vendorinvoice = VendorInvoiceSplit.objects.filter(contract_id=invoice_data.contractid, company=request.company, status=1)
                exchange_rate = vendorinvoice.values_list('exchange_rate',flat=True).first()
                contract_number = vendorinvoice.values_list('contract__reference_number',flat=True).first()
                project=contract.projects
                
            else:
                amendment_data=Amendment.objects.filter(id=invoice_data.contractid ,status=1).first()
                contract=ContractMaster.objects.filter(id=amendment_data.service_id,status=1).first()
                vendorpayment = VendorPaymentTerms.objects.filter(vendor_id=invoice_data.vendor.id, amendment_id=invoice_data.contractid, company=request.company, status=1)
                vendorinvoice = VendorInvoiceSplit.objects.filter(amendment_id=invoice_data.contractid, company=request.company, status=1)
                exchange_rate = vendorinvoice.values_list('exchange_rate',flat=True).first()
                contract_number = vendorinvoice.values_list('amendment__amendment_reference_number',flat=True).first()
                project=amendment_data.service.projects
            if (project.flow_level == "discipline"):
                get_levels=ProjectFlowlevel.objects.get_by_level_main(contract.projectdisciplinetype_id,'discipline',request.company,project.id)
            elif (project.flow_level == "clusters"):
                get_levels=ProjectFlowlevel.objects.get_by_level_main(contract.projectdiscipline.cluster_id,'clusters',request.company,project.id)
            else:
                if invoice_data.well_not_applicable == "id":
                    get_levels=ProjectFlowlevel.objects.get_by_level_main(invoice_data.well_id,'well',request.company,project.id)
                else:
                    get_levels=ProjectFlowlevel.objects.get_by_wellbasedlevel_main(contract.projectdisciplinetype_id,'well',request.company,project.id)
            projectflow_modules=ProjectFlowModules.objects.getallactiveflow_level_mul_id(get_levels.values_list('id',flat=True)).filter(module__module_id=2).last()
            approvedcheckuser=0
            if projectflow_modules:
                approvedcheckuser=Invoiceflowmodules.objects.filter(invoice_id=pk,flowlevel_module__module__module_id=2,flowlevel_module=projectflow_modules.id,status=1).count()
                print(f'approvedcheckuser {approvedcheckuser}')
                approvedcheckflow=list(Invoiceflowmodules.objects.filter(invoice_id=pk,flowlevel_module__module__module_id=2,flowlevel_module=projectflow_modules.id,status=1).values_list('id',flat=True).distinct())
                approveduserSignatures=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=approvedcheckflow , status__in =[1,2]).count()
                
            approved_users=duplicate_users=Invoiceflowmodulesusers.objects.getapprovedusersinvoice(pk).exclude(bank_user_status=1).filter(Invoiceflowmodules__module_id__lte=3 , status__in=[1,2])
            try:
                exact_val=0
                duplicate_user=[i['id'] for i in approved_users.values('user','id') if exact_val != (exact_val := i['user'])]
                duplicate_users=approved_users.filter(id__in=duplicate_user, status__in=[1,2])
            except:
                duplicate_users=Invoiceflowmodulesusers.objects.getapprovedusersinvoice(pk).exclude(bank_user_status=1).filter(status__in=[1,2])
            # print(f'dupliacte_user {duplicate_user}')
            print(f'approved_users {approved_users}')
            approved_invoiceapproval=approved_users.filter(Invoiceflowmodules__flowlevel_module__module__module_id=2)
            tax_users=approved_users.filter(Invoiceflowmodules__flowlevel_module__module__module_id=3)
            print(f'tax_users {tax_users}')
            print(f'approved_invoiceapproval {approved_invoiceapproval}')
            print(f'approved_invoiceapproval {approved_invoiceapproval}')
            mapped_creditnote=CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True)
            get_used_creditnotes=list(mapped_creditnote.values_list('credit_note_id',flat=True).distinct())
            deduction=OtherDeductions.objects.filter(invoice_id=pk,status=True)
            additions=OtherAdditions.objects.filter(invoice_id=pk,status=True)
            split_module_value=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
            invoice_details = InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).first()
            try:
                returned_data = Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id=pk,returned=1).last()
            except:
                returned_data = None
            # print(returned_data.status,"RETURNED DATA")
            return {'invoice': invoice_data,'contract': contract,'invoice_details':invoice_details ,'returned_data':returned_data ,'invoice_cost': invoice_cost, 'split_invoices': split_invoices,'split_count': split_invoices.count()+1, 'vendorpayment': vendorpayment, 'main_invoices': vendorinvoice,'imageurl':imageurl, 'basecurreccy': vendorinvoice.values_list('currency__currency_symbol', flat=True).first(), 'pk': pk,'invoice_number':",".join(map(str,invoice_number)),'contract_number':contract_number,'vendor_name':invoice_data.vendor.vendor_name,'exchange_rate':exchange_rate,'get_date':get_date,'approved_users':approved_users,'Check_for_settlement':Check_for_settlement.count(),'settlement_percentage':Check_for_settlement,'check_creditnote':mapped_creditnote.count(),'get_used_creditnotes':get_used_creditnotes,'contract':contract,'invoice_exclusive_type':invoice_exclusive_type.count(),'exclusive_values':invoice_exclusive_type,'deduction_count':deduction.count(),'deduction':deduction.last(),"addition":additions.last(),"additions_count":additions.count(),'approved_invoiceapproval':approved_invoiceapproval,'tax_users':tax_users,'tax_user_count':tax_users.count(),'approvedcheckuser':approvedcheckuser,'duplicate_users':duplicate_users , "split_module_value":split_module_value , "split_module_count":len(split_module_value),'approveduserSignatures':approveduserSignatures}
        except ValueError:
            return {'invoice': invoice_data, 'pk': pk}
        else:
            return {}
        
    def post(self, request,pk):
        return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
    
class CoversheetPDFView(View):
    template_name = 'coversheet_pdf.html'
    def get(self,request,pk):
        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')  # Convert the image to RGB mode
            image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        print(f"encoded_image {encoded_image}")
        coversheet_view = invoiceCoverSheet()
        context = coversheet_view.get_context_data(request,pk)
        output_coversheet = render_to_string(self.template_name,context,request)
        approved_users=Invoiceflowmodulesusers.objects.getapprovedusersinvoice(pk).exclude(bank_user_status=1).values_list('user',flat=True)
        coversheet_style = coversheet_pdfstyle(encoded_image,approved_users)
        css = CSS(string=coversheet_style)
        
    # Generate the PDF with WeasyPrint
        pdf_buffer = BytesIO()
        HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])

    # Create the Django response object with the PDF content
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')

    # Set the Content-Disposition header to force a download
        response['Content-Disposition'] = 'attachment; filename="CoverSheet PDF.pdf"'

    # Return the response
        return response
    
class GetPaymentInstructionView(View):
    def post(self, request, *args, **kwargs):
        invoice_id = request.POST.get('pk')
        payment_count = request.POST.get('payment_count') or 1
        invoice_data=Invoice.objects.get_by_id(invoice_id)
        payment_split = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_data.id,status=True).values_list('payment_count',flat=True).distinct())
        get_current_exclusives=list(InvoiceExclusive.objects.filter(invoice_id=invoice_id,status=1).values_list('exclusive_id',flat=True))
        CreditNoteInvoice.objects.filter(credit__contract_id=invoice_data.contractid,status=1,credit__usage_status__in=[1,2],credit__credit_status=2)
        contractid=Invoice.objects.get_by_id(invoice_id)
        get_credit=CreditNoteInvoice.objects.filter(invoice_id=contractid.id,status=1)
            # get_credit=CreditNoteInvoice.objects.filter(credit__contract_id=contractid.co
        # get_credit=CreditNoteInvoice.objects.filter(credit__contract_id=invoice_data.contractid,status=1,credit__usage_status__in=[1],credit__credit_status=2,invoice__invoice_status=3,credit__approval_status=4)
        bal_invoices=[]
        for balance in get_credit:
            get_remaining_exclusives=list(InvoiceExclusive.objects.filter(invoice_id=balance.invoice_id,status=1).values_list('exclusive_id',flat=True))
            if sorted(get_remaining_exclusives) == sorted(get_current_exclusives):
                bal_invoices.append(balance.credit_id)
        current_credit_notes=CreditNoteInvoice.objects.filter(invoice_id=invoice_id,credit__contract_id=invoice_data.contractid,status=1,credit__usage_status__in=[1],credit__credit_status=2,credit__approval_status=4).exclude(invoice__invoice_status=3)
        total_credit_notes=bal_invoices+list(current_credit_notes.values_list('credit_id',flat=True))
        list_creditnote=CreditNote.objects.filter(id__in=total_credit_notes,credit_status=2,usage_status=1,
        check_for_pending=True,approval_status=4)
        if (contractid.contracttype != 'original'):
            current_credit_notes=CreditNoteInvoice.objects.filter(invoice_id=invoice_id,credit__amendment_id=invoice_data.contractid)
            list_creditnote=CreditNote.objects.filter(id__in=total_credit_notes)
        list_invoices=[]
        split_invoices = InvoiceCostInvoice.objects.filter(invoice_id=invoice_id, status=1)
  
        for i in list_creditnote:
            get_invoice_id=CreditNoteInvoice.objects.filter(credit_id=i.id,credit__approval_status=4).last()
            invoice_cost=CreditNoteContractInvoice.objects.filter(credit_id=i.id,status=1).values('id','credit_note_no','date')
            list_invoices.append({'credit_id':i.id,'credit_number':list(invoice_cost),'invoice_value':get_invoice_id.invoice_id})        
        credit_cost=list(CreditNoteContractInvoice.objects.filter(credit_id__in=list(get_credit.values_list('credit_id',flat=True))).values('id','credit_note_no','date'))
        get_credit_note=CreditNoteContractInvoice.objects.filter(credit_id__in=list(get_credit.values_list('credit_id',flat=True)))
        adjusted_creditnote=list(CreditNoteMappingBase.objects.filter(invoice_id=invoice_id,status=True,company_id=request.company.id).values_list('credit_note_id',flat=True).distinct())
        selected_users=CreditNote.objects.filter(id__in=adjusted_creditnote,credit_status=2,approval_status=4)
        print(f'selected_users {selected_users}')
        for k in adjusted_creditnote:
            common_credit=CreditNote.objects.filter(id=k,credit_status=2,approval_status=4)
            
            if int(k) not in total_credit_notes:
                for k in common_credit:
                    get_invoice_id=CreditNoteInvoice.objects.filter(credit_id=k.id,credit__approval_status=4).last()
                    invoice_cost=CreditNoteContractInvoice.objects.filter(credit_id=k.id,status=1).values('id','credit_note_no','date')
                    list_invoices.append({'credit_id':k.id,'credit_number':list(invoice_cost),'invoice_value':get_invoice_id.invoice_id})
        
        if PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,status=True,payment_count=payment_count).exists():
            editable_true = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,is_editable=True,status=True,payment_count=payment_count)
            check_creditnote=list(editable_true.values_list('invoice_type',flat=True)) 
            if 2 in check_creditnote:
                credit_value=True
            else:
                credit_value=False
            if editable_true.exists():
                payment_instruction_template =  render_to_string('components/paymentinstruction.html',{'data':True,'payment_instruction':editable_true,'invoice_id':int(invoice_id),'create':False,'update':False,'credit_value':credit_value,'credit_count':len(bal_invoices)+current_credit_notes.count(),'list_creditnote':list_invoices,'selected_users':list(selected_users.values_list('id',flat=True)),"split_invoices":split_invoices , "payment_split":len(payment_split)},request,)
                return JsonResponse({'success': True,'payment_instruction_template':payment_instruction_template})
            else:
                # exclude data if sum of  payment_percentage == 100 
                filtered_data = []
                invoice_cost = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id).values('invoicecost').annotate(total_percentage=Sum('payment_percentage')).filter(total_percentage__lt=100).values_list('invoicecost',flat=True)
                for i in invoice_cost:
                    filtered_data.append(PaymentInstruction.objects.filter(invoicecost_id=i).values_list('id',flat=True).first())
                data = PaymentInstruction.objects.filter(id__in=filtered_data,status=True)
                check_creditnote=list(data.values_list('invoice_type',flat=True))
                if 2 in check_creditnote:
                    credit_value=True
                else:
                    credit_value=False
                payment_instruction_template =  render_to_string('components/paymentinstruction.html',{'data':True,'payment_instruction':data,'invoice_id':invoice_id,'edit':True,'create':True,'update':True,'credit_value':credit_value,'credit_count':len(bal_invoices)+current_credit_notes.count(),'list_creditnote':list_invoices,'selected_users':list(selected_users.values_list('id',flat=True)), "payment_split":len(payment_split)},request)
                return JsonResponse({'success': True,'payment_instruction_template':payment_instruction_template})
        else:
            editable_true = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,is_editable=False,status=True)
            check_creditnote=list(editable_true.values_list('invoice_type',flat=True))
            print(f'editable_true {editable_true}, check_creditnote {check_creditnote}')
            if 2 in check_creditnote:
                credit_value=True
                data=True
            else:
                credit_value=False
                data=False
            # get_credit=CreditNoteInvoice.objects.filter(credit__contract_id=invoice_data.contractid,status=1,credit__usage_status=1,credit__credit_status=2)
            invoice_split = InvoiceCostInvoice.objects.filter(invoice_id=invoice_id)
            payment_instruction_template =  render_to_string('components/paymentinstruction.html',{'data':data,'payment_instruction':invoice_split,'invoice_id':int(invoice_id),'credit_count':len(bal_invoices)+current_credit_notes.count(),'get_credit_note':get_credit_note,'list_creditnote':list_invoices,'credit_value':credit_value,'list_creditnote':list_invoices,'selected_users':list(selected_users.values_list('id',flat=True)),'if_paymentinstruct':True,"payment_split":len(payment_split)},request)
            return JsonResponse({'success': False,'payment_instruction_template':payment_instruction_template,'create':True,'update':False})
    

class PostPaymentInstructionView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        # print('data',data)
        check_type=data.get('check_type')
        payment_count = data.get('payment_count')
        print(f'check_type {check_type}')
        if check_type == '1':
            invoice_id = data.get('invoice_id')
            is_create = data.get('create')
            is_update = data.get('update')
            print(f'payment_count {payment_count}')
            print(f'is_create {is_create}, is_update {is_update} ')
            if is_create == 'True' and is_update == 'True':
                filtered_data = []
                invoice_cost = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,payment_count=payment_count).values('invoicecost').annotate(total_percentage=Sum('payment_percentage')).filter(total_percentage__lt=100).values_list('invoicecost',flat=True)
                for i in invoice_cost:
                    filtered_data.append(PaymentInstruction.objects.filter(invoicecost_id=i,payment_count=payment_count).values_list('id',flat=True).first())
                queryset = PaymentInstruction.objects.filter(id__in=filtered_data)
                for i in queryset:
                    key = f'bank{i.invoicecost_id}'
                    print('key------',key)
                    bank_data = data.get(key)
                    bank_user_status = int(data.get(f'bank_user_status{i.invoicecost_id}'))
                    if bank_user_status == 3 :
                        PaymentInstruction.objects.create(
                            company=request.company,
                            invoicecost_id=i.invoicecost_id,
                            payment_percentage=data.get(f'payment_percentage{i.invoicecost_id}'),
                            pi_number=payment_instruction_number(request.company.id,bank_data ,bank_user_status),
                            payable_amount=convert_to_int(data.get(f'payable_amount{i.invoicecost_id}')),
                            pending_amount=convert_to_int(data.get(f'remaining_amount{i.invoicecost_id}')),
                            masterbank_id=bank_data,
                            companyuserstatus=bank_user_status,
                            payment_count=payment_count,
                        )
                    else :
                        PaymentInstruction.objects.create(
                        company=request.company,
                        invoicecost_id=i.invoicecost_id,
                        payment_percentage=data.get(f'payment_percentage{i.invoicecost_id}'),
                        pi_number=payment_instruction_number(request.company.id,bank_data ,bank_user_status),
                        payable_amount=convert_to_int(data.get(f'payable_amount{i.invoicecost_id}')),
                        pending_amount=convert_to_int(data.get(f'remaining_amount{i.invoicecost_id}')),
                        companybank_id=bank_data,
                        companyuserstatus=bank_user_status,
                        payment_count=payment_count,
                        )
                    invoice_percentage=partial_payment_percentage(i.invoicecost)
                    if invoice_percentage ==100 or invoice_percentage == '100':
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id,id=i.invoicecost.id,status=1).update(partial_status=3)
                    else :
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=1)
            elif is_create == 'True':
                print('1111')
                invoice_split = InvoiceCostInvoice.objects.filter(invoice_id=invoice_id ,partial_status=1 )
                for i in invoice_split:
                    bankid=data.get(f'bank{i.id}')
                    bank_user_status=int(data.get(f'bank_user_status{i.id}'))
                    if bankid:
                        if bank_user_status == 3:
                            PaymentInstruction.objects.create(
                                company=request.company,
                                invoicecost_id=i.id,
                                payment_percentage=data.get(f'payment_percentage{i.id}'),
                                pi_number=payment_instruction_number(request.company.id,data.get(f"bank{i.id}"),int(data.get(f'bank_user_status{i.id}')) ),
                                payable_amount=convert_to_int(data.get(f'payable_amount{i.id}')),
                                pending_amount=convert_to_int(data.get(f'remaining_amount{i.id}')),
                                masterbank_id = int(data.get(f'bank{i.id}')),
                                companyuserstatus=bank_user_status,
                                payment_count=payment_count,
                            )
                        else :
                            PaymentInstruction.objects.create(
                            company=request.company,
                            invoicecost_id=i.id,
                            payment_percentage=data.get(f'payment_percentage{i.id}'),
                            pi_number=payment_instruction_number(request.company.id,data.get(f"bank{i.id}"),int(data.get(f'bank_user_status{i.id}')) ),
                            payable_amount=convert_to_int(data.get(f'payable_amount{i.id}')),
                            pending_amount=convert_to_int(data.get(f'remaining_amount{i.id}')),
                            companybank_id = int(data.get(f'bank{i.id}')),
                            companyuserstatus=bank_user_status,
                            payment_count=payment_count,
                        )
                    else:
                        PaymentInstruction.objects.create(
                            company=request.company,
                            invoicecost_id=i.id,
                            payment_percentage=data.get(f'payment_percentage{i.id}'),
                            payable_amount=convert_to_int(data.get(f'payable_amount{i.id}')),
                            pending_amount=convert_to_int(data.get(f'remaining_amount{i.id}')),
                            payment_count=payment_count,
                                
                        )
                    invoice_percentage=partial_payment_percentage(i.id)
                    if invoice_percentage ==100 or invoice_percentage == '100':
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoice.id,id=i.id,status=1).update(partial_status=3)
                    else :
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoice.id,id=i.id,status=1).update(partial_status=1)
                    
            else:   
                print('22222')
                edit_data = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,is_editable=True,status=True,payment_count=payment_count)
                for i in edit_data:
                    bank_data=data.get(f'bank{i.invoicecost.id}')
                    bank_user_status=int(data.get(f'bank_user_status{i.invoicecost.id}'))
                    
                    if i.companybank :
                        if bank_data:
                            if i.companybank.id != int(data.get(f'bank{i.invoicecost.id}')) :
                                if bank_user_status == 3 :
                                    pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                    i.pi_number = pi_number
                                    i.updated_at = datetime.now()
                                    i.masterbank_id = int(data.get(f'bank{i.invoicecost.id}'))
                                    i.companyuserstatus = bank_user_status
                                    i.save()
                                else :
                                    pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                    i.pi_number = pi_number
                                    i.updated_at = datetime.now()
                                    i.companybank_id = int(data.get(f'bank{i.invoicecost.id}'))
                                    i.companyuserstatus = bank_user_status
                                    i.save()
                            else:
                                i.payment_percentage = data.get(f'payment_percentage{i.invoicecost.id}')
                                i.payable_amount = convert_to_int(data.get(f'payable_amount{i.invoicecost.id}'))
                                i.pending_amount = convert_to_int(data.get(f'remaining_amount{i.invoicecost.id}'))
                                i.save()
                    elif i.masterbank :
                        if bank_data:
                            if i.masterbank.id != int(data.get(f'bank{i.invoicecost.id}')):
                                if bank_user_status == 3 :
                                    pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                    i.pi_number = pi_number
                                    i.updated_at = datetime.now()
                                    i.masterbank_id = int(data.get(f'bank{i.invoicecost.id}'))
                                    i.companyuserstatus = bank_user_status
                                    i.save()
                                else :
                                    pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                    i.pi_number = pi_number
                                    i.updated_at = datetime.now()
                                    i.companybank_id = int(data.get(f'bank{i.invoicecost.id}'))
                                    i.companyuserstatus = bank_user_status
                                    i.save()
                            else:
                                i.payment_percentage = data.get(f'payment_percentage{i.invoicecost.id}')
                                i.payable_amount = convert_to_int(data.get(f'payable_amount{i.invoicecost.id}'))
                                i.pending_amount = convert_to_int(data.get(f'remaining_amount{i.invoicecost.id}'))
                                i.save()
                    else:
                        i.payment_percentage = data.get(f'payment_percentage{i.invoicecost.id}')
                        i.payable_amount = convert_to_int(data.get(f'payable_amount{i.invoicecost.id}'))
                        i.pending_amount = convert_to_int(data.get(f'remaining_amount{i.invoicecost.id}'))
                        i.save()
                    invoice_percentage=partial_payment_percentage(i.invoicecost)
                    
                    if invoice_percentage ==100 or invoice_percentage == '100':
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=3)
                    else :
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=1)


        else:
            is_create = data.get('create_credit')
            is_update = data.get('update_credit')
            invoice_id = data.get('invoice_credit_id')
            split_ids=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_id).values_list('vendor_invoice',flat=True))
            get_inv=Invoice.objects.filter(id=invoice_id).first()
            credit_notes=data.getlist('credit_note')
            mapped_creditnote=list(CreditNoteInvoice.objects.filter(invoice_id=invoice_id,credit__approval_status=4).values_list('credit_id',flat=True))
            contract_credit=list(CreditNote.objects.filter(id__in=mapped_creditnote,usage_status=1,approval_status=4).values_list('id',flat=True))
            credit_notes=contract_credit+credit_notes
            # credit_notes.extend(contract_credit)
            credit_notes=[int(i) for i in credit_notes]
            print(f'credit_notes {credit_notes}')
            print(f'is_create {is_create}, is_update {is_update}, invoice_id {invoice_id}, credit_notes {credit_notes}')
            if is_create == 'True' and is_update == 'True':
                print(1)
                filtered_data = []
                invoice_cost = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id).values('invoicecost').annotate(total_percentage=Sum('payment_percentage')).filter(total_percentage__lt=100).values_list('invoicecost',flat=True)
                for i in invoice_cost:
                    filtered_data.append(PaymentInstruction.objects.filter(invoicecost_id=i).values_list('id',flat=True).first())
                queryset = PaymentInstruction.objects.filter(id__in=filtered_data)
                for i in queryset:
                    key = f'bank_credit{i.invoicecost_id}'
                    bank_data = data.get(key)
                    bank_user_status = int(data.get(f'bank_user_status{i.invoicecost_id}'))
                    if bank_user_status ==3 :
                        PaymentInstruction.objects.create(
                            company=request.company,
                            invoicecost_id=i.invoicecost_id,
                            payment_percentage=data.get(f'payment_percentage_credit{i.invoicecost_id}'),
                            pi_number=payment_instruction_number(request.company.id,bank_data,bank_user_status),
                            payable_amount=convert_to_int(data.get(f'payable_amount_credit{i.invoicecost_id}')),
                            pending_amount=convert_to_int(data.get(f'remaining_amount_credit{i.invoicecost_id}')),
                            masterbank_id=bank_data,
                            companyuserstatus=bank_user_status,
                            invoice_type=2,
                            payment_count=payment_count,
                        )
                    else :
                        PaymentInstruction.objects.create(
                            company=request.company,
                            invoicecost_id=i.invoicecost_id,
                            payment_percentage=data.get(f'payment_percentage_credit{i.invoicecost_id}'),
                            pi_number=payment_instruction_number(request.company.id,bank_data,bank_user_status),
                            payable_amount=convert_to_int(data.get(f'payable_amount_credit{i.invoicecost_id}')),
                            pending_amount=convert_to_int(data.get(f'remaining_amount_credit{i.invoicecost_id}')),
                            companybank_id=bank_data,
                            companyuserstatus=bank_user_status,
                            invoice_type=2,
                            payment_count=payment_count,
                        )
                    invoice_percentage=partial_payment_percentage(i.invoicecost)
                    if invoice_percentage ==100 or invoice_percentage == '100':
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=3)
                    else :
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=1)
            elif is_create == 'True':
                print(2)
                print('req',request.POST)
                create_data = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,is_editable=True,status=True,payment_count=payment_count)
                print(f'create_data {create_data}')
                balance_credit_note=request.POST.getlist('balance_credit_note')
                credit_to_update=request.POST.get('credit_to_update')
                print(f'balance_credit_note {balance_credit_note}')
                get_invoice_cost_values=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_id).values_list('new_netpayable',flat=True))
                invoice_total={}
                for invoice_cost,i in zip(get_invoice_cost_values,range(len(get_invoice_cost_values))):
                    invoice_total[f'cost{i}']=invoice_cost #current invoice amount
                for credits in credit_notes:
                    get_contract_credit=CreditNoteContractInvoice.objects.filter(credit_id=credits,status=1)
                    for splits,j in zip(get_contract_credit,range(len(get_invoice_cost_values))):
                        credit_val=convert_six_digits(splits.new_netpayable) #creditnote originl amount
                        CreditNoteMappin=CreditNoteMappingBase.objects.filter(credit_note_split_id=splits.id,status=True)
                        print(f'CreditNoteMappin {CreditNoteMappin}')
                        credit_org_val=0
                        if CreditNoteMappin.count() == 0:
                            credit_val=credit_val
                        else:
                            for base in CreditNoteMappin:
                                credit_org_val+=float(base.credit_payable)
                            # check_balance=credit_org_val
                            credit_val=float(credit_val)-credit_org_val
                            if credit_val:
                                credit_val=0
                        print(f'credit_val {credit_val},credit_val')
                        if type(invoice_total[f"cost{j}"]) == str:
                            invoice_total[f"cost{j}"]=float(convert_six_digits(invoice_total[f"cost{j}"]))
                        check_used_amount=invoice_total[f"cost{j}"]-float(credit_val)
                        if check_used_amount<0:
                            check_used_amount=0
                        credit_payable=invoice_total[f"cost{j}"]-check_used_amount
                        invoice_total[f"cost{j}"]=int(check_used_amount)
                        pending_credit_val=float(credit_val)-credit_payable
                        CreditNoteContractInvoice.objects.filter(id=splits.id,status=1).update(pending_value=pending_credit_val)
                        CreditNoteMappingBase.objects.create(invoice_id=invoice_id,invoice_split_id=splits.vendor_split_invoice_id,credit_note_id=credits,credit_note_split_id=splits.id,credit_note_value=splits.payment_currency_amount,credit_payable=credit_payable,user_id=request.user.id,company=request.company,pending_credit_value=pending_credit_val)
                    check_for_pending=list(get_contract_credit.values_list('pending_value',flat=True))
                    check_for_pending=sum([float(i) for i in check_for_pending])
                    pending_check=True
                    usage_status=1
                    if check_for_pending == 0:
                        pending_check=False
                        usage_status=2
                    CreditNote.objects.filter(id=credits,approval_status=4).update(check_for_pending=pending_check,usage_status=usage_status)
                if create_data.count() > 0:
                    for i in create_data:
                        bank_user_status=int(data.get(f'bank_user_status{i.invoicecost.id}'))
                        if i.companybank.id != int(data.get(f'bank_credit{i.invoicecost.id}')) or i.masterbank.id != int(data.get(f'bank_credit{i.invoicecost.id}')):
                            if bank_user_status == 3:
                                pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank_credit{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                i.pi_number = pi_number
                                i.updated_at = datetime.now()
                                i.masterbank_id = int(data.get(f'bank_credit{i.invoicecost.id}'))
                                i.companyuserstatus = bank_user_status
                                i.invoice_type=2
                                i.save()
                            else :
                                pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank_credit{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                i.pi_number = pi_number
                                i.updated_at = datetime.now()
                                i.companybank_id = int(data.get(f'bank_credit{i.invoicecost.id}'))
                                i.companyuserstatus = bank_user_status
                                i.invoice_type=2
                                i.save()
                        else:
                            i.payment_percentage = data.get(f'payment_percentage_credit{i.invoicecost.id}')
                            i.payable_amount = convert_to_int(data.get(f'payable_amount_credit{i.invoicecost.id}'))
                            i.pending_amount = convert_to_int(data.get(f'remaining_amount_credit{i.invoicecost.id}'))
                            i.invoice_type=2
                            i.save()
                        invoice_percentage=partial_payment_percentage(i.invoicecost)
                        if invoice_percentage ==100 or invoice_percentage == '100':
                            InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=3)
                        else :
                            InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=1)
                else:
                    invoice_split = InvoiceCostInvoice.objects.filter(invoice_id=invoice_id ).exclude(partial_status=3)
                    print(f'invoice_split {invoice_split}')
                    for i in invoice_split:
                        print('vvvvvvv', {data.get(f'payment_percentage_credit{i.id}')})
                        bank_user_status = int(data.get(f'bank_user_status{i.id}'))
                        if bank_user_status ==3 :
                            PaymentInstruction.objects.create(
                                company=request.company,
                                invoicecost_id=i.id,
                                payment_percentage=data.get(f'payment_percentage_credit{i.id}'),
                                pi_number=payment_instruction_number(request.company.id,data.get(f"bank_credit{i.id}") ,int(data.get(f'bank_user_status{i.id}'))),
                                payable_amount=convert_to_int(data.get(f'payable_amount_credit{i.id}')),
                                pending_amount=convert_to_int(data.get(f'remaining_amount_credit{i.id}')),
                                masterbank_id=data.get(f'bank_credit{i.id}'),
                                companyuserstatus =bank_user_status,
                                invoice_type=2,
                                payment_count=payment_count,
                            )
                        else :
                            PaymentInstruction.objects.create(
                                company=request.company,
                                invoicecost_id=i.id,
                                payment_percentage=data.get(f'payment_percentage_credit{i.id}'),
                                pi_number=payment_instruction_number(request.company.id,data.get(f"bank_credit{i.id}") ,int(data.get(f'bank_user_status{i.id}'))),
                                payable_amount=convert_to_int(data.get(f'payable_amount_credit{i.id}')),
                                pending_amount=convert_to_int(data.get(f'remaining_amount_credit{i.id}')),
                                companybank_id=data.get(f'bank_credit{i.id}'),
                                companyuserstatus = bank_user_status,
                                invoice_type=2,
                                payment_count=payment_count,
                            )
                            
                        invoice_percentage=partial_payment_percentage(i.id)
                        if invoice_percentage ==100 or invoice_percentage == '100':
                            InvoiceCostInvoice.objects.filter(invoice_id=i.invoice.id,id=i.id,status=1).update(partial_status=3)
                        else :
                            InvoiceCostInvoice.objects.filter(invoice_id=i.invoice.id,id=i.id,status=1).update(partial_status=1)
            else:
                print(f'check_crediteeeeeeeeeeeeeeeeees {CreditNoteMappingBase.objects.filter(invoice_id=invoice_id,status=True)}')
                contract_credit_list=list(CreditNote.objects.filter(id__in=mapped_creditnote,usage_status=2,approval_status=4).values_list('id',flat=True))
                credit_notes=contract_credit_list+credit_notes
                balance_credit_note=request.POST.getlist('balance_credit_note')
                check_credits=CreditNoteMappingBase.objects.filter(invoice_id=invoice_id,status=True)
                new=[]
                old=[]
                for i in list(check_credits.values_list('credit_note_id',flat=True).distinct()):
                    if int(i) not in credit_notes:
                        old.append(i)
                for j in credit_notes:
                    if int(j) not in list(check_credits.values_list('credit_note',flat=True).distinct()):
                        new.append(j)

                CreditNote.objects.filter(id__in=list(check_credits.exclude(credit_note_id__in=list(CreditNoteInvoice.objects.filter(invoice_id=invoice_id,credit__approval_status=4).values_list('credit_id',flat=True))).values_list('credit_note_id',flat=True).distinct()),credit_status=2,approval_status=4).update(usage_status=1,check_for_pending=True)
                CreditNoteMappingBase.objects.filter(credit_note_id__in=list(check_credits.values_list('credit_note_id',flat=True).distinct()),company=request.company,invoice_id=invoice_id).delete()

                get_invoice_cost_values=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_id).values_list('new_netpayable',flat=True))
                invoice_total={}
                for invoice_cost,i in zip(get_invoice_cost_values,range(len(get_invoice_cost_values))):
                    invoice_total[f'cost{i}']=invoice_cost #current invoice amount

                for old_value in old:
                    credit_note_contract=CreditNoteContractInvoice.objects.filter(credit_id=old_value)
                    for split,crn in zip(split_ids,credit_note_contract):
                        initial_value_crn=convert_to_digits(crn.new_netpayable)
                        update_pending=CreditNoteMappingBase.objects.filter(credit_note_id=old_value,company=request.company,invoice_split_id=split)
                        credit_org_val=0
                        if update_pending.count() == 0:
                            initial_value_crn=initial_value_crn
                        else:
                            for base in update_pending:
                                credit_org_val+=float(base.credit_payable)
                            # check_balance=credit_org_val
                            initial_value_crn=float(initial_value_crn)-credit_org_val
                        update_pending.update(pending_credit_value=initial_value_crn)
                        print(f'final_amount {initial_value_crn}')


                for credits in credit_notes:
                    print(f'credits {credits},id')
                    get_contract_credit=CreditNoteContractInvoice.objects.filter(credit_id=credits,status=1)
                    for splits,j in zip(get_contract_credit,range(len(get_invoice_cost_values))):
                        credit_val=convert_six_digits(splits.new_netpayable) #creditnote originl amount
                        CreditNoteMappin=CreditNoteMappingBase.objects.filter(credit_note_split_id=splits.id,status=True)
                        credit_org_val=0 
                        if CreditNoteMappin.count() == 0:
                            credit_val=credit_val
                        else:
                            for base in CreditNoteMappin:
                                credit_org_val+=float(base.credit_payable)
                            # check_balance=credit_org_val
                            credit_val=float(credit_val)-credit_org_val
                            if credit_val<= 0:
                                credit_val=0
                        if type(invoice_total[f"cost{j}"]) == str:
                            invoice_total[f"cost{j}"]=float(convert_six_digits(invoice_total[f"cost{j}"]))
                        check_used_amount=invoice_total[f"cost{j}"]-float(credit_val)
                        if check_used_amount<0:
                            check_used_amount=0
                        credit_payable=invoice_total[f"cost{j}"]-check_used_amount
                        if credit_payable <=0:
                            credit_payable=0
                        invoice_total[f"cost{j}"]=int(check_used_amount)
                        pending_credit_val=float(credit_val)-float(credit_payable)
                        if pending_credit_val<=0:
                            pending_credit_val=0
                        print(f'pending_credit_val {pending_credit_val}, check_used_amount {check_used_amount}, credit_payable {credit_payable},credit_val {credit_val}')
                        CreditNoteContractInvoice.objects.filter(id=splits.id,status=1).update(pending_value=pending_credit_val)
                        CreditNoteMappingBase.objects.create(invoice_id=invoice_id,invoice_split_id=splits.vendor_split_invoice_id,credit_note_id=credits,credit_note_split_id=splits.id,credit_note_value=splits.payment_currency_amount,credit_payable=credit_payable,user_id=request.user.id,company=request.company,pending_credit_value=pending_credit_val)
                    check_for_pending=list(get_contract_credit.values_list('pending_value',flat=True))
                    check_for_pending=sum([float(i) for i in check_for_pending])
                    pending_check=True
                    usage_status=1
                    if check_for_pending <= 0:
                        pending_check=False
                        usage_status=2
                    CreditNote.objects.filter(id=credits,approval_status=4).update(check_for_pending=pending_check,usage_status=usage_status)
                edit_data = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,is_editable=True,status=True,payment_count=payment_count)
                for i in edit_data:
                    bank_user_status=int(data.get(f'bank_user_status{i.invoicecost.id}'))
                    if  i.companybank :
                        if i.companybank.id != int(data.get(f'bank_credit{i.invoicecost.id}')):
                            if bank_user_status == 3 :
                                pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank_credit{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                i.pi_number = pi_number
                                i.updated_at = datetime.now()
                                i.masterbank_id = int(data.get(f'bank_credit{i.invoicecost.id}'))
                                i.companyuserstatus =bank_user_status
                                i.invoice_type=2
                                i.save()
                            else :
                                pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank_credit{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                i.pi_number = pi_number
                                i.updated_at = datetime.now()
                                i.companybank_id = int(data.get(f'bank_credit{i.invoicecost.id}'))
                                i.companyuserstatus =bank_user_status
                                i.invoice_type=2
                                i.save()
                        else:
                            i.payment_percentage = data.get(f'payment_percentage_credit{i.invoicecost.id}')
                            i.payable_amount = convert_to_int(data.get(f'payable_amount_credit{i.invoicecost.id}'))
                            i.pending_amount = convert_to_int(data.get(f'remaining_amount_credit{i.invoicecost.id}'))
                            i.invoice_type=2
                            i.save()
                    elif i.masterbank:
                        if i.masterbank.id != int(data.get(f'bank_credit{i.invoicecost.id}')):
                            if bank_user_status == 3 :
                                pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank_credit{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                i.pi_number = pi_number
                                i.updated_at = datetime.now()
                                i.masterbank_id = int(data.get(f'bank_credit{i.invoicecost.id}'))
                                i.companyuserstatus =bank_user_status
                                i.invoice_type=2
                                i.save()
                            else :
                                pi_number = update_payment_instruction_number(i.pi_number,int(data.get(f'bank_credit{i.invoicecost.id}')),int(data.get(f'bank_user_status{i.invoicecost.id}')))
                                i.pi_number = pi_number
                                i.updated_at = datetime.now()
                                i.companybank_id = int(data.get(f'bank_credit{i.invoicecost.id}'))
                                i.companyuserstatus =bank_user_status
                                i.invoice_type=2
                                i.save()
                        else:
                            i.payment_percentage = data.get(f'payment_percentage_credit{i.invoicecost.id}')
                            i.payable_amount = convert_to_int(data.get(f'payable_amount_credit{i.invoicecost.id}'))
                            i.pending_amount = convert_to_int(data.get(f'remaining_amount_credit{i.invoicecost.id}'))
                            i.invoice_type=2
                            i.save()
                    invoice_percentage=partial_payment_percentage(i.invoicecost)
                    if invoice_percentage ==100 or invoice_percentage == '100':
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=3)
                    else :
                        InvoiceCostInvoice.objects.filter(invoice_id=i.invoicecost.invoice.id, id=i.invoicecost.id,status=1).update(partial_status=1)
        return JsonResponse({'success': True})
    
    
class Calculator(View):
    def get(self, request):
        return render(request, 'calculator.html') 
    

class ExchangeRateCalculation(View):
    def post(self, request, *args, **kwargs):
        invoice_id = request.POST.get('pk')
        document_list=getDocumentlist()
        contractid=Invoice.objects.get_by_id(invoice_id)
        general=Settings.objects.get_company(request.company).first()
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(contractid.contractid ).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
            get_submit_type=list(vendorinvoice.values_list('exchange_rate',flat=True))
            currency_name=contract.currency
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
            get_submit_type=list(vendorinvoice.values_list('exchange_rate',flat=True))
            currency_name=contract.service.currency
        submit_type = 1
        if '2' in get_submit_type:
            submit_type=2
        print(f'submit_type {submit_type}')
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(invoice_id,1)
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(invoice_id,1).first()
        invoice_module=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(invoice_id,3)
        if (invoicedetail == None):
            invoicedetail=""
        print(f'currency_name {currency_name}')
        invoice_split = InvoiceCostInvoice.objects.filter(invoice_id=invoice_id)
        payment_instruction_template =  render_to_string('components/exchangeratecalculate.html',{'data':False,'payment_instruction':invoice_split,'invoice_id':invoice_id,'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':invoice_id,'document_list':document_list,'invoicedetail':invoicedetail,'general':general,'submit_type':submit_type,'contract':currency_name,'invoice_module':invoice_module},request)
        return JsonResponse({'success': False,'payment_instruction_template':payment_instruction_template,'create':True,'update':False})



class PostExchangeRate(View):
    def post(self, request,*args, **kwargs):
        pk=request.POST.get('pk')
        hidden_vendor_id=request.POST.getlist('hidden_vendor_id')
        invoice_total_amount=request.POST.getlist('invoice_total_amount')
        check_exchange_rate=request.POST.getlist('check_exchange_rate')
        exchangerate=request.POST.getlist('exchangerate')
        print(f'exchangerate {exchangerate}, hidden_vendor_id {hidden_vendor_id},invoice_total_amount {invoice_total_amount},check_exchange_rate {check_exchange_rate}')
        invoice=Invoice.objects.filter(id=pk).first()
        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=invoice.id,status=1)
        Invoiceflowmodules.objects.filter(invoice_id=invoice.id,status=0,module_id=3).update(exchangerate_confirm_status=1,tax_confirm_status=0)
        for invoice in invoice_cost:
            PastExchangeRate.objects.create(invoice_id=invoice.id,invoice_base_amount=invoice.invoice_base_amount,invoice_exchange_rate=invoice.invoice_exchange_rate,invoice_total_amount=invoice.invoice_total_amount)
        for vendor_id,type,exchange_rate,total_amount in zip(hidden_vendor_id,check_exchange_rate,exchangerate,invoice_total_amount):
            InvoiceCostInvoice.objects.filter(id=vendor_id).update(invoice_exchange_rate=exchange_rate,invoice_total_amount=total_amount)
        return JsonResponse({'status':True})


class InvoiceApprovalTrack(View):
    def get(self,request,pk):
        invoice_detail = Invoice.objects.get_by_id(pk)
        invoice_cost_details=InvoiceCostInvoice.objects.filter(invoice_id=invoice_detail,status=1).first()
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
        payment_status=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('payment_status',flat=True))
        bank_user=Settings.objects.getcompany_settings(request.user.company.id)
        print(payment_status,"PAYMENT STATUS")
        paid_status = 1
        if 1 in payment_status and 2 in payment_status:
            paid_status = 1
        elif 1 in payment_status:
            paid_status = 2
        elif 2 in payment_status:
            paid_status = 3
        print(paid_status,"PAID STATUS")
        all_invoice=', '.join(str(e) for e in invoice_number)
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        # check_for_dispute=DisputedInvoiceTrack.objects.filter(invoice_id=pk,status=True)
        completed_invoice=Invoiceflowmodules.objects.getinvoiceflowmodules_by_invoice_id(pk).filter(status=1).exclude(module=None)
        pending_invoice_status=Invoiceflowmodules.objects.getinvoiceflowmodules_by_invoice_id(pk).filter(status=0)
        if (invoice_detail.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(invoice_detail.contractid)
            projectdisciplinetype=contract.projectdisciplinetype_id
            cluster_ids=contract.projectdiscipline.cluster_id
            project=contract.projects
        else:
            contract=Amendment.objects.get_by_id(invoice_detail.contractid ,1).first()
            projectdisciplinetype=contract.service.projectdisciplinetype_id
            project=contract.service.projects
            cluster_ids=contract.service.projectdiscipline.cluster_id
        if (project.flow_level == "discipline"):
                get_levels=ProjectFlowlevel.objects.get_by_level_main(projectdisciplinetype,'discipline',request.company,project.id)
        elif (project.flow_level == "clusters"):
            get_levels=ProjectFlowlevel.objects.get_by_level_main(cluster_ids,'clusters',request.company,project.id)
        else:
            if invoice_detail.well_not_applicable == "id":
                get_levels=ProjectFlowlevel.objects.get_by_level_main(invoice_detail.well_id,'well',request.company,project.id)
            else:
                get_levels=ProjectFlowlevel.objects.get_by_wellbasedlevel_main(projectdisciplinetype,'well',request.company,project.id)
        projectflow_modules=ProjectFlowModules.objects.getallactiveflow_level_mul_id(get_levels.values_list('id',flat=True))
        invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_by_invoice_id(pk).filter(status=1).exclude(module=None).count()
        approval_status=True if len(projectflow_modules) == invoiceflow_modules else False
        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('id',flat=True)
        invoice_cost_data=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
        print(invoice_cost_data , "INVOICE COST DATA")
        get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost).exclude(is_editable=1)
        payment_instruction_list=[]
        for instruction in get_payment_instruction:
            get_bank_uers=CompanyBankUser.objects.filter(companybank_id=instruction.companybank_id)
            payment_instruction_list.append({'payment_instruction':instruction,'users_data':get_bank_uers})   
        created_invoice_flow=invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_by_invoice_id(pk) 
        module_flowes=invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_by_invoice_id(pk).last()
        module_split_value=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
        disputed_inv=SettlementInvoice.objects.filter(invoice_id=pk,company_id=request.company.id,status=True,acceptance_status=2)
        data={'project_id':project,'paid_status':paid_status,'get_levels':get_levels,'pk':pk,'contract':contract,'approval_status':approval_status,'payment_instruction_list':payment_instruction_list,'created_invoice_flow':created_invoice_flow,'completed_invoice':completed_invoice,'pending_invoice_status':pending_invoice_status,'invoice_detail':invoice_detail,'allVendors':allVendors,'all_invoice':all_invoice,'disputed_inv':disputed_inv,'check_for_dispute':disputed_inv.count(),'invoice_cost':invoice_cost_data , 'module_flowes':module_flowes ,'bank_user_status':bank_user ,'module_split_value':module_split_value , "module_split_count":len(module_split_value) ,'get_levels_count':get_levels.count() , 'invoice_cost_details':invoice_cost_details}
        return render(request,'invoiceapprovalrack.html',data)

class InvoiceOverrideUsers(View):
    def get(self,request,pk):
        get_invoice_flow=Invoiceflowmodules.objects.filter(invoice_id=pk).last()
        get_users=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_invoice_flow.id).values_list('user',flat=True)
        new_users_list=ProjectUser.objects.getnewuser_byproject(get_invoice_flow.project_id,get_users)
        data={'pk':pk,'new_users_list':new_users_list}
        return render(request,'invoiceoverrideassignusers.html',data)

    def post(self,request,pk):
        users_list=request.POST.getlist('users')
        get_invoice_flow=Invoiceflowmodules.objects.filter(invoice_id=pk).last()
        for user_id in users_list:
            project_user=ProjectUser.objects.getuser_byproject_userid(get_invoice_flow.project_id,user_id)
            Invoiceflowmodulesusers.objects.createoverrideinvoiceusers(get_invoice_flow.project_id,project_user.id,get_invoice_flow.id,user_id,0)
        return redirect('invoice:vendorbasedinvoice')

class BankUserApproval(View):
    def get(self,request,pk):
        contractid=Invoice.objects.get_by_id(pk)
        bankdetails=CompanyBank.objects.get_by_company(request.company)
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(contractid.contractid).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        get_data=Invoiceflowmodules.objects.get_by_only_module_id(pk,None)
        bank_user=Invoiceflowmodulesusers.objects.get_bankuser_invoicefloemodule(get_data.id,request.user.id,1)
        payment_details=PaymentInstruction.objects.get_by_payment_id(pk,bank_user.payment_instruction.id)
        data={'payment_details':list(payment_details),'maininvoices':vendorinvoice,'pk':pk,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'invoice_detail':contractid,'bank_user':bank_user}
        return render(request,'bankuserapproval.html',data)
    def post(self,request,pk):
        print(request.POST)
        current_date=datetime.now()
        invoice_detail = Invoice.objects.get_by_id(pk)
        pay_id=request.POST.get('pay_id')
        PaymentInstruction.objects.update_verification_status(pay_id,1)
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        get_data=Invoiceflowmodules.objects.get_by_only_module_id(pk,None)
        bank_user=Invoiceflowmodulesusers.objects.get_bankuser_invoicefloemodule(get_data.id,request.user.id,1)
        Payment=PaymentInstruction.objects.get_by_payment_id(pk,bank_user.payment_instruction.id).values_list('pi_number',flat=True)
        pi_number=",".join(map(str,Payment))
        # verb="Payment Instruction Received"
        # description=f'Instruction {pi_number} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service}   has been received by {request.user.name} {request.user.lastname}.'
        invoiceflow_modules=Invoiceflowmodules.objects.get_by_module_id(pk,1,6)
        approved_flow_user=Invoiceflowmodulesusers.objects.get_approved_users(invoiceflow_modules.id).first()
        userdata=User.objects.get(id=approved_flow_user.user)
        # notify_invoice_flow(request,userdata,"invoice/vendorbasedinvoice",verb,description)
        #check bank user module approved or not 
        check_data=Invoiceflowmodules.objects.get_by_module_id(pk,1,None)
        print('af',check_data)
        if (check_data):
            #update only user status
            invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_only_byinvoice(pk,None)
            Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,1,None)
        else:
            invoice_flow_func(pk,None,request,None,"1","Approved")
        return redirect(reverse_lazy("invoice:vendorbasedinvoice"))


class BankUserApprovalAjax(View):
    def post(self,request):
        invoice_id=request.POST.get('invoice_id')
        invoicecost_id=request.POST.get('invoicecost_id')
        get_type=request.POST.get('type')
        code=request.POST.get('code')
        payment_id=request.POST.get('payment_id')
        payment_li=request.POST.getlist('payment_id')
        pay_id=request.POST.get('pay_id')
        invoice_detail = Invoice.objects.get_by_id(invoice_id)
        name_of_service = invoice_detail.name_service
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        get_data=Invoiceflowmodules.objects.filter(invoice_id=invoice_id,module_id=None)
        # check_data=InvoiceCostInvoice.objects.check_verification_code(invoicecost_id,code)
        check_data=PaymentInstruction.objects.check_verification_code(payment_id,code)
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1).values_list('invoice_number',flat=True))
        all_invoice=', '.join(str(e) for e in invoice_number)
       

        if (check_data):
            payment_user = PaymentInstruction.objects.filter(id=payment_id,status=True).first()
            pi_number = payment_user.pi_number
            recept_upload=Invoiceflowmodules.objects.filter(invoice_id=invoice_id,invoicecost_id=invoicecost_id,module_id=7,payment_instruct=None,status=0).first()

            if recept_upload :
                recept_upload.payment_instruct_id=payment_id
                recept_upload.save()
            
            PaymentInstruction.objects.update_verification_status(payment_id,1)
            PaymentInstruction.objects.filter(id=payment_id).update(bankuser_verification=1,payment_status=2)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=get_data,bank_user_status=1,payment_instruction__invoicecost_id=invoicecost_id,payment_instruction_id=payment_id).update(bank_user_verification=2,status=1,comments=None,created_at=datetime.now())
            invoiceflow=Invoiceflowmodules.objects.filter_by_module_id(invoice_id,1,None).filter(payment_instruct__payment_count=pay_id)

            # Sending mail to bank user
            mail_send_to_verified_bank_user(request,pi_number,check_data,all_invoice,name_of_service)
            # Sending notification to bank user
            main_url="invoice/vendorbasedinvoice"
            main_verb='Invoice'+" "+'Payment Code Verified'
            content = f'Payment instruction No {pi_number} for invoice {all_invoice} for Vendor {check_data.invoicecost.vendor.vendor_name} for services {name_of_service} has been verified for payment by {request.company.company_name}'
            now = datetime.now()
      
            notify_invoice_flow(request,check_data.verified_bank_user,main_url,main_verb,content)
            print(f'invoiceflow--------- {invoiceflow}')
           

            if invoiceflow.count() == 0:
                invoice_flow_func(invoice_id,None,request,None,"1","Approved",pay_id,payment_li)
            else :
                current_date=datetime.now()
                comments = None
                module =None
                submit_type = "1"
                invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoiceids(invoice_id,module)
                if payment_li and module == None or module > 4:

                    with_instructions=invoiceflow_modules.filter(payment_instruct__in=payment_li )
                    print('with_instructions ',with_instructions)
                if (invoiceflow_modules.count() > 0):
                    flow_modules=list(invoiceflow_modules.values_list('id',flat=True))
                    try:
                        with_instructionsmodule=list(with_instructions.values_list('id',flat=True))
                    except:
                        with_instructionsmodule=[]
                    if module and  module < 5:
                        Invoiceflowmodules.objects.filter(id__in=list(invoiceflow_modules.values_list('id',flat=True))).update(status=1)
                        Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_modules,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date)
                    else:
                        
                        Invoiceflowmodules.objects.filter(id__in=list(with_instructions.values_list('id',flat=True))).update(status=1 ,payment_instruct_id = payment_li[0] )
                        Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=with_instructionsmodule,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date)
            datas={'data':'success'}
        else:
            datas={'data':'failure'}
        data=datas
        return JsonResponse(data)

class DisputedInvoices(View):
    def get(self,request):
        context = {}
        user_right=0
        vendorid=ContractMasterVendor.objects.filter(vin=self.request.user.cin_number).first()
        if(self.request.user.roles_id==3):
            # allinvoices=[]
            getprojects=ProjectUser.objects.getprojectuser_byuserid(self.request.user.id)
            if(UserRights.objects.filter(user_id=request.user.id,module_id=18).first()):
                if(UserRights.objects.filter(user_id=request.user.id,module_id=18).first().create == '1'):
                    # context['Invoices'] = Invoice.objects.filter(status=1,invoice_status=6,company=self.request.company,dispute_status=2).order_by('-id')
                    user_right=1
                else:
                    if getprojects.count() > 0:
                        user_right=1
                        # for project in getprojects:
                        #     contracts=ContractMaster.objects.get_contract_project(project.project_id)
                        #     for contract in contracts:
                        #         invoices=Invoice.objects.getdisputedinvoiceby_contract(contract.id)
                        #         for invoice in invoices:
                        #             allinvoices.append(invoice)
                        # sorted_data=sorted(allinvoices, key=lambda x: x.id, reverse = True)
                        # context['Invoices'] = sorted_data
            else:
                if getprojects.count() > 0:
                    user_right=1
                    # for project in getprojects:
                    #     contracts=ContractMaster.objects.get_contract_project(project.project_id)
                    #     for contract in contracts:
                    #         invoices=Invoice.objects.getdisputedinvoiceby_contract(contract.id)
                    #         for invoice in invoices:
                    #             allinvoices.append(invoice)
                    # sorted_data=sorted(allinvoices, key=lambda x: x.id, reverse = True)
                    # context['Invoices'] = sorted_data
        else:
            # context['Invoices'] = Invoice.objects.filter_by_company(1,6,self.request.company).order_by('-id')
            user_right=1
        context['userid'] = self.request.user.id
        context['vendorid']=vendorid
        context['user_right']=user_right
        print(f'user_right {user_right}')
        return render(request,'disputedinvoiceslist.html',context)
    
class DisputedInvoiceQueryHistory(View):
    def get(self,request,pk):
        query=Invoice.objects.get_by_id(pk)
        ref_num=ContractMaster.objects.filter(id=query.contractid).first()
        check_InvoiceExceptional=InvoiceExceptional.objects.filter(invoice_id=pk,status=1).exclude(exceptional_type=5).count()
        get_settlement_count=SettlementInvoice.objects.filter(invoice_id=pk,company=request.company).count()
        print(f'get_settlement_count {get_settlement_count}')
        invoice_exceptional_instance = InvoiceExceptional.objects.filter(invoice_id=pk).last()

        # Check if the instance exists and then retrieve the checked_messages field
        if invoice_exceptional_instance:
            checked_messages = invoice_exceptional_instance.checked_messages
        else:
            checked_messages = None  
        get_flow=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id=query.id,Invoiceflowmodules__module_id=2,Invoiceflowmodules__status=1)
        get_flow=Invoiceflowmodules.objects.filter(company_id=request.company.id,invoice_id=query.id,status=1,module_id=2)
        # print('get_flow_usercomment',get_flow_usercomment)
        vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
        # vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
        # allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=18,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights).count()
        print(f'get_dispute_users {get_dispute_users}')
        wcc_files=other_documents()
        print(f'wcc_files {wcc_files}')
        # get_status=DisputedInvoiceTrack.objects.filter(invoice_id=pk,stage=4).first()
        querylist=AddNewDisputedQuery.objects.filter(query_id=pk)
        closed_query_count=list(querylist.filter(query_status=1).order_by('returned_count').values_list('returned_count',flat=True).distinct())
        print(f'closed_query_count {closed_query_count}')
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
        all_invoice=', '.join(str(e) for e in invoice_number)
        data={'querylists':querylist.filter(query_status=0),'checked_messages':checked_messages,'all_invoice':all_invoice,'query':query,'pk':pk,'contact_person':vendor,'wcc_files':wcc_files,'settlement_count':get_settlement_count,'ref_num':ref_num,'check_InvoiceExceptional':check_InvoiceExceptional,'get_dispute_users':get_dispute_users,'closed_query_count':closed_query_count}
        returned_count=returned_count_invoice_credit(pk,1)
        vendor_acceptance=DisputedInvoiceTrack.objects.filter(invoice_id=pk,stage=2,status=True,vendor_confirmation__gte=1,returned_count=returned_count).first()
        if vendor_acceptance:
            data['vendor_acceptance']=vendor_acceptance
        return render(request,'disputedquerylist.html',data)
    
    def post(self,request,pk):
        print(f' reqe {request.POST}')
        today = date.today()
        date_today = today.strftime("%d-%b-%Y")
        query=Invoice.objects.get(id=pk)
        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
        invoice_number=list(invoice_cost.values_list('invoice_number',flat=True))
        all_invoice=', '.join(str(e) for e in invoice_number)
        get_submit=request.POST.get('submit_type')
        vendor_comfirmation=request.POST.get('vendor_comfirmation')
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=18,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights)
        invoice_detail = Invoice.objects.get_by_id(pk)
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        returned_count=returned_count_invoice_credit(pk,1)
        if(get_submit):
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            get_user=request.user
            if submit_type == '8':
                file=request.POST.get('file')
                if file != None and file !='' : 
                   
                    fs = FileSystemStorage()
                    file_name=file.name 
                else :
                    file_name =file
                get_exceptional=request.POST.getlist('exceptional')
                exceptional_list=[InvoiceExceptional(invoice_id=pk,exceptional_type=i,confirm_dispute=1) for i in get_exceptional]
                InvoiceExceptional.objects.bulk_create(exceptional_list)
                Invoice.objects.filter(id=pk).update(dispute_status=2,invoice_status=6 ,return_dispute_status=2 )
                invoice_cost.update(approval_status=6)
                returned_count=returned_count_invoice_credit(pk,1)
                DisputedInvoiceTrack.objects.create(invoice_id=pk,stage=3,status=True,user=request.user,created_at=datetime.now(),reason=comments,returned_count=returned_count)
                main_url=f"invoice/invoicequeryhistory/{pk}"
                subject=f"Recommendation for Invoice Dispute"
                reason=f'Invoice {all_invoice} has been recommended for Dispute for {vendor.vendor_name} on {date_today} for {query.name_service}'
                for user in get_dispute_users:
                    url='https://irockinfo.mo.vc/'
                    moved_as_dispute_mail(request,user,all_invoice,url,invoice_detail,vendor,comments)
                    notify_invoice_flow(request,user,main_url,subject,reason)
                # allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
                # for notifications in allVendors:
                    # notify_invoice_flow(request,notifications,main_url,reason,reason)
                AddNewDisputedQuery.objects.create_disputed_query(pk,reason,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                AddNewDisputedQuery.objects.create_disputed_query(pk,comments,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                return redirect("invoice:listdisputeinvoices")
            elif submit_type == '6':
                percentage_val=request.POST.get('settlement_val')
                file=request.POST.get('file')
                if file != None and file !='' : 
                    fs = FileSystemStorage()
                    file_name=file.name 
                else :
                    file_name =file
                DisputedInvoiceTrack.objects.create(invoice_id=pk,stage=4,status=True,user=request.user,created_at=datetime.now(),reason=comments,returned_count=returned_count)
                get_disputed_percentage=100 - float(percentage_val)
                get_invoice_value=InvoiceCostInformation.objects.get_invoice_id(pk,1)
                get_module=AddNewDisputedQuery.objects.filter(query_id=pk,returned_count=returned_count).first()
                invoice_Exclusive_tax=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
                if(get_invoice_value.count() >= 1):
                    #get_settlement_val=get_invoice_value.first()
                    #match =''.join(filter(str.isdigit, get_settlement_val.finalvalue))
                    #get_invoice="{:.2f}".format(float(match)*(float(percentage_val)/100))
                    for costinvoice in invoice_cost:
                        base_amount=replacecommaid(amount_convertion(costinvoice.invoice_base_amount))
                        exclusive_tax=float(remove_symbol(invoice_Exclusive_tax.total_exclusive_value))
                        invoice_percentage=float(costinvoice.invoice_percentage)
                        invoice_exclusive_amount=round_of_two_values((exclusive_tax * invoice_percentage)/100)
                        invoice_gross_amount_without_exclusice_tax= float(round_of_two_values(float(base_amount) - float(invoice_exclusive_amount)))
                        approved_exclusive_tax=round_of_two_values(float(invoice_exclusive_amount)*(float(percentage_val)/100))
                        approved_gross_amount=round_of_two_values(float(invoice_gross_amount_without_exclusice_tax)*(float(percentage_val)/100))
                        # approved_amount=float(base_amount)*(float(percentage_val)/100)
                        approved_amount=float(approved_exclusive_tax)+float(approved_gross_amount)
                        approved_amount=new_round_of_two_values(approved_amount)
                        disputed_exclusive_tax=round_of_two_values(float(invoice_exclusive_amount)*(float(get_disputed_percentage)/100))
                        disputed_gross_amount=round_of_two_values(float(invoice_gross_amount_without_exclusice_tax)*(float(get_disputed_percentage)/100))
                        # disputed_amount=float(base_amount)*(float(get_disputed_percentage)/100)
                        disputed_amount=float(disputed_exclusive_tax)+float(disputed_gross_amount)
                        disputed_amount=new_round_of_two_values(disputed_amount)
                        
                        if SettlementInvoice.objects.filter(invoice_id=pk,invoicecostinvoice_id=costinvoice.id).exists():
                            SettlementInvoice.objects.filter(invoice_id=pk,invoicecostinvoice_id=costinvoice.id).update(user=get_user,module_id=get_module.module_id,accepted_percentage=float(percentage_val),disputed_percentage=get_disputed_percentage,invoicevalue_accepted=approved_amount,invoicevalue_declined=disputed_amount,old_value=base_amount,status=True)
                        else:
                            SettlementInvoice.objects.create(invoice_id=pk,invoicecostinvoice_id=costinvoice.id,user=get_user,company=request.company,module_id=get_module.module_id,accepted_percentage=float(percentage_val),disputed_percentage=get_disputed_percentage,invoicevalue_accepted=approved_amount,invoicevalue_declined=disputed_amount,old_value=base_amount)
                reason=f'Invoice No {all_invoice} has been approved for {percentage_val}% and disputed for {int(get_disputed_percentage)}% by {request.user.name} '
                main_url=f"invoice/invoicequeryhistory/{pk}"
                vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
                returned_count=returned_count_invoice_credit(pk,1)
                AddNewDisputedQuery.objects.create_disputed_query(pk,reason,request.user,time_stamp,vendor.id,file,returned_count,file_name )
                AddNewDisputedQuery.objects.create_disputed_query(pk,comments,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
                main_verb='Invoice Disputed'
                content=f'Invoice {all_invoice} has been disputed by {request.user.name} on {date_today} for {query.name_service}'
                for notifications in allVendors:
                    notify_invoice_flow(request,notifications,main_url,main_verb,content)
                    invoice_Settlement_mail(request,notifications,vendor,submit_name,invoice_detail,comments,all_invoice,get_disputed_percentage,percentage_val)
                return redirect('invoice:invoicequeryhistory',pk=pk)
            elif submit_type == 'A1':
                Invoice.objects.filter(id=pk).update(dispute_status=3)
                SettlementInvoice.objects.filter(invoice_id=pk,status=True).update(acceptance_status=2)
                allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
                main_url=f"invoice/invoicequeryhistory/{pk}"
                disputed_user=AddNewDisputedQuery.objects.filter(query_id=pk,returned_count=returned_count).first()
                reason=f"Disputed Invoice accepted by {request.user.name}."
                content=f" Dispute Invoice {all_invoice} has been accepted and resolved by {request.user.name} on {date_today} for services {invoice_detail.name_service}."
                file = None
                file_name = None
                AddNewDisputedQuery.objects.create_disputed_query(pk,comments,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                if disputed_user.user:
                    notify_invoice_flow(request,disputed_user.user,main_url,reason,content)
                    dispute_vendor_acceptmail_touser(request,disputed_user.user,all_invoice,invoice_detail,vendor)
                for user in get_dispute_users:
                    dispute_vendor_acceptmail_touser(request,user,all_invoice,invoice_detail,vendor)
                    notify_invoice_flow(request,user,main_url,reason,content)
                reason=f"Disputed Invoice accepted and resolved."
                content=f" Dispute for invoice {all_invoice} for services {invoice_detail.name_service} has been accepted and resolved by {request.company}"
                for notifications in allVendors:  
                    notify_invoice_flow(request,notifications,main_url,reason,content)
                    dispute_vendor_acceptmail(request,notifications,all_invoice,invoice_detail,vendor)
                return redirect('invoice:invoicequeryhistory',pk=pk)
            elif submit_type == 'A2':
                main_url=f"invoice/listdisputeinvoices"
                verb=f"Disputed Invoice Contested by {request.user.name}"
                reason=f'Dispute on Invoice No.{all_invoice} has been contested by {request.user.name} on {date_today} for {invoice_detail.name_service}'
                SettlementInvoice.objects.filter(invoice_id=pk,status=True).update(acceptance_status=3)
                disputed_user=AddNewDisputedQuery.objects.filter(query_id=pk,returned_count=returned_count).first()
                if disputed_user.user:
                    notify_invoice_flow(request,disputed_user.user,main_url,verb,reason)
                    dispute_vendor_declinemail_touser(request,disputed_user.user,all_invoice,invoice_detail,vendor,comments)
                for user in get_dispute_users:
                    dispute_vendor_declinemail_touser(request,user,all_invoice,invoice_detail,vendor,comments)
                    notify_invoice_flow(request,user,main_url,verb,reason)
                Invoice.objects.filter(id=pk).update(dispute_status=4)
                return redirect('invoice:invoicequeryhistory',pk=pk)
            else:
                get_module=AddNewDisputedQuery.objects.filter(query_id=pk,returned_count=returned_count).first()
                check_possiblity=BackToDisputeQuery.objects.filter(query_id=pk).count()
                if(check_possiblity>0):
                    get_module=BackToDisputeQuery.objects.filter(query_id=pk).first()
                DisputedInvoiceTrack.objects.create(invoice_id=pk,stage=5,status=True,user=request.user,created_at=datetime.now(),reason=comments,returned_count=returned_count)
                Invoice.objects.filter(id=pk).update(invoice_status=2)
                InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=1)
                split_count=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).count()
                inv_flow=Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=get_module.module_id).order_by('-id')[:split_count]
                file = None
                file_name = None
                AddNewDisputedQuery.objects.create_disputed_query(pk,comments,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                print(f'inv_flow {inv_flow}')
                if inv_flow.count() > 0:
                    Invoiceflowmodules.objects.filter(id__in=list(inv_flow.values_list('id',flat=True))).update(status=0)
                    Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=list(inv_flow.values_list('id',flat=True))).update(status=0)
                main_url=f"invoice/vendorbasedinvoice"
                verb=f'Invoice for Approval'
                reason=f'Invoice No.{all_invoice} has been moved from Dispute process and Passed for your Approval'
                notify_invoice_flow(request,get_module.user,main_url,verb,reason)
                if request.user.roles_id == 2 or request.user.roles_id ==3:
                    return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
                else:
                    return redirect(reverse_lazy("invoice:listdisputeinvoices"))
        elif vendor_comfirmation:
            print(f'vendor_comfirmation {vendor_comfirmation}')
            accept_status = 'unaccepted' if vendor_comfirmation in ['2', 2] else 'accepted'
            reason_status = 'Unaccepted' if vendor_comfirmation in ['2', 2] else 'Accepted'
            last_name=request.user.lastname
            if not last_name:
                last_name=''
            try:
                vendor_name=f'({vendor.vendor_name})'
            except:
                vendor_name=''
            reason=f'Invoice No.{all_invoice} query has been {accept_status} by {request.user.name} {last_name} {vendor_name}'
            returned_count=returned_count_invoice_credit(pk,1)
            confirmation_query=AddNewDisputedQuery.objects.create_disputed_query(pk,reason,request.user,time_stamp,vendor.id,None,returned_count,None)
            AddNewDisputedQuery.objects.filter(id=confirmation_query.id).update(highlighted_content=True)
            disputed_invoice=DisputedInvoiceTrack.objects.create(stage=2,invoice_id=pk,status=True,user=request.user,created_at=datetime.now(),returned_count=returned_count)
            DisputedInvoiceTrack.objects.filter(id=disputed_invoice.id).update(vendor_confirmation=vendor_comfirmation)
            main_url=f"invoice/invoicequeryhistory/{pk}"
            main_verb=f'Invoice NO.{all_invoice} {reason_status} by {request.user.name} {request.user.lastname} '
            content=f'Invoice NO.{all_invoice} {reason_status} for Approval by {request.user.name} on {date_today} for {query.name_service} '
            get_user=AddNewDisputedQuery.objects.filter(query_id=pk).first()
            notify_invoice_flow(request,get_user.user,main_url,main_verb,content)
            return redirect('invoice:invoicequeryhistory',pk=pk)
        else:
            deniedreason=request.POST.get('message')
            files_upload=request.POST.get('files_upload')
            document_type=request.POST.get('document_type')
            document_name=request.POST.get('document_name')
            vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
            allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            check_InvoiceExceptional=InvoiceExceptional.objects.filter(invoice_id=pk,exceptional_type=1,status=1).count()
            main_url=f"invoice/invoicequeryhistory/{pk}"
            verb=f"Response to Invoice Returned Clarification."
            reason=f'Invoice {all_invoice} has been received response for returned invoice from {request.user.name} on {date_today} for {query.name_service}'
            if request.user.roles_id == 4:
               
                url='https://irockinfo.mo.vc/' 
                team=f'The Invoice Approval Process System'
                if query.invoice_status == 6:
                    pass
                    # for users in get_dispute_users:
                    #     notify_invoice_flow(request,users,main_url,verb,reason)
                    #     response_to_vendor_mail(request,users,all_invoice,url,query,team)
                else:
                    returned_user=AddNewDisputedQuery.objects.filter(query_id=pk).first()
                    if returned_user.user:
                        notify_invoice_flow(request,returned_user.user,main_url,verb,reason)
                        response_to_vendor_mail(request,returned_user.user,all_invoice,url,query,team)
            else:
                if query.invoice_status == 6:
                    pass
                else:
                    url='https://irockinfo.mo.vc/vendorlogin' 
                    team=f'The Finance Team'
                    for vendor_data in allVendors:
                        notify_invoice_flow(request,vendor_data,main_url,verb,reason)
                        response_to_vendor_mail(request,vendor_data,all_invoice,url,query,team)
            returned_count=returned_count_invoice_credit(pk,1)
            if check_InvoiceExceptional > 0 and request.user.roles_id == 4:
                files=request.FILES.getlist('file')
                if len(files) > 0:
                    get_dispute=AddNewDisputedQuery.objects.create_disputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None,returned_count,None)
                    for file in files:
                        if file != None and file !='' : 
                            fs = FileSystemStorage()
                            file_name=file.name 
                        else :
                            file_name =file
                        
                        create_file=InvoiceFileUpload.objects.create(invoice_id=query.id,support=files_upload,support_file=file,vendor_id=query.vendor_id,contractid=query.contractid,filetype='new',file_name=file_name,return_status=2)
                        DisputedQueryFiles.objects.create(disputedquery=get_dispute,file=file,document_name=document_name,document_type=document_type,original_file_name=file_name)
                else:
                    get_dispute=AddNewDisputedQuery.objects.create_disputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None,returned_count,None)
            else:
                files=request.FILES.getlist('file')
                if len(files) > 0:
                    for file in files:
                        if file != None and file !='' : 
                            fs = FileSystemStorage()
                            file_name=file.name 
                            file = fs.save(file.name, file)
                        else :
                            file_name =file
                        get_dispute=AddNewDisputedQuery.objects.create_disputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                else :
                    get_dispute=AddNewDisputedQuery.objects.create_disputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None,returned_count,None)
            
            scheme=request.scheme
            gethost=request.get_host()
            if request.user.roles_id == 4:
                if query.invoice_status == 6:
                    sender = User.objects.get_by_id(request.user.id)
                    url=f"{scheme}://{gethost}/invoice/invoicequeryhistory/{query.id}"
                    description=f'Reply received from {vendor.vendor_name}'
                    getCompanyUserlist(request,sender,url,'Reply Received for Disputed Invoice',description)
            else:
                if query.invoice_status == 6:
                    sender = User.objects.filter(id=request.user.id).first()
                    recipients = User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
                    print('recipients',recipients)
                    url=f"{scheme}://{gethost}/invoice/invoicequeryhistory/{query.id}"
                    notify.send(sender, recipient=recipients,data=url, verb='Reply Received for Disputed Invoice', description=f'Reply received from {sender.name} {sender.lastname if sender.lastname != None else ""}')    
            return redirect('invoice:invoicequeryhistory',pk=pk)
    

class Invoicecompletereport(View):
    def get(self, request,reportname):
        countries=Countries.objects.all()
        projects=Projectcreation.objects.filter(company=request.company)
        discipline_subtype = DisciplineSubtype.objects.filter(status=1).values_list('discipline_subtype', flat=True).distinct()
        vendors=ContractMasterVendor.objects.filter_company(request.company,1)
        company=Settings.objects.filter(company_id=request.company.id).first()
        getcurrencylist=ast.literal_eval(company.currency)
        companycurrency=Basecountries.objects.filter(id__in=getcurrencylist)
        allreports=CompleteReport.objects.filter(company_id=request.company,status=1,reportname=reportname).first()
        vendors_list=ContractMasterVendor.objects.filter_company(request.company,1)
        if allreports:
            selectedproject = [int(item) for item in ast.literal_eval(str(allreports.project))] if allreports and allreports.project else []
            attributes = ['discipline', 'service', 'vendor', 'country', 'approvalstatus', 'paymentstatus', 'ageingperiod','amountfilter']
            processed_data = {attr: ast.literal_eval(getattr(allreports, attr, '[]')) for attr in attributes}
            for attr in ['vendor', 'country', 'paymentstatus', 'ageingperiod']:
                    processed_data[attr] = [int(item) for item in processed_data[attr]]
            selecteddiscipline = processed_data['discipline']
            selectedservice = processed_data['service']
            selectedvendor = processed_data['vendor']
            selectedcountry = processed_data['country']
            selectedapprovalstatus = processed_data['approvalstatus']
            selectedpaymentstatus = processed_data['paymentstatus']
            selectedageingperiod = processed_data['ageingperiod']
            amountfilter = processed_data['amountfilter']
            selectedexceptions = [int(item) for item in ast.literal_eval(str(allreports.exceptions))] if allreports and allreports.exceptions else []
            period=allreports.period 
            
        context={'countries':countries,'projects':projects,'discipline_subtype':discipline_subtype,'vendorslist':vendors,'companycurrency':companycurrency,'allreports':allreports,'reportname':reportname,'vendors_list':vendors_list}
        if allreports:
            context.update({'selectedproject':selectedproject,'selecteddiscipline':selecteddiscipline,'selectedservice':selectedservice,'selectedvendor':selectedvendor,'selectedcountry':selectedcountry,'selectedapprovalstatus':selectedapprovalstatus,'selectedpaymentstatus':selectedpaymentstatus,'selectedageingperiod':selectedageingperiod,'period':period,'selectedexceptions':selectedexceptions,'selectedcurrency':allreports.currency,'amountfilter':amountfilter})
        if reportname == 'payment_account':
            return render(request, "addpaymentaccount.html",context)
        else:
           return render(request, "invoicecompletereport.html",context)
   
    def post(self, request,reportname):
        context={}
        current_date = timezone.now()
        current_datetime = timezone.now()
       
        if request.POST:
            submitfield=request.POST.get('submitfield',None)
            reportname=request.POST.get('reportname')
            period=request.POST.get('period',None)
            getfromdate=request.POST.get('fromdate',None)
            gettodate=request.POST.get('todate',None)
            country=request.POST.getlist('country',None)
            project=request.POST.getlist('project',None)
            discipline=request.POST.getlist('discipline',None)
            service=request.POST.getlist('service',None)
            vendor=request.POST.getlist('vendor',None)
            currency=request.POST.get('currency',None)
            approvalstatus=request.POST.getlist('approvalstatus',None)
            paymentstatus=request.POST.getlist('paymentstatus',None)
            ageingperiod=request.POST.getlist('ageingperiod',None)
            vendorranking=request.POST.get('vendorranking',None)
            ageing_report=request.POST.get('ageing_report',None)
            amountfilter=request.POST.getlist('amountfilter',None)
            exceptions=request.POST.getlist('exceptions',None)
           
            if reportname=='approval_status':
               if approvalstatus == []:
                    approvalstatus=['Approved','Awaiting Approval','Disputed']
            if reportname=="ageing_report" or reportname=='unpaidinvoice_overdue':
                paymentstatus=['1']
            if reportname=="paidinvoice_paymentdays":
                paymentstatus=['2']
            if reportname == "exception_report":
                if approvalstatus == [] and exceptions == []:
                    approvalstatus=['Disputed','Returned','Rejected']
                
                

            #Get values from post method
           
            selectedcurrency = currency
            selectedproject=[int(item) for item in (ast.literal_eval(str(project)))]
            selecteddiscipline=ast.literal_eval(str(discipline))
            selectedservice=ast.literal_eval(str(service))
            selectedvendor=[int(item) for item in (ast.literal_eval(str(vendor)))]
            selectedcountry=[int(item) for item in (ast.literal_eval(str(country)))]
            selectedapprovalstatus=ast.literal_eval(str(approvalstatus))
            selectedpaymentstatus=[int(item) for item in (ast.literal_eval(str(paymentstatus)))]
            selectedageingperiod=[int(item) for item in (ast.literal_eval(str(ageingperiod)))]
            selectedexceptions=[int(item) for item in (ast.literal_eval(str(exceptions)))]
            period=period 
            #period
            if period:
                #Today
                if period == 'today':
                    todaytodate = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=0)
                    todayfromdate = todaytodate - timedelta(days=0)  
                    fromdate = todayfromdate.strftime("%Y-%m-%d %H:%M:%S")
                    todate =  todayfromdate.strftime("%Y-%m-%d %H:%M:%S")  

                #lastmonth calculation
                if period == 'lastmonth':
                    first_day_of_current_month = current_date.replace(day=1)
                    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
                    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
                    fromdate = first_day_of_previous_month.strftime("%Y-%m-%d %H:%M:%S")  
                    todate = last_day_of_previous_month.strftime("%Y-%m-%d %H:%M:%S") 

                #last Quarter
                if period == 'lastquarter':
                    current_month = current_date.month
                    current_year = current_date.year
                    if current_month in [1, 2, 3]:
                        last_quarter_end = datetime(current_year - 1, 12, 31)
                    elif current_month in [4, 5, 6]:
                        last_quarter_end = datetime(current_year, 3, 31)
                    elif current_month in [7, 8, 9]:
                        last_quarter_end = datetime(current_year, 6, 30)
                    else:
                        last_quarter_end = datetime(current_year, 9, 30)
                    last_quarter_start = last_quarter_end - timedelta(days=89)  
                    fromdate = last_quarter_start.strftime("%Y-%m-%d %H:%M:%S")   
                    todate = last_quarter_end.strftime("%Y-%m-%d %H:%M:%S")  
                
                #last Financial Year
                if period == 'financialyear':
                    fiscal_year_end_month = 3
                    current_year = current_date.year
                    if current_date.month >= fiscal_year_end_month:
                        last_financial_year_end = datetime(current_year, fiscal_year_end_month, 31)
                    else:
                        last_financial_year_end = datetime(current_year - 1, fiscal_year_end_month, 31)
                    last_financial_year_start = last_financial_year_end - timedelta(days=364) 
                    fromdate = last_financial_year_start.strftime("%Y-%m-%d %H:%M:%S")    
                    todate = last_financial_year_end.strftime("%Y-%m-%d %H:%M:%S") 
               

            #fromdate and todate
            if getfromdate:
                fromdate=datetime.strptime(getfromdate,"%d-%b-%Y")
                todate=datetime.strptime(gettodate, "%d-%b-%Y")
                
            
            filters = Q(company=request.company, status=1)
            if vendor:
                filters &= Q(vendor_id__in=vendor)
            if service:
               filters &= Q(types_service__in=service)
            if project:
                filters &= Q(project_id__in=project)
          
            queryset=[]
            countries=[]
            currencies=[]
            invoicelist=[]
            invoiceidlist=[]
            invoiceageing=[]
            invoicecurrencylist=[]
            allinvoices = Invoice.objects.filter(filters).exclude(invoice_status=1).order_by('-id')
           
            
            #discipline 
            if discipline:
                disciplinesubtype = DisciplineSubtype.objects.filter(discipline_subtype__in=discipline).values_list('id',flat=True)
                projectdevelopemt = ProjectDevelopmentSubType.objects.filter(discipline_subtype_id__in=disciplinesubtype).values_list('id',flat=True)
                contract = ContractMaster.objects.filter(projectdisciplinetype_id__in=projectdevelopemt,company=request.company,status=1).values_list('id',flat=True)
                invoice = Invoice.objects.filter(id__in=allinvoices,contractid__in=contract,company=request.company,status=1).values_list('id',flat=True)
                allinvoices = Invoice.objects.filter(id__in=invoice).order_by('-id')
               
            for invoice in allinvoices:
              #Fromdate-Todate
              if getfromdate or period:
                filter_date = InvoiceCostInvoice.objects.filter(invoice_id=invoice.id,status=1,invoice_submission_date__range=(fromdate,todate)).first()
                
              #country filter
              if country:
                countries = [int(value) for value in country]
                filter_country=Projectcreation.objects.filter(id__in=Invoice.objects.filter(id=invoice.id).values_list('project_id', flat=True)).values_list('country_id',flat=True).first()
               
              #Approval Status
              if approvalstatus:    
                               
                approval_status=InvoiceCostInvoice.objects.filter(invoice_id=invoice.id,status=1).first() 
                if approval_status!= None:
                    if approval_status.approval_status == 6 and invoice.invoice_status == 6: overallstatus= 'Disputed'
                    elif approval_status.approval_status == 1 and invoice.invoice_status == 2: overallstatus = 'Awaiting Approval'
                    elif approval_status.approval_status == 1 and invoice.invoice_status == 1: overallstatus= 'Not Yet Submitted'
                    elif approval_status.approval_status == 4 and invoice.invoice_status == 4: overallstatus='Returned' 
                    elif approval_status.approval_status == 5 and invoice.invoice_status == 5: overallstatus =  'Rejected' 
                    else: overallstatus= 'Approved' 

             
              if country != [] and approvalstatus != []:
                if filter_country in countries:
                  if overallstatus in approvalstatus:
                            if getfromdate or period:
                                if filter_date != None:
                                   queryset.append(invoice)
                            else:
                                queryset.append(invoice)
              elif  country != []  and approvalstatus == [] :
                 if filter_country in countries:
                    if getfromdate or period:
                        if filter_date != None:
                            queryset.append(invoice)
                    else:
                         queryset.append(invoice)
              
              
              elif country == []  and approvalstatus != [] :
                    if overallstatus in approvalstatus:
                        if getfromdate or period:
                            if filter_date != None:
                                queryset.append(invoice)
                        else:
                           queryset.append(invoice)
              
              else:
                 if getfromdate or period:
                      if filter_date != None:
                        queryset.append(invoice)
                 else:
                    queryset.append(invoice)
            
           #Payment Status
            if paymentstatus:
                for i in paymentstatus:
                    for j in queryset:
                        if(InvoiceCostInvoice.objects.filter(invoice_id=j.id,status=1,payment_status=i)):
                            invoicelist.append(j)
                queryset=invoicelist
            #Aging Period
            if ageingperiod:
                for i in queryset:
                    if reportname == 'ageing_report' or reportname=='unpaidinvoice_overdue':
                        currentdatetime = timezone.now()
                        statuspayment=1
                    else:
                        statuspayment=2
                        currentdatetime=InvoiceCostInvoice.objects.filter(invoice_id=i.id,status=1).values_list('payment_date',flat=True).first()
                       
                    if InvoiceCostInvoice.objects.filter(invoice_id=i.id,status=1,payment_status=statuspayment):
                        invoicesubmitted_date=InvoiceCostInvoice.objects.filter(invoice_id=i.id,status=1).values_list('invoice_submission_date',flat=True).first()
                        if i.contractid:
                            contractid=i.contractid
                        else:
                            contractid=i.invoice.contractid
                        paymentday=VendorPaymentTerms.objects.filter(contract_id=contractid,company=request.company).values_list('payment_day',flat=True).first()
                        time_difference = currentdatetime - invoicesubmitted_date
                        if reportname == 'ageing_report':
                        
                            days_difference = int(time_difference.days)-int(paymentday)
                        else:
                            days_difference = (int(time_difference.days))
                            
                       
                        for j in ageingperiod:
                            if  j == '0':
                                if days_difference <= 0:
                                    invoiceageing.append(i)
                                    invoiceidlist.append(i.id)
                            elif j == '1':
                                if days_difference >= 1 and days_difference <= 30:
                                    invoiceageing.append(i)
                                    invoiceidlist.append(i.id)
                            elif j == '2':
                                if days_difference >= 31 and days_difference <= 60:
                                    invoiceageing.append(i)
                                    invoiceidlist.append(i.id)
                            elif j == '3':
                                if days_difference >= 61 and days_difference <= 90:
                                    invoiceageing.append(i)
                                    invoiceidlist.append(i.id)
                            elif j == '4':
                                if days_difference >= 91 and days_difference <= 120:
                                    invoiceageing.append(i)
                                    invoiceidlist.append(i.id)
                            else:
                                if days_difference > 120:
                                    invoiceageing.append(i)
                                    invoiceidlist.append(i.id)
                   
                queryset=invoiceageing
            else:
                for j in queryset:
                    invoiceidlist.append(j.id)

            #currency filter
            if currency:
                for i in queryset:
                   invoice_currency = InvoiceCostInvoice.objects.filter(invoice_id=i.id,currency_id=currency).first()
                   if invoice_currency:
                        invoicecurrencylist.append(invoice_currency)
          
          
           #Exceptions
            exceptionlist=[]
            exceptionrankinglist=[]
            exceptionreasonlist=[]
            countexception=0
            if exceptions:
                for i in invoicecurrencylist:
                    countexception=0
                    if InvoiceExceptional.objects.filter(invoice_id=i.invoice_id,exceptional_type__in=exceptions,status=1):
                            exceptionlist.append(i)
                for i in exceptions:
                    for j in exceptionlist:
                        if InvoiceExceptional.objects.filter(invoice_id=j.invoice_id,exceptional_type=i,status=1):
                            countexception+=1
                    exceptionreasonlist.append((i,countexception))
                exceptionreasonlist = sorted(exceptionreasonlist, key=lambda x: x[1], reverse=True)
                exceptionreasonlist = exceptionreasonlist[:int(5)]
            else:
                exceptionlist=invoicecurrencylist
            vendorlist=ContractMasterVendor.objects.filter(company_id=request.company)  
            for i in vendorlist:
                    try:
                        count=0
                        contract=ContractMaster.objects.filter(contractvendor_id=i.id,status=1)  
                        invoicelist=Invoice.objects.filter(contractid__in=contract,status=1).exclude(invoice_status=1)
                
                        for j in invoicelist:
                            for k in exceptionlist:
                                invoicecostcount=InvoiceCostInvoice.objects.filter(id=k.id,invoice_id=j.id,currency_id=currency)
                                if invoicecostcount:
                                    count += 1
                            
                        exceptionrankinglist.append((i,count))
                    except:
                        pass
            exceptionrankinglist = sorted(exceptionrankinglist, key=lambda x: x[1], reverse=True)
            exceptionrankinglist = exceptionrankinglist[:int(5)]
            #Approval Status Report
            months_data = [] 
           
            projectlist=[]
            aprrovalstatus_invoicelist=[]
            if reportname == 'payment_status' or reportname == 'approval_status' or reportname == 'ageing_report':
                   
                    for i in invoicecurrencylist:
                        contractid=Projectcreation.objects.filter(id=(ContractMaster.objects.filter(id=(Invoice.objects.filter(id=i.invoice_id).values_list('contractid',flat=True).first())).values_list('projects_id',flat=True).first())).first()
                        projectlist.append(contractid.id)
                        aprrovalstatus_invoicelist.append(i.id)
                    projectlist=list(set(projectlist))
                   
            elif reportname == 'submission_count':
                    # Convert the input date strings to datetime objects
                    if period:
                        input_datetimefrom = datetime.strptime(fromdate, "%Y-%m-%d %H:%M:%S")
                        input_datetimeto = datetime.strptime(todate, "%Y-%m-%d %H:%M:%S")
                    else:
                        input_datetimefrom = fromdate
                        input_datetimeto = todate
                    start_date = (input_datetimefrom.year, input_datetimefrom.month, input_datetimefrom.day)
                    end_date = (input_datetimeto.year, input_datetimeto.month, input_datetimeto.day)
                    current_date = datetime(input_datetimefrom.year, input_datetimefrom.month, 1)
                    while current_date <= input_datetimeto:
                        start_of_month = datetime(current_date.year, current_date.month, 1)
                        _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
                        end_of_month = datetime(current_date.year, current_date.month, days_in_month)
                        month_name = current_date.strftime('%B')
                        months_data.append((start_of_month, end_of_month, month_name,current_date.year))
                        # Move to the next month
                        if current_date.month == 12:
                            current_date = datetime(current_date.year + 1, 1, 1)
                        else:
                            current_date = datetime(current_date.year, current_date.month + 1, 1)

                   
                    
            # #Rankingvendor
            vendorlist=[]
            rankinglist=[]
            if vendorranking:
                vendorlist=ContractMasterVendor.objects.filter(company_id=request.company,status=1)  
                for i in vendorlist:
                    amount=0
                    contract=ContractMaster.objects.filter(contractvendor_id=i.id,status=1)  
                    invoicelist=Invoice.objects.filter(contractid__in=contract,status=1).exclude(invoice_status=1)
                
                    for j in invoicelist:
                        for k in invoicecurrencylist:
                            invoicecostamount=InvoiceCostInvoice.objects.filter(id=k.id,invoice_id=j.id,currency_id=currency)
                            if invoicecostamount:
                                amount += int(gettotalgrossamountint(invoicecostamount))
                        
                    rankinglist.append((i,amount))
                rankinglist = sorted(rankinglist, key=lambda x: x[1], reverse=True)
                rankinglist = rankinglist[:int(vendorranking)]
               
           #partially_paid
            partialypaid_invoicelist=[]
            if reportname == 'partially_paid':
                for i in invoicecurrencylist:
                    paid_invoice=InvoiceCostInvoice.objects.filter(id=i.id,payment_status=2).first()
                    if paid_invoice:
                        paymentdetails=PaymentInstruction.objects.filter(invoicecost_id=paid_invoice.id).first()
                        if paymentdetails:
                            if paymentdetails.pending_amount != 0:
                                partialypaid_invoicelist.append(i)
            if submitfield == 'draft': 
               
                kwargs = {
                    'country': country,
                    'project': project,
                    'discipline': discipline,   
                    'service': service,
                    'vendor': vendor,
                    'approvalstatus': approvalstatus,
                    'paymentstatus': paymentstatus,
                    'ageingperiod': ageingperiod,
                    'company':request.company,
                    'reportname':reportname,
                    'ageingperiod':ageingperiod,
                    'ranklist':vendorranking,
                    'exceptions':exceptions,
                    'amountfilter':amountfilter
                }
                if currency:
                    kwargs['currency'] = currency

                if getfromdate:
                    formatted_fromdate = datetime.strptime(getfromdate, '%d-%b-%Y').strftime('%Y-%m-%d')
                    formatted_todate = datetime.strptime(gettodate, '%d-%b-%Y').strftime('%Y-%m-%d')
                    kwargs['getfromdate'] = formatted_fromdate
                    kwargs['gettodate'] = formatted_todate
                elif period:
                    kwargs['period'] = period
                if submitfield=='save':
                    kwargs['status']=0
                if kwargs:
                    if CompleteReport.objects.filter(reportname=reportname,company=request.company):
                        CompleteReport.objects.filter(reportname=reportname).update(**kwargs)
                    else:
                        CompleteReport.objects.create(**kwargs)
                    return redirect('invoice:listinvoicereport')    
            countries=Countries.objects.all()
            projects=Projectcreation.objects.filter(company=request.company)
            discipline_subtype = DisciplineSubtype.objects.filter(status=1).values_list('discipline_subtype', flat=True).distinct()
            vendors=ContractMasterVendor.objects.filter_company(request.company,1)
            company=Settings.objects.filter(company_id=request.company.id).first()
            getcurrencylist=ast.literal_eval(company.currency)
            companycurrency=Basecountries.objects.filter(id__in=getcurrencylist)
            selectedcurrencysymbol=Basecountries.objects.filter(id=currency).first()
            
            #PDF Generate
            request.session['amountfilter'] = amountfilter
            if reportname=='approval_status':
                 request.session['invoice_ids'] = [invoice for invoice in projectlist]
                 request.session['selectedapprovalstatus']=selectedapprovalstatus
                 request.session['aprrovalstatus_invoicelist']=aprrovalstatus_invoicelist
            elif reportname=='submission_count':
                months_data_serializable = [(str(item[0]), str(item[1]), item[2], item[3]) for item in months_data]
                request.session['months_data'] = json.dumps(months_data_serializable)
            elif reportname=='vendors_ranking':
                rankinglist_serializable = [(item[0].id, item[1]) for item in rankinglist]
                request.session['rankinglist'] = json.dumps(rankinglist_serializable)
            elif reportname=='payment_status':
                request.session['ageing_report']=ageing_report
                request.session['invoice_ids'] = [invoice.id for invoice in invoicecurrencylist]
            elif reportname=='partially_paid':
                 request.session['invoice_ids'] = [invoice.id for invoice in partialypaid_invoicelist]
            elif reportname=='exception_report':
                request.session['invoice_ids'] = [invoice.id for invoice in exceptionlist]
            else:
                request.session['invoice_ids'] = [invoice.id for invoice in invoicecurrencylist]
            request.session['selectedcurrencysymbol_id'] = selectedcurrencysymbol.id
           
        #Chart Modules
            #Approval Status Chart
            projectname=[]
            approvalstatus_matrix=[]
            if reportname == 'approval_status':
                approvalstatus_matrix = [[0 for _ in range(len(projectlist))] for _ in range(len(selectedapprovalstatus))]
                for i, project in enumerate(projectlist):
                    projectname.append(getprojectname_only(project))
                    for j, status in enumerate(selectedapprovalstatus):
                        finalamount = statusvalue(project, status, aprrovalstatus_invoicelist)
                        approvalstatus_matrix[j][i] = finalamount
            
            #Invoice submission count chart
            year_month=[]
            invoicecount=[]
            if reportname =='submission_count':
                invoicesubmissionlist = getinvoicecount(invoicecurrencylist,months_data)
                for i,j,k in invoicesubmissionlist:
                    year_month.append(str(i)+str(j))
                    invoicecount.append(k)
            #Payment Status chart
            paidamount=[]
            unpaidamount=[]
            for project in projectlist:
                    projectname.append(getprojectname_only(project))   
                    paid_amount, unpaid_amount = getpaidamount(project, invoicecurrencylist)
                    paidamount.append(paid_amount)
                    unpaidamount.append(unpaid_amount)
            #Ranking Vendor chart
            vendorname=[]
            vendorrankingamount=[]
            if reportname =='vendors_ranking':
                for i,amount in rankinglist:
                    vendorrankingamount.append(amount)
                    vendorname.append(i.vendor_name)
                vendorname.append('Total Result')
                vendorrankingamount.append(float(rankinglisttotalamount(rankinglist).replace(',', '')))
            #unpaidinvoice Overdue Chart
            unpaidinvoice_count = {
                'Not Yet Due':0,
                '1-30 days': 0,
                '31-60 days': 0,
                '61-90 days': 0,
                '91-120 days': 0,
                'Over 120 days': 0
            }
            min_amount = {
                'Not Yet Due':0,
                '1-30 days': 0,
                '31-60 days': 0,
                '61-90 days': 0,
                '91-120 days': 0,
                'Over 120 days': 0
            }
            max_amount = {
                'Not Yet Due':0,
                '1-30 days': 0,
                '31-60 days': 0,
                '61-90 days': 0,
                '91-120 days': 0,
                'Over 120 days': 0
            }
            if reportname == 'unpaidinvoice_overdue' or reportname == 'paidinvoice_paymentdays' :
                for invoice in invoicecurrencylist:
                    invdisval = invoicegrossamount(invoice.id)
                    invdistax = invoicetaxamount(invoice.id)
                    invoiceamount = float(replacecommaid(addvalues(invdisval,invdistax)))
                    if reportname == 'unpaidinvoice_overdue':
                        days_difference = getdaysforunpaid(invoice.invoice.id, invoice.invoice.contractid, invoice.invoice.company_id)
                    else:
                        days_difference = getdaysforpayment(invoice.invoice.id,invoice.invoice.contractid,invoice.invoice.company_id) 
                    if days_difference == 0:
                         unpaidinvoice_count['Not Yet Due'] += 1
                         if min_amount['Not Yet Due'] == 0:
                             min_amount['Not Yet Due'] = invoiceamount
                         else:
                            if min_amount['Not Yet Due'] > invoiceamount:
                               min_amount['Not Yet Due'] = invoiceamount
                         if max_amount['Not Yet Due'] == 0:
                            max_amount['Not Yet Due'] = invoiceamount
                         else:
                             if max_amount['Not Yet Due'] < invoiceamount:
                                max_amount['Not Yet Due'] = invoiceamount
                    elif days_difference >= 1 and days_difference <= 30:
                        unpaidinvoice_count['1-30 days'] += 1
                        if min_amount['1-30 days'] == 0:
                             min_amount['1-30 days'] = invoiceamount
                        else:
                            if min_amount['1-30 days'] > invoiceamount:
                               min_amount['1-30 days'] = invoiceamount
                        if max_amount['1-30 days'] == 0:
                            max_amount['1-30 days'] = invoiceamount
                        else:
                             if max_amount['1-30 days'] < invoiceamount:
                                max_amount['1-30 days'] = invoiceamount
                    elif days_difference >= 31 and days_difference <= 60:
                        unpaidinvoice_count['31-60 days'] += 1
                        if min_amount['31-60 days'] == 0:
                             min_amount['31-60 days'] = invoiceamount
                        else:
                            if min_amount['31-60 days'] > invoiceamount:
                               min_amount['31-60 days'] = invoiceamount
                        if max_amount['31-60 days'] == 0:
                            max_amount['31-60 days'] = invoiceamount
                        else:
                             if max_amount['31-60 days'] < invoiceamount:
                                max_amount['31-60 days'] = invoiceamount
                    elif days_difference >= 61 and days_difference <= 90:
                        unpaidinvoice_count['61-90 days'] += 1
                        if min_amount['61-90 days'] == 0:
                             min_amount['61-90 days'] = invoiceamount
                        else:
                            if min_amount['61-90 days'] > invoiceamount:
                               min_amount['61-90 days'] = invoiceamount
                        if max_amount['61-90 days'] == 0:
                            max_amount['61-90 days'] = invoiceamount
                        else:
                             if max_amount['61-90 days'] < invoiceamount:
                                max_amount['61-90 days'] = invoiceamount
                    elif days_difference >= 91 and days_difference <= 120:
                        unpaidinvoice_count['91-120 days'] += 1
                        if min_amount['91-120 days'] == 0:
                             min_amount['91-120 days'] = invoiceamount
                        else:
                            if min_amount['91-120 days'] > invoiceamount:
                               min_amount['91-120 days'] = invoiceamount
                        if max_amount['91-120 days'] == 0:
                            max_amount['91-120 days'] = invoiceamount
                        else:
                             if max_amount['91-120 days'] < invoiceamount:
                                max_amount['91-120 days'] = invoiceamount
                    elif days_difference > 120:
                        unpaidinvoice_count['Over 120 days'] += 1
                        if min_amount['Over 120 days'] == 0:
                             min_amount['Over 120 days'] = invoiceamount
                        else:
                            if min_amount['Over 120 days'] > invoiceamount:
                               min_amount['Over 120 days'] = invoiceamount
                        if max_amount['Over 120 days'] == 0:
                            max_amount['Over 120 days'] = invoiceamount
                        else:
                             if max_amount['Over 120 days'] < invoiceamount:
                                max_amount['Over 120 days'] = invoiceamount
            
            unpaidinvoice_range = list(unpaidinvoice_count.keys())
            unpaidinvoice_counts = list(unpaidinvoice_count.values())
            min_amount = list(min_amount.values())
            max_amount = list(max_amount.values())
            #Ageing chart
            keys = ['Not Yet Due','1-30 days', '31-60 days', '61-90 days', '91-120 days', 'Over 120 days']
            num_charts = len(projectlist) 
            chartageingamount = [{key: 0 for key in keys} for _ in range(num_charts)]
                     
            ageningamountlist={
                'Not Yet Due':0,
                '1-30 days': 0,
                '31-60 days': 0,
                '61-90 days': 0,
                '91-120 days': 0,
                'Over 120 days': 0
            }
            currentdatetime = timezone.now()
            statuspayment=1
            project_data = {}
            if reportname == 'ageing_report':
                def ageingreport_fun(projectid):
                  for i in invoicecurrencylist:
                    if InvoiceCostInvoice.objects.filter(id=i.id,status=1,payment_status=statuspayment,invoice__project_id=projectid):
                        invoicesubmitted_date=InvoiceCostInvoice.objects.filter(id=i.id,status=1,invoice__project_id=projectid).values_list('invoice_submission_date',flat=True).first()
                        if i.contractid:
                            contractid=i.contractid
                        else:
                            contractid=i.invoice.contractid
                        paymentday=VendorPaymentTerms.objects.filter(contract_id=contractid,company=request.company).values_list('payment_day',flat=True).first()
                        if paymentday == None:
                            paymentday=0
                        time_difference = currentdatetime - invoicesubmitted_date
                        days_difference = (int(time_difference.days)-int(paymentday))
                        for j in ageingperiod:
                            if  j == '0':
                                if days_difference <= 0:
                                    ageningamountlist['Not Yet Due']+=1
                                    project_data[projectid]['Not Yet Due']+=1
                            elif j == '1':
                                if days_difference >= 1 and days_difference <= 30:
                                    ageningamountlist['1-30 days']+=1
                                    project_data[projectid]['1-30 days']+=1
                            elif j == '2':
                                if days_difference >= 31 and days_difference <= 60:
                                    ageningamountlist['31-60 days']+=1
                                    project_data[projectid]['31-60 days']+=1
                            elif j == '3':
                                if days_difference >= 61 and days_difference <= 90:
                                    ageningamountlist['61-90 days']+=1
                                    project_data[projectid]['61-90 days']+=1
                            elif j == '4':
                                if days_difference >= 91 and days_difference <= 120:
                                    ageningamountlist['91-120 days']+=1
                                    project_data[projectid]['91-120 days']+=1
                            elif j == '5':
                                if days_difference > 120:
                                    ageningamountlist['Over 120 days']+=1
                                    project_data[projectid]['Over 120 days']+=1
                if ageingperiod == []:
                    ageingperiod = ['0','1','2','3','4','5']
                # ageingreport_fun(projectid=None)
                
                for i in projectlist:
                    project_data[i] = {
                        'Not Yet Due':0,
                        '1-30 days': 0,
                        '31-60 days': 0,
                        '61-90 days': 0,
                        '91-120 days': 0,
                        'Over 120 days': 0
                        }
                    ageingreport_fun(projectid=i)
            context={'allinvoices':queryset,'paymentstatus':paymentstatus,'countries':countries,'projects':projects,'discipline_subtype':discipline_subtype,'vendorslist':vendors,'companycurrency':companycurrency,'selectedcurrency':int(selectedcurrency),'selectedproject':selectedproject,'selectedvendor':selectedvendor,'selectedpaymentstatus':selectedpaymentstatus,'selectedageingperiod':selectedageingperiod,'selectedcountry':selectedcountry,'period':period,'reportname':reportname,'selecteddiscipline':selecteddiscipline,'selectedapprovalstatus':selectedapprovalstatus,'selectedapprovalstatus':selectedapprovalstatus,'selectedservice':selectedservice,'fromdate':getfromdate,'todate':gettodate,'invoicecurrencylist':invoicecurrencylist,'selectedcurrencysymbol':selectedcurrencysymbol,'selectedexceptions':selectedexceptions,'reportname':reportname,'ageing_report':ageing_report,'projectlist':projectlist,'months_data':months_data,'amountfilter':amountfilter,'rankinglist':rankinglist,'vendorranking':vendorranking,'aprrovalstatus_invoicelist':aprrovalstatus_invoicelist,'partialypaid_invoicelist':partialypaid_invoicelist,'exceptionlist':exceptionlist,'exceptionrankinglist':exceptionrankinglist,'exceptionreasonlist':exceptionreasonlist,'approvalstatus_matrix':approvalstatus_matrix,'projectname':projectname,'year_month':year_month,'paidamount':paidamount,'unpaidamount':unpaidamount,'vendorrankingamount':vendorrankingamount,'vendorname':vendorname,'download_pdf':1}
            if reportname == 'unpaidinvoice_overdue' or reportname == 'paidinvoice_paymentdays':
                context['unpaidinvoice_range']=unpaidinvoice_range
                context['unpaidinvoice_counts']=unpaidinvoice_counts
                context['min_amount']=min_amount
                context['max_amount']=max_amount
            if reportname == 'ageing_report':
                context['ageingchart_range']=list(ageningamountlist.keys())
                context['ageingchart_counts']=list(ageningamountlist.values())
                context['project_data']=project_data
            if reportname == 'submission_count':
                context['invoicecount']=invoicecount
           
        return render(request, "invoicecompletereport.html",context)


def CloseInvoiceQuery(request,pk):
    query=Invoice.objects.get(id=pk)
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
    invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
    all_invoice=', '.join(str(e) for e in invoice_number)
    accepted_member=f'Invoice No.{all_invoice} has been accepted by {request.user.name} {request.user.lastname}'
    vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
    utc_timezone = pytz.utc
    utc_time = datetime.now(utc_timezone)
    time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    file=request.FILES.get('file') 
    filename=None
    if file != None and file !='' : 
        fs = FileSystemStorage()
        file_name=file.name 
    else :
        file_name =file
    returned_count=returned_count_invoice_credit(pk,1)
    returned_user=AddNewDisputedQuery.objects.filter(query_id=pk,returned_count=returned_count).first() 
    get_dispute=AddNewDisputedQuery.objects.create_disputed_query(pk,accepted_member,request.user,time_stamp,vendor.id,file,returned_count,filename)
    if request.user.roles.id == 3 or request.user.roles.id == 2:
        disputed_invoice=DisputedInvoiceTrack.objects.create(stage=3,invoice_id=pk,status=True,user=request.user,created_at=datetime.now(),returned_count=returned_count)
        get_invoice=Invoice.objects.filter_by_id(pk).update(dispute_status=1,invoice_status=2)
        AddNewDisputedQuery.objects.filter(query_id=pk).update(query_status=1)
        InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=1)
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        main_url=f"invoice/invoicequeryhistory/{pk}"
        main_verb=f'Invoice NO.{all_invoice} Accepted for Approval'
        content=f'Invoice NO.{all_invoice} Accepted for Approval by {request.user.name} on {date_today} for {query.name_service} '
        for notifications in allVendors:
            notify_invoice_flow(request,notifications,main_url,main_verb,content)
        if returned_user:
            get_invoiceflow=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__module_id=returned_user.module_id,status=3,Invoiceflowmodules__invoice_id=pk)
            Invoiceflowmodules_id=list(get_invoiceflow.values_list('Invoiceflowmodules_id',flat=True))
            if get_invoiceflow.count() > 0:
                # invoiceflowid=get_invoiceflow.last()
                get_invoiceflow.update(status=0)
                Invoiceflowmodules.objects.filter(id__in=Invoiceflowmodules_id).update(status=0)
            url=getinvoiceroute(returned_user.module_id)
            return redirect(f'invoice:{url}', pk=pk)
    else:
        disputed_invoice=DisputedInvoiceTrack.objects.create(stage=2,invoice_id=pk,status=True,user=request.user,created_at=datetime.now(),returned_count=returned_count)
        
    return redirect('invoice:invoicequeryhistory', pk=pk)


class Generateinvoicereport(View):
    template_name = 'invoicecompletereport_pdf.html'
    def get(self,request,reportname):
        invoice_ids = request.session.get('invoice_ids')
        amountfilter = request.session.get('amountfilter')
        invoicelist=InvoiceCostInvoice.objects.filter(id__in=invoice_ids)
        selectedcurrencysymbol_id=request.session.get('selectedcurrencysymbol_id')
        selectedcurrencysymbol=Basecountries.objects.filter(id=selectedcurrencysymbol_id).first()
        companyImage= Companies.objects.filter(id=request.company.id).first()
        
        context = {'company': request.company,'invoicecurrencylist':invoicelist,'reportname':reportname,'selectedcurrencysymbol':selectedcurrencysymbol,'amountfilter':amountfilter}
        if reportname == 'approval_status':
            selectedapprovalstatus = request.session.get('selectedapprovalstatus') 
            aprrovalstatus_invoicelist=request.session.get('aprrovalstatus_invoicelist')
            context['projectlist'] = invoicelist.values_list('id',flat=True)
            context['selectedapprovalstatus']=selectedapprovalstatus
            context['aprrovalstatus_invoicelist']=aprrovalstatus_invoicelist
        elif reportname=='submission_count':
                months_data_serializable = json.loads(request.session['months_data'])
                months_data = [(datetime.fromisoformat(item[0]), datetime.fromisoformat(item[1]), item[2], item[3]) for item in months_data_serializable]
                context['months_data']=months_data  
        elif reportname=='vendors_ranking':
            rankinglist_serializable = json.loads(request.session['rankinglist'])
            rankinglist = [(item[0], item[1]) for item in rankinglist_serializable]
            context['rankinglist']=rankinglist
        elif reportname=="partially_paid":
            context['partialypaid_invoicelist']=invoicelist
        elif reportname=='exception_report':
            context['exceptionlist']=invoicelist
       
              
        if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB') 
            image = image.resize((120, 80))     
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            imageurl = None
        filename=reportname+'.pdf'   
      
        context['imageurl']=imageurl
        output_coversheet = render_to_string(self.template_name,context,request)
        css = CSS(string=getreport_css(encoded_image))
        pdf_buffer = BytesIO()
        HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename='+filename+''
        return response
    
       
class Listinvoicereport(View):
    def get(self, request):
        reports=CompleteReport.objects.filter(company=request.company).order_by('-id')
        starredreports=starredreport.objects.filter(company=request.company)
        get_settings = Settings.objects.get_company(request.company).values_list('currency',flat=True).first()
        if get_settings!=None:
            currency = Basecountries.objects.get_by_id(literal_eval(get_settings))
            currency_count=currency.count()
        else:
            currency_count=0
            currency=[]
        context={'reports':reports,'starredreports':starredreports,'currency_count':currency_count}
        return render(request,'listinvoicereport.html',context)
    
class DisputedInvoiceApproval(View):
    def get(self, request,pk):
        document_list=getDocumentlist()
        contractid=Invoice.objects.get_by_id(pk)
        print(f'{contractid} contractid {pk} pk')
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(contractid.contractid)
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        if (invoicedetail == None):
            invoicedetail=""
        invoiceflow_modules=Invoiceflowmodules.objects.filter_by_module_id(pk,0,2).first()
        get_settlement_count=SettlementInvoice.objects.filter(invoice_id=pk,company=request.company).count()
        get_role_id=invoiceflow_modules.flowlevel_module.role_id
        roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
        context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,'get_role_id':get_role_id,'roles_rights':roles_rights,'settlement_count':get_settlement_count}
        return render(request, "disputedinvoiceapproval.html",context)
    def post(self, request,pk):
        if request.POST:
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            get_user=request.user
            print(f'submit_type {submit_type}, submit_name {submit_name}, comments {comments}')
            if submit_type == '6':
                percentage_val=request.POST.get('settlement_val')
                invoice_detail = Invoice.objects.get_by_id(pk)
                get_invoice_value=InvoiceCostInformation.objects.get_invoice_id(pk,1)
                if(get_invoice_value.count() >= 1):
                    get_settlement_val=get_invoice_value.first()
                    match =''.join(filter(str.isdigit, get_settlement_val.finalvalue))
                    get_invoice="{:.2f}".format(float(match)*(float(percentage_val)/100))
                    #SettlementInvoice.objects.create(settlement=percentage_val,invoice_id=pk,user=get_user,invoice_value=get_invoice,company=request.company)
                invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
                all_invoice=', '.join(str(e) for e in invoice_number)
                main_url="credit/list"
                vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
                vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
                allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
                main_verb='Invoice Moved to Settlement Process'
                content=f'Create Credit Note for Invoice NO.{submit_name} by {request.user.name} for {invoice_detail.name_service} '
                for notifications in allVendors:
                    notify_invoice_flow(request,notifications,main_url,main_verb,content)
                    invoice_Settlement_mail(request,vendor_data,vendor,submit_name,invoice_detail,comments,all_invoice)
                # invoice_submission_fpoc(request.company,recipientuser,invoice_type.first(),getvendordetails,request)
                return redirect("invoice:listdisputeinvoices")
            else:
                Invoice.objects.filter(id=pk).update(invoice_status=2)
                InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=1)
                invoice_flow_func(pk,2,request,comments,submit_type,submit_name)
                return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            return render(request, "disputedinvoiceapproval.html",context)
        
class Viewinvoicereport(View):
    def get(self, request,pk):
        context={'pk':pk}
        invoice=CompleteReport.objects.filter(id=pk).first()
        invoicelist=Invoice.objects.filter(id__in=(ast.literal_eval((invoice.invoiceid))))
        context={'allinvoices':invoicelist,'pk':pk,'invoice':invoice}
        return render(request, "viewinvoicereport.html",context)
    
class Starredreport(View):
    def post(self,request):
        reportname = request.POST.get('reportname')
        status = request.POST.get('status')
        stattedfilter=starredreport.objects.filter(reportname=reportname,company=request.company)
        if stattedfilter:
           stattedfilter.update(starred=status)
        else:
            starredreport.objects.create(reportname=reportname,company=request.company,starred=status)
        return JsonResponse  


def updatePaymentInstruction(request):
    print('request',request.POST)
    id=request.POST.get('id')
    instuctions=PaymentInstruction.objects.filter(invoicecost__invoice_id=id).update(status=False,pi_number=None)
    print(f'instuctions {instuctions}')
    return JsonResponse({'status':True})

class Getinvoicereport(View):
    def post(self,request):
        reportid=request.POST.get('reportid')
        reportdetails=CompleteReport.objects.filter(id=reportid).first()
        print('reportdetails---',reportdetails)
        return JsonResponse({'period':reportdetails.period,'gettodate':reportdetails.gettodate,'getfromdate':reportdetails.getfromdate})
    

def invoice_return_flow(invoice_id,module_id,submit_type,comments,request,submit_name):
    print(f'module_id ,{module_id}')
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    current_date=datetime.now()
    # invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(invoice_id,module_id)
    invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoiceids(invoice_id,module_id)
    if (invoiceflow_modules.count() > 0):
        flow_modules=list(invoiceflow_modules.values_list('id',flat=True))
        Invoiceflowmodules.objects.filter(id__in=list(invoiceflow_modules.values_list('id',flat=True))).update(status=1)
        Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_modules,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date,returned=1,returned_date=current_date)
        # Invoiceflowmodules.objects.updateinvoiceflowmodules(invoiceflow_modules.id)
        # Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,submit_type,comments)
        # Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=invoiceflow_modules.id,user=request.user.id).update(returned=1,returned_date=current_date)
    Invoice.objects.filter(id=invoice_id).update(invoice_status=4,dispute_status=0 , return_dispute_status=1)
    InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1).update(approval_status=4,approval_date=current_date)
    returnCheck=DisputedInvoiceTrack.objects.filter(invoice_id=invoice_id).count()
    invoice_detail = Invoice.objects.get_by_id(invoice_id)
    invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1).values_list('invoice_number',flat=True))
    all_invoice=', '.join(str(e) for e in invoice_number)
    content=f'Invoice {all_invoice} has been {submit_name} for clarification by {request.user.name} on {date_today} for {invoice_detail.name_service} '
    vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
    vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
    allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
    main_url=f'invoice/invoicequeryhistory/{invoice_id}'
    main_verb='Invoice '+submit_name+' for Clarification.' 
    if module_id == 1 or module_id == 2:
        for notifications in allVendors:
            invoive_return_mail(request,notifications,vendor,submit_name,invoice_detail,comments,all_invoice,submit_type)
            notify_invoice_flow(request,notifications,main_url,main_verb,content)
    if returnCheck== 0:
        invoice_detail = Invoice.objects.get_by_id(invoice_id)
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        DisputedInvoiceTrack.objects.create(user_id=request.user.id,invoice_id=invoice_id,stage=1,created_at=current_date,module_id=module_id,returned_count=1)
        AddNewDisputedQuery.objects.reason_for_dispute(invoice_id,comments,request.user,time_stamp,vendor.id,module_id,1)
    else:
        main_url="invoice/vendorbasedinvoice"
        invoice_detail = Invoice.objects.get_by_id(invoice_id)
        get_prev_user=AddNewDisputedQuery.objects.filter(query_id=invoice_id).last()
        try:
            returned_time=get_prev_user.returned_count+1
        except:
            returned_time=0
        #notify_invoice_flow(request,get_prev_user.user,main_url,main_verb,content)
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
        DisputedInvoiceTrack.objects.create(user_id=request.user.id,invoice_id=invoice_id,stage=1,created_at=current_date,module_id=module_id,returned_count=returned_time)
        AddNewDisputedQuery.objects.reason_for_dispute(invoice_id,comments,request.user,time_stamp,vendor.id,module_id,returned_time)
        #BackToDisputeQuery.objects.reason_for_dispute(invoice_id,comments,request.user,time_stamp,vendor.id,module_id)
    return


class ReturnedQueryHandling(View):
    def get(self,request,pk):
        query=Invoice.objects.get_by_id(pk)
        ref_num=ContractMaster.objects.filter(id=query.contractid).first()
        get_settlement_count=SettlementInvoice.objects.filter(invoice_id=pk,company=request.company).count()
        print(f'get_settlement_count {get_settlement_count}')
        get_flow=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id=query.id,Invoiceflowmodules__module_id=2,Invoiceflowmodules__status=1)
        get_flow=Invoiceflowmodules.objects.filter(company_id=request.company.id,invoice_id=query.id,status=1,module_id=2)
        # print('get_flow_usercomment',get_flow_usercomment)
        vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
        # vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
        # allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=18,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights).count()
        wcc_files=other_documents()
        print(f'wcc_files {wcc_files}')
        get_status=DisputedInvoiceTrack.objects.filter(invoice_id=pk,stage=4).first()
        querylist=BackToDisputeQuery.objects.filter(query_id=pk)
        data={'querylists':querylist,'query':query,'pk':pk,'contact_person':vendor,'wcc_files':wcc_files,'settlement_count':get_settlement_count,'ref_num':ref_num,'get_status':get_status,'get_dispute_users':get_dispute_users}
        return render(request,'returnedqueryhandling.html',data)
    
    def post(self,request,pk):
        print(f' reqe {request.POST}')
        query=Invoice.objects.get(id=pk)
        print(f'query {query}')
        get_submit=request.POST.get('submit_type')
        print(f'get_submit {get_submit}')
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=18,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights)
        if(get_submit):
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            get_user=request.user
            print(f'submit_type {submit_type}, submit_name {submit_name}, comments {comments}')
            invoice_detail = Invoice.objects.get_by_id(pk)
            vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            if submit_type == '8':
                file=request.POST.get('file')
                if file != None and file !='' : 
                    fs = FileSystemStorage()
                    file_name=file.name 
                else :
                    file_name =file
                get_exceptional=request.POST.getlist('exceptional')
                exceptional_list=[InvoiceExceptional(invoice_id=pk,exceptional_type=i,confirm_dispute=1) for i in get_exceptional]
                InvoiceExceptional.objects.bulk_create(exceptional_list)
                Invoice.objects.filter(id=pk).update(dispute_status=2,invoice_status=6)
                InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=6)
                reason=f'Invoice No.{all_invoice} has been moved to Dispute Committee '
                main_url="invoice/listdisputeinvoices"
                for user in get_dispute_users:
                    notify_invoice_flow(request,user,main_url,reason,reason)
                returned_count=returned_count_invoice_credit(pk,1)
                AddNewDisputedQuery.objects.create_disputed_query(pk,reason,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                return redirect("invoice:listdisputeinvoices")
            elif submit_type == '6':
                percentage_val=request.POST.get('settlement_val')
                file=request.POST.get('file')
                if file != None and file !='' : 
                    fs = FileSystemStorage()
                    file_name=file.name 
                else :
                    file_name =file
                get_approved_percentage=100 - float(percentage_val)
                get_invoice_value=InvoiceCostInformation.objects.get_invoice_id(pk,1)
                if(get_invoice_value.count() >= 1):
                    get_settlement_val=get_invoice_value.first()
                    match =''.join(filter(str.isdigit, get_settlement_val.finalvalue))
                    get_invoice="{:.2f}".format(float(match)*(float(percentage_val)/100))
                    #SettlementInvoice.objects.create(settlement=percentage_val,invoice_id=pk,user=get_user,invoice_value=get_invoice,company=request.company)
                reason=f'Invoice No {all_invoice} has been approved for {int(get_approved_percentage)}% and disputed for {percentage_val}% by {request.user.name} '
                main_url="credit/list"
                vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
                returned_count=returned_count_invoice_credit(pk,1)
                AddNewDisputedQuery.objects.create_disputed_query(pk,reason,request.user,time_stamp,vendor.id,file,returned_count,file_name)
                allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
                main_verb='Invoice Moved to Settlement Process'
                content=f'Create Credit Note for invoice Invoice {submit_name} by {request.user.name} for {invoice_detail.name_service} '
                for notifications in allVendors:
                    notify_invoice_flow(request,notifications,main_url,main_verb,content)
                    invoice_Settlement_mail(request,vendor_data,vendor,submit_name,invoice_detail,comments,all_invoice)
                # invoice_submission_fpoc(request.company,recipientuser,invoice_type.first(),getvendordetails,request)
                return redirect('invoice:invoicequeryhistory',pk=pk)
            else:
                get_module=BackToDisputeQuery.objects.filter(query_id=pk).first()
                Invoice.objects.filter(id=pk).update(invoice_status=2)
                InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=1)
                print(f'get_module.module_id {get_module.module.id}')
                Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=get_module.module_id).update(status=0)
                invoice_flow_func(pk,get_module.module_id,request,comments,submit_type,submit_name)
                print(f'pk {pk},comments {comments},submit_type {submit_type},submit_name {submit_name}')
                return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
        else:
            deniedreason=request.POST.get('message')
            vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
            file=request.FILES.get('file')
            if file != None and file !='' : 
                fs = FileSystemStorage()
                file_name=file.name 
                file = fs.save(file.name, file)
            else :
                file_name =file
                
            get_dispute=BackToDisputeQuery.objects.create_disputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,file)
          
        
            # scheme=request.scheme
            # gethost=request.get_host()
            # if request.user.roles_id == 4:
            #     sender = User.objects.get_by_id(request.user.id)
            #     url=f"{scheme}://{gethost}/invoice/invoicequeryhistory/{query.id}"
            #     description=f'Reply received from {vendor.vendor_name}'
            #     getCompanyUserlist(request,sender,url,'Reply Received for Disputed Invoice',description)
            # else:
            #     print('To Vendor')
            #     sender = User.objects.filter(id=request.user.id).first()
            #     recipients = User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
            #     print('recipients',recipients)
            #     url=f"{scheme}://{gethost}/invoice/invoicequeryhistory/{query.id}"
            #     notify.send(sender, recipient=recipients,data=url, verb='Reply Received for Disputed Invoice', description=f'Reply received from {sender.name} {sender.lastname if sender.lastname != None else ""}')
            return redirect('invoice:returnqueryhandling',pk=pk)

# def convert_to_digitsno(string_val):
#     match =''.join(filter(str.isdigit, string_val))
#     get_invoice="{:.2f}".format(float(match))
#     return get_invoice

def convert_to_digits(string_val):
    match = ''.join(filter(lambda x: x.isdigit() or x == '.', string_val))
    get_invoice="{:.2f}".format(float(match))
    return get_invoice

def convert_six_digits(string_val):
    match = ''.join(filter(lambda x: x.isdigit() or x == '.', string_val))
    get_invoice="{:.2f}".format(float(match))
    return get_invoice

def get_total_credit_val(request):
    credit_ids=request.POST.getlist('id[]')
    invoiceid=request.POST.get('invoiceid')
    credit_note_base=CreditNoteMappingBase.objects.filter(invoice_id=invoiceid,credit_note_id__in=credit_ids)
    # invoice_id=request.POST.get('invoice_id')
    # print(f'invoice_id {invoice_cost},invoice_id {invoice_id}')
    # get_invoice=Invoice.objects.get_by_id(invoice_id)
    # CreditNoteInvoice.objects.filter(credit__contract_id=get_invoice.contractid,status=1,credit__usage_status__in=[1,2])
    # print(f'get_invoice {get_invoice}')
    get_credit=CreditNote.objects.filter(id__in=credit_ids,status=1,credit_status=2,approval_status=4)
    
    # print(f'pending_val {pending_val}')
    # get_credit=CreditNoteInvoice.objects.filter(id__in=credit_ids,status=1,credit__credit_status=2)
    empty_li=[]
    for credit in get_credit:
        get_credit_note=CreditNoteContractInvoice.objects.filter(credit_id=credit.id)
        credit_current_datas={'id':credit.id,'contract_credit':list(get_credit_note.values('id','new_netpayable','symbol','vendor_split_invoice'))}
        for i,j in zip(get_credit_note,range(len(list(get_credit_note.values_list('id',flat=True))))):
            pending_val=CreditNoteMappingBase.objects.filter(credit_note_split_id=i.id,status=True).last()
            if pending_val:
                credit_current_datas['contract_credit'][j]['new_netpayable']=int(float(pending_val.pending_credit_value))
                # print(f'i {i}')
        empty_li.append(credit_current_datas)
    output_data = []
    aggregated_values = {}
    for item in empty_li:
        for credit in item['contract_credit']:
            vendor_split_invoice = credit['vendor_split_invoice']
            payment_amount = credit['new_netpayable']
            if type(payment_amount) == str:
                payment_amount=convert_to_digits(payment_amount)
            if vendor_split_invoice in aggregated_values:
                aggregated_values[vendor_split_invoice] += float(payment_amount)
            else:
                aggregated_values[vendor_split_invoice] = float(payment_amount)
    for i, j in aggregated_values.items():
        output_data.append({'id': i, 'contract_credit': f"{j:,}"})
    print(f'output_data {output_data}')
    if(credit_note_base.count() > 0):
        for i in output_data:
            contract_credit=float(i['contract_credit'].replace(',',''))
            credit_used_datas=CreditNoteMappingBase.objects.filter(invoice_id=invoiceid,credit_note_id__in=credit_ids,invoice_split_id=i['id'])
            print(f'credit_used_datas  {credit_used_datas}')
            for y in credit_used_datas:
                contract_credit+=float(y.credit_payable)
            i['contract_credit']=f"{contract_credit:,}"

    print('o/p',output_data)

    # credit_val=0
    # for credit in get_credit_note:
    #     if credit.payment_currency_amount != None:
    #         print(f'credit {credit.payment_currency_amount}')
    #         get_invoice=convert_to_digit(credit.payment_currency_amount)
    #         credit_val+=float(get_invoice)
    #     else:
    #         credit_val+=0
    # print(f'vendor_split_invoice__currency_id {credit_val}')
    # a= '{:,}'.format(int(credit_val))
    return JsonResponse({'status':True,'data':output_data})

def convert_to_digit(string_val):
    match =''.join(filter(str.isdigit, string_val))
    # get_invoice="{:.2f}".format(float(match))
    return float(match)

class AddPaymentAccount(View):
    def get(self,request):
        currenctlist=[]
        vendors_list=ContractMasterVendor.objects.filter_company(request.company,1)
        currency = Settings.objects.filter(company=request.company).first()
        separated_values = ast.literal_eval(currency.currency)
        for i in separated_values:
           currenctlist.append(Basecountries.objects.get(id=i))
        data={'vendors_list':vendors_list,'companycurrency':currenctlist}
        return render(request,'addpaymentaccount.html',data)

    def post(self,request):
        invoicecurrencylist=[]
        inputfield=request.POST.get('inputfield',None)
        vendor=request.POST.get('vendor',None)
        currency=request.POST.get('currency',None)
        currenctlist=[]
        vendors_list=ContractMasterVendor.objects.filter_company(request.company,1)
        currency_list = Settings.objects.filter(company=request.company).first()
        separated_values = ast.literal_eval(currency_list.currency)
        currency_symbol=Basecountries.objects.getone_by_id(currency)
        for i in separated_values:
           currenctlist.append(Basecountries.objects.get(id=i))
        data={}
        if inputfield == '1':
            amount=request.POST.getlist('amount',None)
            paymentfile=self.request.FILES.getlist('image',None)
            for i in range(len(amount)):
                PaymentAccount.objects.create(vendor_id=vendor,currency_id=currency,amount=amount[i],paymentfile=paymentfile[i],company=request.company,status=1)
        invoicecurrencylist=unpaidinvoice_paymentact(vendor,request.company,currency)    
        paymentacct_details=PaymentAccount.objects.filter(vendor_id=vendor,currency_id=currency,company=request.company).exclude(status=0) 
        data.update({'vendors_list':vendors_list,'companycurrency':currenctlist,'invoicecurrencylist':invoicecurrencylist,'select_vendor':int(vendor),'select_currency':int(currency),'paymentacct_details':paymentacct_details,'currency_symbol':currency_symbol}) 
        return render(request,'addpaymentaccount.html',data) 
    
def getpaymentacctfile(request,id): 
    filefield=PaymentAccount.objects.filter(id=id).first()
    getfilename=filefield.paymentfile.path
    getextension=pathlib.Path(getfilename).suffix
    if (getextension == ".pdf"):  
        with open(getfilename, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response
    else:
        image_data = open(getfilename, "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg") 

def delete_paymentact(request,id):
    PaymentAccount.objects.filter(id=id).update(status=0)
    return JsonResponse({'status':True})

class editpaymentact(View):
    def get(self,request,id):
       paymentact_details=PaymentAccount.objects.filter(id=id).first()
       data={'paymentact_details':paymentact_details}
       return render(request,'editpaymentaccount.html',data)
    def post(self, request, id):
        amount = self.request.POST.get('amount', None)
        paymentfile = self.request.FILES.get('image', None)
        payment_account = PaymentAccount.objects.filter(id=id).first()
        if paymentfile: 
            payment_account.paymentfile.save(paymentfile.name, paymentfile)
        if amount is not None:
            payment_account.amount = amount
            payment_account.save()
        return redirect('invoice:add_paymentonaccount') 
    
class AllocateInvoice(View):
    def get(self,request,id):
        paymentaccount=PaymentAccount.objects.filter(id=id).first()
        invoicecurrencylist=unpaidinvoice_paymentact(paymentaccount.vendor,request.company,paymentaccount.currency)  
        data={'invoicecurrencylist':invoicecurrencylist,'paymentaccount':paymentaccount,'id':id}
        return render(request,'allocateinvoice.html',data)
    def post(self,request,id):
        amountallocated=request.POST.get('saveallocate')
        paymentacct_id=request.POST.get('paymentacct_id')
        invoiceid=request.POST.getlist('invoiceid')
        draft_field=request.POST.get('draft_field',None)
        vendor_vin=request.POST.get('vendor_vin')
        vendor_details=User.objects.filter(cin_number=vendor_vin,company=request.company,status=1)
        contact_person = User.objects.filter(cin_number=vendor_vin,company=request.company,status=1,is_primary=0,is_secondary=0).first()
        print(contact_person.email,'-------------------------------contact_person')
        if draft_field == '1':
            if amountallocated:
                paymentaccount=PaymentAccount.objects.filter(id=paymentacct_id).first()
                if float(amountallocated)!=float(paymentaccount.amount):
                    PaymentAccount.objects.filter(id=paymentacct_id).update(status=2)
                    for invoice_id in invoiceid:
                            if invoice_id:
                                InvoiceCostInvoice.objects.filter(id=invoice_id).update(payment_account=2)
        else: 
            paymentaccount=PaymentAccount.objects.filter(id=paymentacct_id).first() 
            if float(amountallocated)!=float(paymentaccount.amount):
                PaymentAccount.objects.filter(id=paymentacct_id).update(status=1,remaining_amount=float(amountallocated))
                for invoice_id in invoiceid:
                        if invoice_id:
                            InvoiceCostInvoice.objects.filter(id=invoice_id).update(payment_account=1)
                            PaymentAccount_PaidInvoice.objects.create(invoice_id=invoice_id,payment_id=paymentacct_id,date=datetime.now())
                            #Mail for vendor    
                            if Companies.objects.filter(id=request.company.id).filter(Q(image__isnull=True) | Q(image='')):
                                imageurl=''
                            else:
                                imageurl=request.company.image.url
                        
                            company=Companies.objects.get(id=request.company.id)
                            companyusername=company.first_name+' '+company.last_name
                            url=f'{request.scheme}://{request.get_host()}'
                            subject = 'Application of Invoice to Account Payment'
                            invoice_details=InvoiceCostInvoice.objects.filter(id=invoice_id).first()
                            Gross_amount=invoicegrossamount(invoice_details.id)
                            tax_amount=invoicetaxamount(invoice_details.id)
                            total_amount=addvalues(Gross_amount,tax_amount)
                            for i in vendor_details:                                
                                context={'areacode':company.areacode,'role':request.user.designation_role,'landline_countrycode':company.phone_countrycode,'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,'mobile':company.mobile,'website':company.website,'address':company.address,'image':imageurl,'companyname':company.company_name,'cin':company.cin_number,'email':company.email,'url':url,'companyusername':companyusername,'vendor':i,'invoice_details':invoice_details,'total_amount':total_amount}
                                html_message = render_to_string('allocateamount_mailvendor.html', context)
                                plain_message = strip_tags(html_message)
                                from_email = settings.EMAIL_HOST_USER
                                to = i.email
                                recipient= i
                                sender=request.user
                                invoicenum=invoice_details.invoice_number
                                # print(invoicenum)
                            
                                msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)
                                notify.send(sender, recipient=recipient,data=url, verb=' Invoice applied to Payment on Account', description = f'Application of {invoicenum} to Account Payment')
  
                            #Mail for client
                            if Companies.objects.filter(id=request.company.id).filter(Q(image__isnull=True) | Q(image='')):
                                imageurl=''
                            else:
                                imageurl=request.company.image.url
                        
                            company=Companies.objects.get(id=request.company.id)
                            company_email = company.email
                            print(company_email,'kowwwwwww')
                            companyusername=company.first_name+' '+company.last_name
                            url=f'{request.scheme}://{request.get_host()}'
                            subject = 'Application of Invoice to Account Payment'
                            invoice_details=InvoiceCostInvoice.objects.filter(id=invoice_id).first()
                            Gross_amount=invoicegrossamount(invoice_details.id)
                            tax_amount=invoicetaxamount(invoice_details.id)
                            total_amount=addvalues(Gross_amount,tax_amount)
                                                            
                            context={'areacode':company.areacode,'role':request.user.designation_role,'landline_countrycode':company.phone_countrycode,'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,'mobile':company.mobile,'website':company.website,'address':company.address,'image':imageurl,'companyname':company.company_name,'cin':company.cin_number,'email':company.email,'url':url,'companyusername':companyusername,'vendor_details':vendor_details,'invoice_details':invoice_details,'contact_person':contact_person,'total_amount':total_amount}
                            
                            html_message = render_to_string('allocateamount_mailclient.html', context)
                            plain_message = strip_tags(html_message)
                            from_email = settings.EMAIL_HOST_USER
                            to = company_email
                            sender=request.user
                            recipient1 = User.objects.filter(company=request.company,roles_id=2)
                            print(f' recipient1 {recipient1}')
                            msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)
                            notify.send(sender, recipient=recipient1,data=url, verb='Invoice applied to Payment on Account', description = f'Application of Invoice {invoicenum} to Account Payment')

        return redirect(reverse_lazy('invoice:add_paymentonaccount')) 
      
def unpaidinvoice_paymentact(vendor,company,currency):
    invoicecurrencylist=[]
    allinvoices = Invoice.objects.filter(vendor_id=vendor,company=company, status=1).exclude(invoice_status=1).order_by('-id')
    for i in allinvoices:
        invoice_currency = InvoiceCostInvoice.objects.filter(invoice_id=i.id,currency_id=currency,approval_status=1,invoice__invoice_status=2).exclude(payment_account=1)
        for id in invoice_currency:
            if id:
                if Invoiceflowmodules.objects.filter(invoice_id=id.invoice, module_id=3, status=1).first() and not Invoiceflowmodules.objects.filter(invoice_id=id.invoice, module_id=4, status=1).first():
                        invoicecurrencylist.append(id)
    return invoicecurrencylist

class View_AllotedInvoice(View):
    def get(self,request):
        currenctlist=[]
        vendors_list=ContractMasterVendor.objects.filter_company(request.company,1)
        currency = Settings.objects.filter(company=request.company).first()
        separated_values = ast.literal_eval(currency.currency)
        for i in separated_values:
           currenctlist.append(Basecountries.objects.get(id=i))
        data={'vendors_list':vendors_list,'companycurrency':currenctlist}
        return render(request,'viewallocatedinvoice.html',data)
    def post(self,request):
        currenctlist=[]
        vendor=request.POST.get('vendor',None)
        currency=request.POST.get('currency',None)
        allocted_invoice=PaymentAccount_PaidInvoice.objects.filter(payment__vendor_id=vendor,payment__currency_id=currency,payment__company_id=self.request.company,payment__status=1,status=1)
        vendors_list=ContractMasterVendor.objects.filter_company(request.company,1)
        currency_list = Settings.objects.filter(company=request.company).first()
        separated_values = ast.literal_eval(currency_list.currency)
        currency_symbol=Basecountries.objects.getone_by_id(currency)
        for i in separated_values:
           currenctlist.append(Basecountries.objects.get(id=i))
        data={'allocted_invoice':allocted_invoice,'companycurrency':currenctlist,'vendors_list':vendors_list,'select_vendor':int(vendor),'select_currency':int(currency),'currency_symbol':currency_symbol}
        return render(request,'viewallocatedinvoice.html',data) 
    
def ReallocateInvoice(request,id):
    allocated_invoice=PaymentAccount_PaidInvoice.objects.filter(id=id).first()
    payment_account=PaymentAccount.objects.filter(id=allocated_invoice.payment_id).first()
    InvoiceCostInvoice.objects.filter(id=allocated_invoice.invoice_id).update(payment_account=0)
    invdisval = invoicegrossamount(allocated_invoice.invoice_id)
    invdistax = invoicetaxamount(allocated_invoice.invoice_id)
    invoiceamount = float(replacecommaid(addvalues(invdisval,invdistax)))
    finalamount=int(payment_account.remaining_amount)+invoiceamount
    PaymentAccount.objects.filter(id=allocated_invoice.payment_id).update(remaining_amount=finalamount)
    PaymentAccount_PaidInvoice.objects.filter(id=id).update(status=0)
    return JsonResponse({'status':True})

def Remove_Draft_Paymentaccount(request):
    invoiceid=request.POST.get('invoiceid')
    invoicecost=InvoiceCostInvoice.objects.filter(id=invoiceid).first()
    if invoicecost and invoicecost.payment_account == 2:
        invoicecost.payment_account = 0
        invoicecost.save()
    return JsonResponse({'status':True})


def ExchangeRateConfirmation(request):
    invoiceid=request.POST.get('pk')
    confirm_check=request.POST.get('confirm_check')
    flow_id=request.POST.get('invoice_flow_id')
    

    if confirm_check == 'payment_confirm':
        Invoiceflowmodules.objects.filter(invoice_id=invoiceid,id=flow_id).update(tax_confirm_status=1,exchangerate_confirm_status=2)
    

    elif confirm_check == '2':
        Invoiceflowmodules.objects.filter(invoice_id=invoiceid,id=flow_id).update(exchangerate_confirm_status=3,tax_confirm_status=0)
        

    else:
        Invoiceflowmodules.objects.filter(invoice_id=invoiceid,id=flow_id).update(exchangerate_confirm_status=confirm_check,tax_confirm_status=0)
        

    print(f'confirm_check {confirm_check}')
    return JsonResponse({'status':True})


class TaxConfirmView(View):
    def get(self,request,pk):
        coversheet_view = invoiceCoverSheet()
        invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        general=Settings.objects.get_company(request.company).first()
        if (invoicedetail == None):
            invoicedetail=""
        context = coversheet_view.get_context_data(request,pk)
        context['general']=general
        context['invoicedetail'] = invoicedetail
        invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,3)
        context['invoiceflow_modules']=invoiceflow_modules
        settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True)
        invoice_percentage=settlement_invoice.first()
        context['settlement_count']=settlement_invoice.count()
        context['settlement_invoice']=settlement_invoice
        context['invoice_percentage']=invoice_percentage
        return render(request,'taxconfirmview.html',context) 
        
    def post(self,request,pk):
        post_data=request.POST
        print('re',request.POST)
        deduction_check=post_data.get('deduction_check')
        additions_check=post_data.get('additions_check')

        invoice_split=post_data.getlist('split_id')
        additions_amount=post_data.getlist('addition_amount')
        deduction_amount=post_data.getlist('deduction_amount')
        additions_name=post_data.get('additions_name')


        deduction_name=post_data.get('deduction_name')
        bal_amount=post_data.getlist('balance_value')
        new_net_payable=post_data.getlist('new_net_payable')
        for split_invoice,net_payable in zip(invoice_split,new_net_payable):
            InvoiceCostInvoice.objects.filter(id=split_invoice).update(new_netpayable=net_payable)
        if deduction_check == '1':
            InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).update(deductions=1)
            Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=3,status=0).update(tax_confirm_status=1,exchangerate_confirm_status=2)
            for split,amount,balance in zip(invoice_split,deduction_amount,bal_amount):
                if OtherDeductions.objects.filter(invoice_id=pk,invoice_split_id=split).exists():
                    OtherDeductions.objects.filter(invoice_id=pk,invoice_split_id=split).update(description=deduction_name,amount=amount,balance=balance,status=True)
                else:
                    OtherDeductions.objects.create(invoice_id=pk,invoice_split_id=split,description=deduction_name,amount=amount,balance=balance,company=request.company)
        elif deduction_check == '0':
            InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).update(deductions=0)
            Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=3,status=0).update(tax_confirm_status=1,exchangerate_confirm_status=2)
            OtherDeductions.objects.filter(invoice_id=pk).update(status=False)
        if additions_check == '1':
            InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).update(additions=1)
            Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=3,status=0).update(tax_confirm_status=1,exchangerate_confirm_status=2)
            for split,amount,balance in zip(invoice_split,additions_amount,bal_amount):
                if OtherAdditions.objects.filter(invoice_id=pk,invoice_split_id=split).exists():
                    OtherAdditions.objects.filter(invoice_id=pk,invoice_split_id=split).update(description=additions_name,amount=amount,balance=balance,status=True)
                else:
                    OtherAdditions.objects.create(invoice_id=pk,invoice_split_id=split,description=additions_name   ,amount=amount,balance=balance,company=request.company)
        elif additions_check == '0':
            InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).update(additions=0)
            Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=3,status=0).update(tax_confirm_status=1,exchangerate_confirm_status=2)
            OtherAdditions.objects.filter(invoice_id=pk).update(status=False)
        return redirect('invoice:exchangerate',pk=pk)

class ViewCreditNoteInvoices(View):
    def get(self,request,pk):
        get_credit=list(CreditNoteInvoice.objects.filter(invoice_id=pk,status=1,credit__credit_status=2).values_list('credit_id',flat=True))
        credit_note=CreditNote.objects.filter(id__in=get_credit)
        data={'credit_note':credit_note,'credit_note_count':credit_note.count()}
        return render(request,'creditnoteapprovallisting.html',data)

class ApplicableCreditNoteView(View):
    def get(self,request,pk):
        invoice_data=Invoice.objects.get_by_id(pk)
        get_current_exclusives=list(InvoiceExclusive.objects.filter(invoice_id=pk,status=1).values_list('exclusive_id',flat=True))
        get_credit=CreditNoteInvoice.objects.filter(credit__contract_id=invoice_data.contractid,status=1,credit__usage_status__in=[1],credit__credit_status=2,invoice__invoice_status=3,credit__approval_status=4)
        bal_invoices=[]
        for balance in get_credit:
            get_remaining_exclusives=list(InvoiceExclusive.objects.filter(invoice_id=balance.invoice_id,status=1).values_list('exclusive_id',flat=True))
            if sorted(get_remaining_exclusives) == sorted(get_current_exclusives):
                bal_invoices.append(balance.credit_id)
        current_credit_notes=CreditNoteInvoice.objects.filter(invoice_id=pk,credit__contract_id=invoice_data.contractid,status=1,credit__usage_status__in=[1],credit__credit_status=2,credit__approval_status=4).exclude(invoice__invoice_status=3)
        total_credit_notes=bal_invoices+list(current_credit_notes.values_list('credit_id',flat=True))
        list_creditnote=CreditNote.objects.filter(id__in=total_credit_notes,credit_status=2,usage_status=1,check_for_pending=True,approval_status=4)
        list_invoices=[]
        for i in list_creditnote:
            list_invoices.append(i.id)        
        if PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).exists():
            adjusted_creditnote=list(CreditNoteMappingBase.objects.filter(invoice_id=pk,status=True,company_id=request.company.id).values_list('credit_note_id',flat=True).distinct())
            for k in adjusted_creditnote:
                common_credit=CreditNote.objects.filter(id=k,credit_status=2,approval_status=4)
                if int(k) not in total_credit_notes:
                    for k in common_credit:
                        list_invoices.append(k.id)
        get_credit=list(CreditNoteInvoice.objects.filter(invoice_id=pk,status=1,credit__credit_status=2).values_list('credit_id',flat=True))
        credit_note=CreditNote.objects.filter(id__in=list_invoices)
        data={'credit_note':credit_note,'credit_note_count':credit_note.count()}
        return render(request,'creditnoteapprovallisting.html',data)
    

class BankUserApprovalView(View):
    def get(self,request,pk,pay_id):
        contractid=Invoice.objects.get_by_id(pk)
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
        all_invoice=', '.join(str(e) for e in invoice_number)
        bankdetails=CompanyBank.objects.get_by_company(request.company)
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(contractid.contractid).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        get_data=Invoiceflowmodules.objects.filter(invoice_id=pk,module_id=None,payment_instruct__payment_count=pay_id)
        # notify=Notification.objects.filter(recipient_id=request.user.id,verb=f"Payment Instruction Received").order_by('-id')
        if request.user.bankuserstatus == 1:
            check_for_bankuser=checkdynamic_flow(contractid,request.user.id,None)
            bank_user=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=get_data,user=request.user.id,bank_user_status=1)
            payment_id=bank_user.values('payment_instruction_id').distinct()
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=get_data,user=request.user.id,bank_user_status=1).update(bank_user_verification=1)
            payment_details=PaymentInstruction.objects.filter(id__in=payment_id,invoicecost__invoice_id=pk,status=True,payment_count=pay_id)
            invoicecost_id=payment_details.values_list('invoicecost_id',flat=True)
            vendor=ContractMasterVendor.objects.get_byid(contractid.vendor_id,request.company)
            payment_number=payment_details.values_list('pi_number',flat=True)
            invoiceflow_modules=Invoiceflowmodules.objects.filter_by_module_id(pk,1,6).filter(payment_instruct__in=payment_details,invoicecost_id__in=list(invoicecost_id)).last()
            approved_flow_user=Invoiceflowmodulesusers.objects.get_approved_users(invoiceflow_modules.id).first()
            bank_name=''
            try:
                bank_name=approved_flow_user.company_bank_user.companybank.bank_name.bank_name
            except:
                bank_name=''
            userdata=User.objects.get(id=approved_flow_user.user)
            otp_val=list(payment_details.values_list('verified_bank_user_id',flat=True))
            today = date.today()
            date_today = today.strftime("%d-%b-%Y")
            invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('id',flat=True)
            get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost).exclude(payable_amount=0)
            payment_details_new=list(PaymentInstruction.objects.filter(id__in=payment_id,invoicecost__invoice_id=pk,status=True,payment_count=pay_id).values_list('id',flat=True))
            if len(check_for_bankuser) > 0 and  not None in check_for_bankuser:
                if None in otp_val:
                    n = 6
                    random_number=''.join(["{}".format(random.randint(0, 9)) for num in range(0, n)])
                    PaymentInstruction.objects.filter(id__in=payment_details_new).update(verification_code=random_number,verified_bank_user_id=request.user.id)
            #         updated_data=InvoiceCostInvoice.objects.filter(id__in=list(invoicecost_id)).update(verification_code=random_number,verified_bank_user_id=request.user.id)
                    pi_number=",".join(map(str,payment_number))
                    pinumber=''
                    for instruction in get_payment_instruction:
                        pinumber=instruction.pi_number
                    verb="Payment Instruction Received."
                    # description=f'Payment Instruction Received by {bank_name} on {date_today}.Verification Code for Payment ({random_number}).'
                    description=f'Payment Instruction No {pinumber} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {contractid.name_service} has been received by {request.user.name} {request.user.lastname}  .Verification code - ({random_number}).'
                    notify_invoice_flow(request,userdata,f"invoice/bankuserview/{pk}/{pay_id}",verb,description)
                    bank_verification_mail(request,userdata,bank_name,random_number)
            data={'payment_details':list(payment_details),'maininvoices':vendorinvoice,'pk':pk,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'invoice_detail':contractid,'bank_user':bank_user,'check_payment':payment_details.count(),'pay_id':pay_id}
            return render(request,'bankuserapprovalview.html',data)
        else:
            print(f'request.user.bankuserstatus {request.user.bankuserstatus}')
            if request.user.bankuserstatus == 0:
                bank_user=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=get_data,bank_user_status=1,bank_user_verification=1,status=0).values('payment_instruction_id').distinct()
                print(f'bank_user {bank_user}')
                payment_details=PaymentInstruction.objects.filter(id__in=bank_user,invoicecost__invoice_id=pk,status=True,payment_count=pay_id)
                print(f'payment_details {payment_details}')
                invoicecost_id=payment_details.values_list('invoicecost_id',flat=True)
                vendor=ContractMasterVendor.objects.get_byid(contractid.vendor_id,request.company)
                payment_number=payment_details.values_list('pi_number',flat=True)
                invoiceflow_modules=Invoiceflowmodules.objects.get_by_module_id(pk,1,6)
                return render(request,'bankuserapprovalview.html',{'pk':pk,'invoice_detail':contractid,'maininvoices':vendorinvoice,'payment_details':list(payment_details),'check_payment':payment_details.count(),'pay_id':pay_id})

class ViewPaymentInstructions(View):
    def get(self, request,pk,pay_id):
        invoicedata=Invoice.objects.get_by_id(pk)
        # pay_id=get_pay_id()
        if (invoicedata.contracttype == 'original'):
            contract=ContractMaster.objects.filter(id=invoicedata.contractid ,status=1).first()
            vendorinvoice=VendorInvoiceSplit.objects.filter(contract_id=contract.id,company=request.company,status=1)
        else:
            contract=Amendment.objects.filter(id=invoicedata.contractid ,status=1).first()
            vendorinvoice=VendorInvoiceSplit.objects.filter(amendment_id=contract.id,company=request.company,status=1)
        contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
        invoicedetail=InvoiceCostInformation.objects.filter(invoice_id=pk,status=1).first()
        if (invoicedetail == None):
            invoicedetail=""
        # payment_details=PaymentInstruction.objects.get_by_payment(pk)
        payment_details=PaymentInstruction.objects.get_by_payment(pk).filter(payment_count=pay_id)
        settlement_invoice=SettlementInvoice.objects.filter(invoice_id=pk,status=True,acceptance_status=2)
        context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'invoicedetail':invoicedetail,'invoice':invoicedata,'payment_details':payment_details,'settlement_invoice':settlement_invoice,'check_settlement':settlement_invoice.count(),'pay_id':pay_id}
        return render(request,'viewpaymentinstructions.html',context)
        # document_list=getDocumentlist()
        # contractid=Invoice.objects.get_by_id(pk)
        # if (contractid.contracttype == 'original'):
        #     contract=ContractMaster.objects.getcontract(contractid.contractid)
        #     vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        # else:
        #     contract=Amendment.objects.get_by_id(contractid.contractid ,1).first()
        #     vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        # contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        # invoicedetail=InvoiceCostInformation.objects.get_invoice_id(pk,1).first()
        # if (invoicedetail == None):
        #     invoicedetail=""
        # context={'contractcostinvoice':contractcostinvoice,'maininvoices':vendorinvoice,'basecurreccy':vendorinvoice.values_list('currency__currency_symbol',flat=True).first(),'paymentcurrency':vendorinvoice.values_list('currency__currency_symbol',flat=True).last(),'pk':pk,'document_list':document_list,'invoicedetail':invoicedetail,}
        # return render(request, "viewpaymentinstructions.html",context)


class RejectedInvoices(ListView):
    model = Invoice
    template_name = 'rejectedinvoicelist.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        markas_read_status(self.request.get_full_path())
        # if(self.request.user.roles_id==3):
        #     allinvoices=[]
        #     getprojects=ProjectUser.objects.getprojectuser_byuserid(self.request.user.id)
        #     if getprojects.count() > 0:
        #         print(f'getprojects {getprojects}')
        #         for project in getprojects:
        #             contracts=ContractMaster.objects.get_contract_project(project.project_id)
        #             for contract in contracts:
        #                 invoices=Invoice.objects.exclude_approved_invoice(contract.id).filter(invoice_status__in=[4,5])
        #                 for invoice in invoices:
        #                     allinvoices.append(invoice)
        #         sorted_invoices_desc = sorted(allinvoices, key=attrgetter('id'), reverse=True)
        #         context['Invoices'] = sorted_invoices_desc

        # else:
        #     context['Invoices'] = Invoice.objects.exclude_approved_invoice_by_company(self.request.company).filter(invoice_status__in=[4,5])
        context['sign_data']=check_user_sign(self.request.user)
        context['userid'] = self.request.user.id
        return context
        
def view_contractfiles(request,pk):
    contractfile=VendorContractPriceTable.objects.filter(id=pk).first()
    getfilename=contractfile.file_name.path
    getextension=pathlib.Path(getfilename).suffix
    if (getextension == ".pdf"):
    # return render(request,'invoicelist.html') 
        with open(getfilename, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response
    else:
        image_data = open(getfilename, "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg") 
    
    
    
def get_project_vendor(request):
    vendor_id = request.GET.get('vendor_id')
    Project_ids = ContractMaster.objects.filter(contractvendor=vendor_id, status=1).values_list('projects', flat=True).distinct()

    projects_data = {"projects": [],"id":[]}  # Renamed key to plural for clarity
    for project_id in Project_ids:
        project = Projectcreation.objects.filter(id=project_id,active_status=True).first()
        if project:
            projects_data["projects"].append(project.projectname)
            projects_data["id"].append(project.id)

    # Convert projectname values to strings
    projects_data["projects"] = [str(project_name) for project_name in projects_data["projects"]]

    print(projects_data)
    return JsonResponse(projects_data)
def get_contract_with_vendor(request):
    vendor_id = request.GET.get('vendor_id')
    project_id = request.GET.get('project_id')
    
    # Assuming ContractMaster model has fields: id, projects, types_service, reference_number
    contracts = ContractMaster.objects.filter(contractvendor=vendor_id, projects=project_id).values('id', 'projects', 'types_service', 'reference_number')
    
    data = list(contracts)  # Convert QuerySet to list for JsonResponse
    
    return JsonResponse(data, safe=False)

def conformcostcode(request):
    vendor_costcode=request.POST.get('vendor_costcode')
    module_id=request.POST.get('module_id')
    invoice_id=request.POST.get('invoice_id')
    invoice_details=Invoice.objects.get_by_id(invoice_id)
    vendor_details=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    if vendor_details is None:     
        vendor_details=invoice_details.vendor
    print(f"vendor_details {vendor_details}")
    comments=request.POST.get('comments')
    Invoice.objects.update_conform_costcode(invoice_id,vendor_costcode,comments)
    vendor_users=User.objects.getusers_by_cin(invoice_details.vendor.vin)
    invoice_number=list(InvoiceCostInvoice.objects.get_invoice_id(invoice_id,1).values_list('invoice_number',flat=True))
    old_cost_id=invoice_details.costcodevendor.id

    if vendor_costcode !=None or vendor_costcode != '':
        if int(vendor_costcode) != int(old_cost_id) :
            all_invoice=', '.join(str(number) for number in invoice_number)
            url='invoice/invoicelist'
            for user in vendor_users:
                notify_invoice_flow(request,user,url,'Cost Code updated',f'Cost Code for invoice  {all_invoice} for services {invoice_details.name_service} has been updated by {request.company.company_name}')
                # send_conform_costcode_mail(request,vendor_details,all_invoice,invoice_details,user.email) 


    return JsonResponse({'data':'success'})

def get_amendment_contract(request):
    contract_id = request.GET.get('contract_id')
    contracts = ContractMaster.objects.filter(id=contract_id).values('id','reference_number')
    Ame=Amendment.objects.filter(service=contract_id).annotate(reference_number=F('amendment_reference_number')).values('reference_number','id')
    if Ame:
        data = list(Ame)  # Convert QuerySet to list for JsonResponse
        return JsonResponse(data, safe=False)
    else :
        data = list(contracts)  # Convert QuerySet to list for JsonResponse
        return JsonResponse(data, safe=False) 

        
def getunpaidinvoices(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    payment_type = request.GET.get('payment_type') or None
    vendor_name1 = request.GET.get('vendorname')
    service_type1 = request.GET.get('servicetype')
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    print(f'payment_type {type(payment_type)}')
    if payment_type == '1' or payment_type == 1: #for unpaid invoices
        if(request.user.roles_id==2):
            invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice__company_id=request.company.id,invoice__invoice_status__in=[2])& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status__in=[2])).order_by('-invoice_id').values('invoice').distinct()
            invoice_value=invoicecost[start:start+length]       
            if vendor_name1 and service_type1: 
                invoicecost=InvoiceCostInvoice.objects.filter(Q(vendor__vendor_name=vendor_name1,invoice__name_service=service_type1) & Q(invoice__company_id=request.company.id,invoice__invoice_status__in=[2])& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status__in=[2])).order_by('-invoice_id').values('invoice').distinct()
                invoice_value=invoicecost[start:start+length]
        elif (request.user.bankuserstatus == 1):
            get_all_invoice_ids=Invoiceflowmodulesusers.objects.filter_bankuser_invoice(request.user.id,1)
            invoices=Invoice.objects.get_invoice_by_list_ids(get_all_invoice_ids.values_list('Invoiceflowmodules__invoice_id',flat=True))
            invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=invoices)& Q(invoice_number__icontains=search_value,invoice_id__in=invoices)).order_by('-invoice_id').values('invoice').distinct()
            invoice_value=invoicecost[start:start+length]
        elif (request.user.roles_id==3):
            getprojects=ProjectUser.objects.getprojectuser_byuserid(request.user.id)
            if getprojects.count() > 0:
                allinvoices=[]
                for project in getprojects:
                    contracts=ContractMaster.objects.get_contract_project(project.project_id)
                    for contract in contracts:
                        contract_invoices=list(Invoice.objects.exclude_approved_invoice(contract.id).values_list('id',flat=True))
                        allinvoices.extend(contract_invoices)
                    amendments=Amendment.objects.filter(service__projects_id=project.project_id,status=1)
                    for amd in amendments:
                        amd_invoices=list(Invoice.objects.exclude_approved_invoice(amd.id).values_list('id',flat=True))
                        allinvoices.extend(amd_invoices)
                allinvoices=sorted(list(set(allinvoices)),reverse=True)
                invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=allinvoices,invoice__invoice_status__in=[2])& Q(invoice_number__icontains=search_value,invoice_id__in=allinvoices,invoice__invoice_status__in=[2])).order_by('-invoice_id').values('invoice').distinct()
                invoice_value=invoicecost[start:start+length]
            else:
                user_count=checkcreate(request.user.id,'Dispute_Committee')
                if user_count > 0:
                    invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice__company_id=request.company.id,invoice__invoice_status__in=[2])& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status__in=[2])).order_by('-invoice_id').values('invoice').distinct()
                    invoice_value=invoicecost[start:start+length]  
            
    elif payment_type == '2' or payment_type == 2: #for paid invoices
        if (request.user.roles_id==3):
            getprojects=ProjectUser.objects.getprojectuser_byuserid(request.user.id)
            allinvoices=[]
            if getprojects.count() > 0:
                for project in getprojects:
                    contracts=ContractMaster.objects.get_contract_project(project.project_id)
                    for contract in contracts:
                        contract_invoices=list(Invoice.objects.getinvoiceby_payment(contract.id).values_list('id',flat=True))
                        allinvoices.extend(contract_invoices)
                    amendments=Amendment.objects.filter(service__projects_id=project.project_id,status=1)
                    for amd in amendments:
                        amd_invoices=list(Invoice.objects.getinvoiceby_payment(amd.id).values_list('id',flat=True))
                        allinvoices.extend(amd_invoices)
            allinvoices=sorted(list(set(allinvoices)),reverse=True)
            invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=allinvoices)& Q(invoice_number__icontains=search_value,invoice_id__in=allinvoices)).order_by('-invoice_id').values('invoice').distinct()
            invoice_value=invoicecost[start:start+length]
            
        else:
            invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice__company_id=request.company.id,invoice__invoice_status=3,invoice__status=1)& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status=3,invoice__status=1)).order_by('-invoice_id').values('invoice').distinct()
            invoice_value=invoicecost[start:start+length]
            if vendor_name1 and service_type1: 
                invoicecost=InvoiceCostInvoice.objects.filter(Q(vendor__vendor_name=vendor_name1,invoice__name_service=service_type1) &Q(invoice__company_id=request.company.id,invoice__invoice_status=3,invoice__status=1)& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status=3,invoice__status=1)).order_by('-invoice_id').values('invoice').distinct()
                invoice_value=invoicecost[start:start+length]
    elif payment_type == 3 or payment_type == '3': #for disputed invoices
        if(request.user.roles_id==3):
            allinvoices=[]
            getprojects=ProjectUser.objects.getprojectuser_byuserid(request.user.id)
            if(UserRights.objects.filter(user_id=request.user.id,module_id=18).first()):
                if(UserRights.objects.filter(user_id=request.user.id,module_id=18).first().create == '1'):
                    invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice__company_id=request.company.id,invoice__invoice_status=6,invoice__status=1)& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status=6,invoice__status=1)).order_by('-invoice_id').values('invoice').distinct()
                    invoice_value=invoicecost[start:start+length]
                else:
                    if getprojects.count() > 0:
                        for project in getprojects:
                            contracts=ContractMaster.objects.get_contract_project(project.project_id)
                            for contract in contracts:
                                contract_invoices=list(Invoice.objects.getdisputedinvoiceby_contract(contract.id).values_list('id',flat=True))
                                allinvoices.extend(contract_invoices)
                            amendments=Amendment.objects.filter(service__projects_id=project.project_id,status=1)
                            for amd in amendments:
                                amd_invoices=list(Invoice.objects.getdisputedinvoiceby_contract(amd.id).values_list('id',flat=True))
                                allinvoices.extend(amd_invoices)
                    allinvoices=sorted(list(set(allinvoices)),reverse=True)
                    invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=allinvoices)& Q(invoice_number__icontains=search_value,invoice_id__in=allinvoices)).order_by('-invoice_id').values('invoice').distinct()
                    invoice_value=invoicecost[start:start+length]
            else:
                if getprojects.count() > 0:
                    for project in getprojects:
                        contracts=ContractMaster.objects.get_contract_project(project.project_id)
                        for contract in contracts:
                            contract_invoices=list(Invoice.objects.getdisputedinvoiceby_contract(contract.id).values_list('id',flat=True))
                            allinvoices.extend(contract_invoices)
                        amendments=Amendment.objects.filter(service__projects_id=project.project_id,status=1)
                        for amd in amendments:
                            amd_invoices=list(Invoice.objects.getdisputedinvoiceby_contract(amd.id).values_list('id',flat=True))
                            allinvoices.extend(amd_invoices)
                allinvoices=sorted(list(set(allinvoices)),reverse=True)
                invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=allinvoices)& Q(invoice_number__icontains=search_value,invoice_id__in=allinvoices)).order_by('-invoice_id').values('invoice').distinct()
                invoice_value=invoicecost[start:start+length]
        else:
            invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice__company_id=request.company.id,invoice__invoice_status=6,invoice__status=1)& Q(invoice_number__icontains=search_value,invoice__company_id=request.company.id,invoice__invoice_status=6,invoice__status=1)).order_by('-invoice_id').values('invoice').distinct()
            invoice_value=invoicecost[start:start+length]
    elif payment_type == 4 or payment_type == '4': #for rejected invoices
        if(request.user.roles_id==3):
            allinvoices=[]
            getprojects=ProjectUser.objects.getprojectuser_byuserid(request.user.id)
            if getprojects.count() > 0:
                for project in getprojects:
                    contracts=ContractMaster.objects.get_contract_project(project.project_id)
                    for contract in contracts:
                        contract_invoices=list(Invoice.objects.exclude_approved_invoice(contract.id).filter(invoice_status__in=[4,5]).values_list('id',flat=True))
                        allinvoices.extend(contract_invoices)
                    amendments=Amendment.objects.filter(service__projects_id=project.project_id,status=1)
                    for amd in amendments:
                        amd_invoices=list(Invoice.objects.exclude_approved_invoice(contract.id).filter(invoice_status__in=[4,5]).values_list('id',flat=True))
                        allinvoices.extend(amd_invoices)
                allinvoices=sorted(list(set(allinvoices)),reverse=True)
                invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=allinvoices)& Q(invoice_number__icontains=search_value,invoice_id__in=allinvoices)).order_by('-invoice_id').values('invoice').distinct()
                invoice_value=invoicecost[start:start+length]
        else:
            reject_invoices=list(Invoice.objects.exclude_approved_invoice_by_company(request.company).filter(invoice_status__in=[4,5]).values_list('id',flat=True))
            print(f'reject_invoices {reject_invoices}')
            invoicecost=InvoiceCostInvoice.objects.filter(Q(invoice_id__in=reject_invoices)& Q(invoice_number__icontains=search_value,invoice_id__in=reject_invoices)).order_by('-invoice_id').values('invoice').distinct()
            invoice_value=invoicecost[start:start+length]
    try:
        invoice_value=invoice_value
        invoicecost=invoicecost
        invoice_value=invoice_value
    except:
        invoice_value=[]
        invoicecost=InvoiceCostInvoice.objects.none()
        invoice_value=invoicecost[start:start+length]
    allinvoices=[]
    s_no=start+1
    for invoice in invoice_value:
        invoiceapproval_dispute=checkpermission_bank=module1_override=inv_receipt=module2_override=inv_approval=module3_override=tax_confirm=module4_override=payment_gn=payment_apl=module5_override=module6_override=module7_override=returned_user=get_credit_note=0
        data_count=1
        payment_aplwh=payment_cfn=payment_recept=[]
        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=invoice['invoice'],status=1)
        instruction_number=[]
        get_invoice=Invoice.objects.filter(id=invoice['invoice'],status=1).first()
        file_upload=check_get_invoicecost(invoice['invoice'],6)
        withoutbankuser=withoutbankuserapproval(invoice['invoice'],6)
        bankuserstatus=checkforbankuser(request.company)
        if bankuserstatus == 1:
            if file_upload[0] == 1:
                if file_upload[1] != None:
                    for cost in file_upload[1]:
                        try:
                            if cost.payment_instruction.verified_status == 1:
                                data_count=check_invoice_receiptfile_upload_by_payment_id(cost.payment_instruction.id)
                                if data_count == 0:
                                    instruction_number.append({'cost_id':cost.payment_instruction.invoicecost.id,'cost_number':cost.payment_instruction.invoicecost.invoice_number , 'payment_split':cost.payment_instruction.payment_count})
                        except:
                            continue
            else:
                for invoice_cs in invoice_cost:
                    instruction_number.append({'cost_id':invoice_cs.id,'cost_number':invoice_cs.invoice_number})
        else :
            if withoutbankuser[0] == 1:
                if withoutbankuser[1] != None:
                    for cost in withoutbankuser[1]:
                        try:
                            if cost.payment_instruction.companyuserstatus==3 :
                                data_count=check_invoice_receiptfile_upload_by_payment_id(cost.payment_instruction.id)
                                if data_count == 0:
                                    instruction_number.append({'cost_id':cost.payment_instruction.invoicecost.id,'cost_number':cost.payment_instruction.invoicecost.invoice_number , 'payment_split':cost.payment_instruction.payment_count})
                        except:
                            continue
            else:
                for invoice_cs in invoice_cost:
                    instruction_number.append({'cost_id':invoice_cs.id,'cost_number':invoice_cs.invoice_number})

        if request.user.bankuserstatus == 1:
            # checkpermission_bank=checkpermission_bankuser(get_invoice,request.user.id)
            checkpermission_bank=checkdynamic_flow(get_invoice,request.user.id,None)
            print(f' {checkpermission_bank}')
        else:
            checkpermission_bank=check_for_balance_invoice(invoice['invoice'],request)
            module1_override=checkpermission_invoiceoverride(get_invoice,request.user.id,'1')
            inv_receipt=checkpermission_invoicerecipt(get_invoice,request.user.id,'1')
            module2_override=checkpermission_invoiceoverride(get_invoice,request.user.id,"2")
            inv_approval=checkpermission_invoicerecipt(get_invoice,request.user.id,"2")
            module3_override=checkpermission_invoiceoverride(get_invoice,request.user.id,"3")
            tax_confirm=checkpermission_invoicerecipt(get_invoice,request.user.id,"3")
            module4_override=checkpermission_invoiceoverride(get_invoice,request.user.id,"4")
            payment_gn=checkpermission_invoicerecipt(get_invoice,request.user.id,"4")
            payment_aplwh=checkdynamic_flow(get_invoice,request.user.id,"5")
            bu=checkdynamic_flow(get_invoice,request.user.id,None)
            module5_override=checkpermission_invoiceoverride(get_invoice,request.user.id,"5")
            payment_apl=checkpermission_invoicerecipt(get_invoice,request.user.id,"5")
            module6_override=checkpermission_invoiceoverride(get_invoice,request.user.id,"6")
            payment_cfn=checkdynamic_flow(get_invoice,request.user.id,"6")
            print(f'payment_cfn {payment_cfn}')
            module7_override=checkpermission_invoiceoverride(get_invoice,request.user.id,"7")
            payment_recept=checkpermission_invoicerecipt_upload(get_invoice,request.user.id,"7")
            returned_user=checkreturned_documents(get_invoice,request)
            get_credit_note=get_credit_notes(invoice['invoice'])
          
        if get_invoice.invoice_status == 4 :
            if request.user.roles_id == 3 or request.user.roles_id == 2:
                invoiceapproval_dispute=checkpermission_invoiceapproval_dispute(get_invoice,request.user.id,'')
        elif get_invoice.invoice_status == 6 or payment_type =='3' or payment_type == 3 :
            if request.user.roles_id == 3 or request.user.roles_id == 2:
                invoiceapproval_dispute=checkpermission_invoiceapproval_dispute(get_invoice,request.user.id,'')
                dispute_user=get_dispute_committee_member(request,get_invoice)
                if dispute_user > 0:
                    returned_user=resolution_team_approval(get_invoice,request)
                    if returned_user == 1:
                        inv_receipt=1
                    elif returned_user == 2:
                        inv_approval=1
            elif vendorid:
                if vendorid.active_status == 1:
                    invoiceapproval_dispute=1
        else:
            if request.user.roles_id == 3 or request.user.roles_id == 2:
                invoiceapproval_dispute=check_query_history(get_invoice)
        try:
            vin=get_invoice.vendor.vin
            vendor_name=get_invoice.vendor.vendor_name
        except:
            vin=''
            vendor_name=''
        try:
            service_name=get_invoice.name_service
        except:
            service_name=''
        check_bankuser=check_bank_users(request)
        bank_user_currencies=check_bank_user_currencies(request)
        if check_bankuser:
            inv_number=[i.invoice_number for i in invoice_cost if i.currency_id in bank_user_currencies]
            date=[i.invoice_submission_date for i in invoice_cost if i.currency_id in bank_user_currencies]
            invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=invoice['invoice'],status=1).filter(currency__in=bank_user_currencies)
        else:
            inv_number=list(invoice_cost.values_list('invoice_number',flat=True))
            date=list(invoice_cost.values_list('invoice_submission_date',flat=True))
        find_dates=[]
        approval_status=[]
        payment_status=[]
        for dated,inv_cost in zip(date,invoice_cost):
            if inv_cost.approval_status == 0 and get_invoice.invoice_status == 1 or inv_cost.approval_status == 6 and get_invoice.invoice_status == 6:
                approval_status.append('Disputed')
            elif inv_cost.approval_status == 1 and get_invoice.invoice_status == 2 and get_invoice.approval_status == 0:
                approval_status.append('Awaiting Approval')
            elif inv_cost.approval_status == 1 and get_invoice.invoice_status == 1:
                approval_status.append('Not Yet Submitted')
            elif inv_cost.approval_status == 4 and get_invoice.invoice_status == 4:
                approval_status.append('Returned')
            elif inv_cost.approval_status == 5 and get_invoice.invoice_status == 5:
                approval_status.append('Rejected')
            elif inv_cost.approval_status == 1 and get_invoice.invoice_status == 2 and get_invoice.approval_status == 1:
                approval_status.append('Approved')
            else:
                approval_status.append('Approved')
            date_format=confulldate(dated,request.company.id)
            find_dates.append(date_format)
            payment_count=get_payment_detail(get_invoice.id,inv_cost.id)
            payment_percentage=get_new_payment_percentage(get_invoice.id,inv_cost.id)
            confim_payment_percentage=get_confirm_payment_percentage(get_invoice.id,inv_cost.id)
            if inv_cost.payment_status == 1 and payment_count == 0:
                payment_status.append('Unpaid')
            elif inv_cost.payment_status == 1 and payment_count == 1:
                partially = PaymentReceiptFile.objects.filter(payment_receipt__invoice_id=get_invoice.id,payment_receipt__invoice_cost=inv_cost.id,status=True)
                if partially:
                    if payment_percentage == 100 : 
                        payment_status.append(f' Paid -{payment_percentage}%')
                    else :
                        payment_status.append(f'Partially Paid -{payment_percentage}%')
                else:
                    payment_status.append(f'confirmed for payment -{confim_payment_percentage}%')
            else:
                if payment_percentage:
                    payment_status.append(f'Paid- 100%')
                else:
                    payment_status.append(f'Paid') 
        query_status=list(InvoiceExceptional.objects.filter(invoice_id=get_invoice.id,status=1).values())
        if len(query_status) > 0 or invoiceapproval_dispute > 0:
            Invoice.objects.filter(id=invoice['invoice'],status=1).update(query_status=1)
            
        allinvoices.append({
            's_no':s_no,
            'id':invoice['invoice'],
            'inv_number':inv_number,
            'vin':vin,
            'vendor_name':vendor_name,
            'service_name':service_name,
            'date':find_dates,
            'approval_status':approval_status,
            'payment_status':payment_status,
            'invoiceapproval_dispute':invoiceapproval_dispute,
            'checkpermission_bank':checkpermission_bank,
            'module1_override':module1_override,
            'inv_receipt':inv_receipt,
            'module2_override':module2_override,
            'inv_approval':inv_approval,
            'module3_override':module3_override,
            'tax_confirm':tax_confirm,
            'module4_override':module4_override,
            'payment_gn':payment_gn,
            'module5_override':module5_override,
            'payment_apl':payment_aplwh,
            'module6_override':module6_override,
            'payment_cfn':payment_cfn,
            'module7_override':module7_override,
            'payment_recept':payment_recept,
            'returned_user':returned_user,
            'get_credit_notes':get_credit_note,
            'instruction_number':instruction_number,
            'dispute_query_status' : len(query_status),
        })
        s_no+=1
    response = {
        'draw': draw,
        'recordsTotal': invoicecost.count(),
        'recordsFiltered': invoicecost.count(),
        'data': allinvoices
    }

    return JsonResponse(response)
        

def get_invoice_details(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    search_name = request.GET.get('search[value]') or None
    user=User.objects.filter(Q(is_primary=1) | Q(is_secondary=1),id=request.user.id).first()
    vendor_status = True if user else False
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    if search_name:
        invoice_value=InvoiceCostInvoice.objects.filter(Q(invoice__vendor_id=vendorid.id ,invoice__status=1 ) & Q(invoice_number__icontains=search_value,invoice__vendor_id=vendorid.id ,invoice__status=1 )).exclude(invoice__invoice_status=6).order_by('-invoice__id').values('invoice').distinct() if vendor_status == True else InvoiceCostInvoice.objects.filter(Q(invoice__vendor_id=vendorid.id,invoice__status=1,invoice__invoice_status__in=[2,4]) & Q(invoice_number__icontains=search_value,invoice__vendor_id=vendorid.id,invoice__status=1,invoice__invoice_status__in=[2,4])).order_by('-invoice__id').values('invoice').distinct() 
    else:
        invoice_value=Invoice.objects.filter(vendor_id=vendorid.id ,status=1 ).exclude(invoice_status=6).order_by('-id') if vendor_status == True else Invoice.objects.filter(vendor_id=vendorid.id,status=1,invoice_status__in=[2,4]).order_by('-id')
    full_invoice_value=invoice_value[start:start+length]
    all_invoice=[]
    s_no=start+1
    for invoice in full_invoice_value:
        invoiceid=None
        if search_name:
            invoiceid=invoice['invoice']
        else:
             invoiceid=invoice.id

        get_invoice=Invoice.objects.filter(id=invoiceid,status=1).first()
        invoice_approve=InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,status=1)
        final_status=""
        if get_invoice.invoice_status == 1:
            final_status = "Draft"
        else:
            final_status ="Submitted"
        haspermission_invoicerecipt=checkpermission_invoiceapproval_dispute(get_invoice , request.user.id , "")
        inv_count=get_returned_invoice_count(get_invoice.id ,"")
        invoice_num=[]
        find_dates=[]
        approval_status=[]
        approval_date=[]
        payment_status=[]
        payment_date=[]
        if not invoice_approve.exists():
            invoice_num.append("---")   
            find_dates.append("---")
            approval_date.append("---")
            approval_status.append('---')
            payment_date.append("---")
            payment_status.append('---')
        else :
            for inv_cost  in  invoice_approve  :
                if inv_cost.approval_status == 0 and get_invoice.invoice_status == 1 or inv_cost.approval_status == 6 and get_invoice.invoice_status == 6:
                    approval_status.append('Disputed')
                elif inv_cost.approval_status == 1 and get_invoice.invoice_status == 2 and get_invoice.approval_status == 0:
                    approval_status.append('Awaiting Approval')
                elif inv_cost.approval_status == 1 and get_invoice.invoice_status == 1:
                    approval_status.append('Not Yet Submitted')
                elif inv_cost.approval_status == 4 and get_invoice.invoice_status == 4:
                    approval_status.append('Returned')
                elif inv_cost.approval_status == 5 and get_invoice.invoice_status == 5:
                    approval_status.append('Rejected')
                elif inv_cost.approval_status == 1 and get_invoice.invoice_status == 2 and get_invoice.approval_status == 1:
                    approval_status.append('Approved')
                else:
                    approval_status.append('Approved')
                
                date_format=confulldate(inv_cost.invoice_submission_date,request.company.id)
                find_dates.append(date_format)
                if inv_cost.approval_date == None or inv_cost.approval_date == "":
                    approval_date.append("N/A")
                else :
                    approve_date_format =confulldate(inv_cost.approval_date,request.company.id)
                    approval_date.append(approve_date_format)
                    
                if inv_cost.payment_date == None or inv_cost.payment_date == "":
                    payment_date.append("N/A")
                else :
                    payment_date_format =confulldate(inv_cost.payment_date,request.company.id)
                    payment_date.append(payment_date_format)
                
                invoice_num.append(inv_cost.invoice_number)
                payment_count=get_payment_detail(get_invoice.id,inv_cost.id)
                payment_percentage=get_new_payment_percentage(get_invoice.id,inv_cost.id)
                confim_payment_percentage=get_confirm_payment_percentage(get_invoice.id,inv_cost.id)
                if inv_cost.payment_status == 1 and payment_count == 0:
                    payment_status.append('Unpaid')
                elif inv_cost.payment_status == 1 and payment_count == 1:
                    partially = PaymentReceiptFile.objects.filter(payment_receipt__invoice_id=get_invoice.id,payment_receipt__invoice_cost=inv_cost.id,status=True)
                    if partially:
                        payment_status.append(f'Partially Paid -{payment_percentage}%')
                    else:
                        payment_status.append(f'confirmed for payment -{confim_payment_percentage}%')
                else:
                    if payment_percentage:
                        payment_status.append(f'Paid-{payment_percentage}%')
                    else:
                        payment_status.append(f'Paid')
        query_status=list(InvoiceExceptional.objects.filter(invoice_id=get_invoice.id,status=1).values())
        all_invoice.append({
            's_no':s_no,
            'id':invoiceid,
            'invoice_num':invoice_num,
            'submit_date':find_dates,
            'approval_status':approval_status,
            'approval_date':approval_date,
            'payment_status':payment_status,
            'payment_date':payment_date,
            'status':final_status,
            'vendorid':vendorid.id,
            'vendorid_active_status':vendorid.active_status,
            'vendor_status':vendor_status,
            'invoice_invoice_status':get_invoice.invoice_status,
            'invoice_wcc_id':get_invoice.wcc_id,
            'user_id':request.user.roles.id,
            'haspermission_invoicerecipt':haspermission_invoicerecipt,
            'inv_count':inv_count,
            'query_status':len(query_status),
            'query_history_status':get_invoice.query_status,

        })
        s_no+=1
    response = {
        'draw': draw,
        'recordsTotal': invoice_value.count(),
        'recordsFiltered': invoice_value.count(),
        'data': all_invoice
    }
    return JsonResponse(response)

def invoice_flow_function(pk,module,request,comments,submit_type,submit_name):
    current_date=datetime.now()
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoiceids(pk,module)
    bank_usercheck=0
    try:
        check_for_user=Settings.objects.get(company_id=request.company.id)
        bank_usercheck=check_for_user.bank_user
    except:
        bank_usercheck=0
    print(f'bank_usercheck {bank_usercheck}')
    if (invoiceflow_modules):
        Invoiceflowmodules.objects.updateinvoiceflowmodules(invoiceflow_modules.id)
        Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,submit_type,comments)
    invoice_detail = Invoice.objects.get_by_id(pk)
    invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
    all_invoice=', '.join(str(e) for e in invoice_number)
    vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
    vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
    allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
    main_url="invoice/invoicelist"
    main_verb='Invoice '+submit_name
    main_description=f' Invoice for Payment Approval'
    content=f'Invoice {submit_name} by {request.user.name} on {date_today} for {invoice_detail.name_service} '
    now = datetime.now()
    get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
    get_invoice_date=get_payment_term.payment_terms.payment_day
    get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
    calculate_time=add_invoice_time(now,get_company_invoice_time)
    if (submit_type == '3' or submit_type == '4'):
        main_url=f"invoice/invoiceview/{pk}" 
        print(f'main_url {main_url}')
        Invoice.objects.filter(id=pk).update(invoice_status=4) if submit_type == '3' else Invoice.objects.filter(id=pk).update(invoice_status=5) 
        InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=4,approval_date=current_date) if submit_type == '3' else InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=5,approval_date=current_date)
        if(submit_type == '3'):
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=invoiceflow_modules.id,user=request.user.id).update(returned=1,returned_date=current_date)
        if module == 1 or module == 2:
            for notifications in allVendors:
                invoive_return_mail(request,notifications,vendor,submit_name,invoice_detail,comments,all_invoice,submit_type)
                notify_invoice_flow(request,notifications,main_url,main_verb,content)
    else:
        if (invoice_detail.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(invoice_detail.contractid).first()
            contract_data=contract
        else:
            contract=Amendment.objects.get_by_id(invoice_detail.contractid ,1).first()
            contract_data=contract.service
        if True:
            if (module == None):
                invoiceflow_modules=Invoiceflowmodules.objects.get_by_module_id(pk,1,6)
            print(f'invoiceflow_modules {invoiceflow_modules}')
            getnextlevel=ProjectFlowModules.objects.getnextactivelevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.flowlevel_module_id)
            print(f'getnextlevel {getnextlevel},bank_usercheck')
            if(getnextlevel):
                print(f'next module id {getnextlevel.module.module.id}')
                getmodules=ProcessModule.objects.getmodule_byid(getnextlevel.module_id)
                projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnextlevel.id,invoiceflow_modules.flowlevel_id)
                if (getnextlevel.module.module.id == 7 and module == 6):
                    if bank_usercheck == 1:
                        PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).update(verified_status=0)
                            #create invoiceflowmodule bank user
                        invoiceflow=Invoiceflowmodules.objects.createbankinvoiceflowmodules(contract_data.projects.id,request.company,invoiceflow_modules.flowlevel_id,None,pk,None,now,calculate_time)
                        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('id',flat=True)
                        get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost).exclude(payable_amount=0)
                        print(f'get_payment_instruction {get_payment_instruction}')
                        for instruction in get_payment_instruction:
                            get_bank_uers=CompanyBankUser.objects.filter(companybank_id=instruction.companybank_id)
                            for bank_user in get_bank_uers:
                                Invoiceflowmodulesusers.objects.creatbankinvoiceusers(contract_data.projects.id,invoiceflow.id,bank_user.user_id,instruction.id,bank_user.id,1)
                                verb=f'Approved Payment Instructions'
                                description=f'Payment Instruction No {instruction.pi_number} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been sent for payment confirmation by {request.user.name} {request.user.lastname}'
                                urls="invoice/vendorbasedinvoice"
                                notify_invoice_flow(request,bank_user.user,urls,verb,description)
                                bank_user_approvalmail(request,bank_user.user,instruction.pi_number,vendor,invoice_detail,all_invoice,comments)
                                print(f'getnextlevel.module.module.id == 7 and module == 6 ')
                    else:
                        invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,invoiceflow_modules.flowlevel_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
                else:
                    invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,invoiceflow_modules.flowlevel_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
                if (getnextlevel.module.module.id == 5 ):
                    signatory_func(pk,invoice_detail.project.projectname.id,request,getnextlevel,invoiceflow,invoice_detail,all_invoice,vendor,1)
                elif(getnextlevel.module.module.id == 7 and module == 6):
                    if bank_usercheck == 0:
                        for user in projectflow_modules_users:
                            projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                            Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                            recipientuser = User.objects.get(id=projectusers.user_id)
                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                            print('get_users2',get_users)
                            approved_users=User.objects.filter(id__in=get_users)
                            urls=getInvoiceModule(getnextlevel.module.module.id,pk)
                            module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
                else:
                    for user in projectflow_modules_users:
                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                        # command 
                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                        recipientuser = User.objects.get(id=projectusers.user_id)
                        if getnextlevel.module.module.id == 4 or module == 3 and getnextlevel.module.module.id == 3:
                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4]).values_list('user',flat=True)
                        elif getnextlevel.module.module.id == 5:
                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
                        elif getnextlevel.module.module.id == 6 or getnextlevel.module.module.id == 5 and module == 5:
                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
                        else:
                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                        print('get_users2',get_users)
                        approved_users=User.objects.filter(id__in=get_users)
                        urls=getInvoiceModule(getnextlevel.module.module.id,pk)
                        module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
            else:
                print(2)
                if (module == None):
                    invoiceflow_modules=Invoiceflowmodules.objects.get_by_module_id(pk,1,6)
                getnexprocesstlevel=ProjectFlowModules.objects.getnxtprocessactlevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.project_id,invoiceflow_modules.flowlevel.level_id)
                if (getnexprocesstlevel):
                    print(f'next process module id {getnexprocesstlevel.module.module.id}')
                    getmodules=ProcessModule.objects.getmodule_byid(getnexprocesstlevel.module_id)
                    print(3,'next process module')
                    projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnexprocesstlevel.id,getnexprocesstlevel.projectflow_level_id)
                    if (getnexprocesstlevel.module.module.id == 7 and module == 6):
                        if bank_usercheck == 1:
                            PaymentInstruction.objects.filter(invoicecost__invoice_id=pk).update(verified_status=0)
                                #create invoiceflowmodule bank user
                            invoiceflow=Invoiceflowmodules.objects.createbankinvoiceflowmodules(contract_data.projects.id,request.company,invoiceflow_modules.flowlevel_id,None,pk,None,now,calculate_time)
                            invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('id',flat=True)
                            get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost).exclude(payable_amount=0)
                            print(f'get_payment_instruction {get_payment_instruction}')
                            for instruction in get_payment_instruction:
                                get_bank_uers=CompanyBankUser.objects.filter(companybank_id=instruction.companybank_id)
                                for bank_user in get_bank_uers:
                                    Invoiceflowmodulesusers.objects.creatbankinvoiceusers(contract_data.projects.id,invoiceflow.id,bank_user.user_id,instruction.id,bank_user.id,1)
                                    print(f'getnextlevel.module.module.id == 7 and module == 6 ')
                                    verb=f'Approved Payment Instructions'
                                    description=f'Instruction No {instruction.pi_number} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been sent for payment confirmation by {request.user.name} {request.user.lastname}'
                                    urls="invoice/vendorbasedinvoice"
                                    notify_invoice_flow(request,bank_user.user,urls,verb,description)
                                    bank_user_approvalmail(request,bank_user.user,instruction.pi_number,vendor,invoice_detail,all_invoice,comments)
                        else:
                            invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
                    else:
                        invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
                    if (getnexprocesstlevel.module.module.id == 5):
                        signatory_func(pk,invoice_detail.project.projectname.id,request,getnexprocesstlevel,invoiceflow,invoice_detail,all_invoice,vendor,1)
                    elif(getnexprocesstlevel.module.module.id == 7 and module == 6):
                        print(f'v invoiceflow {invoiceflow}')
                        if bank_usercheck == 0:
                            for user in projectflow_modules_users:
                                projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                                recipientuser = User.objects.get(id=projectusers.user_id)
                                get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                                approved_users=User.objects.filter(id__in=get_users)
                                urls=getInvoiceModule(getnexprocesstlevel.module.module.id,pk)
                                module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnexprocesstlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
                                
                    else:
                        for user in projectflow_modules_users:
                            projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                            Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                            recipientuser = User.objects.get(id=projectusers.user_id)
                            if getnexprocesstlevel.module.module.id == 4 or module == 3 and getnexprocesstlevel.module.module.id == 3:
                                get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3]).values_list('user',flat=True)
                            elif getnexprocesstlevel.module.module.id == 5:
                                get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
                            elif getnexprocesstlevel.module.module.id == 6 or getnexprocesstlevel.module.module.id == 5 and module == 5:
                                get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
                            else:
                                get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                            approved_users=User.objects.filter(id__in=get_users)
                            urls=getInvoiceModule(getnexprocesstlevel.module.module.id,pk)
                            module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnexprocesstlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments)
                else:
                    module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,7,all_invoice)
    return
    


def invoice_flow_func(pk,module,request,comments,submit_type,submit_name,payment_count=None,paymentinstruct=None):
    current_date=datetime.now()
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    bank_usercheck=0
    try:
        check_for_user=Settings.objects.get(company_id=request.company.id)
        bank_usercheck=check_for_user.bank_user
    except:
        bank_usercheck=0
    now = datetime.now()
    invoice_detail = Invoice.objects.get_by_id(pk)
    if (invoice_detail.contracttype == 'original'):
        contract=ContractMaster.objects.get_by_id(invoice_detail.contractid).first()
        contract_data=contract
    else:
        contract=Amendment.objects.get_by_id(invoice_detail.contractid ,1).first()
        contract_data=contract.service
    invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).values_list('invoice_number',flat=True))
    all_invoice=', '.join(str(e) for e in invoice_number)
    vendor=ContractMasterVendor.objects.get_byid(invoice_detail.vendor_id,request.company)
    get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
    get_invoice_date=get_payment_term.payment_terms.payment_day
    get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
    calculate_time=add_invoice_time(now,get_company_invoice_time)
    invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoiceids(pk,module)
    if (submit_type == "4"):
        InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_date= current_date )
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        content=f'Invoice {all_invoice} has been {submit_name} by {request.user.name} on {date_today} for {invoice_detail.name_service} '
        main_url="invoice/invoicelist"
        main_verb='Invoice '+submit_name+' '
        if module == 1 or module == 2:
            for notifications in allVendors:
                invoive_return_mail(request,notifications,vendor,submit_name,invoice_detail,comments,all_invoice,submit_type)
                notify_invoice_flow(request,notifications,main_url,main_verb,content)
    if paymentinstruct and module == None or module > 4:
        with_instructions=invoiceflow_modules.filter(payment_instruct__in=paymentinstruct)
    if (invoiceflow_modules.count() > 0):
        flow_modules=list(invoiceflow_modules.values_list('id',flat=True))
        try:
            with_instructionsmodule=list(with_instructions.values_list('id',flat=True))
        except:
            with_instructionsmodule=[]
        if module == None:
            print(11)
            invoice_singleId=Invoiceflowmodules.objects.filter(invoice_id=pk,status=1,module_id=6,payment_instruct__payment_count=payment_count,payment_instruct__in=paymentinstruct).last()
        elif paymentinstruct and module > 4:
            print(12)
            invoice_singleId=Invoiceflowmodules.objects.filter(invoice_id=pk,status=0,module_id=module,payment_instruct__in=paymentinstruct).first()
        else:
            print(13)
            invoice_singleId=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(pk,module)
        if module and  module < 5:
            print(1)
            Invoiceflowmodules.objects.filter(id__in=list(invoiceflow_modules.values_list('id',flat=True))).update(status=1)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_modules,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date)
        else:
            print(2)
            Invoiceflowmodules.objects.filter(id__in=list(with_instructions.values_list('id',flat=True))).update(status=1)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=with_instructionsmodule,user=request.user.id).update(status=submit_type,comments=comments,created_at=current_date)
        if (submit_type == '3' or submit_type == '4'): 
            Invoice.objects.filter(id=pk).update(invoice_status=4) if submit_type == '3' else Invoice.objects.filter(id=pk).update(invoice_status=5) 
            InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=4,approval_date=current_date) if submit_type == '3' else InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1).update(approval_status=5,approval_date=current_date)
            if(submit_type == '3'):
                Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=flow_modules,user=request.user.id).update(returned=1,returned_date=current_date)
        else:
           
            getnextlevel=ProjectFlowModules.objects.getnextactivelevel(invoice_singleId.flowlevel_id,invoice_singleId.flowlevel_module_id)
            print(f'getnextlevel {getnextlevel}')
            if(getnextlevel):
                getmodules=ProcessModule.objects.getmodule_byid(getnextlevel.module_id)
                projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnextlevel.id,getnextlevel.projectflow_level_id)
                if module == 2 and getnextlevel.module.module.id == 3 or module == 1 and getnextlevel.module.module.id == 3:
                    Invoice.objects.filter(id=pk).update(approval_status=1)
                if (getnextlevel.module.module.id == 7 and module == 6):
                    if bank_usercheck == 1:
                        PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,id__in=paymentinstruct).update(verified_status=0)
                            #create invoiceflowmodule bank user
                        for cost_inv in invoice_cost:
                            if check_payment_spit_module(cost_inv.id,payment_count ) :
                                get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                                invoiceflow=Invoiceflowmodules.objects.createbankinvoiceflowmodules(contract_data.projects.id,request.company,invoice_singleId.flowlevel_id,None,pk,None,now,calculate_time)
                                invoiceflow.invoicecost_id=cost_inv.id
                                paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                invoiceflow.payment_instruct_id=paymeny_ids.id
                                invoiceflow.save()
                                get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost.values_list('id',flat=True)).filter(id__in=paymentinstruct).exclude(payable_amount=0)
                                print(f'get_payment_instruction {get_payment_instruction}')
                                slit_value=get_payment_instruction.filter(invoicecost_id = cost_inv.id).first()
                                get_bank_uers=CompanyBankUser.objects.filter(companybank_id=slit_value.companybank_id)
                                
                                for bank_user in get_bank_uers:
                                    Invoiceflowmodulesusers.objects.creatbankinvoiceusers(contract_data.projects.id,invoiceflow.id,bank_user.user_id,slit_value.id,bank_user.id,1)
                                    verb=f'Approved Payment Instructions'
                                    description=f'Payment Instruction No {slit_value.pi_number} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been sent for payment confirmation by {request.user.name} {request.user.lastname}'
                                    urls="invoice/vendorbasedinvoice"
                                    notify_invoice_flow(request,bank_user.user,urls,verb,description)
                                    bank_user_approvalmail(request,bank_user.user,slit_value.pi_number,vendor,invoice_detail,all_invoice,comments) 
                    else:
                        final_percent=[]
                        for cost_inv in invoice_cost:
                                
                                invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,getnextlevel.projectflow_level_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
                                invoiceflow.invoicecost_id=cost_inv.id
                                invoiceflow.save()
                                get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                                if getnextlevel.module.module.id == 5 and module == 4:
                                    get_percent.filter(id__in=paymentinstruct).update(percentage_confirm=True)
                                    if get_percent.aggregate(total=Sum('payment_percentage'))['total'] == 100:
                                        final_percent.append(True)
                                    else:
                                        final_percent.append(False)
                                if (getnextlevel.module.module.id == 5):
                                    paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                    Invoiceflowmodules.objects.filter(id__in=flow_modules,invoicecost_id=cost_inv.id).update(payment_instruct_id=paymeny_ids.id)
                                    invoiceflow.payment_instruct_id=paymeny_ids.id
                                    invoiceflow.save()
                                    signatory_func(pk,invoice_detail.project.projectname.id,request,getnextlevel,invoiceflow,invoice_detail,all_invoice,vendor,1,payment_count,paymentinstruct,cost_inv)
                                else:
                                    if getnextlevel.module.module.id > 5:
                                        paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                        if paymeny_ids:
                                            invoiceflow.payment_instruct_id=paymeny_ids.id
                                            invoiceflow.save()
                                    for user in projectflow_modules_users:
                                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                        # command 
                                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                        if False in final_percent:
                            try:
                                getcurrentlevel=ProjectFlowModules.objects.get_project_flowmodule(invoice_singleId.flowlevel_id,invoice_singleId.flowlevel_module_id)
                                if(getcurrentlevel):
                                    print(f'next module id {getcurrentlevel.module.module.id}')
                                    getmodules=ProcessModule.objects.getmodule_byid(getcurrentlevel.module_id)
                                    projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getcurrentlevel.id,invoice_singleId.flowlevel_id)   
                                    for cost_inv in invoice_cost:
                                        invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getcurrentlevel.project_id,request.company,getnextlevel.projectflow_level_id,getcurrentlevel.id,pk,getmodules.module_id,now,calculate_time)
                                        invoiceflow.invoicecost_id=cost_inv.id
                                        invoiceflow.save()    
                                        for user in projectflow_modules_users:
                                            projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                            # command 
                                            Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getcurrentlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)  
                            except:
                                return

                else:
                    
                    final_percent=[]
                    cost_invoice=invoice_cost.first()
                    notification_count=0
                    inv_approval_notification = 0
                    for cost_inv in invoice_cost:
                        if cost_inv.approval_status != 3 :
                            invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,getnextlevel.projectflow_level_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
                            invoiceflow.invoicecost_id=cost_inv.id
                            invoiceflow.save()
                            inv_approval_notification += 1
                            get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                            if getnextlevel.module.module.id == 5 and module == 4:
                                get_percent.filter(id__in=paymentinstruct).update(percentage_confirm=True)
                                if get_percent.aggregate(total=Sum('payment_percentage'))['total'] == 100:
                                    final_percent.append(True)
                                else:
                                    final_percent.append(False)
                            if (getnextlevel.module.module.id == 5):
                                paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                               
                                Invoiceflowmodules.objects.filter(id__in=flow_modules,invoicecost_id=cost_inv.id).update(payment_instruct_id=paymeny_ids.id)
                                invoiceflow.payment_instruct_id=paymeny_ids.id
                                invoiceflow.save()
                                notification_count+=1
                                signatory_func(pk,invoice_detail.project.projectname.id,request,getnextlevel,invoiceflow,invoice_detail,all_invoice,vendor,1,payment_count,paymentinstruct,notification_count ,cost_inv)
                            else:
                                if getnextlevel.module.module.id > 5:
                                    paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                    if paymeny_ids:
                                        invoiceflow.payment_instruct_id=paymeny_ids.id
                                        invoiceflow.save()
                                for user in projectflow_modules_users:
                                    projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                    recipientuser = User.objects.get(id=projectusers.user_id)
                                    # command 
                                    if getnextlevel.module.module.id == 4 or module == 3 and getnextlevel.module.module.id == 3:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4]).values_list('user',flat=True)
                                    elif getnextlevel.module.module.id == 5:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
                                    elif getnextlevel.module.module.id == 6 or getnextlevel.module.module.id == 5 and module == 5:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
                                    else:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                                    approved_users=User.objects.filter(id__in=get_users)
                                    Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                                    urls=getInvoiceModule(getnextlevel.module.module.id,pk ,payment_count)
                                    if cost_inv.id == cost_invoice.id :
                                        module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments,inv_approval_notification)
                                    
                        else :
                            inv_approval_notification=1
                            if getnextlevel.module.module.id >= 5 and check_payment_spit_module(cost_inv.id,payment_count ) :
                                invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnextlevel.project_id,request.company,getnextlevel.projectflow_level_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)
                                invoiceflow.invoicecost_id=cost_inv.id
                                invoiceflow.save()
                                get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                                if getnextlevel.module.module.id == 5 and module == 4:
                                    get_percent.filter(id__in=paymentinstruct).update(percentage_confirm=True)
                                    if get_percent.aggregate(total=Sum('payment_percentage'))['total'] == 100:
                                        final_percent.append(True)
                                    else:
                                        final_percent.append(False)
                                if (getnextlevel.module.module.id == 5):
                                    paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                
                                    Invoiceflowmodules.objects.filter(id__in=flow_modules,invoicecost_id=cost_inv.id).update(payment_instruct_id=paymeny_ids.id)
                                    invoiceflow.payment_instruct_id=paymeny_ids.id
                                    invoiceflow.save()
                                    signatory_func(pk,invoice_detail.project.projectname.id,request,getnextlevel,invoiceflow,invoice_detail,all_invoice,vendor,1,payment_count,paymentinstruct,cost_inv)
                                else:
                                    if getnextlevel.module.module.id > 5:
                                        paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                        if paymeny_ids:
                                            invoiceflow.payment_instruct_id=paymeny_ids.id
                                            invoiceflow.save()
                                    for user in projectflow_modules_users:
                                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                        # command 
                                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                                        recipientuser = User.objects.get(id=projectusers.user_id) 
                                        if getnextlevel.module.module.id == 4 or module == 3 and getnextlevel.module.module.id == 3:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4]).values_list('user',flat=True)
                                        elif getnextlevel.module.module.id == 5:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
                                        elif getnextlevel.module.module.id == 6 or getnextlevel.module.module.id == 5 and module == 5:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
                                        else:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                                        approved_users=User.objects.filter(id__in=get_users)
                                        urls=getInvoiceModule(getnextlevel.module.module.id,pk,payment_count)
                                        module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments ,inv_approval_notification)


                    invoice_cost.filter(partial_status = 3).update(approval_status=3)
                    if False in final_percent:

                        try:
                            inv_approval_notification = 0
                            getcurrentlevel=ProjectFlowModules.objects.get_project_flowmodule(invoice_singleId.flowlevel_id,invoice_singleId.flowlevel_module_id)
                            if(getcurrentlevel):
                                print(f'next module id {getcurrentlevel.module.module.id}')
                                getmodules=ProcessModule.objects.getmodule_byid(getcurrentlevel.module_id)
                                projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getcurrentlevel.id,invoice_singleId.flowlevel_id)
                                cost_invoice=invoice_cost.first()   
                                for cost_inv in invoice_cost:
                                    invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getcurrentlevel.project_id,request.company,getnextlevel.projectflow_level_id,getcurrentlevel.id,pk,getmodules.module_id,now,calculate_time)
                                    
                                    invoiceflow.invoicecost_id=cost_inv.id
                                    invoiceflow.save()    
                                    inv_approval_notification += 1
                                    for user in projectflow_modules_users:
                                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                        # command 
                                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getcurrentlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)  
                                        recipientuser = User.objects.get(id=projectusers.user_id) 
                                        if getnextlevel.module.module.id == 4 or module == 3 and getnextlevel.module.module.id == 3:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4]).values_list('user',flat=True)
                                        elif getnextlevel.module.module.id == 5:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
                                        elif getnextlevel.module.module.id == 6 or getnextlevel.module.module.id == 5 and module == 5:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
                                        else:
                                            get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                                        approved_users=User.objects.filter(id__in=get_users)
                                        urls=getInvoiceModule(getnextlevel.module.module.id,pk ,payment_count)
                                        if cost_inv.id == cost_invoice.id :
                                            module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnextlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments ,inv_approval_notification)
                        except:
                            return
            else:
                getnexprocesstlevel=ProjectFlowModules.objects.getnxtprocessactlevel(invoice_singleId.flowlevel_id,invoice_singleId.project_id,invoice_singleId.flowlevel.level_id)
                if(getnexprocesstlevel):
                    getmodules=ProcessModule.objects.getmodule_byid(getnexprocesstlevel.module_id)
                    projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnexprocesstlevel.id,getnexprocesstlevel.projectflow_level_id)
                    print(f'getnexprocesstlevel.module.module.id == 7 {getnexprocesstlevel.module.module.id}, getnexprocesstlevel {getnexprocesstlevel}')
                    if module == 2 and getnexprocesstlevel.module.module.id == 3 or module == 1 and getnexprocesstlevel.module.module.id == 3:
                        Invoice.objects.filter(id=pk).update(approval_status=1)
                    if (getnexprocesstlevel.module.module.id == 7 and module == 6):
                        if bank_usercheck == 1:
                            PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,id__in=paymentinstruct).update(verified_status=0)
                                #create invoiceflowmodule bank user
                            for cost_inv in invoice_cost:
                                get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                                invoiceflow=Invoiceflowmodules.objects.createbankinvoiceflowmodules(contract_data.projects.id,request.company,invoice_singleId.flowlevel_id,None,pk,None,now,calculate_time)
                                invoiceflow.invoicecost_id=cost_inv.id
                                paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                invoiceflow.payment_instruct_id=paymeny_ids.id
                                invoiceflow.save()
                                get_payment_instruction=PaymentInstruction.objects.get_all_inv_cost(invoice_cost.values_list('id',flat=True)).filter(id__in=paymentinstruct).exclude(payable_amount=0)
                                print(f'get_payment_instruction {get_payment_instruction}')
                                for instruction in get_payment_instruction:
                                    get_bank_uers=CompanyBankUser.objects.filter(companybank_id=instruction.companybank_id)
                                    for bank_user in get_bank_uers:
                                        Invoiceflowmodulesusers.objects.creatbankinvoiceusers(contract_data.projects.id,invoiceflow.id,bank_user.user_id,instruction.id,bank_user.id,1)
                                        verb=f'Approved Payment Instructions'
                                        description=f'Payment Instruction No {instruction.pi_number} for invoice {all_invoice} for Vendor {vendor.vendor_name} for services {invoice_detail.name_service} has been sent for payment confirmation by {request.user.name} {request.user.lastname}'
                                        urls="invoice/vendorbasedinvoice"
                                        notify_invoice_flow(request,bank_user.user,urls,verb,description)
                                        bank_user_approvalmail(request,bank_user.user,instruction.pi_number,vendor,invoice_detail,all_invoice,comments)
                        else:
                            final_percent=[]
                            for cost_inv in invoice_cost:
                                invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
                                invoiceflow.invoicecost_id=cost_inv.id
                                invoiceflow.save()
                                get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                                if getnexprocesstlevel.module.module.id == 5 and module == 4:
                                    get_percent.filter(id__in=paymentinstruct).update(percentage_confirm=True)
                                    if get_percent.aggregate(total=Sum('payment_percentage'))['total'] == 100:
                                        final_percent.append(True)
                                    else:
                                        final_percent.append(False)
                                if (getnexprocesstlevel.module.module.id == 5):
                                    paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                    Invoiceflowmodules.objects.filter(id__in=flow_modules,invoicecost_id=cost_inv.id).update(payment_instruct_id=paymeny_ids.id)
                                    invoiceflow.payment_instruct_id=paymeny_ids.id
                                    invoiceflow.save()
                                    signatory_func(pk,invoice_detail.project.projectname.id,request,getnexprocesstlevel,invoiceflow,invoice_detail,all_invoice,vendor,1,payment_count,paymentinstruct)
                                else:
                                    if getnexprocesstlevel.module.module.id > 5:
                                        paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                        if paymeny_ids:
                                            invoiceflow.payment_instruct_id=paymeny_ids.id
                                            invoiceflow.save()
                                    for user in projectflow_modules_users:
                                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                        # command 
                                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                            if False in final_percent:
                                try:
                                    getcurrentlevel=ProjectFlowModules.objects.get_project_flowmodule(invoice_singleId.flowlevel_id,invoice_singleId.flowlevel_module_id)
                                    if(getcurrentlevel):
                                        print(f'next module id {getcurrentlevel.module.module.id}')
                                        getmodules=ProcessModule.objects.getmodule_byid(getcurrentlevel.module_id)
                                        projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getcurrentlevel.id,invoice_singleId.flowlevel_id)   
                                        for cost_inv in invoice_cost:
                                            invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getcurrentlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getcurrentlevel.id,pk,getmodules.module_id,now,calculate_time)
                                            invoiceflow.invoicecost_id=cost_inv.id
                                            invoiceflow.save()    
                                            for user in projectflow_modules_users:
                                                projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                                # command 
                                                Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getcurrentlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)  
                                except:
                                    return
                    else:
                        final_percent=[]
                        inv_approval_notification = 0
                        for cost_inv in invoice_cost:
                            invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
                            invoiceflow.invoicecost_id=cost_inv.id
                            invoiceflow.save()
                            get_percent=PaymentInstruction.objects.filter(invoicecost_id=cost_inv.id,status=True)
                            inv_approval_notification+=1
                            if getnexprocesstlevel.module.module.id == 5 and module == 4:
                                get_percent.filter(id__in=paymentinstruct).update(percentage_confirm=True)
                                if get_percent.aggregate(total=Sum('payment_percentage'))['total'] == 100:
                                    final_percent.append(True)
                                else:
                                    final_percent.append(False)
                            if (getnexprocesstlevel.module.module.id == 5):
                                paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                Invoiceflowmodules.objects.filter(id__in=flow_modules,invoicecost_id=cost_inv.id).update(payment_instruct_id=paymeny_ids.id)
                                invoiceflow.payment_instruct_id=paymeny_ids.id
                                invoiceflow.save()
                                signatory_func(pk,invoice_detail.project.projectname.id,request,getnexprocesstlevel,invoiceflow,invoice_detail,all_invoice,vendor,1,payment_count,paymentinstruct , cost_inv)
                            else:
                                if getnexprocesstlevel.module.module.id > 5:
                                    paymeny_ids=get_percent.filter(id__in=paymentinstruct).first()
                                    if paymeny_ids:
                                        invoiceflow.payment_instruct_id=paymeny_ids.id
                                        invoiceflow.save()
                                for user in projectflow_modules_users:
                                    projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                    # command 
                                    Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                                    recipientuser = User.objects.get(id=projectusers.user_id)
                                    if getnexprocesstlevel.module.module.id == 4 or module == 3 and getnexprocesstlevel.module.module.id == 3:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3]).values_list('user',flat=True)
                                    elif getnexprocesstlevel.module.module.id == 5:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[3,4,5]).values_list('user',flat=True)
                                    elif getnexprocesstlevel.module.module.id == 6 or getnexprocesstlevel.module.module.id == 5 and module == 5:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id,Invoiceflowmodules__module_id__in=[4,5]).values_list('user',flat=True)
                                    else:
                                        get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status__in=[1,2],Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                                    approved_users=User.objects.filter(id__in=get_users)
                                    urls=getInvoiceModule(getnexprocesstlevel.module.module.id,pk,payment_count)
                                    module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,getnexprocesstlevel.module.module.id,all_invoice,recipientuser,urls,approved_users,comments,inv_approval_notification)
                                    
                        if False in final_percent:
                            try:
                                getcurrentlevel=ProjectFlowModules.objects.get_project_flowmodule(invoice_singleId.flowlevel_id,invoice_singleId.flowlevel_module_id)
                                if(getcurrentlevel):
                                    print(f'next module id {getcurrentlevel.module.module.id}')
                                    getmodules=ProcessModule.objects.getmodule_byid(getcurrentlevel.module_id)
                                    projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getcurrentlevel.id,invoice_singleId.flowlevel_id)   
                                    for cost_inv in invoice_cost:
                                        invoiceflow=Invoiceflowmodules.objects.createinvoiceflowmodules(getcurrentlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getcurrentlevel.id,pk,getmodules.module_id,now,calculate_time)
                                        invoiceflow.invoicecost_id=cost_inv.id
                                        invoiceflow.save()    
                                        for user in projectflow_modules_users:
                                            projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                                            # command 
                                            Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getcurrentlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)  
                            except:
                                return

                else:
                    module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,7,all_invoice,None,None,None,None,None ,payment_count)
    return
     
    

class split_invoice_amout(View):
    def get(self, request,pk): 
        get_invoice=Invoice.objects.get_by_id_status(pk,1)
        invoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        module_value=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
        get_credit_note=get_credit_notes(get_invoice.id)
        sign_data=check_user_sign(self.request.user)
        context={"pk":pk,"invoice_details":invoice , "get_invoice":get_invoice ,"module_value":module_value ,"module_count":len(module_value),'sign_data':sign_data,'get_credit_note':get_credit_note}
        
        return render(request ,"splitinvoiceamount.html",context)

    def post(self, request,pk):
        current_date=datetime.now()
        invoice_id=request.POST.get('invoice')
        payment_id=request.POST.get('payment_id')
        invoice_cost_list=request.POST.getlist('invoice_cost')
        print(f'invoice_cost_list {invoice_cost_list}, payment_id {payment_id}, invoice_id {invoice_id}')
        for inv_cost in invoice_cost_list:
            payment_instruct=PaymentInstruction.objects.filter(invoicecost_id=inv_cost,payment_count=payment_id,status=True).first()
            payment_instruct_li=list(PaymentInstruction.objects.filter(invoicecost_id=inv_cost,payment_count=payment_id,status=True).values_list('id',flat=True))
            PaymentInstruction.objects.filter(invoicecost_id=inv_cost,payment_count=payment_id,status=True).update(payment_status=3)
            pay_id=PaymentReceipt.objects.create_data(request.company.id,invoice_id,inv_cost,request.user.id)
            pay_id.payment_instruct=payment_instruct
            pay_id.save()
            payment_percentage=request.POST.getlist('payment_percentage_'+str(inv_cost))
            files=request.FILES.getlist('file_'+str(inv_cost)+'[]')
            
            print(f' payment_percentage {payment_percentage}, files {files}')
            for percentage,file in zip(payment_percentage,files):
                if file != "":
                    PaymentReceiptFile.objects.create_file_data(pay_id.id,percentage,file.name,current_date)
                else :
                    PaymentReceiptFile.objects.create_file_data(pay_id.id,percentage,file,current_date)

            # update invoicecost data
            InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1,id=inv_cost).update(payment_date=current_date,approval_date=current_date)
        # complete process
        payemnt_check=True
        if Invoiceflowmodules.objects.filter(module_id=4,status=0,invoice_id=pk).exists():
            payemnt_check=False

        payment_count=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,payment_count=payment_id,status=True).values_list('id',flat=True))
        total_payment=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).count()
        paid_count=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True,payment_status=3).count()
        overall_count=PaymentInstruction.objects.get_by_payment(invoice_id).filter(payment_count=payment_id).exclude(payable_amount=0).count()
        verified_count=PaymentInstruction.objects.get_verified_instruction(invoice_id,1).filter(payment_count=payment_id).exclude(payable_amount=0).count()
        print(f'total_payment{total_payment},paid_count{paid_count},overall_count{overall_count},verified_count{verified_count}')
        if (overall_count == verified_count):
            invoice_flow_func(invoice_id,7,request,None,"1","Approved",payment_id,payment_count)
            if payemnt_check:
                if total_payment == paid_count:
                    Invoice.objects.filter(id=invoice_id).update(invoice_status=3)
                    # InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1,id=inv_cost).update(approval_status=3,payment_status=2,payment_date=current_date,approval_date=current_date)
                    InvoiceCostInvoice.objects.filter(invoice_id=invoice_id,status=1).update(approval_status=3,payment_status=2)
                    return redirect(reverse_lazy("invoice:paidinvoicelist"))
        else:
            invoiceflow_modules=Invoiceflowmodules.objects.filter(invoice_id=invoice_id,module_id=7,payment_instruct_id__in=payment_count)
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=invoiceflow_modules,user=request.user.id).update(status=1,comments=None,created_at=current_date)
        
        return redirect(reverse_lazy("invoice:vendorbasedinvoice"))
    
    
class payment_instructions_view(View):
    def get(self, request,pk ,pay_id): 
        get_invoice=Invoice.objects.get_by_id_status(pk,1)
        invoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
        module_value=list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
        context={"pk":pk,"invoice_details":invoice , "get_invoice":get_invoice ,"module_value":module_value ,"module_count":len(module_value),'paycount':pay_id,'contractcostinvoice':contractcostinvoice}
        
        return render(request ,"payment_instructions_view.html",context)


def payment_receipt_invoice_percentage(request, invoice_id, paycount, invoice_number):
    try:
        payment_split_percentage = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,status=True,payment_count=paycount,invoicecost__invoice_number=invoice_number).first()
        payment_instructions = PaymentInstruction.objects.filter(invoicecost__invoice_id=invoice_id,status=True,payment_count=paycount)
        payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_instructions)

        return JsonResponse({'percentage': payment_split_percentage.payment_percentage})
    
    except Exception as e:
        return JsonResponse({'error': 'An error occurred'}, status=400)
