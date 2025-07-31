from urllib import request
from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Count
from custom_auth.models import *
from projects.models import *
from invoice.models import *
from credit_note.models import *
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta,date
from django.db.models import Q
from django.views.generic import View
import re
from easy_pdf.views import PDFTemplateView
# from itertools import chain
from django.template.loader import get_template
from notifications.signals import notify
from invoice.utils.utils import unique_list
from weasyprint import HTML, CSS
from io import BytesIO
from django.template import RequestContext, Template
import base64
from django.conf import settings
from PIL import Image
from django.template.loader import render_to_string
from custom_auth.helpers import *
from invoice.helpers import *
from .utils import credit_note_pdfstyle
from projectflow.models import ProjectFlowlevel,ProjectFlowModules,ProjectFlowModuleUsers
from InvoiceGuard.models import ProcessModule,RoleRight
from wcc.views import add_time
from .helpers import *
from invoice.templatetags.invoice_custom_tags import checkpermission_creditnoterecipt,check_for_flow,checkpermission_invoiceapproval_dispute
from projects.helpers import create_user_log
import requests
from invoice.templatetags.invoice_custom_tags import confulldate , get_returned_invoice_count
from .templatetags.credit_custom_tags import credit_contract_invoices,remove_symbol,remove_currency_symbol
import json


# Create your views here.
def create_credit_note(request):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu'] = 'credit_list'
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    invoice_contracts=Invoice.objects.filter(vendor_id=vendorid,invoice_status=2,contracttype='original').values_list('contractid',flat=True).annotate(dcount=Count('contractid')).order_by()
    get_contracts=ContractMaster.objects.filter(id__in=list(invoice_contracts))
    company=Settings.objects.filter(company_id=request.company.id).first()
    all_contracts=[]
    creditnote_create_id=''
    for contract in get_contracts:
        active_status=0
        if contract.projects.active_status:
            active_status=1
        all_contracts.append({'id':contract.id,'ref_num':contract.reference_number,'currency_id':contract.currency.id,'currency_symbol':contract.currency.currency_symbol,'contract_type':'original','contract_currency':contract.currency.currency,'active_status':active_status,'project_name':contract.projects.projectname.name})
    invoice_contracts_amendments=Invoice.objects.filter(vendor_id=vendorid,invoice_status=2,contracttype__startswith='a').values_list('contractid',flat=True).annotate(dcount=Count('contractid')).order_by()
    get_amendmnets=Amendment.objects.filter(id__in=list(invoice_contracts_amendments))
    for amendmnet in get_amendmnets:
        active_status=0
        if amendmnet.service.projects.active_status:
            active_status=1
        all_contracts.append({'id':amendmnet.id,'ref_num':amendmnet.amendment_reference_number,'currency_id':amendmnet.amendment_currency.id,'currency_symbol':amendmnet.amendment_currency.currency_symbol,'contract_type':amendmnet.amendment_type,'contract_currency':amendmnet.amendment_currency.currency,'active_status':active_status,'project_name':amendmnet.service.projects.projectname.name})
    # model_combination = list(chain(get_contracts, get_amendmnets))
    if (request.POST):
        post_values=request.POST
        contract=post_values.get('contract')
        contract_type=post_values.get('contract_type')
        contract_invoice=post_values.getlist('invoice')
        total_value=post_values.get('total_value')
        exclusives=post_values.getlist('exclusive')
        added_exclusive_value=post_values.get('final_exclusive_value')
        exclusive_percentage=post_values.getlist('exclusive_percentage')
        exclusive_value=post_values.getlist('exclusive_value')
        totalalltax=post_values.get('totalalltax')
        invoice_ids=post_values.getlist('invoice_id')
        invoice_split=post_values.getlist('invoice_split')
        credit_percentage=post_values.getlist('invoice_percentage')
        credit_symbol=post_values.getlist('invoice_symbol')
        credit_name=post_values.getlist('credit_name')
        credit_date=post_values.getlist('credit_date')
        base_amount=post_values.getlist('base_amount')
        exchange_rate=post_values.getlist('exchange')
        final_amount=post_values.getlist('final_amount')
        companydateformat=post_values.get('dateformat')
        supporting_documents=request.FILES.getlist('support_file')
        print('supporting_documents',supporting_documents)
        invoice_value=post_values.get('total_invoice_value')
        creditvalue_total=post_values.get('creditvalue_total')
        total_invoice_value1 = (''.join(e for e in invoice_value if e.isalnum()).replace(',',''))
        get_total_value1=re.findall(r'[0-9][0-9,.]+', total_invoice_value1)
        get_total_value = get_total_value1[0]
        contractid=Invoice.objects.filter(id__in=contract_invoice).last()
        print('contractid ' , contractid)
        if (contract_type == 'original'):
            create_credit=CreditNote.objects.create(contract_id=contract,contracttype=contract_type,total_value=total_value,total_value_excluisve_tax=totalalltax,vendor_id=vendorid.id,company_id=vendorid.company.id,exclusive_value=added_exclusive_value,total_invoice_value=get_total_value,grossamnt_withoutexclusive=creditvalue_total)
            contract=ContractMaster.objects.filter(id=contract ,status=1).first()
            vendortax=VendorCompanyTaxDetails.objects.filter(vendor_id=vendorid.id,contract_id=contract,company=request.company,status=1)
            contract_data=contract
        else:
            create_credit=CreditNote.objects.create(amendment_id=contract,contracttype=contract_type,total_value=total_value,total_value_excluisve_tax=totalalltax,vendor_id=vendorid.id,company_id=vendorid.company.id,exclusive_value=added_exclusive_value,total_invoice_value=get_total_value,grossamnt_withoutexclusive=creditvalue_total)
            contract=Amendment.objects.filter(id=contract,status=1).first()
            vendortax=VendorCompanyTaxDetails.objects.filter(vendor_id=vendorid.id,amendment_id=contract,company=request.company,status=1)
            contract_data=ContractMaster.objects.filter(id=contract.service.id ,status=1).first()
        print(f'contract {contract},invoice {contractid}')
        inclusivetaxlist=vendortax.filter(Tax_Type="Inclusive").values_list('id',flat=True)
        getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=inclusivetaxlist,status=1).values('id','vendortax_id__tax__Tax_Name','taxpercentage')
        for invoice in contract_invoice:
            if (invoice):
                create_contract_invoice=CreditNoteInvoice.objects.create(credit_id=create_credit.id,invoice_id=invoice)
        for exclusive,percentage,value in zip(exclusives,exclusive_percentage,exclusive_value):
            if (exclusive):
                create_exclusive_tax=CreditNoteExclusive.objects.create(exclusive_id=exclusive,exclusive_percentage=percentage,exclusive_calculated_value=value,credit_id=create_credit.id,created_vendor_id=request.user.id)
        for invoice_id,split,name,dated,base,rate,final,percentage,symbol in zip(invoice_ids,invoice_split,credit_name,credit_date,base_amount,exchange_rate,final_amount,credit_percentage,credit_symbol):
            convert_date=convertdate(companydateformat,dated)
            net_payable_value=get_netpayable(creditvalue_total,rate,getinclusivewithpercentage,percentage)
            get_file=request.FILES.get('credit_file'+str(invoice_id))
            if (get_file == None):
                file=None
            else:
                file=get_file
            remove_circle=re.sub(r'\(|\)', '', final)
            base_currency_amount_re=re.sub(r'\(|\)', '', base)
            create_credit_invoice=CreditNoteContractInvoice.objects.create(credit_id=create_credit.id,vendor_split_invoice_id=invoice_id,currency_split=split,credit_note_no=name,date=convert_date,base_currency_amount=base_currency_amount_re,exchange_rate=rate,payment_currency_amount=remove_circle,file=file,percentage=percentage,symbol=symbol,new_netpayable=net_payable_value)
            creditnote_create_id = create_credit_invoice.credit.id
        for document in supporting_documents:
            create_support_documents=CreditSupportDocuments.objects.create(credit_id=create_credit.id,file=document)
        submit_value=post_values.get('submit_value')
        if (submit_value == '0'):
            return redirect('credit:credit_note_list')
        elif (submit_value == '1'):
            credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=create_credit.id,status=1).values_list('credit_note_no',flat=True))
            all_credit=', '.join(str(e) for e in credit_number)
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            now = datetime.now()
            today = date.today()
            date_today = today.strftime("%d-%b-%Y")
            getvin=request.user.cin_number
            calculate_time=add_time(now,request.company)
            CreditNote.objects.filter(id=create_credit.id).update(created_at=calculate_time,credit_status=2)
            sender = User.objects.filter(id=request.user.id).first()
            recipient = User.objects.filter(company=request.company.id,roles_id=2).first()
            scheme=request.scheme
            gethost=request.get_host()
            url=f"{scheme}://{gethost}/dashboard/dashboard/"
            if (contract_data.projects.flow_level == "discipline"):
                checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdisciplinetype_id,'discipline',request.company,contract_data.projects_id)
            elif (contract_data.projects.flow_level == "clusters"):
                checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdiscipline.cluster_id,'clusters',request.company,contract_data.projects_id)
            else:
                if contractid.well_not_applicable == "id":
                    if (contract_type == 'original'):
                        checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contractid.well_id,'well',request.company,contract.projects_id)
                    else :
                        checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contractid.well_id,'well',request.company,contract.service.projects_id)
                else:
                    #use wellbased field to get data
                    checkflow=ProjectFlowlevel.objects.projectflow_bywellbasedlevel_main(contract_data.projectdisciplinetype_id,'well',request.company,contract_data.projects_id)
            flowlevelmodules=ProjectFlowModules.objects.getactiveflow_level(checkflow.id)
            flowlevelusers=ProjectFlowModuleUsers.objects.getflowusers_active(flowlevelmodules.id,checkflow.id)
            getmodules=ProcessModule.objects.getmodule_byid(flowlevelmodules.module_id)
            get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=contractid.id).first()
            get_invoice_date=get_payment_term.payment_terms.payment_day
            get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
            calculate_time=add_invoice_time(now,get_company_invoice_time)
            creditflow_modules=Invoiceflowmodules.objects.createcreditflowmodules(contract_data.projects_id,request.company,checkflow.id,flowlevelmodules.id,create_credit.id,getmodules.module_id,now,calculate_time)
            for user in flowlevelusers:
                projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(contract_data.projects_id,projectusers.id,creditflow_modules.id,user.id,projectusers.user_id)
                recipientuser = User.objects.get(id=projectusers.user_id)
                url=f"{scheme}://{gethost}/credit/checklist/{creditnote_create_id}"
                notify.send(sender, recipient=recipientuser,data=url, verb='Credit note Received.', description=f'Credit Note received from {get_vendor_company_name(request.user.cin_number)} for {contractid.name_service}')
                credit_submission_mail_user(request,recipientuser,vendorid,all_credit,all_invoice,contractid)

            all_vendors = User.objects.filter(cin_number__iexact=getvin,status=1)
            for notifications in all_vendors:
                url=f"{scheme}://{gethost}/credit/list"
                notify.send(sender, recipient=notifications,data=url, verb='Credit note Received.', description=f'Credit Note received by {recipient.name} on {date_today} for {contractid.name_service} ')
                credit_submission_mail_vendor(request,notifications,vendorid)

            created_credit_invoice=CreditNoteContractInvoice.objects.filter(credit_id=create_credit.id)
            get_count=created_credit_invoice.filter(Q(credit_note_no='') | Q(date__isnull=True) | Q(base_currency_amount='') | Q(exchange_rate='') | Q(payment_currency_amount='') | Q(file='')).count()
            usercreate=request.user.roles_id
            credit_number = f"Credit Note Number{all_credit} Reference Invoice Number {all_invoice}" 
            create_user_log(request,credit_number,'Credit Note','Create','Credit Note Submitted',usercreate)
            return redirect('credit:credit_note_list')
        else:
            return redirect('credit:credit_file_preview',pk=create_credit.id)

    data={'all_contracts':all_contracts,'company':company}
    return render(request,'create_credit_note.html',data)

def get_contract_invoices(request):
    contract_id=request.GET.get('contract_id')
    contract_type=request.GET.get('contract_type').lower()
    vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    get_invoice_ids=Invoice.objects.filter(contractid=contract_id,contracttype=contract_type).exclude(invoice_status=1).values_list('id',flat=True)
    list_invoices=[]
    if (contract_type == 'original'):
        vendortax=VendorCompanyTaxDetails.objects.getvendortaxdetails_by_contract(vendorid.id,contract_id,request.company)
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=vendorid.id,contract_id=contract_id,company=request.company,status=1).values('percentage','exchange_rate','currency_id__currency_symbol','currency_id','id')
        get_exchange_rate=list(VendorInvoiceSplit.objects.filter(vendor_id=vendorid.id,contract_id=contract_id,company=request.company,status=1).values_list('exchange_rate', flat=True).distinct())
        exchange_rate_value=get_exchange_rate[0]
        invoice_count=len(vendorinvoice)
    else:
        vendortax=VendorCompanyTaxDetails.objects.getvendortaxdetails_by_amendment(vendorid.id,contract_id,request.company)
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=vendorid.id,amendment_id=contract_id,company=request.company,status=1).values('percentage','exchange_rate','currency_id__currency_symbol','currency_id','id')
        get_exchange_rate=VendorInvoiceSplit.objects.filter(vendor_id=vendorid.id,amendment_id=contract_id,company=request.company,status=1).values_list('exchange_rate', flat=True).distinct()
        exchange_rate_value=get_exchange_rate[0]
        invoice_count=len(vendorinvoice)
    for i in get_invoice_ids:
        inv_status=Invoice.objects.filter(id=i).first()
        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=i,status=1).values('invoice_number','invoice_date','invoice_exchange_rate','currency')
        if '2' in get_exchange_rate:  
            currency=len(set([ i['currency'] for i in invoice_cost ]))
            invoice_exchange_rate=len(set([ i['invoice_exchange_rate'] for i in invoice_cost ]))
            if currency != 1 and invoice_exchange_rate == 1:
                list_invoices.append({'invoice_id':i,'inv_status':inv_status.invoice_status,'invoice_num':list(invoice_cost)})
            else:
                list_invoices.append({'invoice_id':i,'inv_status':inv_status.invoice_status,'invoice_num':list(invoice_cost)})
                #base_exchange_rate=''.join(set([ i['invoice_exchange_rate'] for i in invoice_cost ]))
        else:
            list_invoices.append({'invoice_id':i,'inv_status':inv_status.invoice_status,'invoice_num':list(invoice_cost)})
    
    inclusivetaxlist=vendortax.filter(Tax_Type="Inclusive").values_list('id',flat=True)
    getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=inclusivetaxlist,status=1).values('id','vendortax_id__tax__Tax_Name','taxpercentage')
    exclusivetaxlist=vendortax.filter(Tax_Type="Exclusive").values_list('id',flat=True)
    getexclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=exclusivetaxlist,status=1).values('id','vendortax_id__tax__Tax_Name','taxpercentage')
    data={'data':list_invoices,'inclusive_taxes':list(getinclusivewithpercentage),'exclusive_taxes':list(getexclusivewithpercentage),'vendor_invoices':list(vendorinvoice),'invoice_count':invoice_count,'exchange_rate_value':exchange_rate_value}
    return JsonResponse(data)

def checkcreditno(request):
    credit_no=request.GET.get('val')
    if (CreditNoteContractInvoice.objects.filter(credit_note_no__exact=credit_no,status=1).exists()):
        data={'data':'exists'}
    else:
        data={'data':'success'}
    return JsonResponse(data)

def credit_file_preview(request,pk):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu'] = 'credit_list'
    credit_note=CreditNote.objects.get(id=pk,status=1)
    credit_note_invoices=CreditNoteContractInvoice.objects.filter(credit_id=credit_note.id)
    credit_invoice_ids=CreditNoteInvoice.objects.filter(credit_id=credit_note.id,status=1).values_list('invoice_id',flat=True)
    invoice_list=[]
    for id in credit_invoice_ids:
        get_invoices_cost=InvoiceCostInvoice.objects.filter(invoice_id=id).values_list('invoice_number',flat=True)
        invoice_list.append({'id':id,'inv_num':list(get_invoices_cost)})
    data={'credit_note_invoice':credit_note_invoices,'pk':pk,'invoice_list':invoice_list,'basecurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency_symbol',flat=True).first(),'exchange_rate':credit_note_invoices.values_list('vendor_split_invoice__exchange_rate',flat=True).first(),'paymentcurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency_symbol',flat=True).last()}
    return render(request,'credit_file_preview.html',data)

def get_supportfiles(request):
    support_id=request.GET.get('support_id','')
    credit_id=request.GET.get('credit_id','')
    if (support_id == "9" or support_id == "10"):
        credit=CreditNote.objects.get(id=credit_id)
        if (credit.contracttype == 'original'):
            contract=ContractMaster.objects.filter(id=credit.contract_id ,status=1).first()
            
            contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,1).values()
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,2).values()
            confile=str(contract.upload_contract)
            price_file=str(contract.upload_pricetable)
            data={'con_file':list(contract_table_files),'price_file':list(price_table_files),'contracttype':credit.contracttype}
            # confile=str(credit.contract.upload_contract)
            # price_file=str(credit.contract.upload_pricetable)
            # data={'con_file':confile,'price_file':price_file}
            
        else:


            contract=Amendment.objects.filter(id=credit.amendment_id ,status=1).first()

            original_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,1).values()
            original_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,2).values()

            amendment_addendum_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,1).values()
            amendment_addendum_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,2).values()
            confile=original_contract_table_files.union(amendment_addendum_contract_table_files)
            price_table_files=original_price_table_files.union(amendment_addendum_price_table_files)
            data={'con_file':list(confile),'price_file':list(price_table_files),'contracttype':credit.contracttype}
            # contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
            # confile=str(credit.amendment.amendment_upload_contract)
            # price_file=str(credit.amendment.amendment_upload_pricetable)
            # data={'con_file':confile,'price_file':price_file}
        return JsonResponse(data,safe=False)
    elif (support_id == '8'):
        get_support_documents=CreditSupportDocuments.objects.filter(credit_id=credit_id,status=1).values()
        data={'filecount':get_support_documents.count(),'files':list(get_support_documents)}
        return JsonResponse(data)

def get_invoice_files(request):
    invoice_id=request.GET.get('invoice_id')
    all_invoice_documents=InvoiceFileUpload.objects.filter(invoice_id=invoice_id,status=1)
    invoice_files=all_invoice_documents.exclude(invoicecostinvoice__isnull=True).values_list('support_file')
    other_files=all_invoice_documents.exclude(invoicecostinvoice__isnull=False).values_list('support_file')
    file_names = [doc.file_name for doc in all_invoice_documents]
    file_names_and_support = {}
    for doc in all_invoice_documents:
        file_names_and_support[doc.file_name] = doc.support
    data={'invoice_files':list(invoice_files),'other_files':list(other_files),'file_name': file_names,'file_names_and_support': file_names_and_support}
    return JsonResponse(data)

def credit_note_list(request):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu'] = 'credit_list'
    user=User.objects.filter(Q(is_primary=1) | Q(is_secondary=1),id=request.user.id).first()
    vendor_status = True if user else False
    vendor_id=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    # credit_note=CreditNote.objects.getcreditnote_by_vendor(vendor_id.id) if vendor_status == True else CreditNote.objects.getcreditnote_by_creditstatus(vendor_id.id)
    # data={'credit_note':credit_note,'vendor_status':vendor_status,'credit_note_count':credit_note.count(),'vendorid':vendor_id}
    data={'vendor_status':vendor_status,'vendorid':vendor_id}
    return render(request,'credit_note_list.html',data)

def credit_view(request,pk):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu'] = 'credit_list'
    credit_note=CreditNote.objects.getcreditnote_by_id(pk)
    contract_id = credit_note.contract_id
    # If you need the contract object itself, you can access it like this:
    contract = credit_note.contract
    ammentment_id = credit_note.amendment

    credit_note_invoices=CreditNoteContractInvoice.objects.getcreditnoteinvoice_by_creditnoteid(credit_note.id)
    credit_invoice_ids=CreditNoteInvoice.objects.getcreditnoteinvoice(credit_note.id)
    invoice_detail = Invoice.objects.filter(id__in=credit_invoice_ids).first()

    invoice_list=[]
    for id in credit_invoice_ids:
        get_invoices_cost=InvoiceCostInvoice.objects.filter(invoice_id=id).values_list('invoice_number',flat=True)
        get_invoice_files=InvoiceFileUpload.objects.filter(invoice_id=id,status=1,invoicecostinvoice__isnull=False)
        invoice_list.append({'id':id,'inv_num':list(get_invoices_cost),'get_invoice_files':get_invoice_files})

    support_documents=CreditSupportDocuments.objects.getsupportdocuments_by_creditnote_id(credit_note.id)
    get_document_data=getDocumentlist()
    # invoicedetail=Invoice.objects.get_by_id_status(pk,1)
    costcodedata=CostCodeVendor.objects.get_by_id(invoice_detail.costcodevendor.id)
    
    listdata = unique_list(list(credit_note_invoices.values_list('vendor_split_invoice__currency__id',flat=True)))
    data={'invoicedetail':invoice_detail,'costcodedata':costcodedata,'credit_note':credit_note,'credit_note_invoice':credit_note_invoices,'pk':pk,'invoice_list':invoice_list,'support_documents':support_documents,'basecurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency',flat=True).first(),'exchange_rate':credit_note_invoices.values_list('vendor_split_invoice__exchange_rate',flat=True).first(),'paymentcurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency',flat=True).last(),'listdata':listdata,'documents_data':get_document_data,'contract':contract ,"amendment":ammentment_id ,'invoice_detail': invoice_detail ,'basecurrency_symbol':credit_note_invoices.values_list('vendor_split_invoice__currency__currency_symbol',flat=True).first()}
    return render(request,'credit_view.html',data)

def edit_credit_note(request,pk):
    request.session['mainmenu']='invoice-detail'
    request.session['submenu'] = 'credit_list'
    credit_note=CreditNote.objects.getcreditnote_by_id(pk)
    vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    invoice_id=CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
    credit_note_id=CreditNoteInvoice.objects.filter(invoice_id=invoice_id.invoice_id,status=1).values_list('credit_id',flat=True)
    credit_multi_value=CreditNote.objects.filter(id__in=credit_note_id)
    credit_sum = sum(float(remove_currency_symbol(credit_added.total_value)) for credit_added in credit_multi_value)
    serialno=str(CreditNoteInvoice.objects.filter(status=1,credit__status=1,invoice_id=invoice_id.invoice_id).exclude(credit__credit_status=1).count()+1)
    # serialno=CreditNote.objects.filter(vendor_id=vendorid.id,status=1).exclude(credit_status=1).count()+1
    if len(serialno) < 2:
        serialno= f'0{serialno}'
    # getcreditids=list(CreditNoteInvoice.objects.filter(invoice_id=invoice_id.invoice_id,status=1).values_list('credit_id',flat=True))
    #serialno=CreditNote.objects.filter(vendor_id=vendorid.id,status=1).exclude(credit_status=1).count()+1
    invoice_contracts=Invoice.objects.filter(vendor_id=vendorid,invoice_status=2,contracttype='original').values_list('contractid',flat=True).annotate(dcount=Count('contractid')).order_by()
    get_contracts=ContractMaster.objects.filter(id__in=list(invoice_contracts))
    company=Settings.objects.filter(company_id=request.company.id).first()
    all_contracts=[]
    for contract in get_contracts:
        all_contracts.append({'id':contract.id,'ref_num':contract.reference_number,'currency_id':contract.currency.id,'currency_symbol':contract.currency.currency_symbol,'contract_type':'original','contract_currency':contract.currency.currency})
    invoice_contracts_amendments=Invoice.objects.filter(vendor_id=vendorid,invoice_status=2,contracttype__startswith='a').values_list('contractid',flat=True).annotate(dcount=Count('contractid')).order_by()
    get_amendmnets=Amendment.objects.filter(id__in=list(invoice_contracts_amendments))
    for amendmnet in get_amendmnets:
        all_contracts.append({'id':amendmnet.id,'ref_num':amendmnet.amendment_reference_number,'currency_id':amendmnet.amendment_currency.id,'currency_symbol':amendmnet.amendment_currency.currency_symbol,'contract_type':amendmnet.amendment_type,'contract_currency':amendmnet.amendment_currency.currency})
    if (credit_note.contracttype == 'original'):
        contract_id=credit_note.contract_id
        get_contract_currency=credit_note.contract.currency.currency_symbol if credit_note.contract != None else ''
        get_contract_cur_symbol=credit_note.contract.currency.currency_symbol+' '+credit_note.contract.currency.currency if credit_note.contract != None else ''
        get_contract_currency_id=credit_note.contract.currency.id if credit_note.contract != None else ''
        vendortax=VendorCompanyTaxDetails.objects.filter(vendor_id=vendorid.id,contract_id=contract_id,company=request.company,status=1)
        get_exchange_rate=list(VendorInvoiceSplit.objects.filter(vendor_id=vendorid.id,contract_id=contract_id,company=request.company,status=1).values_list('exchange_rate', flat=True).distinct())
        exchange_rate_value=get_exchange_rate[0]
    else:
        contract_id=credit_note.amendment_id
        get_contract_currency=credit_note.amendment.amendment_currency.currency_symbol if credit_note.amendment != None else ''
        get_contract_cur_symbol=credit_note.amendment.amendment_currency.currency_symbol+' '+credit_note.amendment.amendment_currency.currency if credit_note.amendment != None else ''
        get_contract_currency_id=credit_note.amendment.amendment_currency.id if credit_note.amendment != None else ''
        vendortax=VendorCompanyTaxDetails.objects.filter(vendor_id=vendorid.id,amendment_id=contract_id,company=request.company,status=1)
        get_exchange_rate=list(VendorInvoiceSplit.objects.filter(vendor_id=vendorid.id,amendment_id=contract_id,company=request.company,status=1).values_list('exchange_rate', flat=True).distinct())
        exchange_rate_value=get_exchange_rate[0]
    get_invoice_ids=Invoice.objects.filter(contractid=contract_id,contracttype=credit_note.contracttype,invoice_status=2).values_list('id',flat=True)
    get_exclusive_tax=InvoiceExclusive.objects.filter(invoice_id=invoice_id.invoice_id,status=1)
    new_list=[{'percentage_id':i.exclusive_id,'tax_name':i.exclusive.vendortax.tax.Tax_Name,'percentage':i.exclusive.taxpercentage} for i in get_exclusive_tax]
    list_invoices=[]
    for i in get_invoice_ids:
        invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=i,status=1).values('invoice_number')
        list_invoices.append({'invoice_id':i,'invoice_num':list(invoice_cost)})
    credit_invoice_ids=list(CreditNoteInvoice.objects.filter(credit_id=credit_note.id,status=1).values_list('invoice_id',flat=True))
    inclusivetaxlist=vendortax.filter(Tax_Type="Inclusive").values_list('id',flat=True)
    getinclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=inclusivetaxlist,status=1).values('id','vendortax_id__tax__Tax_Name','taxpercentage')
    exclusivetaxlist=vendortax.filter(Tax_Type="Exclusive").values_list('id',flat=True)
    getexclusivewithpercentage=VendorCompanyTaxPercentage.objects.filter(vendortax__in=exclusivetaxlist,status=1).values('id','vendortax_id__tax__Tax_Name','taxpercentage')
    created_exclusive_tax=CreditNoteExclusive.objects.filter(credit_id=credit_note.id,status=1)
    create_credit_invoice=CreditNoteContractInvoice.objects.filter(credit_id=credit_note.id,status=1)
    credit_note_files=CreditSupportDocuments.objects.filter(credit_id=credit_note.id,status=1)
    if (request.POST):
        post_values=request.POST
        contract=post_values.get('contract')
        contract_type=post_values.get('contract_type')
        contract_invoice=post_values.getlist('invoice')
        total_value=post_values.get('total_value')
        hdn_exclusive_ids=post_values.getlist('hdn_exclusive_tax')
        exclusives=post_values.getlist('exclusive')
        added_exclusive_value=post_values.get('final_exclusive_value')
        exclusive_percentage=post_values.getlist('exclusive_percentage')
        exclusive_value=post_values.getlist('exclusive_value')
        totalalltax=post_values.get('totalalltax')
        hdn_credit_invoice=post_values.getlist('hdn_credit_invoice')
        contrcat_invoice_id=post_values.getlist('invoice_id')
        invoice_split=post_values.getlist('invoice_split')
        credit_percentage=post_values.getlist('invoice_percentage')
        credit_symbol=post_values.getlist('invoice_symbol')
        credit_name=post_values.getlist('credit_name')
        credit_date=post_values.getlist('credit_date')
        base_amount=post_values.getlist('base_amount')
        exchange_rate=post_values.getlist('exchange')
        final_amount=post_values.getlist('final_amount')
        companydateformat=post_values.get('dateformat')
        hdn_support_ids=post_values.getlist('support_file_ids')
        supporting_documents=request.FILES.getlist('support_file')
        invoice_no=post_values.getlist('invoice')
        contractid=Invoice.objects.filter(id__in=invoice_no).last()
        grossamount_cn=post_values.get('creditvalue_total')
        # invoice_value=post_values.get('total_invoice_value')
        # print('invoice_value',invoice_value)
        # total_invoice_value1 = (''.join(e for e in invoice_value if e.isalnum()).replace(',',''))
        # print('total_invoice_value1',total_invoice_value1)
        # get_total_value1=re.findall(r'[0-9][0-9,.]+', total_invoice_value1)
        # print('get_total_value1',get_total_value1)
        # get_total_value = get_total_value1[0]
        # print('get_total_value',get_total_value)
        # if (contract_type == 'original'):
        #     create_credit=CreditNote.objects.filter(id=pk).update(contract_id=contract,contracttype=contract_type,amendment_id=None,total_value=total_value,total_value_excluisve_tax=totalalltax,vendor_id=vendorid.id,company_id=vendorid.company.id,exclusive_value=added_exclusive_value)
        # else:
        #     create_credit=CreditNote.objects.create(amendment_id=contract,contracttype=contract_type,total_value=total_value,total_value_excluisve_tax=totalalltax,vendor_id=vendorid.id,company_id=vendorid.company.id,exclusive_value=added_exclusive_value)
        if (contract_type == 'original'):
            contract=ContractMaster.objects.filter(id=contract ,status=1).first()
            contract_data=contract
        else:
            contract=Amendment.objects.filter(id=contract,status=1).first()
            contract_data=ContractMaster.objects.filter(id=contract.service.id ,status=1).first()
        CreditNote.objects.filter(id=pk).update(total_value=total_value,total_value_excluisve_tax=totalalltax,exclusive_value=added_exclusive_value,grossamnt_withoutexclusive=grossamount_cn)
        invoice_ids=[]
        for invoice in contract_invoice:
            if (CreditNoteInvoice.objects.filter(credit_id=pk,invoice_id=invoice).exists()):
                credit_inv_ids=CreditNoteInvoice.objects.filter(credit_id=pk,invoice_id=invoice).first()
                CreditNoteInvoice.objects.filter(credit_id=pk,invoice_id=invoice).update(status=1)
                invoice_ids.append(credit_inv_ids.id)
            else:
                create_contract_invoice=CreditNoteInvoice.objects.create(credit_id=pk,invoice_id=invoice)
                invoice_ids.append(create_contract_invoice.id)
        CreditNoteInvoice.objects.filter(credit_id=pk).exclude(id__in=invoice_ids).update(status=0)
        exclusive_ids=[]
        for hdn_exclusive,exclusive,percentage,value in zip(hdn_exclusive_ids,exclusives,exclusive_percentage,exclusive_value):
            if (hdn_exclusive):
                CreditNoteExclusive.objects.filter(id=hdn_exclusive).update(exclusive_id=exclusive,exclusive_calculated_value=value,exclusive_percentage=percentage,created_vendor_id=request.user.id)
                exclusive_ids.append(hdn_exclusive)
            else:
                create_exclusive_tax=CreditNoteExclusive.objects.create(exclusive_id=exclusive,exclusive_percentage=percentage,exclusive_calculated_value=value,credit_id=pk,created_vendor_id=request.user.id)
                exclusive_ids.append(create_exclusive_tax.id)
        CreditNoteExclusive.objects.filter(credit_id=pk).exclude(id__in=exclusive_ids).update(status=0)
        for hd_credit_inv,invoice_id,split,name,dated,base,rate,final,percentage,symbol in zip(hdn_credit_invoice,contrcat_invoice_id,invoice_split,credit_name,credit_date,base_amount,exchange_rate,final_amount,credit_percentage,credit_symbol):
            convert_date=convertdate(companydateformat,dated)
            net_payable_value=get_netpayable(grossamount_cn,rate,getinclusivewithpercentage,percentage)
            get_file_id=request.POST.get('hdn_id_file'+str(invoice_id),'')
            base_currency_amount_re= re.sub(r'[()\s]+', '', base)
            payment_currency_amount_re= re.sub(r'[()\s]+', '', final)
            if (get_file_id):
                CreditNoteContractInvoice.objects.filter(id=hd_credit_inv).update(currency_split=split,credit_note_no=name,date=convert_date,base_currency_amount=base_currency_amount_re,exchange_rate=rate,payment_currency_amount=payment_currency_amount_re,percentage=percentage,symbol=symbol,new_netpayable=net_payable_value)
            else:
                get_file=request.FILES.get('credit_file'+str(invoice_id))
                file=get_file
                if (get_file != None):
                    CreditNoteContractInvoice.objects.filter(id=hd_credit_inv).update(currency_split=split,credit_note_no=name,date=convert_date,base_currency_amount=base_currency_amount_re,exchange_rate=rate,payment_currency_amount=payment_currency_amount_re,file=file,percentage=percentage,symbol=symbol,new_netpayable=net_payable_value)
                    fs = FileSystemStorage()
                    file1 = fs.save(file.name, file)
                else:
                    CreditNoteContractInvoice.objects.filter(id=hd_credit_inv).update(currency_split=split,credit_note_no=name,date=convert_date,base_currency_amount=base_currency_amount_re,exchange_rate=rate,payment_currency_amount=payment_currency_amount_re,file='',percentage=percentage,symbol=symbol,new_netpayable=net_payable_value)
        for document in supporting_documents:
            create_support_documents=CreditSupportDocuments.objects.create(credit_id=pk,file=document)
            hdn_support_ids.append(create_support_documents.id)
        CreditSupportDocuments.objects.filter(credit_id=pk).exclude(id__in=hdn_support_ids).update(status=0)
        submit_value=post_values.get('submit_value')
        if (submit_value == '0'):
            return redirect('credit:credit_note_list')
        elif (submit_value == '1'):
            credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
            all_credit=', '.join(str(e) for e in credit_number)
            invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=contractid.id,status=1).values_list('invoice_number',flat=True))
            all_invoice=', '.join(str(e) for e in invoice_number)
            now = datetime.now()
            today = date.today()
            date_today = today.strftime("%d-%b-%Y")
            getvin=request.user.cin_number
            calculate_time=add_time(now,request.company)
            CreditNote.objects.filter(id=pk).update(credit_status=2,created_at=calculate_time)
            sender = User.objects.filter(id=request.user.id).first()
            recipient = User.objects.filter(company=request.company.id,roles_id=2).first()
            scheme=request.scheme
            gethost=request.get_host()
            # url=f"{scheme}://{gethost}/dashboard/dashboard/"
            if (contract_data.projects.flow_level == "discipline"):
                checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdisciplinetype_id,'discipline',request.company,contract_data.projects_id)
            elif (contract_data.projects.flow_level == "clusters"):
                checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contract_data.projectdiscipline.cluster_id,'clusters',request.company,contract_data.projects_id)
            else:
                if contractid.well_not_applicable == "id":
                    checkflow=ProjectFlowlevel.objects.projectflow_bylevel_main(contractid.well_id,'well',request.company,contract.projects_id)
                else:
                    #use wellbased field to get data
                    checkflow=ProjectFlowlevel.objects.projectflow_bywellbasedlevel_main(contract_data.projectdisciplinetype_id,'well',request.company,contract_data.projects_id)
            flowlevelmodules=ProjectFlowModules.objects.getactiveflow_level(checkflow.id)
            flowlevelusers=ProjectFlowModuleUsers.objects.getflowusers_active(flowlevelmodules.id,checkflow.id)
            getmodules=ProcessModule.objects.getmodule_byid(flowlevelmodules.module_id)
            get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=contractid.id).first()
            get_invoice_date=get_payment_term.payment_terms.payment_day
            get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
            calculate_time=add_invoice_time(now,get_company_invoice_time)
            creditflow_modules=Invoiceflowmodules.objects.createcreditflowmodules(contract_data.projects_id,request.company,checkflow.id,flowlevelmodules.id,pk,getmodules.module_id,now,calculate_time)
            for user in flowlevelusers:
                projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(contract_data.projects_id,projectusers.id,creditflow_modules.id,user.id,projectusers.user_id)
                recipientuser = User.objects.get(id=projectusers.user_id)
                url=f"{scheme}://{gethost}/credit/checklist/{pk}"
                notify.send(sender, recipient=recipientuser,data=url, verb='Credit note Received.', description=f'Credit Note received from {get_vendor_company_name(request.user.cin_number)} for {contractid.name_service}')
                credit_submission_mail_user(request,recipientuser,vendorid,all_credit,all_invoice,contractid)

            all_vendors = User.objects.filter(cin_number__iexact=getvin,status=1)
            for notifications in all_vendors:
                url=f"{scheme}://{gethost}/credit/list"
                notify.send(sender, recipient=notifications,data=url, verb='Credit note Received.', description=f'Credit Note received by {recipient.name} on {date_today} for {contractid.name_service} ')
                credit_submission_mail_vendor(request,notifications,vendorid)

            created_credit_invoice=CreditNoteContractInvoice.objects.filter(credit_id=pk)
            get_count=created_credit_invoice.filter(Q(credit_note_no='') | Q(date__isnull=True) | Q(base_currency_amount='') | Q(exchange_rate='') | Q(payment_currency_amount='') | Q(file='')).count()
            return redirect('credit:credit_note_list')
        else:
            return redirect('credit:credit_file_preview',pk=pk)
    data={'credit_note':credit_note,'all_contracts':all_contracts,'company':company,'list_invoices':list_invoices,'credit_invoice_ids':list(credit_invoice_ids),'inclusive_taxes':list(getinclusivewithpercentage),'exclusive_taxes':list(getexclusivewithpercentage),'created_exclusive_tax':created_exclusive_tax,'get_contract_currency':get_contract_currency,'create_credit_invoice':create_credit_invoice,'contract_currency_id':get_contract_currency_id,'supporting_documents':credit_note_files,'get_contract_cur_symbol':get_contract_cur_symbol,'exchange_rate_value':exchange_rate_value,'pk':pk,'serialno':serialno,'invoice_id':invoice_id.id,'new_list':new_list,'credit_sum':credit_sum , 'credit_sum_count':len(credit_note_id)}
    return render(request,'edit_credit_note.html',data)

# credit note id to credit note invoice number
def get_credit_invoices(credit_id):
    credit_note_invoice=list(CreditNoteContractInvoice.objects.filter(credit_id=credit_id,status=1).values_list('credit_note_no',flat=True))
    return ', '.join(str(e) for e in credit_note_invoice)
def get_vendor_company_name(cin_number):
    vendor_company = ContractMasterVendor.objects.filter(vin=cin_number).first()
    return vendor_company.vendor_name

def totalcost(request):
    invoice_id = request.GET.get('invoice_id')
    get_exclusive_tax=InvoiceExclusive.objects.filter(invoice_id=invoice_id,status=1)
    try:
        new_list=[{'percentage_id':i.exclusive_id,'tax_name':i.exclusive.vendortax.tax.Tax_Name,'percentage':i.exclusive.taxpercentage} for i in get_exclusive_tax]
    except:
        new_list=[]
    print(f'new_list {new_list}')
    print(f'get_exclusive_tax {get_exclusive_tax}')
    getcostinforamation=InvoiceCostInformation.objects.filter(invoice_id=invoice_id,status=1).values_list('total_invoice_value',flat=True).first()
    try:
        value = float(''.join(e for e in getcostinforamation if e.isalnum()).replace(',',''))
    except:
        value=float(re.sub(r'[^0-9.]', '', getcostinforamation))
        getcostinforamation=re.sub(r'[^0-9.]', '', getcostinforamation)
    invoice_cost=getcostinforamation
    # vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    serial_no=str(CreditNoteInvoice.objects.filter(status=1,credit__status=1,invoice_id=invoice_id).exclude(credit__credit_status=1).count()+1)
    credit_note_id=CreditNoteInvoice.objects.filter(invoice_id=invoice_id,status=1).values_list('credit_id',flat=True)
    credit_multi_value=CreditNote.objects.filter(id__in=credit_note_id)
    credit_sum = sum(float(remove_currency_symbol(credit_added.total_value)) for credit_added in credit_multi_value)
    # serialno=CreditNote.objects.filter(vendor_id=vendorid.id,status=1).exclude(credit_status=1).count()+1
    if len(serial_no) < 2:
        serial_no= f'0{serial_no}'
    return JsonResponse({'cost':value,'invoice_cost':invoice_cost,'serial_no':serial_no,'new_list':new_list,'credit_sum':credit_sum , 'credit_sum_count':len(credit_note_id)})
    
class CreditNotePDFView(PDFTemplateView):
    template_name = 'CreditNotePDF.html'
    
    def get(self, request,pk, *args, **kwargs):
        companyImage= Companies.objects.get_by_id(request.company.id)
        if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')  # Convert the image to RGB mode
            image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            buffered = BytesIO()
            image.save(buffered, format="JPEG")  
            credit_note=CreditNote.objects.getcreditnote_by_id(pk)
            contract_id = credit_note.contract_id
            # If you need the contract object itself, you can access it like this:
            contract = credit_note.contract
            ammentment_id = credit_note.amendment
  
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            imageurl = None
        credit_note=CreditNote.objects.getcreditnote_by_id(pk)
        credit_note_invoices=CreditNoteContractInvoice.objects.getcreditnoteinvoice_by_creditnoteid(credit_note.id)
        credit_invoice_ids=CreditNoteInvoice.objects.getcreditnoteinvoice(credit_note.id)
        invoice_list=[]
        for id in credit_invoice_ids:
            get_invoices_cost=InvoiceCostInvoice.objects.filter(invoice_id=id).values_list('invoice_number',flat=True)
            get_invoice_files=InvoiceFileUpload.objects.filter(invoice_id=id,status=1,invoicecostinvoice__isnull=False)
            invoice_list.append({'id':id,'inv_num':list(get_invoices_cost),'get_invoice_files':get_invoice_files})
        invoice_detail = Invoice.objects.filter(id__in=credit_invoice_ids).first()
        costcodedata=CostCodeVendor.objects.get_by_id(invoice_detail.costcodevendor.id)
        get_document_data=getDocumentlist()
        support_documents=CreditSupportDocuments.objects.getsupportdocuments_by_creditnote_id(credit_note.id)
        listdata = unique_list(list(credit_note_invoices.values_list('vendor_split_invoice__currency__id',flat=True)))
        credit_note_numbers  =credit_note_invoices.values_list('credit_note_no',flat=True)
        data={'credit_note':credit_note,'invoicedetail':invoice_detail,'costcodedata':costcodedata,'credit_note_invoice':credit_note_invoices,'pk':pk,'invoice_list':invoice_list,'support_documents':support_documents,'basecurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency',flat=True).first(),'exchange_rate':credit_note_invoices.values_list('vendor_split_invoice__exchange_rate',flat=True).first(),'paymentcurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency',flat=True).last(),'imageurl':imageurl,'comapnyname':companyImage,'listdata':listdata,'request':request,'credit_note_number':",".join(map(str, credit_note_numbers)),'documents_data':get_document_data,'contract':contract ,"amendment":ammentment_id}
        
        html_output = render_to_string('CreditNotePDF.html', data)
        css = CSS(string=credit_note_pdfstyle(encoded_image))

    # Generate the PDF with WeasyPrint
        pdf_buffer = BytesIO()
        HTML(string=html_output).write_pdf(pdf_buffer, stylesheets=[css])

    # Create the Django response object with the PDF content
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')

    # Set the Content-Disposition header to force a download
        response['Content-Disposition'] = 'attachment; filename="Credit Note Summary.pdf"'

    # Return the response
        return response
    
def add_invoice_time(now,company_invoice_time):
    if company_invoice_time.time_unit == 2:
        calculate_time=now+timedelta(minutes=company_invoice_time.time_allotted)
    elif company_invoice_time.time_unit == 0:
        calculate_time=now+timedelta(hours=company_invoice_time.time_allotted)
    else :
        calculate_time=now+timedelta(days=company_invoice_time.time_allotted)
    return calculate_time

class CreditNoteChecklist(View):
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
        credit_detail=CreditNote.objects.filter(id=pk).get()
        document_list=getCreditNoteDocumentlist()
        # document_list=CreditSupportDocuments.objects.getsupportdocuments_by_creditnote_id(pk)
        credit_invoice_ids=CreditNoteInvoice.objects.getcreditnoteinvoice(credit_detail.id)
        invoice_detail = Invoice.objects.filter(id__in=credit_invoice_ids).first()
        supporting_doc=CreditSupportDocuments.objects.filter(credit_id=pk,status=1)
        get_invoices_cost=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_detail.id).values_list('invoice_number',flat=True))  
        # document_list=getDocumentlist()
        invoiceflow_modules=Invoiceflowmodules.objects.getcreditflowmodules_byinvoice(pk,1)
        get_role_id=invoiceflow_modules.flowlevel_module.role
        check_for_committe=CreditExceptional.objects.filter(credit_id=pk,confirm_dispute=1).count()
        roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
        context={'credit_detail':credit_detail,'pk':pk,'get_role_id':get_role_id,'check_for_committe':check_for_committe,'document_list':document_list,'invoice_detail':invoice_detail,'roles_rights':roles_rights,'supportingdocument_count':supporting_doc.count(),'get_invoices_cost':get_invoices_cost}
        return render(request, "creditnotechecklist.html",context)
    def post(self, request,pk):
        contractid=CreditNote.objects.filter(id=pk).get()
        credit_invoice_ids=CreditNoteInvoice.objects.getcreditnoteinvoice(contractid.id)
        invoice_detail = Invoice.objects.filter(id__in=credit_invoice_ids).first()
        credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
        credit_numbers=', '.join(str(e) for e in credit_number)
        if request.POST:
            print('r',request.POST)
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            if (submit_type == "3" or submit_type == "4"):
                messages_json = request.POST.get('selected_messages')
                messages = json.loads(messages_json)
                get_exceptional=request.POST.getlist('exceptional')
                exceptional_list=[CreditExceptional(credit_id=pk,exceptional_type=i) for i in get_exceptional]
                CreditExceptional.objects.bulk_create(exceptional_list)
                if messages:
                    
                    ok=CreditExceptional.objects.filter(credit_id=pk)
                    
                    CreditExceptional.objects.filter(credit_id=pk).update(checked_messages=messages_json)
                usercreate=request.user.roles_id
                create_user_log(request,credit_numbers,'Invoice','Create',f'Invoice Receipt has been {submit_name}',usercreate)    
            document_list=getCreditNoteDocumentlist()
            for val in document_list:
                    confirm_status=request.POST.get('confirmlist-'+str(val.get('data')))
                    val_comments=request.POST.get('comment-'+str(val.get('data')))
                    InvoiceFlowChecklist.objects.createcreditchecklist(pk,val.get('data'),confirm_status,val_comments)
            if(submit_type != "3"):
                get_credit=credit_flow_func(pk,1,request,comments,submit_type,submit_name)
                usercreate=request.user.roles_id
                create_user_log(request,credit_numbers,'Invoice','Create',f'Invoice Receipt has been {submit_name}',usercreate)    
                if get_credit == 1:
                    return redirect("credit:unapprovedcreditnotes")
                elif get_credit == 2:
                    return redirect("credit:approvedcreditnotes")
            else:
                print(f'get_credit {submit_type}')
                credit_return_flow(pk,1,submit_type,comments,request,submit_name)
    #         if(submit_type == '3'):
    #             invoice_return_flow(pk,1,submit_type,comments,request,submit_name)
            if (submit_type == '3' or submit_type == '4'):
                return redirect("credit:rejectedcreditnotes")
            return redirect("credit:unapprovedcreditnotes")


def getSupportFilesCredit(request):
    supportid=request.GET.get('supportid','')
    print(f'supportid {supportid}')
    invoiceid=request.GET.get('invoiceid','')
    credit_id=request.GET.get('credit_id','')
    wcc_id=request.GET.get('wcc_id','')
    get_wcc_files=[]
    support_file=[]
    if (supportid == "3" or supportid == "4"):
        contractid=Invoice.objects.get_by_id(invoiceid)
        if (contractid.contracttype == 'original'):
            contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
            confile=str(contract.upload_contract)
            price_file=str(contract.upload_pricetable)
            contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,1).values()
            price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,2).values()
            data={'con_file':list(contract_table_files),'price_file':list(price_table_files),'contracttype':contractid.contracttype}
        else:
            contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
            original_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,1).values()
            original_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,2).values()

            amendment_addendum_contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,1).values()
            amendment_addendum_price_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,2).values()
            confile=original_contract_table_files.union(amendment_addendum_contract_table_files)
            price_table_files=original_price_table_files.union(amendment_addendum_price_table_files)
            data={'con_file':list(confile),'price_file':list(price_table_files),'contracttype':contractid.contracttype}
        return JsonResponse(data,safe=False)
    elif supportid == '2':
        getfiles=list(CreditSupportDocuments.objects.filter(credit_id=credit_id,status=1).values())
        print(f'getfiles {getfiles}')
        support_file.extend(getfiles)
        print(f'support_file {support_file}')
        data={'filecount':len(support_file),'files':support_file,'file_type':'credit'}
        return JsonResponse(data)
    else:
        print(f'11111v {supportid}')
        # getfiles=list(InvoiceFileUpload.objects.filter(invoice_id=invoiceid,support=supportid,status=1).values())
        getfiles=list(CreditNoteContractInvoice.objects.filter(credit_id=credit_id,status=1).values())
        get_wcc_files.extend(getfiles)
        data={'filecount':len(get_wcc_files),'files':get_wcc_files,'file_type':'Invoice'}
        return JsonResponse(data)
    
def credit_flow_func(pk,module,request,comments,submit_type,submit_name):
    current_date=datetime.now()
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    invoiceflow_modules=Invoiceflowmodules.objects.getcreditflowmodules_byinvoice(pk,module)
    print(f'invoiceflow_modules {invoiceflow_modules}')
    print(f'modulemodule {module}')
    if (invoiceflow_modules):
        Invoiceflowmodules.objects.updateinvoiceflowmodules(invoiceflow_modules.id)
        Invoiceflowmodulesusers.objects.updateinvoicelowusers(invoiceflow_modules.id,request.user.id,current_date,submit_type,comments)
    invoice_detail = CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
    contractid=Invoice.objects.filter(id=invoice_detail.invoice_id).last()
    get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=contractid.id).first()
    get_invoice_date=get_payment_term.payment_terms.payment_day
    get_company_invoice_time=InvoiceTimeTrigger.objects.filter(Q(payment_terms_from__lte=get_invoice_date) & Q(payment_terms_to__gte=get_invoice_date)).first()
    calculate_time=add_invoice_time(current_date,get_company_invoice_time)
    credit_details=CreditNote.objects.getcreditnote_by_id(pk)
    get_invoice=CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
    invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=get_invoice.invoice_id).values_list('invoice_number',flat=True))
    # credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
    invoice_number=', '.join(str(e) for e in invoice_number)
    credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
    all_credit=', '.join(str(e) for e in credit_number)
    vendor=ContractMasterVendor.objects.get_byid(credit_details.vendor_id,request.company)
    vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
    allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
    main_url="credit/list"
    user_main_url = f"credit/creditapprovallist/{pk}"
    main_verb='Credit Note '+submit_name
    approval_verb="Credit Note for Approval"
    content=f'Credit Note {submit_name} by {request.user.name} on {date_today} for {contractid.name_service}'
    now = datetime.now()
    get_payment_term=InvoiceCostInformation.objects.filter(invoice_id=pk).first()
    print(f'submit_type {submit_type}')
    if (submit_type == '3' or submit_type == '4'):
        CreditNote.objects.filter(id=pk).update(approval_status=3, approval_date=now) if submit_type == '3' else CreditNote.objects.filter(id=pk).update(approval_status=2, approval_date=now)
            # invoive_return_mail(request,vendor_data,vendor,submit_name,invoice_detail,comments,all_invoice)
        for notifications in allVendors:
            notify_credit_flow(request,notifications,main_url,main_verb,content)
            credit_return_mail(request,notifications,vendor,submit_name,contractid,comments,all_credit)
        return 3
    else:
        if (credit_details.contracttype == 'original'):
            contract=ContractMaster.objects.get_by_id(credit_details.contract_id).first()
            contract_data=contract
        else:
            contract=Amendment.objects.get_by_id(credit_details.amendment_id ,1).first()
            contract_data=contract
                    
        getnextlevel=ProjectFlowModules.objects.getnextactivelevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.flowlevel_module_id)
        
        if(getnextlevel):
            getmodules=ProcessModule.objects.getmodule_byid(getnextlevel.module_id)
            if module == 1 or module == 2:
                # if module == 2:
                #         for notifications in allVendors:
                #             notify_credit_flow(request,notifications,main_url,main_verb,content)
                #             credit_return_mail(request,notifications,vendor,submit_name,contractid,comments,all_credit)
                # for notifications in allVendors:
                #     notify_invoice_flow(request,notifications,main_url,main_verb,content)
                if getnextlevel.module.module.id < 3:
                    projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnextlevel.id,invoiceflow_modules.flowlevel_id)
                    invoiceflow=Invoiceflowmodules.objects.createcreditflowmodules(getnextlevel.project_id,request.company,invoiceflow_modules.flowlevel_id,getnextlevel.id,pk,getmodules.module_id,now,calculate_time)

                    get_users=list(Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status__in=[1,2],Invoiceflowmodules__creditnote_id=pk).values_list('user',flat=True).distinct())
                    # approval_user=User.objects.filter(id__in=get_users)
                    # all_user=', '.join(str(e.name) for e in approval_user)
                    multiple_users=User.objects.filter(id__in=get_users)
                        # credit_return_mail(request,notifications,vendor,submit_name,contractid,comments,all_credit)
                    user_data=''
                    if get_users:
                        for name in get_users:
                            user_name=User.objects.filter(id=name).first()
                            user_data+=f'{user_name.name}, '
                    if getnextlevel.module.module.id == 1:
                        user_main_url = f"credit/checklist/{pk}"
                         
                    main_content=f"Credit Note {all_credit} for Vendor {vendor.vendor_name} for services has been reviewed by {user_data} and passed for your approval."
                    for user in projectflow_modules_users:
                        projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                        Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnextlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                        notify_credit_flow(request,user.user.user,user_main_url,approval_verb,main_content)
                        credit_approval_mail(request,user.user.user,vendor,all_credit,invoice_number,get_invoice.invoice,multiple_users,invoiceflow_modules)
                        # recipientuser = User.objects.get(id=projectusers.user_id)
                        # get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnextlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                        # print('get_users2',get_users)
                        # approved_users=User.objects.filter(id__in=get_users)
                        # urls="invoice/vendorbasedinvoice"
                        # module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,all_invoice,recipientuser,urls,approved_users,comments)
                    return 1
                else:
                    CreditNote.objects.filter(id=pk).update(approval_status=4,approval_date=today)
                    return 2
        else:
            getnexprocesstlevel=ProjectFlowModules.objects.getnxtprocessactlevel(invoiceflow_modules.flowlevel_id,invoiceflow_modules.project_id,invoiceflow_modules.flowlevel.level_id)
            if (getnexprocesstlevel):
                getmodules=ProcessModule.objects.getmodule_byid(getnexprocesstlevel.module_id)
                print(3,'next process module')
                if module == 1 or module == 2:
                    if module == 2:
                        for notifications in allVendors:
                            notify_credit_flow(request,notifications,main_url,main_verb,content)
                            credit_return_mail(request,notifications,vendor,submit_name,contractid,comments,all_credit)
                    # for notifications in allVendors:
                    #     notify_invoice_flow(request,notifications,main_url,main_verb,content)
                    if getnexprocesstlevel.module.module.id < 3:
                        projectflow_modules_users=ProjectFlowModuleUsers.objects.getflowusers_active(getnexprocesstlevel.id,getnexprocesstlevel.projectflow_level_id)
                        invoiceflow=Invoiceflowmodules.objects.createcreditflowmodules(getnexprocesstlevel.project_id,request.company,getnexprocesstlevel.projectflow_level_id,getnexprocesstlevel.id,pk,getmodules.module_id,now,calculate_time)
                        
                        get_users=list(Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status__in=[1,2],Invoiceflowmodules__creditnote_id=pk).values_list('user',flat=True)).append(request.user.id)
                        # approval_user=User.objects.filter(id__in=get_users)
                        # all_user=', '.join(str(e.name) for e in approval_user)
                        user_data=''
                        if get_users:
                            for name in get_users:
                                if name:
                                    user_data+=f'{User.objects.filter(id=name).name}, '
                        main_content=f"Credit Note {all_credit} for Vendor {vendor.vendor_name} for services has been reviewed by {user_data}and passed for your approval"
                        print(f'get_users {get_users}')
                        for user in projectflow_modules_users:
    
                            projectusers=ProjectUser.objects.getprojectuser_byid(user.user_id)
                            Invoiceflowmodulesusers.objects.createinvoiceflowmodulesusers(getnexprocesstlevel.project_id,projectusers.id,invoiceflow.id,user.id,projectusers.user_id)
                            notify_credit_flow(request,user.user.user,user_main_url,approval_verb,main_content)
                            # recipientuser = User.objects.get(id=projectusers.user_id)
                        
                            # get_users=Invoiceflowmodulesusers.objects.filter(created_at__isnull=False,project_id=getnexprocesstlevel.project_id,status=1,Invoiceflowmodules__invoice_id=invoice_detail.id).values_list('user',flat=True)
                            # approved_users=User.objects.filter(id__in=get_users)
                            # urls="invoice/vendorbasedinvoice"
                        # module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,all_invoice,recipientuser,urls,approved_users,comments)
                        return 1
                    else:
                        CreditNote.objects.filter(id=pk).update(approval_status=4,approval_date=today)
                        print('ithuvu m okay dha pah')
                        return 2
            else:
                CreditNote.objects.filter(id=pk).update(approval_status=4,approval_date=today)
                # module_based_data(pk,request,module,vendor,invoice_detail,date_today,invoiceflow_modules,all_invoice)
                return 2
    return

class CreditApprovalProcess(View):
    def get(self, request,pk):
        creditnotedetails=CreditNote.objects.filter(id=pk).get()
        credit_note_invoices=CreditNoteContractInvoice.objects.filter(credit_id=creditnotedetails.id)
        credit_invoice_ids=CreditNoteInvoice.objects.getcreditnoteinvoice(creditnotedetails.id)
        invoice_detail = Invoice.objects.filter(id__in=credit_invoice_ids).first()
        document_list=newCreditNoteDocumentlist()
        if (creditnotedetails.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(creditnotedetails.contract_id)
            vendorinvoice=VendorInvoiceSplit.objects.get_split_invoice(contract.id,request.company,1)
        else:
            contract=Amendment.objects.get_by_id(creditnotedetails.amendment_id ,1).first()
            vendorinvoice=VendorInvoiceSplit.objects.get_split_amendment(contract.id,request.company,1)
        invoiceflow_modules=Invoiceflowmodules.objects.getcreditflowmodules_byinvoice(pk,2)
        get_invoices_cost=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_detail.id).values_list('invoice_number',flat=True))
        get_role_id=invoiceflow_modules.flowlevel_module.role
        roles_rights=RoleRight.objects.filter_by_role(get_role_id,True)
        check_for_committe=CreditExceptional.objects.filter(credit_id=pk,confirm_dispute=1).count()
        dispute_user=DisputedInvoiceTrack.objects.filter(credit_id=pk,stage=5,status=True)
        
        context={'maininvoices':vendorinvoice,'pk':pk,'document_list':document_list,'get_role_id':get_role_id,'roles_rights':roles_rights,'check_for_committe':check_for_committe,'invoice_detail':invoice_detail,'dispute_user':dispute_user.count(),'dispute_user_check':dispute_user.first(),'get_invoices_cost':get_invoices_cost,'credit_detail':creditnotedetails,'basecurrency':credit_note_invoices.values_list('vendor_split_invoice__currency__currency_symbol',flat=True).first(),'exchange_rate':credit_note_invoices.values_list('vendor_split_invoice__exchange_rate',flat=True).first()}
        return render(request, "creditapproval.html",context)
    def post(self, request,pk):
        if request.POST:
            comments=request.POST.get('main_comments',None)
            submit_type=request.POST.get('submit_type')
            submit_name=request.POST.get('submit_name')
            credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
            credit_numbers=', '.join(str(e) for e in credit_number)
            # invoice_number=CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
            # invoice_numberss=list(InvoiceCostInvoice.objects.filter(invoice_id=invoice_number.id,status=1).values_list('invoice_number',flat=True))
            # all_invoice=', '.join(str(e) for e in invoice_numberss)
            # print(all_invoice , "INVOICE NUMBER")
            # print(credit_numbers,"CR$EDIT NUMBER")
            # invoice_numbers = request.POST.getlist('credit_invoice_reference_no')
            # print(invoice_number,"INVOICE NUMBERS")
            # credit_nnmmm
            if (submit_type == "3" or submit_type == "4" or submit_type == "5"):
                get_exceptional=request.POST.getlist('exceptional')
                messages_json = request.POST.get('selected_messages')
                messages = json.loads(messages_json)
                get_exceptional=request.POST.getlist('exceptional')
                exceptional_list=[CreditExceptional(credit_id=pk,exceptional_type=i) for i in get_exceptional]
                CreditExceptional.objects.bulk_create(exceptional_list)
                if messages:
                    
                    ok=CreditExceptional.objects.filter(credit_id=pk)
                    
                    CreditExceptional.objects.filter(credit_id=pk).update(checked_messages=messages_json)
                # exceptional_list=[CreditExceptional(credit_id=pk,exceptional_type=i) for i in get_exceptional]
                # CreditExceptional.objects.bulk_create(exceptional_list)
                usercreate=request.user.roles_id
                create_user_log(request,credit_numbers,'Invoice','Create',f'Invoice Approval has been {submit_name}',usercreate)    
            if submit_type == "3":
                credit_return_flow(pk,2,submit_type,comments,request,submit_name)
                usercreate=request.user.roles_id
                create_user_log(request,credit_numbers,'Invoice','Create',f'Invoice Approval has been {submit_name}',usercreate)
                return redirect("credit:rejectedcreditnotes")
            else:
                get_credit= credit_flow_func(pk,2,request,comments,submit_type,submit_name)
                usercreate=request.user.roles_id
                create_user_log(request,credit_numbers,'Invoice','Create',f'Invoice Approval has been {submit_name}',usercreate)
                if get_credit == 1:
                    return redirect("credit:unapprovedcreditnotes")
                elif get_credit == 2:
                    return redirect("credit:approvedcreditnotes")
        #         if(submit_type == '3'):
        #             invoice_return_flow(pk,1,submit_type,comments,request,submit_name)
                elif (submit_type == '3' or submit_type == '4'):
                    return redirect("credit:rejectedcreditnotes")
                return redirect("credit:unapprovedcreditnotes")


class ViewApprovedCreditNotes(View):
    def get(self,request):
        credit_note=CreditNote.objects.filter(credit_status=2,company=self.request.company,approval_status=4).order_by('-id')
        data={'credit_note':credit_note,'credit_note_count':credit_note.count(),'credit_type':4}
        return render(request,'approvedcreditnotes.html',data)

class ViewUnApprovedCreditNotes(View):
    def get(self,request):
        credit_note=CreditNote.objects.filter(credit_status=2,company=self.request.company,approval_status=1).order_by('-id')
        data={'credit_note':credit_note,'credit_note_count':credit_note.count(),'credit_type':1}
        return render(request,'approvedcreditnotes.html',data)

class ViewReturnedRejectedCreditNotes(View):
    def get(self,request): 
        credit_note=CreditNote.objects.filter(credit_status=2,company=self.request.company,approval_status__gte=2).exclude(approval_status=4).order_by('-id')
        data={'credit_note':credit_note,'credit_note_count':credit_note.count(),'credit_type':3}
        return render(request,'approvedcreditnotes.html',data)
    
class CreditApprovalTrack(View):
    def get(self,request,pk):
        credit_detail= CreditNote.objects.filter(id=pk).first()
        get_invoice=CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
        invoice_detail = Invoice.objects.get_by_id(get_invoice.invoice_id)
        credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
        all_creditnotes=', '.join(str(e) for e in credit_number)
        vendor=ContractMasterVendor.objects.get_byid(credit_detail.vendor_id,request.company)
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        # check_for_dispute=DisputedInvoiceTrack.objects.filter(invoice_id=pk,status=True)
        completed_invoice=Invoiceflowmodules.objects.getinvoiceflowmodules_by_credit_id(pk).filter(status=1).exclude(module=None)
        pending_invoice_status=Invoiceflowmodules.objects.getinvoiceflowmodules_by_credit_id(pk).filter(status=0)
        if (credit_detail.contracttype == 'original'):
            contract=ContractMaster.objects.getcontract(credit_detail.contract_id)
            project=contract.projects
        else:
            contract=Amendment.objects.get_by_id(credit_detail.amendment_id ,1).first()
            project=contract.service.projects
        if (project.flow_level == "discipline"):
                if (credit_detail.contracttype == 'original'):
                    get_levels=ProjectFlowlevel.objects.get_by_level_main(contract.projectdisciplinetype_id,'discipline',request.company,project.id)
                else:
                    get_levels=ProjectFlowlevel.objects.get_by_level_main(contract.service.projectdisciplinetype_id,'discipline',request.company,project.id)
        elif (project.flow_level == "clusters"):
            if (credit_detail.contracttype == 'original'):
                get_levels=ProjectFlowlevel.objects.get_by_level_main(contract.projectdiscipline.cluster_id,'clusters',request.company,project.id)
            else :
                get_levels=ProjectFlowlevel.objects.get_by_level_main(contract.service.projectdiscipline.cluster_id,'clusters',request.company,project.id)
        else:
            if invoice_detail.well_not_applicable == "id":
                get_levels=ProjectFlowlevel.objects.get_by_level_main(invoice_detail.well_id,'well',request.company,project.id)
            else:
                get_levels=ProjectFlowlevel.objects.get_by_wellbasedlevel_main(contract.projectdisciplinetype_id,'well',request.company,project.id)
        projectflow_modules=ProjectFlowModules.objects.getallactiveflow_level_mul_id(get_levels.values_list('id',flat=True))
        invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_by_credit_id(pk).filter(status=1).exclude(module=None).count()
        print(f'projectflow_modules {projectflow_modules}, invoiceflow_modules {invoiceflow_modules}')
        approval_status=True if len(projectflow_modules) == invoiceflow_modules else False
        invoice_cost_data=CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1)
        created_invoice_flow=invoiceflow_modules=Invoiceflowmodules.objects.getinvoiceflowmodules_by_credit_id(pk) 
        data={'project_id':project,'get_levels':get_levels,'pk':pk,'contract':contract,'approval_status':approval_status,'created_invoice_flow':created_invoice_flow,'completed_invoice':completed_invoice,'pending_invoice_status':pending_invoice_status,'invoice_detail':invoice_detail,'allVendors':allVendors,'all_invoice':all_creditnotes,'invoice_cost':invoice_cost_data,'credit_note_no': all_creditnotes ,'get_invoice':get_invoice}
        return render(request,'creditapprovaltrack.html',data)

def getcreditnotes(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    Creditnote_type = request.GET.get('Creditnote_type', '') 
    if Creditnote_type == '3':
        full_credit=CreditNoteContractInvoice.objects.filter(Q(credit__company_id=request.company.id,credit__approval_status__in=[2,3,6]) & Q(credit_note_no__icontains=search_value,credit__company_id=request.company.id,credit__approval_status__in=[2,3,6])).order_by('-credit_id').values('credit').distinct()
        credit_note_value=full_credit[start:start+length]
        
    else:
        full_credit=CreditNoteContractInvoice.objects.filter(Q(credit__company_id=request.company.id,credit__approval_status=Creditnote_type) & Q(credit_note_no__icontains=search_value,credit__company_id=request.company.id,credit__approval_status=Creditnote_type)).order_by('-credit_id').values('credit').distinct()
        credit_note_value=full_credit[start:start+length]
        
    print(f'credit_note_value {credit_note_value.count()}')
    vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    allcredit_note=[]
    s_no=start+1
    for credit_no in credit_note_value:
        get_invoice=CreditNoteInvoice.objects.filter(credit_id=credit_no['credit'],status=1).first()
        vendor=ContractMasterVendor.objects.get_byid(get_invoice.credit.vendor_id,request.company)
        if vendor:
            vendor=vendor.active_status
        else:
            vendor=0
        returned_query=checkpermission_invoiceapproval_dispute('',request.user.id,get_invoice.credit)
        if returned_query > 0:
            CreditNote.objects.filter(id=get_invoice.credit.id, status=1).update(history_status=2)


        check_creadit_status=CreditNote.objects.filter(id=get_invoice.credit.id, status=1).first()
        print(f'returned_query {returned_query}, vendor {vendor}')
        checkpermission_creditnote_ir=checkpermission_creditnoterecipt(get_invoice.credit,request.user.id,'1')
        check_for_invreceipt=0
        if checkpermission_creditnote_ir > 0:
            check_for_invreceipt=check_for_flow(get_invoice.credit,request.user.id,'1')
        checkpermission_creditnote_ia=checkpermission_creditnoterecipt(get_invoice.credit,request.user.id,'2')
        check_for_invapproval=0
        if checkpermission_creditnote_ia > 0:
            check_for_invapproval=check_for_flow(get_invoice.credit,request.user.id,'2')
        invoice_number=list(InvoiceCostInvoice.objects.filter(invoice_id=get_invoice.invoice_id).values_list('invoice_number',flat=True))
        # credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
        invoice_number=', '.join(str(e) for e in invoice_number)
        credit_no=CreditNoteContractInvoice.objects.filter(credit_id=credit_no['credit'],status=1)
        credit_number=list(credit_no.values_list('credit_note_no',flat=True))
        date=list(credit_no.values_list('date',flat=True))
        find_dates=[]
        appr_status=''
        apprv_date=''
        for dated in date:
            if dated:
                date_format=confulldate(dated,request.company.id)
                find_dates.append(date_format)
            else:
                find_dates.append('N/A')

        if get_invoice.credit.approval_status == 1:
            appr_status='Pending'
            apprv_date='N/A'
        elif get_invoice.credit.approval_status == 2:
            appr_status='Rejected'
            approval_date=confulldate(get_invoice.credit.approval_date,request.company.id)
            apprv_date=approval_date
        elif get_invoice.credit.approval_status == 3:
            appr_status='Returned'
            approval_date=confulldate(get_invoice.credit.approval_date,request.company.id)
            apprv_date=approval_date
        elif get_invoice.credit.approval_status == 6:
            appr_status='Disputed'
            apprv_date='N/A'
        else:
            appr_status='Approved'
            # approval_date=(get_invoice.credit.approval_date.date()).strftime("%d-%m-%Y")
            approval_date=confulldate(get_invoice.credit.approval_date,request.company.id)
            apprv_date=approval_date
        allcredit_note.append({
            's_no':s_no,
            'Credit_no':credit_number,
            'date':find_dates,
            'invoice_number':invoice_number,
            'apprv_date':apprv_date,
            'appr_status':appr_status,
            'credit_id':get_invoice.credit_id,
            'checkpermission_creditnote_ir':checkpermission_creditnote_ir,
            'check_for_invreceipt':check_for_invreceipt,
            'checkpermission_creditnote_ia':checkpermission_creditnote_ia,
            'check_for_invapproval':check_for_invapproval,
            'vendorid':vendor,
            'returned_query':returned_query,
            'history':check_creadit_status.history_status,
        })
        s_no+=1
    response = {
        'draw': draw,
        'recordsTotal': full_credit.count(),
        'recordsFiltered': full_credit.count(),
        'data': allcredit_note
    }

    return JsonResponse(response)

def notify_credit_flow(request,userdata,url,verb,description):
    sender = request.user
    recipient=userdata
    scheme=request.scheme
    gethost=request.get_host()
    url=f"{scheme}://{gethost}/{url}"
    notify.send(sender, recipient=recipient,data=url, verb=verb, description=description)
    return

import pytz
def credit_return_flow(credit_id,module_id,submit_type,comments,request,submit_name):
    print(f'module_id ,{module_id}')
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    current_date=datetime.now()
    creditflow_modules=Invoiceflowmodules.objects.getcreditflowmodules_byinvoice(credit_id,module_id)
    if (creditflow_modules):
        Invoiceflowmodules.objects.updateinvoiceflowmodules(creditflow_modules.id)
        Invoiceflowmodulesusers.objects.updateinvoicelowusers(creditflow_modules.id,request.user.id,current_date,submit_type,comments)
    CreditNote.objects.filter(id=credit_id).update(approval_status=3 , approval_date=current_date)
    returnCheck=DisputedInvoiceTrack.objects.filter(credit_id=credit_id).count()
    credit_detail = CreditNote.objects.getcreditnote_by_id(credit_id)
    inv_val=''
    get_invoice=CreditNoteInvoice.objects.filter(credit_id=credit_id,status=1).first()
    if get_invoice:
        inv_val=get_invoice.invoice
    credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=credit_id,status=1).values_list('credit_note_no',flat=True))
    all_credit=', '.join(str(e) for e in credit_number)
    # content=f'Credit Note {all_credit} has been {submit_name} for clarification by {request.user.name} on {date_today} for {inv_val.name_service} '
    invoice_detail = CreditNoteInvoice.objects.filter(credit_id=credit_id,status=1).first()
    contractid=Invoice.objects.filter(id=invoice_detail.invoice_id).last()     
    content=f'Credit Note {submit_name} for clarification by {request.user.name} on {date_today} for {contractid.name_service}'
    vendor=ContractMasterVendor.objects.get_byid(credit_detail.vendor_id,request.company)
    vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
    allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
    # main_url="credit/unapprovedcreditnotes"
    main_url="credit/list"
    # main_verb='Credit Note '+submit_name+' for Clarification.' 
    main_verb='Credit Note '+submit_name+' for Clarification.'
    # if module_id == 1 or module_id == 2:
    for notifications in allVendors:
        # invoive_return_mail(request,notifications,vendor,submit_name,credit_detail,comments,all_invoice,submit_type)
        notify_credit_flow(request,notifications,main_url,main_verb,content)
        credit_return_mail(request,notifications,vendor,submit_name,contractid,comments,all_credit)
    # invoice_detail = CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
    # contractid=Invoice.objects.filter(id=invoice_detail.invoice_id).last()     
    # credit_details=CreditNote.objects.getcreditnote_by_id(pk)
    # vendor=ContractMasterVendor.objects.get_byid(credit_details.vendor_id,request.company)
    # allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
    # main_url="credit/list"
    # user_main_url = f"credit/creditapprovallist/{pk}"
    # main_verb='Credit Note '+submit_name
    # approval_verb="Credit Note for Approval"
    # content=f'Credit Note {submit_name} by {request.user.name} on {date_today} for {contractid.name_service}'
    
    if returnCheck== 0:
        DisputedInvoiceTrack.objects.create(user_id=request.user.id,credit_id=credit_id,stage=1,created_at=current_date,module_id=module_id)
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        vendor=ContractMasterVendor.objects.get_byid(credit_detail.vendor_id,request.company)
        AddNewDisputedQuery.objects.reason_for_creditdispute(credit_id,comments,request.user,time_stamp,vendor.id,module_id)
    else:
        main_url="credit/unapprovedcreditnotes"
        get_prev_user=AddNewDisputedQuery.objects.filter(credit_id=credit_id).first()
        # notify_invoice_flow(request,get_prev_user.user,main_url,main_verb,content)
        utc_timezone = pytz.utc
        utc_time = datetime.now(utc_timezone)
        time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
        vendor=ContractMasterVendor.objects.get_byid(credit_detail.vendor_id,request.company)
        BackToDisputeQuery.objects.reason_for_creditdispute(credit_id,comments,request.user,time_stamp,vendor.id,module_id)
    return

class DisputedCreditQueryHistory(View):
    def get(self,request,pk):
        # query=Invoice.objects.get_by_id(pk)
        credit=CreditNote.objects.getcreditnote_by_id(pk)
        ref_num=ContractMaster.objects.filter(id=credit.contract_id).first()
        check_InvoiceExceptional=CreditExceptional.objects.filter(credit_id=pk,status=1).exclude(exceptional_type=5).count()
        vendor=ContractMasterVendor.objects.get_byid(credit.vendor_id,request.company)
        checked_messages = CreditExceptional.objects.filter(credit_id=pk, status=1).exclude(exceptional_type=5).values_list('checked_messages', flat=True)
        #
        get_users=list(User.objects.filter(roles_id=3,company_id=request.company.id).values_list('id',flat=True))
        get_rights=list(UserRights.objects.filter(user_id__in=get_users,module_id=18,create='1').values_list('user_id',flat=True))
        get_dispute_users=User.objects.filter(roles_id=3,company_id=request.company.id,id__in=get_rights).count()
        # wcc_files=other_documents()
        # print(f'wcc_files {wcc_files}')
        get_status=DisputedInvoiceTrack.objects.filter(credit_id=pk,stage=4).first()
        querylist=AddNewDisputedQuery.objects.filter(credit_id=pk)

        data={'querylists':querylist,'query':credit,'pk':pk,'contact_person':vendor,'ref_num':ref_num,'get_status':get_status,'check_InvoiceExceptional':check_InvoiceExceptional,'get_dispute_users':get_dispute_users,'checked_messages':checked_messages}
        return render(request,'disputedcreditquerylist.html',data)

    def post(self,request,pk):
        print(f' reqe {request.POST}')
        today = date.today()
        date_today = today.strftime("%d-%b-%Y")
        query=CreditNote.objects.getcreditnote_by_id(pk)
        invoice_id=None
        get_invoice=CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
        if get_invoice:
            invoice_id=get_invoice.invoice
        credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
        all_credit=', '.join(str(e) for e in credit_number)
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
            credit_detail = CreditNote.objects.getcreditnote_by_id(pk)
            vendor=ContractMasterVendor.objects.get_byid(credit_detail.vendor_id,request.company)
            if submit_type == '8':
                file=request.POST.get('file')
                get_exceptional=request.POST.getlist('exceptional')
                exceptional_list=[CreditExceptional(credit_id=pk,exceptional_type=i,confirm_dispute=1) for i in get_exceptional]
                CreditExceptional.objects.bulk_create(exceptional_list)
                CreditNote.objects.filter(id=pk).update(dispute_status=2,approval_status=6)
                DisputedInvoiceTrack.objects.create(credit_id=pk,stage=3,status=True,user=request.user,created_at=datetime.now(),reason=comments)
                main_url="credit/rejectedcreditnotes"
                subject=f"Recommendation for CreditNote Dispute"
                reason=f'CreditNote {all_credit} has been recommended for Dispute for {vendor.vendor_name} on {date_today} for {invoice_id.name_service}'
                # for user in get_dispute_users:
                #     url='https://irockinfo.mo.vc/'
                #     moved_as_dispute_mail(request,user,all_credit,url,credit_detail,vendor,comments)
                #     notify_invoice_flow(request,user,main_url,subject,reason)
                AddNewDisputedQuery.objects.create_creditdisputed_query(pk,reason,request.user,time_stamp,vendor.id,file)
                return redirect("credit:rejectedcreditnotes")
            # elif submit_type == '6':
            #     percentage_val=request.POST.get('settlement_val')
            #     file=request.POST.get('file')
            #     DisputedInvoiceTrack.objects.create(invoice_id=pk,stage=4,status=True,user=request.user,created_at=datetime.now(),reason=comments)
            #     get_approved_percentage=100 - float(percentage_val)
            #     get_invoice_value=InvoiceCostInformation.objects.get_invoice_id(pk,1)
            #     get_module=AddNewDisputedQuery.objects.filter(query_id=pk).first()
            #     check_possiblity=BackToDisputeQuery.objects.filter(query_id=pk).count()
            #     if(check_possiblity>0):
            #         get_module=BackToDisputeQuery.objects.filter(query_id=pk).first()
            #     if(get_invoice_value.count() >= 1):
            #         get_settlement_val=get_invoice_value.first()
            #         match =''.join(filter(str.isdigit, get_settlement_val.finalvalue))
            #         get_invoice="{:.2f}".format(float(match)*(float(percentage_val)/100))
            #         SettlementInvoice.objects.create(settlement=percentage_val,invoice_id=pk,user=get_user,invoice_value=get_invoice,company=request.company,module_id=get_module.module_id)
            #     reason=f'Invoice No {all_credit} has been approved for {int(get_approved_percentage)}% and disputed for {percentage_val}% by {request.user.name} '
            #     main_url=f"invoice/invoicequeryhistory/{pk}"
            #     vendor_data=User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
            #     AddNewDisputedQuery.objects.create_disputed_query(pk,reason,request.user,time_stamp,vendor.id,file)
            #     allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            #     main_verb='Invoice Disputed'
            #     content=f'Invoice {all_credit} has been disputed by {request.user.name} on {date_today} for {invoice_id.name_service}'
                # for notifications in allVendors:
                #     notify_invoice_flow(request,notifications,main_url,main_verb,content)
                #     invoice_Settlement_mail(request,notifications,vendor,submit_name,invoice_detail,comments,all_credit,get_approved_percentage,percentage_val)
                # return redirect('invoice:invoicequeryhistory',pk=pk)
            # elif submit_type == 'A1':
            #     Invoice.objects.filter(id=pk).update(dispute_status=3)
            #     allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            #     main_url=f"invoice/invoicequeryhistory/{pk}"
            #     disputed_user=AddNewDisputedQuery.objects.filter(query_id=pk).first()
            #     reason=f"Disputed Invoice accepted by {request.user.name}."
            #     content=f" Dispute Invoice {all_credit} has been accepted and resolved by {request.user.name} on {date_today} for services {invoice_id.name_service}."
            #     # if disputed_user.user:
            #     #     notify_invoice_flow(request,disputed_user.user,main_url,reason,content)
            #     #     dispute_vendor_acceptmail_touser(request,disputed_user.user,all_credit,invoice_detail,vendor)
            #     # for user in get_dispute_users:
            #     #     dispute_vendor_acceptmail_touser(request,user,all_credit,invoice_detail,vendor)
            #     #     notify_invoice_flow(request,user,main_url,reason,content)
            #     reason=f"Disputed Invoice accepted and resolved."
            #     content=f" Dispute for invoice {all_credit} for services {invoice_id.name_service} has been accepted and resolved by {request.company}"
                # for notifications in allVendors:  
                #     notify_invoice_flow(request,notifications,main_url,reason,content)
                #     dispute_vendor_acceptmail(request,notifications,all_credit,invoice_detail,vendor)
                
                # return redirect('invoice:invoicequeryhistory',pk=pk)
            # elif submit_type == 'A2':
            #     main_url=f"invoice/listdisputeinvoices"
            #     verb=f"Disputed Invoice Contested by {request.user.name}"
            #     reason=f'Dispute on Invoice No.{all_credit} has been contested by {request.user.name} on {date_today} for {invoice_id.name_service}'
            #     disputed_user=AddNewDisputedQuery.objects.filter(query_id=pk).first()
            #     # if disputed_user.user:
            #     #     notify_invoice_flow(request,disputed_user.user,main_url,verb,reason)
            #     #     dispute_vendor_declinemail_touser(request,disputed_user.user,all_credit,invoice_detail,vendor,comments)
            #     # for user in get_dispute_users:
            #     #     dispute_vendor_declinemail_touser(request,user,all_credit,invoice_detail,vendor,comments)
            #     #     notify_invoice_flow(request,user,main_url,verb,reason)
            #     Invoice.objects.filter(id=pk).update(dispute_status=4)
            #     return redirect('invoice:invoicequeryhistory',pk=pk)
            else:
                get_module=AddNewDisputedQuery.objects.filter(credit_id=pk).first()
                check_possiblity=BackToDisputeQuery.objects.filter(credit_id=pk).count()
                if(check_possiblity>0):
                    get_module=BackToDisputeQuery.objects.filter(credit_id=pk).first()
                DisputedInvoiceTrack.objects.create(credit_id=pk,stage=5,status=True,user=request.user,created_at=datetime.now(),reason=comments)
                CreditNote.objects.filter(id=pk).update(approval_status=1)
                Invoiceflowmodules.objects.filter(creditnote_id=pk,module_id=get_module.module_id).update(status=0)
                print(f'get_module.module_id {get_module.module_id}')
                credit_flow_func(pk,get_module.module_id,request,comments,submit_type,submit_name)
                print(f'pk {pk},comments {comments},submit_type {submit_type},submit_name {submit_name}')
                if request.user.roles_id == 2 or request.user.roles_id ==3:
                    return redirect("credit:unapprovedcreditnotes")
                else:
                    return redirect("credit:unapprovedcreditnotes")
        else:
            deniedreason=request.POST.get('message')
            files_upload=request.POST.get('files_upload')
            document_type=request.POST.get('document_type')
            document_name=request.POST.get('document_name')
            vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
            allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
            check_InvoiceExceptional=CreditExceptional.objects.filter(credit_id=pk,exceptional_type=1,status=1).count()
     
            main_url=f"credit/creditqueryhistory/{pk}"
            verb=f"Response to Credit Note Returned Clarification."
            reason=f'Credit Note {all_credit} has been received response for returned Credit Note from {request.user.name} on {date_today} for {invoice_id.name_service}'
            if request.user.roles_id == 4:
                url='https://irockinfo.mo.vc/' 
                team=f'The Invoice Approval Process System'
                # if query.invoice_status == 6:
                #     for users in get_dispute_users:
                #         notify_invoice_flow(request,users,main_url,verb,reason)
                #         response_to_vendor_mail(request,users,all_credit,url,query,team)
                # else:
                #     returned_user=AddNewDisputedQuery.objects.filter(query_id=pk).first()
                #     if returned_user.user:
                #         notify_invoice_flow(request,returned_user.user,main_url,verb,reason)
                #         response_to_vendor_mail(request,returned_user.user,all_credit,url,query,team)
            else:
                url='https://irockinfo.mo.vc/vendorlogin' 
                team=f'The Finance Team'
                # for vendor_data in allVendors:
                #     notify_invoice_flow(request,vendor_data,main_url,verb,reason)
                #     response_to_vendor_mail(request,vendor_data,all_credit,url,query,team)
            print(f'check_InvoiceExceptional---- {check_InvoiceExceptional}')
            if check_InvoiceExceptional > 0 and request.user.roles_id == 4:
                files=request.FILES.getlist('file')
                print(f'files {files}')
                if len(files) > 0:
                    get_dispute=AddNewDisputedQuery.objects.create_creditdisputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None)
                    for file in files:
                        if (file != None): 
                            fs = FileSystemStorage()
                            file = fs.save(file.name, file)
                        create_file=CreditSupportDocuments.objects.create(credit_id=pk,file=file,filetype='new')
                        DisputedQueryFiles.objects.create(disputedquery=get_dispute,file=file,document_name=document_name,document_type=document_type)
                else:
                    get_dispute=AddNewDisputedQuery.objects.create_creditdisputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,None)
            else:
                file=request.FILES.get('file')
                if (file != None): 
                    fs = FileSystemStorage()
                    file = fs.save(file.name, file)
                get_dispute=AddNewDisputedQuery.objects.create_creditdisputed_query(pk,deniedreason,request.user,time_stamp,vendor.id,file)
          
            scheme=request.scheme
            gethost=request.get_host()
            if request.user.roles_id == 4:
                sender = User.objects.get_by_id(request.user.id)
                url=f"{scheme}://{gethost}/credit/creditqueryhistory/{pk}"
                description=f'Reply received from {vendor.vendor_name}'
                # getCompanyUserlist(request,sender,url,'Reply Received for Disputed Invoice',description)
            else:
                print('To Vendor')
                sender = User.objects.filter(id=request.user.id).first()
                recipients = User.objects.filter(cin_number=vendor.vin,contactpersonstatus=1).first()
                print('recipients',recipients)
                url=f"{scheme}://{gethost}/credit/creditqueryhistory/{query.id}"
                notify.send(sender, recipient=recipients,data=url, verb='Reply Received for Disputed Credit Note', description=f'Reply received from {sender.name} {sender.lastname if sender.lastname != None else ""}')
            return redirect('credit:creditqueryhistory',pk=pk)
    

def CloseCreditQuery(request,pk):
    query=CreditNote.objects.getcreditnote_by_id(pk)
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
    credit_number=list(CreditNoteContractInvoice.objects.filter(credit_id=pk,status=1).values_list('credit_note_no',flat=True))
    all_credit=', '.join(str(e) for e in credit_number)
    accepted_member=f'Credit Note No.{all_credit} query has been accepted by {request.user.name} {request.user.lastname}'
    vendor=ContractMasterVendor.objects.get_byid(query.vendor_id,request.company)
    utc_timezone = pytz.utc
    utc_time = datetime.now(utc_timezone)
    time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    invoice_id=''
    get_invoice=CreditNoteInvoice.objects.filter(credit_id=pk,status=1).first()
    if get_invoice:
        invoice_id=get_invoice.invoice.name_service
    file=request.FILES.get('file')  
    get_dispute=AddNewDisputedQuery.objects.create_creditdisputed_query(pk,accepted_member,request.user,time_stamp,vendor.id,file)
    get_invoice=CreditNote.objects.filter(id=pk).update(dispute_status=1)
    DisputedInvoiceTrack.objects.create(stage=2,credit_id=pk,status=True,user=request.user,created_at=datetime.now())
    if request.user.roles.id == 3 or request.user.roles.id == 2:
        allVendors=User.objects.filter(cin_number__iexact=vendor.vin,status=1)
        main_url=f"credit/creditqueryhistory/{pk}"
        main_verb=f'Credit Note NO.{all_credit} Accepted for Approval Flow '
        content=f'Credit Note NO.{all_credit} Accepted for Approval by {request.user.name} on {date_today} for {invoice_id} '
        now = datetime.now()
        # for notifications in allVendors:
        #     notify_invoice_flow(request,notifications,main_url,main_verb,content)
    else:
        main_url=f"credit/creditqueryhistory/{pk}"
        main_verb=f'Credit Note NO.{all_credit} Accepted by {request.user.name} {request.user.lastname} '
        content=f'Credit Note NO.{all_credit} Accepted for Approval by {request.user.name} on {date_today} for {invoice_id} '
        get_user=AddNewDisputedQuery.objects.filter(credit_id=pk).first()
        # notify_invoice_flow(request,get_user.user,main_url,main_verb,content)
    return redirect('credit:creditqueryhistory', pk=pk)



def get_creadit_note_details(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')  
    user=User.objects.filter(Q(is_primary=1) | Q(is_secondary=1),id=request.user.id).first()
    vendor_status = True if user else False
    vendorid=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
    credit_value = CreditNoteContractInvoice.objects.filter(Q(credit__vendor_id=vendorid.id,credit__status=1) & Q(credit_note_no__icontains=search_value,credit__vendor_id=vendorid.id,credit__status=1)).order_by('-credit__id').values('credit').distinct() if vendor_status == True else CreditNoteContractInvoice.objects.filter(Q(credit__vendor_id=vendorid.id,credit__status=1,credit__credit_status=2) & Q(credit_note_no__icontains=search_value,credit__vendor_id=vendorid.id,credit__status=1,credit__credit_status=2)).order_by('-credit__id').values('credit').distinct()
    full_wcc_value=credit_value[start:start+length]
    print(f"credit_value{credit_value.count()}")
    print(f"full_wcc_value{full_wcc_value.count()}")
    all_creadit_note=[]
    s_no=start+1
    for credit in full_wcc_value :
        credit_note_num=list(CreditNoteContractInvoice.objects.filter(credit_id=credit['credit'],status=1).values_list("credit_note_no",flat=True))
        print("credit_note_num",credit_note_num)
        # print("credit.credit.id",credit.credit.id)

        check_creadit_status = CreditNote.objects.filter(id=credit["credit"] ,status=1).first()
        credit_status=""
        if check_creadit_status.credit_status == 1:
            credit_status="Draft"
        else :
            credit_status="Submitted"
        inv_count= get_returned_invoice_count(check_creadit_status.id , "")
        credit_note_values=CreditNoteContractInvoice.objects.filter(credit_id=credit['credit'],status=1)
        find_dates=[]
        approval_status=[]
        approval_date=[]
        ref_inv_num=[]
        for credit_note in credit_note_values:
            if credit_note.credit.approval_status == 1 :
                approval_status.append("Pending")                            
            elif credit_note.credit.approval_status == 2 :
                approval_status.append("Rejected")
            elif credit_note.credit.approval_status == 3:
                approval_status.append("Returned")
            elif credit_note.credit.approval_status == 6 :
                approval_status.append("Disputed")                     
            else :
                approval_status.append("Approved")
                                 
            date_format=confulldate(credit_note.date,request.company.id)
            find_dates.append(date_format)

            if credit_note.credit.approval_date == None or credit_note.credit.approval_date == "":
                approval_date.append("N/A")
            else :
                approve_date_format=confulldate(credit_note.credit.approval_date,request.company.id)
                approval_date.append(approve_date_format)
            
            ref_invoice=credit_contract_invoices(credit_note.credit.id , "inv")
            ref_number=[]
            for ref in ref_invoice :
                ref_number.append(ref)
            
            ref_inv_num.append(ref_number)
        

        all_creadit_note.append({
            's_no':s_no,
            'id':credit['credit'],
            'credit_num':credit_note_num,
            'date':find_dates,
            'ref_num':ref_inv_num,
            'approval_status':approval_status,
            'approval_date':approval_date,
            'status':credit_status,
            'vendorid':vendorid.id,
            'vendorid_active_status':vendorid.active_status,
            'vendor_status':vendor_status,
            'credit_credit_status':check_creadit_status.credit_status,
            'credit_approve_status':check_creadit_status.approval_status,
            'inv_count':inv_count,
            'history':check_creadit_status.history_status,

        })
        s_no+=1 
        print(f'all_creadit_note {all_creadit_note}')   
    response = {
        'draw': draw,
        'recordsTotal': credit_value.count(),
        'recordsFiltered': credit_value.count(),
        'data': all_creadit_note
    }
    return JsonResponse(response)



