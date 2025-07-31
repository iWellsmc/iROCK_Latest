from itertools import count
import json
from time import strftime
import re
import datetime
import ast
from functools import reduce
from datetime import date
from datetime import datetime
import pytz
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
import base64
from PIL import Image
from io import BytesIO
from ..utils.utils import convert_to_int
import operator
from django.db.models import Q
from invoice.models import Invoiceflowmodules,Invoiceflowmodulesusers
from credit_note.models import *
from finance.models import *
from cost_code.models import CostCodeVendor
from django.db.models import Q,Sum
from datetime import datetime, timedelta
# import urllib, cStringIO, base64

from django.http import request
from django.http.response import JsonResponse
from custom_auth.models import *
from projects.models import *
from invoice.models import *
from finance.models import CompanyBank,CompanyBankUser
from django import template
from projectflow.models import *

# Local application/library-specific imports
from InvoiceGuard.models import RoleRight,SignatoriesSettings ,SignatoriesUsers
from projects.templatetags.custom_tags import convert_val_to_float,get_credit_investment,get_net_payableamount
from credit_note.templatetags.credit_custom_tags import remove_symbol,creaditenote_gross_amount
from decimal import Decimal


register = template.Library()


def getcontractname(value,contracttype):
    if  (contracttype == "original"):
        get_contract_master=ContractMaster.objects.filter(id=value).first()   
        getcontractname=get_contract_master.reference_number
    else:
        get_contract_master=Amendment.objects.filter(id=value).first() 
        getcontractname=get_contract_master.amendment_reference_number

    return getcontractname


@register.filter
def get_contract_type_coversheet(value):
    if value == "service_supply":
        return f"Services & supply"
    else:
        return value

@register.simple_tag
def getcontract(value,contracttype):
    try:
        if  (contracttype == "original"):
            get_contract_master=ContractMaster.objects.filter(id=value).first()
            invoicesonum=get_contract_master.reference_number
        else:
            get_contract_master=Amendment.objects.filter(id=value).first()
            invoicesonum=get_contract_master.amendment_reference_number
        return invoicesonum,get_contract_master
    except ValueError:
        return

def getdiscountvalue(percentage,invoiceid):
    getcostinforamation=InvoiceCostInformation.objects.filter(invoice_id=invoiceid,status=1).first()
    getamount=getcostinforamation.total_discount_value
    split_value=getamount.split(" ")
    remove_comma=split_value[1].replace(',', '')
    get_discount_value=float(remove_comma)*float(percentage)/100
    return split_value[0]+" "+"{:,.2f}".format(get_discount_value)
#tax
@register.simple_tag
def get_taxvalue(percentage,invoiceid):
    getcostinforamation=InvoiceCostInformation.objects.filter(invoice_id=invoiceid,status=1).first()
    getamount=getcostinforamation.total_exclusive_value
    if (getamount != None):
        split_value=getamount.split(" ")
        remove_plus=split_value[0].replace('+','')
        finalval=split_value[1].replace(',', '')
        get_discount_value=float(finalval)*float(percentage)/100
        return remove_plus[0]+" "+"{:,.2f}".format(get_discount_value)
    else:
        finalval=0
        value=getcostinforamation.total_discount_value
        currencysymbol=value.split(" ")
        get_discount_value=float(finalval)*float(percentage)/100
        return currencysymbol[0]+" "+"{:,.2f}".format(get_discount_value)

#use for string date
def convertinvoicedate(value,companyid):
    if (value != None and value !=""):
        convert_date=datetime.strptime(value ,"%Y-%m-%d").date()
        company_generalsetting=Settings.objects.filter(company_id=companyid).first()
        all_dateformat = {'dd-M-yy':"%d-%b-%Y",'dd-mm-yy':"%d-%m-%Y",'dd/mm/yy':"%d/%m/%Y",'mm-dd-yy':'%m-%d-%Y','mm/dd/yy':'%m/%d/%Y','yy-mm-dd':'%Y-%m-%d','yy/mm/dd':'%Y/%m/%d'}
        for key,values in all_dateformat.items():
            if (key == company_generalsetting.dateformat):
                return convert_date.strftime(values)
    else:
        return ""
        # for key,values in all_dateformat.items():
        #     if (key == company_generalsetting.dateformat):
        #         return convert_date.strftime(values)

#use for datetime object
def confulldate(value,companyid):
    try:
        if (value != None):
            company_generalsetting=Settings.objects.filter(company_id=companyid).first()
            all_dateformat = {'dd-M-yy':"%d-%b-%Y",'dd-mm-yy':"%d-%m-%Y",'dd/mm/yy':"%d/%m/%Y",'mm-dd-yy':'%m-%d-%Y','mm/dd/yy':'%m/%d/%Y','yy-mm-dd':'%Y-%m-%d','yy/mm/dd':'%Y/%m/%d'}
            for key,values in all_dateformat.items():
                if (key == company_generalsetting.dateformat):
                    return value.strftime(values)
    except:
        return
    

def getinvoicefiles(invoicecostid,invoiceid):
    fileurl=InvoiceFileUpload.objects.filter(invoice_id=invoiceid,invoicecostinvoice_id=invoicecostid,status=1).first()
    if (fileurl != None):
        replace_text=str(fileurl.support_file)
       
        if not replace_text:
            replace_text=str(fileurl.support_file)
           
        return replace_text.replace("invoicedocuments/","")
    else:
        return ""
@register.filter
def getinvoicefile(invoicecostid,invoiceid):
    fileurl=InvoiceFileUpload.objects.filter(invoice_id=invoiceid,invoicecostinvoice_id=invoicecostid,status=1).first()
    if (fileurl != None):
        replace_text=fileurl.file_name
       
        if not replace_text:
            replace_text=str(fileurl.support_file)
           
        return replace_text.replace("invoicedocuments/","")
    else:
        return ""


def getinvoicefileid(invoicecostid,invoiceid):
    fileurl=InvoiceFileUpload.objects.filter(invoice_id=invoiceid,invoicecostinvoice_id=invoicecostid,status=1).first()
    if (fileurl != None):
        return fileurl.id
    else:
        return ""


def getinvoices(invoiceid):
    invoices=InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,status=1) 
    return invoices

@register.simple_tag
def checkinvoicesedit(invoiceid,request):
    invoices=InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,status=1) 
    contractid=Invoice.objects.get_by_id(invoiceid)
    getvin=request.user.cin_number
    getvendordetails=ContractMasterVendor.objects.filter(vin=getvin,company=request.company,status=1).first()

    if (contractid.contracttype == 'original'):
        contract=ContractMaster.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(contract_id=contract.id,status=1)
    else:
        contract=Amendment.objects.filter(id=contractid.contractid ,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(amendment_id=contract.id,status=1)
    return vendorinvoice.count(),invoices.count()

def subinvoice(invoiceid,contractinvid):
    invoices=InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,vendor_invoice_id=contractinvid,status=1) 
    print(f'invoices {invoices}')
    return invoices

@register.filter
def zip_lists(a, b):
    if not b:
        b= list(a).copy()   
    return zip(a, list(b))

@register.simple_tag
def checkallinvoice(invoiceid,contractinvid):
    invoices=InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,vendor_invoice_id=contractinvid,status=1) 
    inv_count=invoices.filter(Q(invoice_number__isnull=True) | Q(invoice_number__exact='') | Q(invoice_date__isnull=True) | Q(invoice_date__exact='') | Q(invoice_date__exact='') | Q(invoice_exchange_rate='')).count()
    return inv_count

    
def checkblockval(value):
    try:
        if (value == None):
            return "Not Applicable"
        else:
            return value.block.block_name
    except AttributeError:
        return
    else:
        return

def checkfieldval(value):
    try:
        if (value == None):
            return "Not Applicable"
        else:
            return value.field.field_name
    except AttributeError:
        return
    else:
        return

def checkwellval(value):
    try:
        if (value == None):
            return "Not Applicable"
        else:
            return value.wellname.well_subname
    except AttributeError:
        return
    else:
        return

@register.simple_tag
def getinvoicesupportfile(invoiceid,supportid,contract=None):
    invoice_details=Invoice.objects.get_by_id(invoiceid)
    contract=invoice_details
    if supportid == '10':
        if invoice_details.contracttype == 'original' and contract!=None:
            files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.contractid,2)
        else:
            if invoice_details.contracttype == 'amendment' or invoice_details.contracttype =="addendum":
                contract=Amendment.objects.filter(id=invoice_details.contractid,status=1).first()
                files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service.id,2)
        # print(f"files {files}")

    elif supportid == '9':
        if invoice_details.contracttype == 'original' and contract!=None:
            files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.contractid,1)
        else:
            if invoice_details.contracttype == 'amendment' or invoice_details.contracttype =="addendum":
                contract=Amendment.objects.filter(id=invoice_details.contractid,status=1).first()
                files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service.id,1)

    else:
        files=InvoiceFileUpload.objects.filter(invoice_id=invoiceid,support=supportid,status=1)
    return files,files.count()

@register.simple_tag
def getoriginalcontract_price_files(contract,contracttype,file_type):
    if contracttype == 'original':
        contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.id,file_type).values()

    else:
        contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract.service_id,file_type).values()
    return contract_table_files

@register.simple_tag
def getamendmentcontract_price_files(contract,contracttype,file_type):
    contract_table_files=VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id,file_type).values()
    # print(f"contract_table_files {contract_table_files}")  
    return contract_table_files



@register.simple_tag
def workcomplition(string):
    if (string == "") or (string == None) or (string == "['']"):
        return []
    # type of ast.literal_eval is list
    if type(ast.literal_eval(string)) == list:
        if string != None:
            ast.literal_eval(string)
            #['10','10'] to [10,10]
            # list1 = [int(i) for i in string]
            list1 = [eval(i.replace(',', '')) for i in ast.literal_eval(string)]
            return list1
        else:
            return int(string.replace(',', ''))
            # remove thousand separator and convert to int

    else:
        return []
def invoices(vin_num,type):
    vendorid=ContractMasterVendor.objects.filter(vin=vin_num,status=1).first()
    if (type == "totsubinv"):
        invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendorid.id,status=1)
        totalinvoices=invoices.count()
        return totalinvoices
    elif (type == "approved"):
        invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendorid.id,status=1,approval_status=2)
        approvedinvoices=invoices.count()
        return approvedinvoices
    elif (type == "awaitingapproval"):
        invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendorid.id,status=1,approval_status=1)
        awaitinginvoices=invoices.count()
        return awaitinginvoices
    elif (type == "invoicedispute"):
        invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendorid.id,status=1,approval_status=0)
        disputinvoices=invoices.count()
        return disputinvoices
    elif (type == "paidinvoice"):
        invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendorid.id,status=1,approval_status=2,payment_status=2)
        paidinvoices=invoices.count()
        return paidinvoices
    elif (type == "unpaidinvoice"):
        invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendorid.id,status=1,approval_status=2,payment_status=1)
        unpaidinvoices=invoices.count()
        return unpaidinvoices

def convert_two_degit_value(value):
    amount = Decimal(str(value))
    print(amount )
    print(round(amount, 2))
    return "{:,.2f}".format(amount)


def new_round_of_two_values(number):
    number_val=float(number)
    number_str = f"{number_val:.3f}"  
    integer_part, decimal_part = number_str.split('.') 
    if int(decimal_part[2]) >= 5:
        rounded_decimal = str(int(decimal_part[:2]) + 1).zfill(2)
        if rounded_decimal == "100":
            integer_part = str(int(integer_part) + 1)
            rounded_decimal = "00"
    else:
        rounded_decimal = decimal_part[:2]
    result = f"{integer_part}.{rounded_decimal}"
    newResult=float(result)
    return "{:,.2f}".format(newResult)


def round_of_two_values(number):
    number_val=float(number)
    number_str = f"{number_val:.3f}"
    integer_part, decimal_part = number_str.split('.') 
    if int(decimal_part[2]) >= 5:
        rounded_decimal = str(int(decimal_part[:2]) + 1).zfill(2)
        if rounded_decimal == "100":
            integer_part = str(int(integer_part) + 1)
            rounded_decimal = "00"
    else:
        rounded_decimal = decimal_part[:2]
    result = f"{integer_part}.{rounded_decimal}"
    newResult=float(result)
    return "{:.2f}".format(newResult)

@register.simple_tag
def invoiceafterdiscount(percentage,discount_value,exchange_value):
    # print(f'percentage {percentage}, discount_value {discount_value}, exchange_value {exchange_value}')
    if discount_value:
        # print(f"exchange_value.strip() {exchange_value.strip()}")
        if (exchange_value =="N/A" or exchange_value.strip() ==""):

            remove_curencysymbol=discount_value.split(" ")

            replace_comma=float(remove_curencysymbol[1].replace(",",""))
            final_value=replace_comma*float(percentage)/100
            # print(f'final_value {final_value}')
            return new_round_of_two_values(final_value)
        else:
            if (exchange_value == ""):
                exchange_value_rate=0
            else:
                exchange_value_rate=exchange_value
            remove_curencysymbol=discount_value.split(" ")
            replace_comma=float(remove_curencysymbol[1].replace(",",""))
            new_value=round_of_two_values(replace_comma*float(percentage)/100)
            # rounded_value = round(new_value, 2)
            final_value=float(new_value)*float(exchange_value_rate)
            
            return new_round_of_two_values(final_value)
    else:
        return "0.00"
    
@register.simple_tag
def invoiceexclusivevalue(percentage,excluive_value,exchange_value):
    if (excluive_value == None):
        excluive_value=0
        if (exchange_value =="N/A" or exchange_value ==""):
            final_value=excluive_value*float(percentage)/100
            return new_round_of_two_values(final_value)
        else:
            final_value=excluive_value*float(percentage)/100*float(exchange_value)
            return new_round_of_two_values(final_value)
    else:
        if (exchange_value =="N/A" or exchange_value ==""):
            remove_curencysymbol=excluive_value.split(" ")
            if len(remove_curencysymbol)>1:
                try:
                    replace_comma=float(remove_curencysymbol[1].replace(",",""))
                except:
                    replace_comma=0
            else:
                try:
                    replace_comma=float(remove_curencysymbol[0].replace(",",""))
                except:
                    replace_comma=0
            final_value=replace_comma*float(percentage)/100
            
            return new_round_of_two_values(final_value)
        else:
            if (exchange_value == ""):
                exchange_value_rate=0
            else:
                exchange_value_rate=exchange_value
            remove_curencysymbol=excluive_value.split(" ")
            if len(remove_curencysymbol)>1:
                try:
                    replace_comma=float(remove_curencysymbol[1].replace(",",""))
                except:
                    replace_comma=0
            else:
                try:
                    replace_comma=float(remove_curencysymbol[0].replace(",",""))
                except:
                    replace_comma=0
            new_value=float(round_of_two_values((replace_comma*float(percentage))/100))
            # rounded_value = round(new_value, 2)
            final_value=new_value*float(exchange_value_rate)
            return new_round_of_two_values(final_value)


@register.simple_tag
def newinvoiceexclusivevalues(pk, grossamount):
    try:
        grossamountvalue = float(replacecommaid(grossamount))
        invoice_exclusive_percentage = InvoiceExclusive.objects.filter(invoice_id=pk, status=1)
        amount = 0
        for tax in invoice_exclusive_percentage:
            taxes = float(tax.exclusive.taxpercentage)  # Get tax percentage\
            tax_value = (float(grossamountvalue) * float(taxes)) / 100  # Calculate tax valuE   
            amount += float(round_of_two_values(tax_value))  # Round and add tax value
            
        return round_of_two_values(amount)

    except ObjectDoesNotExist:
        return 0

    except Exception as e:
        return 0


def addvalues(disval,excval):
    if excval == None or excval == "" :
        excval = 0
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=str(excval).replace(",","")
    final_value=float(remove_discount_comma)+float(remove_exclusive_comma)
    return new_round_of_two_values(final_value)



def addpreviewvalues(disval,excval):
    if excval == None or excval == "" :
        excval = 0
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=str(excval).replace(",","")
    final_value=float(remove_discount_comma)+float(remove_exclusive_comma)
    final_value = Decimal(str(final_value))
    return "{:,.2f}".format(final_value)



@register.simple_tag
def Taxsubstractvalues(disval,excval=None ,inxval=None):
    if excval== None or excval == "":
        excval=0
    elif inxval == None or inxval == "":
        inxval =0
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=excval.replace(",","")
    remove_inclusive_comma=inxval.replace(",","")
    final_value=float(remove_discount_comma)+float(remove_exclusive_comma)-float(remove_inclusive_comma)
    return "{:,.2f}".format(final_value)

def minivalues(disval,excval):
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=excval.replace(",","")
    final_value=float(remove_discount_comma)-float(remove_exclusive_comma)
    return "{:,.2f}".format(final_value)

def replacecommaid(id):
    try:
        if (id != ''):
            con_str=str(id)
            return con_str.replace(',','')
        else:
            return ''
    except:
        return '0'

@register.simple_tag
def checkeditstatus(vin,companyid,invoiceid,contractid,type):
    getvendordetails=ContractMasterVendor.objects.filter(vin=vin,company_id=companyid,status=1).first()
    status=0
    if (contractid != ''):
        if (type == 'original'):
            contract=ContractMaster.objects.filter(id=contractid,status=1).first()
        else:
            contract=Amendment.objects.filter(id=contractid,status=1).first()
        vendorinvoice=VendorInvoiceSplit.objects.filter(vendor_id=getvendordetails.id,contract_id=contract.id,company_id=companyid,status=1).count()
        contractcostinvoice=InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,status=1)
        list_cost_ids=list(contractcostinvoice.values_list('id',flat=True))
        cost_count=contractcostinvoice.count()
        invoicesupportfile=InvoiceFileUpload.objects.filter(invoice_id=invoiceid,invoicecostinvoice_id__in=list_cost_ids,status=1).count()
        if (vendorinvoice == cost_count  and vendorinvoice == invoicesupportfile):
            status=1
        else:
            status=0
    else:
        status=0
    return status


def addtwovalues(a,b):
    return a + b

def capitalize_letter(letter):
    return letter.capitalize()


@register.simple_tag
def add(a, request):
    prevalue = request.session.get('values', 0)
    # print(f"float(str(prevalue).replace(',','')) {float(str(prevalue).replace(',',''))},float(str(a).replace(',','') {float(str(a).replace(',',''))},.......prevalue {prevalue},   a {a}.")
    value = request.session['values'] = float(str(prevalue).replace(',','')) + float(str(a).replace(',',''))
    # c = str(b).replace(',','')
    return True

@register.simple_tag(takes_context=True)
def previoussessionvalue(context):
    request = context['request']
    prevalue = request.session.get('values', 0)
    # print(f'prevalue {prevalue}')
    request.session['values'] = 0
    return "{:,}".format(prevalue)

def get_curreny(pk,ids):
    currency = Basecountries.objects.get(id=ids).currency
    return currency

@register.simple_tag
def addtwovalues(a,request):
    prevalue = request.session.get('values', 0)
    value = request.session['values'] = prevalue + a
    return value
    
@register.filter
def clearsessionvalue(request):
    request.session['values'] = 0
    return True

@register.filter
def pdfserialnumber(request):
    prevalue = request.session.get('serialno', 1)
    value = request.session['serialno'] = 1 + prevalue
    return value

@register.simple_tag
def clearpdfserial(request):
    request.session['serialno'] = 0
    return ''

@register.filter
def converturl(url):
    return url

@register.simple_tag
def custom_range_func(range,request):
    modules_list=[1,2,3,4,5,6,7]
    invoice_list=Invoice.objects.filter_by_company(1,2,request.company).filter(invoice_status=2).order_by('-id')
    pending_approval_invoice=[]
    # for module in modules_list:
    for invoice in invoice_list:
        if (Invoiceflowmodules.objects.filter(invoice_id=invoice.id).exists()):
        # data=checkpermission_invoicerecipt(invoice,request.user.id,module)
            pending_approval_invoice.append(invoice.id)
    return pending_approval_invoice

@register.simple_tag
def checkpermission_invoicerecipt(invoice,user_id,module_id):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid)
        try:
            project_id=contract_details[0].projects_id
        except:
            project_id=None
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
        try:
            project_id=contract_details.projects_id
        except:
            project_id=None
        
    if(contract_details):
        invoiceflowmodules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(invoice.id,module_id)
        if(invoiceflowmodules):
            if (module_id == "5"):
                checkuser_data=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_byuser(user_id,project_id,invoiceflowmodules.id)
                # print('as',user_id)
                # single user multiple currency
                checkuser_flow=0
                for data in checkuser_data:
                    check_data=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_payapp(invoiceflowmodules.id,data.payment_instruction_id).count()
                    if (check_data == 0):
                        checkuser_flow += 1
            else:
                checkuser_flow=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_byuser(user_id,project_id,invoiceflowmodules.id).count()
        else:
            checkuser_flow=0
    else:
        checkuser_flow=0
    return checkuser_flow

@register.simple_tag
def checkpermission_invoicerecipt_upload(invoice,user_id,module_id):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid)
        try:
            project_id=contract_details[0].projects_id
        except:
            project_id=None
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
        try:
            project_id=contract_details.projects_id
        except:
            project_id=None
    checkuser_flow=[]
    if(contract_details):
        invoiceflowmodules=Invoiceflowmodules.objects.filter_by_module_id(invoice.id,0,module_id)
        if(invoiceflowmodules.count()> 0):
            checkuser_flow=list(Invoiceflowmodulesusers.objects.filter(user=user_id,project_id=project_id,Invoiceflowmodules__in=invoiceflowmodules,status=0).values_list('Invoiceflowmodules__payment_instruct__payment_count',flat=True).distinct())
    return checkuser_flow

@register.simple_tag
def checkpermission_invoiceapproval_dispute(invoice,user_id,credit):
    if invoice:
        dispute_track=DisputedInvoiceTrack.objects.filter(invoice_id=invoice.id,user_id=user_id).first()
        dispute_track_count=0
        if dispute_track:
            dispute_track_count=1
        elif UserRights.objects.filter(module_id=18,user_id=user_id).first():
            if UserRights.objects.filter(module_id=18,user_id=user_id).first().create == '1':
                dispute_track_count=1
        return dispute_track_count
    else:
        print(credit)
        dispute_track=DisputedInvoiceTrack.objects.filter(credit_id=credit.id,user_id=user_id).first()
        dispute_track_count=0
        if dispute_track:
            dispute_track_count=1
        elif UserRights.objects.filter(module_id=18,user_id=user_id).first():
            if UserRights.objects.filter(module_id=18,user_id=user_id).first().create == '1':
                dispute_track_count=1
        return dispute_track_count


@register.simple_tag
def back_to_dispute(invoice):
    check_for_possiblity=BackToDisputeQuery.objects.filter(query_id=invoice.id).count()
    return check_for_possiblity

@register.simple_tag
def get_dispute_committee_member(request,invoice):
    dispute_member=0
    if(invoice.dispute_status == 2):
        if UserRights.objects.filter(module_id=18,user_id=request.user.id).first():
            if UserRights.objects.filter(module_id=18,user_id=request.user.id).first().create == '1':
                dispute_member=1
    elif(invoice.dispute_status == 3):
        if UserRights.objects.filter(module_id=18,user_id=request.user.id).first():
            if UserRights.objects.filter(module_id=18,user_id=request.user.id).first().create == '1':
                dispute_member=1
    return dispute_member


@register.simple_tag
def checkpermission_invoiceoverride(invoice,user_id,module_id):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid)
        try:
            project_id=contract_details[0].projects_id
        except:
            project_id=None
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
        try:
            project_id=contract_details.projects_id
        except:
            project_id=None
    # contract_details=ContractMaster.objects.get_by_id(invoice.contractid)
    if(contract_details):
        # project_id=contract_details[0].projects_id
        invoiceflowmodules=Invoiceflowmodules.objects.getinvoiceflowmodules_byinvoice(invoice.id,module_id)
        if(invoiceflowmodules):
            checkuser_flow=Invoiceflowmodulesusers.objects.getinvoiceoverrideflowmodulesusers_byuser(user_id,project_id,invoiceflowmodules.id).count()
        else:
            checkuser_flow=0
    else:
        checkuser_flow=0
    return checkuser_flow

@register.simple_tag
def checkpermission_bankuser(invoice,user_id):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid)
        try:
            project_id=contract_details[0].projects_id
        except:
            project_id=None
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
        try:
            project_id=contract_details.projects_id
        except:
            project_id=None
    #contract_details=ContractMaster.objects.get_by_id(invoice.contractid)

    if(contract_details):
        # project_id=contract_details[0].projects_id
        invoiceflowmodules=Invoiceflowmodules.objects.getinvoiceflowmodules_only_byinvoice(invoice.id,None)
        # print(f'aaa {invoiceflowmodules}, invoice {invoice.id}')
        if(invoiceflowmodules):
            get_data=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_by_only_user(user_id,project_id,invoiceflowmodules.id).filter(bank_user_verification=0).first()
            if get_data:
                checkuser_flow=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_payins(project_id,invoiceflowmodules.id,get_data.payment_instruction_id).count()
                checkuser_flow = 0 if checkuser_flow > 0 else 1 
            else:
                get_data=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_by_only_user(user_id,project_id,invoiceflowmodules.id).filter(bank_user_verification=1).first()
                if get_data:
                    checkuser_flow=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_payins(project_id,invoiceflowmodules.id,get_data.payment_instruction_id).count()
                    checkuser_flow = 0 if checkuser_flow > 0 else 1 
                else:
                    checkuser_flow=0
        else:
            checkuser_flow=0
    else:
        checkuser_flow=0
    return checkuser_flow

@register.filter
def vendorbasedbank(currency_id,request):
    company_bank = CompanyBank.objects.filter(currency_id=currency_id,company_id=request.company.id,status=1)
    return company_bank

@register.filter
def withoutbankuserbanklist(currency_id,request):
    company_bank = UserBankMaster.objects.filter(company_id=request.company.id,status=1 )
    id_list=[]
    for bank in company_bank:
        vals=str(currency_id) in bank.currency
        if vals:
            id_list.append(bank.id)
    bank_details=UserBankMaster.objects.filter(company_id=request.company.id,status=1 , id__in=id_list )
    return bank_details

@register.filter
def fetbankaccountnumber(bank_id):
    try:
        acc_num=UserBankAccountno.objects.filter(userbank_id=bank_id).first()
        return acc_num.accountno
    except:
        return

@register.filter
def fetch_bank_details(bank_id,request):
    company_bank = UserBankMaster.objects.filter(company_id=request.company.id,status=1,id=bank_id ).first()
    return company_bank.bank_name

@register.filter
def remainingvalue(invoicecost_id):
    payement = PaymentInstruction.objects.filter(invoicecost_id=invoicecost_id,is_editable=False)
    if payement.exists():
        return 100 - payement.aggregate(Sum('payment_percentage'))['payment_percentage__sum']
    else:
        return 100


@register.filter
def inclusivetaxes(invoice,type):
    try:
        if invoice.contracttype=='original':
            vendorcompanytaxdetails = VendorCompanyTaxPercentage.objects.filter(vendortax__contract_id=invoice.contractid,vendortax__status=1,vendortax__Tax_Type=type,vendortax__tax__isnull=False,status=1)
        else:
            vendorcompanytaxdetails=VendorCompanyTaxPercentage.objects.filter(vendortax__amendment_id=invoice.contractid,vendortax__status=1,vendortax__Tax_Type=type,vendortax__tax__isnull=False,status=1)
        return vendorcompanytaxdetails
    except:
        return

@register.filter
def count_total_text(invoice):
    tax_count=invoice.count()
    return tax_count

@register.simple_tag
def get_tax_values(tax,counter):
    # level_amount=convert_to_int(counter)
    tax=convert_to_int(counter.invoice_total_amount)*float(tax)/100
    return tax

@register.simple_tag
def get_cost_code(pk,company):
    invoice_data = Invoice.objects.get_by_id(pk)
    if invoice_data.costcodevendor == None:
        costcodedata=0
    else:
        costcodedata=CostCodeVendor.objects.get_by_id(invoice_data.costcodevendor.id)
    return costcodedata

@register.simple_tag
def get_tax_by_type(tax,counter):
    # print(f'tax {tax}, counter {counter}')
    # level_amount=convert_to_int(counter)
    tax=float(convert_to_int(tax))*float(convert_to_int(counter))/100
    return new_round_of_two_values(tax)

@register.simple_tag
def get_total_percentage(tax,counter):
    # print(f'tax {tax}')
    level_amount=convert_to_int(counter)
    real_val=0
    for taxes in tax:
        real_val+=float(level_amount)*float(taxes.taxpercentage)/100
    # level_amount=convert_to_int(counter.invoice_base_amount)
    # tax=float(level_amount)*float(tax)/100
    return "{:,.2f}".format(real_val+float(level_amount))

@register.simple_tag
def get_split_percentage(amount,percentage,exchange_rate):
    exchange_rate = 1 if (exchange_rate == 'N/A' or exchange_rate.strip() == '') else float(exchange_rate)
    amount=round_of_two_values((convert_to_int(amount)*convert_to_int(percentage))/100)
    # round_amount =round(amount, 2)
    final_val=float(amount)*float(exchange_rate)
    return new_round_of_two_values(final_val)

@register.simple_tag
def get_total_val(counter,total_amount):
    # level_amount=convert_to_int(counter.invoice_base_amount)
    get_percentage=convert_to_int(total_amount)*counter.invoice_payment/100
    # real_val=0
    # for taxes in tax:
    #     real_val+=float(level_amount)*float(taxes.taxpercentage)/100
    # level_amount=convert_to_int(counter.invoice_base_amount)
    # tax=float(level_amount)*float(tax)/100
    return "{:,.2f}".format(get_percentage)

@register.simple_tag
def get_final_value(tax,base_amount):
    level_amount=convert_to_int(base_amount)
    real_val=level_amount-float(tax)
    # level_amount=convert_to_int(counter.invoice_base_amount)
    # tax=float(level_amount)*float(tax)/100
    return "{:,.2f}".format(real_val)

@register.simple_tag
def get_invoice_split_id(id,company_id):
    data=InvoiceCostInvoice.objects.filter(vendor_invoice_id=id).first()
    return data

@register.filter
def get_past_exchange_rate(invoicecost):
    return PastExchangeRate.objects.filter(invoice_id=invoicecost,status=True)

@register.simple_tag
def get_user(user_id):

    return User.objects.get(id=user_id)

@register.simple_tag
def get_process_modules(level):
    # if check_for_dispute >0 :
    #     return ProjectFlowModules.objects.getallactiveflow_level(level.id).exclude(module__module_id=2)
    # else:
        return ProjectFlowModules.objects.getallactiveflow_level(level.id)


@register.simple_tag
def get_approved_users(invoice_id,level_id,module_id ,module=None ,paycount=None):
    if module <=3 :
        get_data=Invoiceflowmodules.objects.getinvoiceflowmodules_invoice(invoice_id,level_id,module_id).first()
    elif paycount !=None:
        get_data=Invoiceflowmodules.objects.getinvoiceflowmodules_invoice(invoice_id,level_id,module_id).filter(payment_instruct__payment_count=paycount).last()
    else :
        get_data=Invoiceflowmodules.objects.getinvoiceflowmodules_invoice(invoice_id,level_id,module_id).filter(payment_instruct__payment_count=1).last()
    
    if (get_data):
        if module == 5:
            flowuser_id=find_aproval_users(invoice_id ,paycount )
            # get_invoice_app_users=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=get_data.id).exclude(user_status=0)
            get_invoice_app_users=Invoiceflowmodulesusers.objects.filter(id__in=flowuser_id)
        else :
            get_invoice_app_users=Invoiceflowmodulesusers.objects.get_approved_users(get_data.id)
        app_value=True
        if (get_invoice_app_users.count() == 0):
            get_invoice_app_users=Invoiceflowmodulesusers.objects.get_invflow_users(get_data.id)
            app_value=False
    else:
        get_invoice_app_users=[]
        app_value=False
    return get_data,get_invoice_app_users,app_value

@register.simple_tag
def find_aproval_users(pk,paycount):
    invoiceflow_id=[]
    if paycount !=None:
        get_data=Invoiceflowmodules.objects.filter(invoice=pk , status =1 ,module_id=5, payment_instruct__payment_count=paycount)
    else :
        get_data=Invoiceflowmodules.objects.filter(invoice=pk , status =1,module_id=5 ,payment_instruct__payment_count=1)
    for module in get_data:
        get_invoice_app_users=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=module.id,status =1).first()
        if get_invoice_app_users :
            invoiceflow_id.append(get_invoice_app_users.id)

    return invoiceflow_id

@register.simple_tag
def get_completed_approved_users(invoice_id,invflow_module_id , module_id, payment_count):
    if module_id == 5 :
        flowuser_id=find_aproval_users(invoice_id ,payment_count )
        get_invoice_app_users=Invoiceflowmodulesusers.objects.filter(id__in=flowuser_id)
    else :
        get_invoice_app_users=Invoiceflowmodulesusers.objects.get_approved_users(invflow_module_id)
    return get_invoice_app_users

@register.simple_tag
def get_approved_bank_user(pk):
    get_data=Invoiceflowmodules.objects.get_by_module_id(pk,1,None)
    users=[]
    if (get_data):
        users=Invoiceflowmodulesusers.objects.get_approved_users(get_data.id)
    return users
@register.simple_tag
def get_flow_users(level_id,module_id):
    return ProjectFlowModuleUsers.objects.getflowusers_active(module_id,level_id)

@register.simple_tag
def check_get_invoicecost(pk,module):
    get_data=list(Invoiceflowmodules.objects.filter_by_module_id(pk,1,None).values_list('id',flat=True))
    if (get_data):
        # check_project=Projectcreation.objects.get(id=get_data.project_id)
        # if check_project.invoice_bank_user == 1:
            # if (get_data):
        
        users=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=get_data).exclude(status=0).distinct()
        return 1,users
            # else:
            #     return 1,None
    else:
        return 0,None
    
@register.simple_tag
def withoutbankuserapproval(pk,module):
    get_data=list(Invoiceflowmodules.objects.filter_by_module_id(pk,1,module).values_list('id',flat=True))
    if (get_data):
        users=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id__in=get_data).exclude(status=0).distinct()

        get_module_data=Invoiceflowmodules.objects.filter_by_module_id(pk,1,module)
        for data in get_module_data :
            Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=data).update(payment_instruction=data.payment_instruct)
        return 1,users
    else:
        return 0,None
    
@register.simple_tag
def check_invoice_receiptfile_upload(invcost_id):
    return PaymentReceipt.objects.get_by_invcost(invcost_id).count()

@register.simple_tag
def check_invoice_receiptfile_upload_by_payment_id(payment_instruct_id):
    return PaymentReceipt.objects.get_by_payment(payment_instruct_id).count()

@register.simple_tag
def get_payment_receipt_data(inv_id,user_id , paycount):
    invoiceuser=PaymentReceipt.objects.filter_by_inv_user(inv_id,user_id).filter(payment_instruct__payment_count = paycount)
    return invoiceuser

@register.simple_tag
def getinvoicestatus(status,invoiceid):
    count=0
    if InvoiceCostInvoice.objects.filter(invoice_id=invoiceid,status=1,payment_status=status):
        count=1 
    return count

@register.simple_tag
def getcountry(invoiceid):
    country=Projectcreation.objects.filter(id__in=Invoice.objects.filter(id=invoiceid).values_list('project_id', flat=True)).first()
    if country:
        return country.country.name

@register.simple_tag
def invoicegrossamount(costinvoiceid):
    costinvoice = InvoiceCostInvoice.objects.filter(id=costinvoiceid).first()
    totaldiscount = InvoiceCostInformation.objects.filter(invoice_id=costinvoice.invoice_id).first()
    exchange_value=costinvoice.invoice_exchange_rate
    percentage=costinvoice.invoice_percentage
    discount_value=totaldiscount.total_discount_value
    if (exchange_value =="N/A" or exchange_value ==""):
        remove_curencysymbol=discount_value.split(" ")
        replace_comma=float(remove_curencysymbol[1].replace(",",""))
        final_value=replace_comma*float(percentage)/100
        return "{:,.2f}".format(final_value)
    else:
        if (exchange_value == ""):
            exchange_value_rate=0
        else:
            exchange_value_rate=exchange_value
        remove_curencysymbol=discount_value.split(" ")
        replace_comma=float(remove_curencysymbol[1].replace(",",""))
        final_value=replace_comma*float(percentage)/100*float(exchange_value_rate)
        return "{:,.2f}".format(final_value)


@register.simple_tag
def invoicetaxamount(costinvoiceid):  
    costinvoice = InvoiceCostInvoice.objects.filter(id=costinvoiceid).first()
    totaldiscount = InvoiceCostInformation.objects.filter(invoice_id=costinvoice.invoice_id).first()
    exchange_value=costinvoice.invoice_exchange_rate
    percentage=costinvoice.invoice_percentage
    excluive_value=totaldiscount.total_exclusive_value
    if (excluive_value == None):
        excluive_value=0
        if (exchange_value =="N/A" or exchange_value ==""):
            final_value=excluive_value*float(percentage)/100
            return "{:,.2f}".format(final_value)
        else:
            final_value=excluive_value*float(percentage)/100*float(exchange_value)
            return "{:,.2f}".format(final_value)
    else:
        if (exchange_value =="N/A" or exchange_value ==""):
            remove_curencysymbol=excluive_value.split(" ")
            replace_comma=float(remove_curencysymbol[1].replace(",",""))
            final_value=replace_comma*float(percentage)/100
            return "{:,.2f}".format(final_value)
        else:
            if (exchange_value == ""):
                exchange_value_rate=0
            else:
                exchange_value_rate=exchange_value
            remove_curencysymbol=excluive_value.split(" ")
            replace_comma=float(remove_curencysymbol[1].replace(",",""))
            final_value=replace_comma*float(percentage)/100*float(exchange_value_rate)
            return "{:,.2f}".format(final_value)
   

   
@register.simple_tag
def getdiscipline(invoiceid):
    discipline_subtypes = DisciplineSubtype.objects.filter(
    id__in=ProjectDevelopmentSubType.objects.filter(
        id__in=ContractMaster.objects.filter(
            id__in=Invoice.objects.filter(id=invoiceid).values('contractid')
        ).values('projectdisciplinetype__id')
    ).values('discipline_subtype')
).first()

    return discipline_subtypes.discipline_subtype

@register.filter(name='to_int')
def to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0
    
@register.simple_tag
def getprojectdiscipline(invoiceid):
   contractid=Invoice.objects.filter(id=invoiceid,status=1).values_list('contractid',flat=True).first()
   projectdevelopmentsubtypeid=ContractMaster.objects.filter(id=contractid,status=1).values_list('projectdisciplinetype_id',flat=True).first()
   developmentsubtypeid=ProjectDevelopmentSubType.objects.filter(id=projectdevelopmentsubtypeid).values_list('discipline_subtype_id',flat=True).first()
   discipline=DisciplineSubtype.objects.filter(id=developmentsubtypeid).values_list('discipline_subtype',flat=True).values_list('discipline_subtype',flat=True).first()
   return discipline
    
@register.simple_tag
def gettotalgrossamount(allinvoice):
   
    sumgrossamount=0
    for i in allinvoice:
        costinvoice = InvoiceCostInvoice.objects.filter(id=i.id)
        for j in costinvoice:
            totaldiscount = InvoiceCostInformation.objects.filter(invoice_id=j.invoice_id).first()
            exchange_value=j.invoice_exchange_rate
            percentage=j.invoice_percentage
            discount_value=totaldiscount.total_discount_value
            if (exchange_value =="N/A" or exchange_value ==""):
                remove_curencysymbol=discount_value.split(" ")
                replace_comma=float(remove_curencysymbol[1].replace(",",""))
                final_value=replace_comma*float(percentage)/100
                sumgrossamount += int(final_value)
                
                
            else:
                if (exchange_value == ""):
                    exchange_value_rate=0
                else:
                    exchange_value_rate=exchange_value
                remove_curencysymbol=discount_value.split(" ")
                replace_comma=float(remove_curencysymbol[1].replace(",",""))
                final_value=replace_comma*float(percentage)/100*float(exchange_value_rate)
                sumgrossamount += int(final_value)
      
    return "{:,.2f}".format(sumgrossamount)

@register.simple_tag
def gettotalgrossamountint(allinvoice):
   
    sumgrossamount=0
    for i in allinvoice:
        costinvoice = InvoiceCostInvoice.objects.filter(id=i.id)
        for j in costinvoice:
            totaldiscount = InvoiceCostInformation.objects.filter(invoice_id=j.invoice_id).first()
            exchange_value=j.invoice_exchange_rate
            percentage=j.invoice_percentage
            discount_value=totaldiscount.total_discount_value
            if (exchange_value =="N/A" or exchange_value ==""):
                remove_curencysymbol=discount_value.split(" ")
                replace_comma=float(remove_curencysymbol[1].replace(",",""))
                final_value=replace_comma*float(percentage)/100
                sumgrossamount += int(final_value)
                
                
            else:
                if (exchange_value == ""):
                    exchange_value_rate=0
                else:
                    exchange_value_rate=exchange_value
                remove_curencysymbol=discount_value.split(" ")
                replace_comma=float(remove_curencysymbol[1].replace(",",""))
                final_value=replace_comma*float(percentage)/100*float(exchange_value_rate)
                sumgrossamount += int(final_value)
      
    return sumgrossamount

@register.simple_tag
def gettotaltaxamount(allinvoice):  
    totaltaxamount=0
    for i in allinvoice:
        costinvoice = InvoiceCostInvoice.objects.filter(id=i.id)
        for j in costinvoice:
            totaldiscount = InvoiceCostInformation.objects.filter(invoice_id=j.invoice_id).first()
            exchange_value=j.invoice_exchange_rate
            percentage=j.invoice_percentage
            excluive_value=totaldiscount.total_exclusive_value
            if (excluive_value == None):
                excluive_value=0
                if (exchange_value =="N/A" or exchange_value ==""):
                    final_value=excluive_value*float(percentage)/100
                    totaltaxamount += final_value
                    
                else:
                    final_value=excluive_value*float(percentage)/100*float(exchange_value)
                    totaltaxamount += final_value
            else:
                if (exchange_value =="N/A" or exchange_value ==""):
                    remove_curencysymbol=excluive_value.split(" ")
                    replace_comma=float(remove_curencysymbol[1].replace(",",""))
                    final_value=replace_comma*float(percentage)/100
                    totaltaxamount += final_value
                
                else:
                    if (exchange_value == ""):
                        exchange_value_rate=0
                    else:
                        exchange_value_rate=exchange_value
                    remove_curencysymbol=excluive_value.split(" ")
                    replace_comma=float(remove_curencysymbol[1].replace(",",""))
                    final_value=replace_comma*float(percentage)/100*float(exchange_value_rate)
                    totaltaxamount += final_value
              
    return "{:,.2f}".format(totaltaxamount)

@register.simple_tag
def addvaluesamount(disval,excval):
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=excval.replace(",","")
    final_value=float(remove_discount_comma)+float(remove_exclusive_comma)
    return final_value

@register.filter
def addvaluesamount(disval,excval):
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=excval.replace(",","")
    final_value=float(remove_discount_comma)+float(remove_exclusive_comma)
    return final_value

@register.filter
def multiple_two_values(disval,excval):
    remove_discount_comma=str(disval).replace(",","")
    remove_exclusive_comma=excval.replace(",","")
    final_value=float(remove_discount_comma) * float(remove_exclusive_comma)
    return new_round_of_two_values(final_value)

@register.simple_tag
def getpaidamount(i,invoicecurrencylist):
    paidlist=0
    unpaidlist=0
   
    for j in invoicecurrencylist:
            invoices = Invoice.objects.filter(project_id=i,id=j.invoice_id).first()
            if invoices:
                #paidinvoice
                paidinvoice=InvoiceCostInvoice.objects.filter(id=j.id,invoice_id=invoices.id,status=1,payment_status=2).first()
                #unpaidinvoice
                unpaidinvoice=InvoiceCostInvoice.objects.filter(id=j.id,invoice_id=invoices.id,status=1,payment_status=1).first()
                           
                if paidinvoice:
                    netamount=addvaluesamount(invoicegrossamount(paidinvoice.id),invoicetaxamount(paidinvoice.id))
                    paidlist= paidlist+int(netamount)
                  
                if unpaidinvoice:
                    netamount=addvaluesamount(invoicegrossamount(unpaidinvoice.id),invoicetaxamount(unpaidinvoice.id))
                    unpaidlist=unpaidlist+int(netamount)
    return paidlist,unpaidlist

@register.simple_tag
def getprojectname(i):
    return Projectcreation.objects.filter(id=i).first()

@register.simple_tag
def getprojectname_only(i):
    return Projectcreation.objects.filter(id=i).values_list('projectname__name',flat=True).first()

@register.simple_tag
def getinvoicecount(invoicecurrencylist,months_data):
    invoicelist=[]
    for start, end, month,year in months_data:
        count=0
        fromdate=start.strftime('%Y-%m-%d')
        todate=end.strftime('%Y-%m-%d')
        for j in invoicecurrencylist:
            filter_date = InvoiceCostInvoice.objects.filter(id=j.id,status=1,invoice_submission_date__range=(fromdate,todate)).first()
            if filter_date:
                count+=1
                # print('filter_date--',month,year,filter_date)
            # print(f"Month: {month}, Start Date: {start.strftime('%Y-%m-%d')}, End Date: {end.strftime('%Y-%m-%d')}")
        invoicelist.append((month,year,count))
    # for month,year,count in invoicelist:
    #    print('date--',month,year)
    #    print('count--',count)
    return invoicelist

def exceptional_data(company):
    data=[ {"value":"1", "name":"Supporting Document Missing"},
        {"value":"2", "name":"Relevant Contract not selected for invoice"},
        {"value":"3", "name":"Work Completion Certificate uploaded or Timesheet mismatch with Invoice billing details"},
        {"value":"4", "name":"Material Delivery Ticket or Certificate Mismatch with Invoice Billing details"},
        {"value":"5", "name":"Mismatch between price quoted on invoice and selected contract"},
        {"value":"6", "name":"Disputed Invoices"},
        {"value":"7", "name":"Other Reasons"},]
    return data

@register.simple_tag
def sumoftwono(val1,val2):
    return "{:,.2f}".format((val1+val2))

@register.simple_tag
def getagingperiod(id,contractid,companyid):
    currentdatetime = timezone.now()
    invoicesubmitted_date=InvoiceCostInvoice.objects.filter(invoice_id=id,status=1).values_list('invoice_submission_date',flat=True).first()
    paymentday=VendorPaymentTerms.objects.filter(contract_id=contractid,company=companyid).values_list('payment_day',flat=True).first()
    if invoicesubmitted_date == None :
        invoicesubmitted_date = 0
    if paymentday == None :
        paymentday=0
    time_difference = currentdatetime - invoicesubmitted_date
    days_difference = (int(time_difference.days)-int(paymentday))
    if days_difference <= 0:
        days_difference=0
    return days_difference
       
@register.simple_tag
def getdaysforpayment(id,contractid,companyid):
    try:
        currentdatetime=InvoiceCostInvoice.objects.filter(invoice_id=id,status=1).values_list('payment_date',flat=True).first()
        invoicesubmitted_date=InvoiceCostInvoice.objects.filter(invoice_id=id,status=1).values_list('invoice_submission_date',flat=True).first()
        time_difference = currentdatetime - invoicesubmitted_date
        days_difference = abs((int(time_difference.days)))
        return days_difference
    except :
        return 0

@register.simple_tag
def getdaysforunpaid(id,contractid,companyid):
    currentdatetime = timezone.now()
    invoicesubmitted_date=InvoiceCostInvoice.objects.filter(invoice_id=id,status=1).values_list('invoice_submission_date',flat=True).first()
    time_difference = currentdatetime - invoicesubmitted_date
    days_difference = abs((int(time_difference.days)))
    return days_difference

@register.simple_tag
def getduedate(id,contractid,companyid):
    invoicesubmitted_date=InvoiceCostInvoice.objects.filter(invoice_id=id,status=1).values_list('invoice_submission_date',flat=True).first()
    paymentday=VendorPaymentTerms.objects.filter(contract_id=contractid,company=companyid).values_list('payment_day',flat=True).first()
    original_date = datetime.strptime(str(invoicesubmitted_date), "%Y-%m-%d %H:%M:%S%z")
    if invoicesubmitted_date == None :
        invoicesubmitted_date = 0
    if paymentday == None :
        paymentday=0
    new_date = original_date + timedelta(days=int(paymentday))
    new_date_str = new_date.isoformat()
    original_date = datetime.fromisoformat(new_date_str.replace("Z", "+00:00"))
    return original_date.strftime("%d-%b-%Y")

@register.simple_tag
def commoseperator(amount):
    return "{:,.2f}".format(amount)

@register.filter
def commoseperator(amount):
    return "{:,.2f}".format(amount)

@register.filter
def rankinglisttotalamount(rankinglist):
    totalamount=0
    for i,amount in rankinglist:
        totalamount+=amount
    return "{:,.2f}".format(totalamount)
    
@register.simple_tag
def getamountpercentage(totalamountinvoice,rankinglist):
    totalamount=0
    for i,amount in rankinglist:
        totalamount+=amount
    percentage=(totalamountinvoice/totalamount)*100
    return percentage

@register.simple_tag
def statusvalue(project,approvalststatus,invoicelist):
    if approvalststatus == 'Disputed':
        approval=6
        invoicestatus=6
    elif approvalststatus == 'Awaiting Approval':
        approval=1
        invoicestatus=2
    elif approvalststatus == 'Not Yet Submitted':
        approval=1
        invoicestatus=1
    elif approvalststatus == 'Returned':
        approval=4
        invoicestatus=4
    elif approvalststatus == 'Rejected':
        approval=5
        invoicestatus=5
    else:
        approval=3
        invoicestatus=3
    finalval=0.00
    for i in invoicelist:
        invoice_cost_invoices = InvoiceCostInvoice.objects.filter(id=i,status=1,approval_status=approval).first()
        if invoice_cost_invoices:
            invoice_list=Invoice.objects.filter(id=invoice_cost_invoices.invoice_id,invoice_status=invoicestatus,project_id=project)
            if invoice_list:
                final_invoice_cost=InvoiceCostInvoice.objects.filter(id=invoice_cost_invoices.id).first()
                invdisval = invoicegrossamount(final_invoice_cost.id) 
                invdistax= invoicetaxamount(final_invoice_cost.id)
                finalval+=addvaluesamount(invdisval,invdistax)
    return "{:,.2f}".format(finalval)

@register.simple_tag
def grandtotal(project,approvalststatus,invoicelist):
    if approvalststatus == 'Disputed':
        approval=6
        invoicestatus=6
    elif approvalststatus == 'Awaiting Approval':
        approval=1
        invoicestatus=2
    elif approvalststatus == 'Not Yet Submitted':
        approval=1
        invoicestatus=1
    elif approvalststatus == 'Returned':
        approval=4
        invoicestatus=4
    elif approvalststatus == 'Rejected':
        approval=5
        invoicestatus=5
    else:
        approval=3
        invoicestatus=3
    finalval=0.00
    for k in project:
        for i in invoicelist:
            invoice_cost_invoices = InvoiceCostInvoice.objects.filter(id=i,status=1,approval_status=approval).first()
            if invoice_cost_invoices:
                invoice_list=Invoice.objects.filter(id=invoice_cost_invoices.invoice_id,invoice_status=invoicestatus,project_id=k)
                if invoice_list:
                    final_invoice_cost=InvoiceCostInvoice.objects.filter(id=invoice_cost_invoices.id).first()
                    invdisval = invoicegrossamount(final_invoice_cost.id) 
                    invdistax= invoicetaxamount(final_invoice_cost.id)
                    finalval+=addvaluesamount(invdisval,invdistax)
    return "{:,.2f}".format(finalval)

@register.simple_tag
def grandtotalapprovalstatus(project,approvalststatus,invoicelist):
    grandtotal=0.00
    for k in approvalststatus:
        
        if approvalststatus == 'Disputed':
            approval=0
            invoicestatus=1
        elif approvalststatus == 'Awaiting Approval':
            approval=1
            invoicestatus=2
        elif approvalststatus == 'Not Yet Submitted':
            approval=1
            invoicestatus=1
        elif approvalststatus == 'Returned':
            approval=4
            invoicestatus=4
        elif approvalststatus == 'Rejected':
            approval=5
            invoicestatus=5
        else:
            approval=3
            invoicestatus=3
        finalval=0.00
        
        for k in project:
            for i in invoicelist:
                invoice_cost_invoices = InvoiceCostInvoice.objects.filter(id=i,status=1,approval_status=approval).first()
                if invoice_cost_invoices:
                    invoice_list=Invoice.objects.filter(id=invoice_cost_invoices.invoice_id,invoice_status=invoicestatus,project_id=k)
                    if invoice_list:
                        final_invoice_cost=InvoiceCostInvoice.objects.filter(id=invoice_cost_invoices.id).first()
                        invdisval = invoicegrossamount(final_invoice_cost.id) 
                        invdistax= invoicetaxamount(final_invoice_cost.id)
                        finalval+=addvaluesamount(invdisval,invdistax)
       
                grandtotal+=finalval
    return "{:,.2f}".format(grandtotal)

@register.simple_tag
def getamountpercentage(totalamountinvoice,rankinglist):
    totalamount=0
    for i,amount in rankinglist:
        totalamount+=amount
    if totalamount != 0:
        percentage=(totalamountinvoice/totalamount)*100
        return percentage
    else:
        return 0.00

@register.simple_tag
def grandtotalproject(project,approvalststatus,invoicelist):
    grandtotal=0.00
  
    for k in approvalststatus:
        finalval=0.00
        if k == 'Disputed':
            approval=6
            invoicestatus=6
        elif k == 'Awaiting Approval':
            approval=1
            invoicestatus=2
        elif k == 'Not Yet Submitted':
            approval=1
            invoicestatus=1
        elif k == 'Returned':
            approval=4
            invoicestatus=4
        elif k == 'Rejected':
            approval=5
            invoicestatus=5
        else:
            approval=3
            invoicestatus=3
      
        for i in invoicelist:
            invoice_cost_invoices = InvoiceCostInvoice.objects.filter(id=i,status=1,approval_status=approval).first()
            if invoice_cost_invoices:
                invoice_list=Invoice.objects.filter(id=invoice_cost_invoices.invoice_id,invoice_status=invoicestatus,project_id=project)
                if invoice_list:
                    final_invoice_cost=InvoiceCostInvoice.objects.filter(id=invoice_cost_invoices.id).first()
                    invdisval = invoicegrossamount(final_invoice_cost.id) 
                    invdistax= invoicetaxamount(final_invoice_cost.id)
                    finalval+=addvaluesamount(invdisval,invdistax)
        grandtotal+=finalval
    return "{:,.2f}".format(grandtotal)

@register.filter
def commoseperatorfilter(amount):
    return "{:,.2f}".format(amount)

@register.simple_tag
def getpartialypaidamount(invoiceid,companyid):
    amount=PaymentInstruction.objects.filter(invoicecost_id=invoiceid,company_id=companyid).first()
    return "{:,.2f}".format(amount.payable_amount),"{:,.2f}".format(amount.pending_amount)

@register.simple_tag
def gettotalparialypaidinvoice(invoicelist,companyid):
    totalpayable=0
    totalpending=0
    for i in invoicelist:
        amount=PaymentInstruction.objects.filter(invoicecost_id=i.id,company_id=companyid).first()
        totalpayable+=amount.payable_amount
        totalpending+=amount.pending_amount
    return "{:,.2f}".format(totalpayable),"{:,.2f}".format(totalpending)

@register.simple_tag
def getexceptions(invoiceid,companyid,approvalstatus,invoicestatus):
    if approvalstatus == 6 and  invoicestatus == 6:
        confirmdispute=1
    else:
        confirmdispute=0
    exceptions_reasons = InvoiceExceptional.objects.filter(invoice_id=invoiceid,status=1,confirm_dispute=confirmdispute)
    return exceptions_reasons

@register.simple_tag
def getcomments(invoiceid,companyid):
    flowmodels=Invoiceflowmodules.objects.filter(invoice_id=invoiceid)
    for i in flowmodels:
        comments=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules_id=i.id)
        # for j in comments:
        #     print('comments---',j.comments)
    return 0
@register.simple_tag
def getobjectinvoice(id):
    return InvoiceCostInvoice.objects.filter(id=id).first()


@register.simple_tag
def get_committee_users(request,dispute_track):
    users=list(User.objects.filter(company_id=request.company,roles_id=3,status=1).values_list('id',flat=True))
    user_right=UserRights.objects.filter(user_id__in=users,module_id=18,create="1")
    get_dispute_user=User.objects.filter(id__in=list(user_right.values_list('user_id',flat=True)),status=1,roles_id=3)
    return get_dispute_user

@register.simple_tag
def get_single_user(invoice_id,request):
    single_user=DisputedInvoiceTrack.objects.filter(invoice_id=invoice_id,stage=1,status=True).first()
    return  single_user

@register.simple_tag
def query_closed_user(stage,invoice,credit):
    # print(f'pk {invoice}, stage {stage}, credit {credit}')
    if invoice:
        current_user=DisputedInvoiceTrack.objects.filter(stage=stage,invoice_id=invoice,status=True).last()
        return current_user
    elif credit:
        current_user=DisputedInvoiceTrack.objects.filter(stage=stage,credit_id=credit,status=True).last()
        # print(f'current_user {current_user}')
        return current_user
    else:
        return

@register.simple_tag
def dispute_internal_discussion(invoice,request):
    returned_user=False
    first_possiblity=AddNewDisputedQuery.objects.filter(query_id=invoice.id).first()
    second_possiblity=BackToDisputeQuery.objects.filter(query_id=invoice.id).first()
    # print(f'second_possiblity {second_possiblity}')
    if first_possiblity:
        if first_possiblity.user_id==request.user.id:
            returned_user=True
    if second_possiblity:
        # print(f'dispute_internal_discussion')
        if second_possiblity.user_id==request.user.id:
            returned_user=True
    # print(f'possiblities {returned_user}')
    return returned_user

@register.simple_tag
def check_approvaluser(request,invoice):
    returned_user=False
    back_to_dispute=BackToDisputeQuery.objects.filter(query_id=invoice).first()
    if back_to_dispute:
        if back_to_dispute.user.id==request.user.id:
            returned_user=True
    # print(f'returned_user {returned_user}')
    return returned_user

@register.simple_tag
def get_returned_invoice_count(invoice,credit):
    if invoice:
        return BackToDisputeQuery.objects.filter(query_id=invoice).count()
    elif credit:
        return BackToDisputeQuery.objects.filter(credit_id=credit).count()
    else:
        return 0

@register.simple_tag
def get_approved_percentage(disputed_percentage):
    get_approved_percentage=int(100 - float(disputed_percentage))
    return get_approved_percentage

@register.simple_tag
def get_approved_total(percentage,inv_amount):
    tax=convert_to_int(inv_amount)*float(percentage)/100
    # print(f'inv_amount {type(tax)},type= {type(inv_amount)}')
    return '{:,.2f}'.format(tax)

@register.simple_tag
def get_final_invoice_amount(tax,invoice_amount):
    tax=convert_to_int(tax)+convert_to_int(invoice_amount)
    return '{:,.2f}'.format(tax)

@register.filter
def amountallocated(id):
    payment_account=PaymentAccount.objects.filter(id=id).first()
    if payment_account.remaining_amount:
        final_amount=payment_account.amount-payment_account.remaining_amount
    else:
        final_amount=0
    return '{:,.2f}'.format(final_amount)

@register.simple_tag
def get_creditnote_contract_invoice(credit_id):
    credit_note_invoices=CreditNoteContractInvoice.objects.getcreditnoteinvoice_by_creditnoteid(credit_id)
    return credit_note_invoices

@register.simple_tag
def applied_credit_value(credit_split,credit,invoice_id):
    applied_creditnote=CreditNoteMappingBase.objects.filter(invoice_split_id=credit_split.vendor_split_invoice_id,invoice_id=invoice_id,credit_note_id=credit,credit_note_split_id=credit_split.id)
    credit_value=0
    exclusive_tax_values=0
    if applied_creditnote.count() > 0:
        netpayable_amount=applied_creditnote.last().credit_payable
        percentage=applied_creditnote.last().credit_note_split.percentage
        exclusive_tax=applied_creditnote.last().credit_note_split.credit.exclusive_value
        exchange_rate=applied_creditnote.last().credit_note_split.exchange_rate
        creditenote_id=applied_creditnote.last().credit_note.id
        creditenote_grossamount=applied_creditnote.last().credit_note.total_value
        if exchange_rate == 'N/A':
            exchange_rate=1
         
        ex_calc=creaditenote_gross_amount(creditenote_grossamount, percentage , exchange_rate)
        credite_exclusive_percentage=CreditNoteExclusive.objects.filter(credit_id=creditenote_id).values_list('exclusive_percentage', flat=True)
        for exc in list(credite_exclusive_percentage):
            exc_value=round_of_two_values(float(ex_calc)*float(exc)/100)
            exclusive_tax_values += float(exc_value)
            print(exc_value)
    # split_exclusive=round_of_two_values((float(exclusive_tax)*float(percentage))/100)
    # exchange_exclusive=round_of_two_values(float(split_exclusive)*float(exchange_rate))
    credit_value=(float(netpayable_amount)+float(exclusive_tax_values)) 
    # print(f'credit_split {credit_split},credit {credit},invoice_id {invoice_id},applied_creditnote {applied_creditnote}')
    return new_round_of_two_values(float(credit_value))

@register.filter
def convert_to_thousand_separator(numeric):
    if numeric:
        remove_comma=str(numeric).replace(',', '')
        sepator_val=float(remove_comma)
        return '{:,.2f}'.format(float(sepator_val))
    return 

    
@register.filter
def converttothousandseparator(numeric):
    if numeric:
        new_value=str(numeric)
        remove_comma=new_value.replace(',', '')
        sepator_val=float(remove_comma)
        return '{:,.2f}'.format(float(sepator_val))
    return


@register.simple_tag
def getpaymentaccount_count(id):
    account_count=PaymentAccount_PaidInvoice.objects.filter(payment_id=id,status=1).count()
    return account_count

@register.simple_tag
def getaccount_action(id):
    account_count=PaymentAccount_PaidInvoice.objects.filter(payment_id=id,status=1).count()
    if account_count == 0:
        return 0
    else:
        remaningamount=PaymentAccount.objects.filter(id=id,remaining_amount__gt=0).count()
        if remaningamount > 0:
            return 0
       
@register.filter
def amount_convertion(amount):
    if amount.strip() != '':
        base_amount=convert_to_int(amount)
        decimal_amount=Decimal(str(base_amount))
        return '{:,.2f}'.format(decimal_amount) 
    else:
        return '0'

@register.filter
def newamount_convertion(amount):
    if amount.strip() != '':
        base_amount=convert_to_int(amount)
        decimal_amount=Decimal(str(base_amount))
        return new_round_of_two_values(decimal_amount)
    else:
        return '0'

@register.filter
def amount_convertion_to_separtors(amount):
    if amount.strip() != '':
        base_amount=convert_to_int(amount)
        return new_round_of_two_values(base_amount)
    else:
        return '0'

@register.filter
def getpaymentaccountid(id):
    id = PaymentAccount_PaidInvoice.objects.filter(invoice=id,status=1).first()
    if id:
        return id
   
@register.filter
def getpaymentaccountdraft(invoiceid,id):
    # print('id----------',id)
    draft_list = PaymentAccount.objects.filter(id=id).first()
    return draft_list

@register.simple_tag
def get_exclusive_value(exclusive_tax,exchange_rate,invoice_percentage):
    invoice_percentage_float = float(invoice_percentage)
    split_value=exclusive_tax.split(" ")
    remove_comma=split_value[1].replace(',', '')
    exclusive=(float(remove_comma)*(invoice_percentage_float))/100
    # rounded_value = round(exclusive, 2)
    exchange_rate=exchange_rate
    if exchange_rate == 'N/A' or exchange_rate.strip() == '':
        exchange_rate=1
    final_exclusive=exclusive*float(exchange_rate)
    return new_round_of_two_values(final_exclusive) 

@register.simple_tag
def new_exclusive_value(grossamount,exclusive_percentage):
    grossamountvalue = replacecommaid(grossamount)
    exclusive_value=float(exclusive_percentage)
    final_exclusive=(float(grossamountvalue)*float(exclusive_value))/100
    print('final_exclusive ',final_exclusive)
    return new_round_of_two_values(final_exclusive)




@register.simple_tag
def get_inclusive_with_exclusive(inclusives,tax,invoice):
    type_of_tax=0
    
    for inclu in inclusives:
        inclusivee=inclu.taxpercentage
        type_of_tax+=convert_to_int(get_tax_by_type(tax,inclusivee))
    print(f'type_of_tax {round_of_two_values(type_of_tax)}')
        # {%  get_split_percentage invoice_cost.total_after_otherdetails split.invoice_payment split.invoice_exchange_rate as final_val %}
    #     {%  get_tax_by_type final_val tax.taxpercentage as mid_val %}
    # print(f'inclusives {inclusives}')
    counter=1
    # print(f'tax {tax}, counter {counter}')
    # # level_amount=convert_to_int(counter)
    # tax=float(convert_to_int(tax))*float(convert_to_int(counter))/100
    # return "{:,}".format(tax)
    return new_round_of_two_values(type_of_tax)

@register.simple_tag
def delvalues(disval, excval, addition=None):
    remove_discount_comma = str(disval).replace(",", "")
    remove_exclusive_comma = str(excval).replace(",", "")
    remove_addition_comma = str(addition).replace(",", "") if addition else "0"
    try:
        final_value = float(remove_discount_comma) - float(remove_exclusive_comma) + float(remove_addition_comma)
        return new_round_of_two_values(final_value)
    except ValueError:
        return "0.00"
    
@register.simple_tag
def newdelvalues(disval, excval, addition=None):
    remove_discount_comma = str(disval).replace(",", "")
    remove_exclusive_comma = str(excval).replace(",", "")
    remove_addition_comma = str(addition).replace(",", "") if addition else "0"
    try:
        final_value = float(remove_discount_comma) - float(remove_exclusive_comma) + float(remove_addition_comma)
        return new_round_of_two_values(final_value)
    except ValueError:
        return "0.00"

@register.filter(name='get_decimal_total')
def get_decimal_total(total_val):
    try:
        numeric_string = ''.join(char for char in total_val if char.isdigit() or char == '.')
        final_value=float(numeric_string)
        return "{:,}".format(final_value)
    except:
        return ''

@register.simple_tag
def get_base_amount(exchange_rate,total_val):
    exchange_rate=exchange_rate
    if exchange_rate.strip() == '' or exchange_rate =='N/A':
        exchange_rate=1
    remove_total_comma=total_val.replace(",","")
    
    
    print('remove_total_comma',remove_total_comma)
    print('exchange_rate' , exchange_rate)
    if (remove_total_comma == '0' or remove_total_comma == '0.00') and (exchange_rate == '0' or exchange_rate =='0.00'):
        final_value=0
    else:    
        final_value=float(remove_total_comma)/float(exchange_rate)
    print(f'get_base_amount {exchange_rate},total_val {total_val}')
    return new_round_of_two_values(final_value)

@register.filter
def get_exclusive_percentage(exclusives):
    print(f'exclusives {exclusives}')
    get_tax=VendorCompanyTaxPercentage.objects.filter(vendortax_id=exclusives.exclusive_id,status=1,vendortax__status=1).last()
    print(f'get_tax {get_tax}')
    tax_percent=0
    if get_tax.taxpercentage:
        tax_percent=get_tax.taxpercentage
    return tax_percent

@register.simple_tag
def get_deduction_amount(split,invoice_id):
    print(f'invoice_id {invoice_id},split {split}')
    deduct_amount=OtherDeductions.objects.filter(invoice_id=invoice_id,invoice_split_id=split,status=True).last()
    print(f'deduct_amount {deduct_amount}')
    remove_comma=0
    if deduct_amount:
        if deduct_amount.amount:
            split_value=deduct_amount.amount.split(" ")
            remove_comma=split_value[1].replace(',', '')
            remove_comma=remove_comma.replace(')', '')
            if remove_comma.strip()=='':
                remove_comma=0
            print(f'split_value {split_value},remove_comma {remove_comma}')
    return new_round_of_two_values(float(remove_comma))

@register.simple_tag
def get_additions_amount(split,invoice_id):
    print(f'invoice_id {invoice_id},split {split}')
    deduct_amount=OtherAdditions.objects.filter(invoice_id=invoice_id,invoice_split_id=split,status=True).last()
    print(f'deduct_amount {deduct_amount}')
    remove_comma=0
    if deduct_amount:
        if deduct_amount.amount:
            split_value=deduct_amount.amount.split(" ")
            remove_comma=split_value[1].replace(',', '')
            remove_comma=remove_comma.replace(')', '')
            if remove_comma.strip()=='':
                remove_comma=0
            print(f'split_value {split_value},remove_comma {remove_comma}')
    return new_round_of_two_values(float(remove_comma))

@register.filter
def get_credit_notes(invoice_id):
    get_credit=CreditNoteInvoice.objects.filter(invoice_id=invoice_id,status=1,credit__credit_status=2)
    return get_credit.count()


@register.simple_tag
def checkpermission_creditnoterecipt(credit_id,user_id,module_id):
    if credit_id.contracttype=='original':
        contract_details=ContractMaster.objects.get_by_id(credit_id.contract_id)
    else:
        contract_details = Amendment.objects.get_by_id(credit_id.amendment_id, 1).first()
        if contract_details is not None:
            contract_details = contract_details.service
        else:
        # Handle the case where no contract detail is found for the given contract_id
            print("No contract detail found for contract_id:", credit_id.contract_id)
    if(contract_details):
        try:
            if credit_id.contracttype=='original':
                project_id=contract_details[0].projects_id
            else:
                project_id = contract_details.projects_id
                print(project_id)
        except:
            project_id=None
        invoiceflowmodules=Invoiceflowmodules.objects.getcreditflowmodules_byinvoice(credit_id,module_id)
        if(invoiceflowmodules):
            
            if (module_id == "5"):
                checkuser_data=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_byuser(user_id,project_id,invoiceflowmodules.id)
                print('as',user_id)
                # single user multiple currency
                checkuser_flow=0
                for data in checkuser_data:
                    check_data=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_payapp(invoiceflowmodules.id,data.payment_instruction_id).count()
                    if (check_data == 0):
                        checkuser_flow += 1
            else: 
                checkuser_flow=Invoiceflowmodulesusers.objects.getinvoiceflowmodulesusers_byuser(user_id,project_id,invoiceflowmodules.id).count()
        else:
            checkuser_flow=0
    else:
        checkuser_flow=0
    return checkuser_flow


@register.simple_tag
def check_for_flow(credit_id,user_id,module_id):
    if credit_id.contracttype=='original':
        contract_details=ContractMaster.objects.get_by_id(credit_id.contract_id)
    else:
        contract_details = Amendment.objects.get_by_id(credit_id.amendment_id, 1).first()
        if contract_details is not None:
            contract_details = contract_details.service
        else:
        # Handle the case where no contract detail is found for the given contract_id
            print("No contract detail found for contract_id:", credit_id.contract_id)
    get_invoice=CreditNoteInvoice.objects.filter(credit_id=credit_id).first()
    invoiceflowmodules=0
    if(contract_details):
        invoiceflow=Invoiceflowmodules.objects.getcreditflowmodules_byinvoice(credit_id.id,module_id)
        try:
            if credit_id.contracttype=='original':
                project_id=contract_details[0].projects_id
            else:
                project_id = contract_details.projects_id
                
        except:
            project_id=None
        if get_invoice.invoice_id:
            invoiceflowmodules=Invoiceflowmodules.objects.filter(invoice_id=get_invoice.invoice_id,status=0,module_id=module_id,flowlevel_module_id=invoiceflow.flowlevel_module_id).first()
            if invoiceflowmodules:
                invoiceflowmodules=invoiceflowmodules.status
    return invoiceflowmodules

@register.simple_tag
def remove_session(request,pk):
    request.session['values'] = 0
    return

@register.simple_tag
def get_payment_detail(invoice,invoice_cost): 
    get_len=0
    payment_term=list(PaymentInstruction.objects.filter(invoicecost_id=invoice_cost,invoicecost__invoice_id=invoice,status=True).values_list('bankuser_verification',flat=True))
    if 1 in payment_term:
        get_len=1
    return get_len

@register.simple_tag
def get_payment_percentage(invoice,invoice_cost ,paycount=None): 
    if paycount != None :
        payment_percentage=PaymentInstruction.objects.filter(invoicecost_id=invoice_cost,invoicecost__invoice_id=invoice,status=True, payment_count=paycount).first()
    else :
        payment_percentage=PaymentInstruction.objects.filter(invoicecost_id=invoice_cost,invoicecost__invoice_id=invoice,status=True).first()
    if payment_percentage:
        return payment_percentage.payment_percentage
    return

@register.simple_tag
def get_new_payment_percentage(invoice,invoice_cost ,paycount=None): 
   
    payment_percentage=PaymentInstruction.objects.filter(invoicecost_id=invoice_cost,invoicecost__invoice_id=invoice,status=True ,verified_status = 1,bankuser_verification=1 ,new_payment_status = 2)
    payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_percentage)
    if payment_percentage_sum:
        return payment_percentage_sum
    return 0


@register.simple_tag
def get_confirm_payment_percentage(invoice,invoice_cost ,paycount=None): 
   
    payment_percentage=PaymentInstruction.objects.filter(invoicecost_id=invoice_cost,invoicecost__invoice_id=invoice,status=True ,verified_status = 1,bankuser_verification=1 )
    payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_percentage)
    if payment_percentage_sum:
        return payment_percentage_sum
    return


@register.simple_tag
def get_signed_users(invoice_cost,request,payment_count=None): 
    try:
        if payment_count == None:
            approved_users=list(Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id = invoice_cost.invoice.id ,Invoiceflowmodules__module_id= 5 , status = 1).values('id','invoice_costinvoice','user'))
        else:
            approved_users=list(Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id = invoice_cost.invoice.id ,Invoiceflowmodules__module_id= 5 , status = 1,payment_instruction__payment_count=payment_count).values('id','invoice_costinvoice','user'))
        user_data=''
        for users in approved_users:
            if users['invoice_costinvoice'] != None:
                if str(invoice_cost.id) in users['invoice_costinvoice']:
                    user_data= User.objects.filter(id=users['user']).first()
        return user_data
    except:
        return

@register.filter(name='wccvalues')
def wccvalues(wcc_amount): 
    try:
       original_string = wcc_amount
       modified_string = re.sub(r"[^\d.,]+", "", original_string)
    #    print(modified_string,"MODIFIED STRING")
       return modified_string
    except:
        return
@register.filter(name='currency_convert')
def currency_convert(wcc_amount): 
    try:
       original_string = wcc_amount
       modified_string = re.sub(r"[^\d.,]+", "", original_string)
    #    print(modified_string,"MODIFIED STRING")
       return modified_string
    except:
        return    

@register.simple_tag
def check_for_balance_invoice(invoice_id,request):
    invoiceflow_modules=Invoiceflowmodules.objects.filter_by_module_id(invoice_id,1,6)
    final_list=[]
    if invoiceflow_modules.count() > 0:
        approved_flow_user=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflow_modules).exclude(status=0)
        print(f'approved_flow_user {approved_flow_user}')
        for aprv in approved_flow_user:
            if aprv.projectflow_user.user.user_id == request.user.id:
                verification_count=list(PaymentInstruction.objects.filter(id=aprv.Invoiceflowmodules.payment_instruct_id,status=1,bankuser_verification=0).exclude(verification_code=None).values_list('payment_count',flat=True))
                final_list.extend(verification_count)
    final_list=[i  for i in final_list  if i]
    final_list=list(set(final_list))      
    print(f'final_list {final_list}')         
    return final_list

@register.simple_tag
def get_balance_percentage(invoice_amount , cost_id,paycount):
    payment=track_payment_status(cost_id,paycount)
    if invoice_amount:
        if float(invoice_amount) < 100:
            get_inv=100-float(payment)
            return "{:,.2f}".format(get_inv)
        else:
            return False
    else:
        return False



    


register.filter('exceptional_data',exceptional_data)
register.filter('get_past_exchange_rate',get_past_exchange_rate)
register.filter('addtwovalues',addtwovalues)
register.filter('capitalize_letter',capitalize_letter)
register.filter('replacecommaid',replacecommaid)
register.filter('addvalues',addvalues)
register.filter('addpreviewvalues',addpreviewvalues)
register.filter('new_round_of_two_values',new_round_of_two_values)
register.filter('round_of_two_values',round_of_two_values)
register.filter('minivalues',minivalues)
register.filter('add',add)
register.filter('invoices',invoices)
register.filter('getcontractname',getcontractname)
register.filter('getdiscountvalue',getdiscountvalue)
register.filter('convertinvoicedate',convertinvoicedate)
register.filter('confulldate',confulldate)
register.filter('getinvoicefiles',getinvoicefiles) 
register.filter('getinvoicefileid',getinvoicefileid)
register.filter('getinvoices',getinvoices)
register.filter('checkblockval',checkblockval)
register.filter('checkfieldval',checkfieldval)
register.filter('checkwellval',checkwellval)
register.filter('subinvoice',subinvoice)
register.filter('get_curreny',get_curreny)
register.filter('get_exclusive_percentage',get_exclusive_percentage)



@register.simple_tag
def getinvoice_url(invoice_id, module_name):
    redirectUrl = ''  # Default value

    if module_name == 'Invoice Approval':
        redirectUrl = '/invoice/invoiceapproval/' + str(invoice_id)
    elif module_name == 'Tax Confirmation':
        redirectUrl = '/invoice/exchangerate/' + str(invoice_id)
    elif module_name == 'Payment Instruction Generation':
        redirectUrl = '/invoice/generatepayment/' + str(invoice_id)
    elif module_name == 'Payment Instruction Approval':
        redirectUrl = '/invoice/signatory/' + str(invoice_id)
    elif module_name == 'Payment Confirmation':
        redirectUrl = '/invoice/accountpayable/' + str(invoice_id)
    elif module_name == 'Bank User':
        redirectUrl = '/invoice/bankuserapproval/' + str(invoice_id)
    elif module_name == 'Payment Receipt Upload':
        redirectUrl = '/invoice/vendorbasedinvoice'
    elif module_name == 'Invoice Receipt':
        redirectUrl = '/invoice/checklist/' + str(invoice_id)

    return redirectUrl


@register.filter
def get_split_currency(pk,ids):
    get_invoice_currency=InvoiceCostInvoice.objects.filter(invoice_id=pk,vendor_invoice__currency_id=ids,status=1).first()
    get_curreny_symbol=0
    if get_invoice_currency:
        if get_invoice_currency.invoice_exchange_rate== 'N/A' or get_invoice_currency.invoice_exchange_rate.strip() == '':
            get_curreny_symbol=0
        else:
            get_curreny_symbol=1
    return get_curreny_symbol

@register.simple_tag
def checkreturned_documents(invoice,request):
    returned_user=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id=invoice.id,status=3,user=request.user.id)
    if returned_user.last():
        try:
            module_id=returned_user.last().Invoiceflowmodules.module_id
        except:
            module_id=None
        return module_id

@register.simple_tag
def invoicebaseexclusivevalue(percentage,excluive_value):
    if (excluive_value == None):
        excluive_value=1
        final_value=excluive_value*float(percentage)/100
        return new_round_of_two_values(final_value)
    else:
        remove_curencysymbol=excluive_value.split(" ")
        replace_comma=float(remove_curencysymbol[1].replace(",",""))
        final_value=replace_comma*float(percentage)/100
        return new_round_of_two_values(final_value)
    
@register.simple_tag
def check_query_history(invoice):
    try:
        return AddNewDisputedQuery.objects.filter(query_id=invoice.id,query__dispute_status=1).count()
    except:
        return 0
       
@register.simple_tag
def get_previous_histories(count,invoice):
    return AddNewDisputedQuery.objects.filter(query_id=invoice.id,returned_count=count)


@register.simple_tag
def resolution_team_approval(invoice,request):
    returned_user=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id=invoice.id,status=3)
    if returned_user.last():
        try:
            module_id=returned_user.last().Invoiceflowmodules.module_id
        except:
            module_id=None
        return module_id
        
@register.filter
def check_bank_user(userid):
    try:
        bankuser = CompanyBankUser.objects.filter(user_id=userid).first()
        if bankuser :
            return True
        else :
            return False
    except ObjectDoesNotExist:
        return False
    else:
        return False

@register.filter
def check_bank_user_currency(userid):
    try:
        bankuser = CompanyBankUser.objects.filter(user_id=userid).first()
        return bankuser.companybank.currency.currency_symbol
    except ObjectDoesNotExist:
        return None
    else:
        return False

    
@register.filter
def remove_commas(value):
    if isinstance(value, str):
        return re.sub(r'[^0-9]',"0", value)
    return value


@register.simple_tag
def get_vendor_vin(vendorid):
    try:
        vendor_id = ContractMasterVendor.objects.get(pk=vendorid)
        if vendor_id:
            return vendor_id.vin
        else:
            return ''
    except ObjectDoesNotExist:
        return None

@register.simple_tag
def get_vendor_name(vendorid):
    try:
        vendor_id = ContractMasterVendor.objects.get(pk=vendorid)
        if vendor_id:
            return vendor_id.vendor_name
        else:
            return ''
    except ObjectDoesNotExist:
        return None
    
@register.simple_tag
def check_rolerights(rights_name,role):
    try:
        check_rights=RoleRight.objects.check_module_rights(role.id,rights_name)
        return check_rights 
    except:
        return False

@register.simple_tag
def check_for_settlement(costinvoice):
    invoice_acceptance=SettlementInvoice.objects.filter(invoice_id=costinvoice.invoice_id,invoicecostinvoice_id=costinvoice.id,status=True)
    checkforsettlement=False
    if invoice_acceptance.exists():
        checkforsettlement=True
    return checkforsettlement,invoice_acceptance.first()

@register.simple_tag
def settlement_value(amount,percentage):
    base_amount=replacecommaid(amount_convertion(amount))
    try:
        approved_amount=float(base_amount)*(float(percentage)/100)
        approved_amount=new_round_of_two_values(approved_amount)
    except:
        approved_amount='0.00'
    return approved_amount

@register.simple_tag
def check_payment_track_status(pk ,paycount):
    payment_status = True
    invoice_cost_data = InvoiceCostInvoice.objects.filter(invoice_id=pk, status=1)
    for invoice in invoice_cost_data:
        pay_percentage = get_payment_percentage( pk,invoice.id,paycount)
        if pay_percentage != 100:
            payment_status = False
    
    return payment_status

@register.filter
def check_bank_user_currencies(request):
    try:
        bankuser = list(CompanyBankUser.objects.filter(user_id=request.user.id,companybank__company_id=request.company.id).values_list('companybank__currency_id',flat=True))
        try:
            bankuser=[int(i) for i in bankuser if i]
        except:
            bankuser=bankuser
        return bankuser
    except ObjectDoesNotExist:
        return []
    else:
        return []
    
@register.filter
def check_bank_users(request):
    try:
        bankuser = CompanyBankUser.objects.filter(user_id=request.user.id,companybank__company_id=request.company.id).count()
        if bankuser > 0 :
            return True
        else :
            return False
    except ObjectDoesNotExist:
        return False
    else:
        return False

@register.filter
def costinvoicepaidvalue(invoicecost_id):
    try:
        costInvoice=InvoiceCostInvoice.objects.filter(id=invoicecost_id,status=1).first()
        net_payable = float(convert_val_to_float(costInvoice.invoice_total_amount))
        if costInvoice.new_netpayable:
            net_payable=float(costInvoice.new_netpayable.replace(',', ''))
        payment = PaymentInstruction.objects.filter(invoicecost_id=invoicecost_id,is_editable=False,status=True,percentage_confirm=True)
        print(f'net_payable-1 {net_payable},payment {payment}')
        if payment.exists():
            return payment.aggregate(Sum('payable_amount'))['payable_amount__sum']
        else:
            return 0
    except:
        return 0

@register.simple_tag
def checkdynamic_flow(invoice,user_id,module_id):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid).first()
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
    if(contract_details):
        if module_id:
            invoiceflowmodules=Invoiceflowmodules.objects.filter_by_module_id(invoice.id,0,module_id)
            print(f'invoiceflowmodules {invoiceflowmodules}')
            get_data=list(Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflowmodules, user_status=0,user=user_id,status=0).values_list('Invoiceflowmodules__payment_instruct__payment_count',flat=True).distinct())
            print(f'get_data {get_data}')
            return get_data
        else:
            invoiceflowmodules=Invoiceflowmodules.objects.filter_by_module_id(invoice.id,0,None)
            print(f'invoiceflowmodulesinvoiceflowmodules {invoiceflowmodules}')
            get_data=list(Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflowmodules,user=user_id,project_id=contract_details.projects_id,bank_user_verification=0,status=0).values_list('payment_instruction__payment_count',flat=True).distinct())
            get_datas=list(Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflowmodules,user=user_id,project_id=contract_details.projects_id,bank_user_verification=1,status=0).values_list('payment_instruction__payment_count',flat=True).distinct())
            get_data.extend(get_datas)
            get_data=list(set(get_data))
            print(f'get_1 {get_data}')
            return get_data
    return []

@register.simple_tag
def Check_pending_amount(invoicecost_id,request):
    try:
        costInvoice=InvoiceCostInvoice.objects.filter(id=invoicecost_id,status=1).first()
        net_payable = float(convert_val_to_float(costInvoice.invoice_total_amount))
        if costInvoice.new_netpayable:
            net_payable=float(costInvoice.new_netpayable.replace(',', ''))
        total_credit=get_credit_investment(costInvoice,request)
        payment = costinvoicepaidvalue(invoicecost_id)
        get_net_payable=get_net_payableamount(str(net_payable),total_credit)
        final_val=float(get_net_payable.replace(',', '')) if float(get_net_payable.replace(',', '')) > 0 else net_payable
        return Decimal(final_val)-payment
    except:
        costInvoice=InvoiceCostInvoice.objects.filter(id=invoicecost_id,status=1).first()
        net_payable = float(convert_val_to_float(costInvoice.invoice_total_amount))
        if costInvoice.new_netpayable:
            net_payable=float(costInvoice.new_netpayable.replace(',', ''))
        return Decimal(net_payable)



@register.simple_tag
def check_next_flow_module(pk, flow_module):
    try:
        getnextlevel = ProjectFlowModules.objects.getnextactivelevel( flow_module.projectflow_level.id,flow_module.id)
        return getnextlevel
    except :
        getnextprocesstlevel=ProjectFlowModules.objects.getnxtprocessactlevel(flow_module.projectflow_level_id,flow_module.project_id,flow_module.projectflow_level.level_id)
        return getnextprocesstlevel
    
# @register.simple_tag
# def getnetpayment_bysplit(invoice_id,split_id,new_netpayable):
#     invoice_details=Invoice.objects.get_by_id(invoice_id)
#     split_invoice=InvoiceCostInvoice.objects.get_id(split_id)
#     contract_details=ContractMaster.objects.getcontract(invoice_details.contractid)
#     if(new_netpayable != '0'):
#         invoice_amount=split_invoice.new_netpayable.replace(',', '')
#         # print(f"split_invoice.invoice_percentage {type(split_invoice.invoice_percentage)}")
#         inclusivetaxes=VendorCompanyTaxPercentage.objects.getinclusivetaxes_bycontractid(invoice_details.contractid)
#         inclusivetaxpercentage=0
#         for inclusivetax in inclusivetaxes:
#             inclusivetaxpercentage +=float(inclusivetax.taxpercentage)
#         invoice_exclusivetax=InvoiceExclusive.objects.get_by_id(invoice_id)
#         exclusive_amount=0
#         for exclusive in invoice_exclusivetax:
#             split_amount=exclusive.exclusive_calculated_value.split(" ")
#             correct_amount=split_amount[1].replace(',', '')
#             exclusive_amount +=float(correct_amount)
        
#         inclusive_amount=float(invoice_amount)*inclusivetaxpercentage/100
#         exclusive_amount=exclusive_amount*float(split_invoice.invoice_percentage)/100
#         netpayment=float(invoice_amount)-inclusive_amount+exclusive_amount

#         # print(f"exclusive_amount {exclusive_amount}")
#         otheraddition=OtherAdditions.objects.getotheraddition_by_splitid(split_invoice.id)
#         otherdeduction=OtherDeductions.objects.getotherdeduction_by_splitid(split_invoice.id)
#         if otheraddition:
#             other_addition_split_amount=otheraddition.amount.split(" ")
#             other_addition_amount=float(other_addition_split_amount[1])
#             netpayment=netpayment+other_addition_amount

#         if otherdeduction:
#             other_deduction_split_value=otherdeduction.amount.split(" ")
#             other_deduction_amount=other_deduction_split_value[1].replace(',', '')
#             other_deduction_amount=float(other_deduction_amount.replace(')', ''))
#             netpayment=netpayment-other_deduction_amount

#     else:
#         split_amount=split_invoice.invoice_total_amount.split(" ")
#         invoice_amount_with_exclusive_tax=float(split_amount[1].replace(',', ''))
#         invoice_exclusivetax=InvoiceExclusive.objects.get_by_id(invoice_id)

#         exclusive_amount=0
#         for exclusive in invoice_exclusivetax:
#             split_amount=exclusive.exclusive_calculated_value.split(" ")
#             correct_amount=split_amount[1].replace(',', '')
#             exclusive_amount +=float(correct_amount)
#         exclusive_amount=exclusive_amount*float(split_invoice.invoice_percentage)/100
#         if(contract_details.currency.currency_symbol == split_invoice.invoice_currency):
#             exclusive_amount=exclusive_amount
#         else:
#             if split_invoice.invoice_exchange_rate == 'N/A' or split_invoice.invoice_exchange_rate.strip() == '':
#                 exchange_rate=1
#             else: 
#                 exchange_rate=split_invoice.invoice_exchange_rate
#             exclusive_amount=exclusive_amount*float(exchange_rate)

#         invoice_amount=invoice_amount_with_exclusive_tax-exclusive_amount

#         inclusivetaxes=VendorCompanyTaxPercentage.objects.getinclusivetaxes_bycontractid(invoice_details.contractid)
#         inclusivetaxpercentage=0
#         for inclusivetax in inclusivetaxes:
#             inclusivetaxpercentage +=float(inclusivetax.taxpercentage)
#         inclusive_amount=float(invoice_amount)*inclusivetaxpercentage/100
#         otheraddition=OtherAdditions.objects.getotheraddition_by_splitid(split_invoice.id)
#         otherdeduction=OtherDeductions.objects.getotherdeduction_by_splitid(split_invoice.id)
#         netpayment=invoice_amount-inclusive_amount+exclusive_amount

#         if otheraddition:
#             other_addition_split_amount=otheraddition.amount.split(" ")
#             other_addition_amount=float(other_addition_split_amount[1])
#             netpayment=netpayment+other_addition_amount

#         if otherdeduction:
#             other_deduction_split_value=otherdeduction.amount.split(" ")
#             other_deduction_amount=other_deduction_split_value[1].replace(',', '')
#             other_deduction_amount=float(other_deduction_amount.replace(')', ''))
#             netpayment=netpayment-other_deduction_amount


#         # print(f"invoice_amount {invoice_amount}")
#         # print(f"exclusive_amount {exclusive_amount}")
#         # print(f"inclusive_amount {inclusive_amount}")
#     return netpayment


@register.simple_tag
def getnetpayment_bysplit(invoice_id,split_id,new_netpayable):
    invoice_details=Invoice.objects.get_by_id(invoice_id)
    split_invoice=InvoiceCostInvoice.objects.get_id(split_id)
    settlement_invoice=SettlementInvoice.objects.filter(invoice_id=invoice_id,status=True).first()
    if invoice_details.contracttype=='original':
        contract_details=ContractMaster.objects.getcontract(invoice_details.contractid)
        contract_currency=contract_details.currency.currency_symbol
    else :
        contract_details = Amendment.objects.get_by_id(invoice_details.contractid, 1).first()
        contract_currency=contract_details.service.currency.currency_symbol


    if(settlement_invoice):
        settlement_percentage=settlement_invoice.accepted_percentage
        # invoice_amount=split_invoice.new_netpayable.replace(',', '')
        # print(f"split_invoice.invoice_percentage {type(split_invoice.invoice_percentage)}")
        split_amount=split_invoice.invoice_total_amount.split(" ")
        invoice_amount_with_exclusive_tax=float(split_amount[1].replace(',', ''))
        invoice_exclusivetax=InvoiceExclusive.objects.get_by_id(invoice_id)

        exclusive_amount=0
        for exclusive in invoice_exclusivetax:
            split_amount=exclusive.exclusive_calculated_value.split(" ")
            correct_amount=split_amount[1].replace(',', '')
            round_of_exclusive_value = round_of_two_values(float(correct_amount))
            remove_comma=str(round_of_exclusive_value).replace(',', '')
            exclusive_amount +=float(remove_comma)

        round_of_exclusive_amount=exclusive_amount*float(split_invoice.invoice_percentage)/100
        exclusive_amount=round_of_two_values(float(round_of_exclusive_amount))


        if(contract_currency == split_invoice.invoice_currency):
            exclusive_amount=str(exclusive_amount).replace(',', '')
            exclusive_amount=float(exclusive_amount)
        else:
            if split_invoice.invoice_exchange_rate == 'N/A' or split_invoice.invoice_exchange_rate.strip() == '':
                exchange_rate=1
            else: 
                exchange_rate=split_invoice.invoice_exchange_rate

            exclusive_amount=str(exclusive_amount).replace(',', '')
            exclusive_amount=float(exclusive_amount)*float(exchange_rate)
            exclusive_amount=float(round_of_two_values(float(exclusive_amount)))

        

        
        invoice_amount =invoice_amount_with_exclusive_tax-exclusive_amount
        inclusivetaxes=VendorCompanyTaxPercentage.objects.getinclusivetaxes_bycontractid(invoice_details.contractid)
        inclusivetaxpercentage=0
        for inclusivetax in inclusivetaxes:
            inclusivetaxpercentage +=float(inclusivetax.taxpercentage)

        
        invoice_exclusivetax=InvoiceExclusive.objects.get_by_id(invoice_id)
        exclusive_amount=0
        for exclusive in invoice_exclusivetax:
            split_amount=exclusive.exclusive_calculated_value.split(" ")
            correct_amount=split_amount[1].replace(',', '')
            exclusive_amount +=float(correct_amount)
        inclusive_amount=float(invoice_amount)*inclusivetaxpercentage/100
        exclusive_amount=exclusive_amount*float(split_invoice.invoice_percentage)/100

        if split_invoice.invoice_exchange_rate == 'N/A' or split_invoice.invoice_exchange_rate.strip() == '':
            exchange_rate=1
        else: 
            exchange_rate=split_invoice.invoice_exchange_rate

        exclusive_amount=exclusive_amount*float(exchange_rate)
        new_exclusive_amount=round_of_two_values(newinvoiceexclusivevalues(invoice_id , round_of_two_values(invoice_amount)))
        invoice_amount_with_settlement=float(invoice_amount)*float(settlement_percentage)/100
        inclusive_amount_with_settlement=round_of_two_values(float(inclusive_amount)*float(settlement_percentage)/100)
        exclusive_amount_with_settlement=round_of_two_values(float(new_exclusive_amount)*float(settlement_percentage)/100)

        netpayment=float(round_of_two_values(float(invoice_amount_with_settlement)-float(inclusive_amount_with_settlement)+float(exclusive_amount_with_settlement)))
        # print(f"exclusive_amount {exclusive_amount}")
        otheraddition=OtherAdditions.objects.getotheraddition_by_splitid(split_invoice.id)
        otherdeduction=OtherDeductions.objects.getotherdeduction_by_splitid(split_invoice.id)
        if otheraddition:
            other_addition_split_amount=otheraddition.amount.split(" ")
            other_addition_amount=float(other_addition_split_amount[1].replace(',', ''))
            netpayment=float(round_of_two_values(netpayment+other_addition_amount))

        if otherdeduction:
            other_deduction_split_value=otherdeduction.amount.split(" ")
            other_deduction_amount=other_deduction_split_value[1].replace(',', '')
            other_deduction_amount=float(other_deduction_amount.replace(')', ''))
            netpayment=float(round_of_two_values(netpayment-other_deduction_amount))

        

    else:

        split_amount=split_invoice.invoice_total_amount.split(" ")
        invoice_amount_with_exclusive_tax=float(split_amount[1].replace(',', ''))
        invoice_exclusivetax=InvoiceExclusive.objects.get_by_id(invoice_id)

        exclusive_amount=0
        for exclusive in invoice_exclusivetax:
            split_amount=exclusive.exclusive_calculated_value.split(" ")
            correct_amount=split_amount[1].replace(',', '')
            round_of_exclusive_value = round_of_two_values(float(correct_amount))
            remove_comma=str(round_of_exclusive_value).replace(',', '')
            exclusive_amount +=float(remove_comma)

        round_of_exclusive_amount=exclusive_amount*float(split_invoice.invoice_percentage)/100
        exclusive_amount=round_of_two_values(float(round_of_exclusive_amount))


        if(contract_currency == split_invoice.invoice_currency):
            exclusive_amount=str(exclusive_amount).replace(',', '')
            exclusive_amount=float(exclusive_amount)
        else:
            if split_invoice.invoice_exchange_rate == 'N/A' or split_invoice.invoice_exchange_rate.strip() == '':
                exchange_rate=1
            else: 
                exchange_rate=split_invoice.invoice_exchange_rate

            exclusive_amount=str(exclusive_amount).replace(',', '')
            exclusive_amount=float(exclusive_amount)*float(exchange_rate)
            exclusive_amount=float(round_of_two_values(float(exclusive_amount)))

        

        
        invoice_amount =invoice_amount_with_exclusive_tax-exclusive_amount
        # invoice_amount=round(float(round_of_invoice), 2)
        if invoice_details.contracttype == 'original' :
            inclusivetaxes=VendorCompanyTaxPercentage.objects.getinclusivetaxes_bycontractid(invoice_details.contractid)
        else :
            inclusivetaxes=VendorCompanyTaxPercentage.objects.getinclusivetaxes_byammendment(invoice_details.contractid)

        inclusivetaxpercentage=0
        inclusice_tax_amount=0
        for inclusivetax in inclusivetaxes:
            inclusivetaxpercentage =float(inclusivetax.taxpercentage)
            inclusive_amount=float(invoice_amount)*inclusivetaxpercentage/100
            remove_comma=str(inclusive_amount).replace(',', '')
            newamount=round_of_two_values(remove_comma)

            newamount=str(newamount).replace(',', '')
            inclusice_tax_amount +=float(newamount)

        new_exclusive_amount=newinvoiceexclusivevalues(invoice_id , round_of_two_values(invoice_amount))
        otheraddition=OtherAdditions.objects.getotheraddition_by_splitid(split_invoice.id)
        otherdeduction=OtherDeductions.objects.getotherdeduction_by_splitid(split_invoice.id)


        netpayment=(invoice_amount-inclusice_tax_amount)+float(new_exclusive_amount)

        if otheraddition:
            other_addition_split_amount=otheraddition.amount.split(" ")
            other_addition_amount=other_addition_split_amount[1]
            other_addition_amount=float(other_addition_amount.replace(',', ''))
            netpayment=netpayment+other_addition_amount
        if otherdeduction:
            other_deduction_split_value=otherdeduction.amount.split(" ")
            other_deduction_amount=other_deduction_split_value[1].replace(',', '')
            other_deduction_amount=float(other_deduction_amount.replace(')', ''))
            netpayment=netpayment-other_deduction_amount

        
        
    data={
        'netamount_separator':new_round_of_two_values(netpayment),
        'netpayment':netpayment
    }
    return data


@register.simple_tag
def get_project_id(contractid, type):
    try:
        if type == 'original':
            if contractid != '':
                contractmasterdata = ContractMaster.objects.filter(id=contractid).first()
                return contractmasterdata.projects.id
        else:
            if contractid != '':
                amendmentdata = Amendment.objects.filter(id=contractid, status=1).first()
                return amendmentdata.service.projects.id
    except ObjectDoesNotExist:
        return None  # Handle the case where the object does not exist gracefully
    except Exception as e:
        # Log or handle other exceptions here
        return None

@register.simple_tag
def get_payment_generate_split(pk, paycount):
    approved_users=duplicate_users= Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__invoice_id=pk,Invoiceflowmodules__payment_instruct__payment_count=paycount,status=1,bank_user_status=0).exclude(status=0, bank_user_status=1, Invoiceflowmodules__module=None)
    try:
        exact_val=0
        duplicate_user=[i['id'] for i in approved_users.values('user','id') if exact_val != (exact_val := i['user'])]
        print("duplicate_user ",duplicate_user)
        duplicate_users=approved_users.filter(id__in=duplicate_user)
        new_duplicate = list(duplicate_users.values_list('Invoiceflowmodules',flat=True).distinct())
        dub_value=[]
        for module_id in new_duplicate:
            new_value=duplicate_users.filter(Invoiceflowmodules_id=module_id).first()
            dub_value.append(new_value)
    except:
        duplicate_users=Invoiceflowmodulesusers.objects.getapprovedusersinvoice(pk).exclude(bank_user_status=1)
    return dub_value
        

@register.simple_tag
def checkfor_invoicerecipt_upload(invoice,user_id,module_id,payment_count):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid)
        try:
            project_id=contract_details[0].projects_id
        except:
            project_id=None
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
        try:
            project_id=contract_details.projects_id
        except:
            project_id=None
    checkuser_flow=False
    if(contract_details):
        invoiceflowmodules=Invoiceflowmodules.objects.filter_by_module_id(invoice.id,0,module_id).filter(payment_instruct__payment_count=payment_count)
        print(f'invoiceflowmodules {invoiceflowmodules}')
        if Invoiceflowmodulesusers.objects.filter(user=user_id,project_id=project_id,Invoiceflowmodules__in=invoiceflowmodules,status=0).exists(): 
            checkuser_flow=True
    print(f'checkuser_flow {checkuser_flow}')  
    return checkuser_flow

@register.simple_tag
def checkbal_for_balance_invoice(invoice_id,request,payment_count):
    invoiceflow_modules=Invoiceflowmodules.objects.filter_by_module_id(invoice_id,1,6).filter(payment_instruct__payment_count=payment_count)
    final_list=[]
    if invoiceflow_modules.count() > 0:
        approved_flow_user=Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflow_modules).exclude(status=0)
        print(f'approved_flow_user {approved_flow_user}')
        for aprv in approved_flow_user:
            if aprv.projectflow_user.user.user_id == request.user.id:
                verification_count=list(PaymentInstruction.objects.filter(id=aprv.Invoiceflowmodules.payment_instruct_id,status=1,bankuser_verification=0).exclude(verification_code=None).values_list('payment_count',flat=True))
                final_list.extend(verification_count)
    final_list=[i  for i in final_list  if i]
    final_list=list(set(final_list))      
    print(f'final_list {final_list}')        
    return len(final_list)

@register.simple_tag
def find_payment_percentage(paymentcount, invoiceid):
    try:
        pay_percentage = PaymentInstruction.objects.filter(invoicecost_id=invoiceid, payment_count=paymentcount,status=True).first()
        return pay_percentage
    except PaymentInstruction.DoesNotExist:
        return None  
    except Exception as e:
        return None


@register.simple_tag
def checkapprovalmodule_flow(invoice,user_id,module_id,payment_count):
    if invoice.contracttype == 'original':
        contract_details=ContractMaster.objects.get_by_id(invoice.contractid).first()
    else:
        contract_detail=Amendment.objects.get_by_id(invoice.contractid,1).first()
        contract_details=contract_detail.service
    get_data=False
    if(contract_details):
        if module_id:
            invoiceflowmodules=Invoiceflowmodules.objects.filter_by_module_id(invoice.id,0,module_id).filter(payment_instruct__payment_count=payment_count)
            print(f'invoiceflowmodules {invoiceflowmodules}')
            if Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflowmodules,user=user_id,status=0).exists():
                get_data=True
            print(f'get_data {get_data}')
            return get_data
        else:
            invoiceflowmodules=Invoiceflowmodules.objects.filter_by_module_id(invoice.id,0,None).filter(payment_instruct__payment_count=payment_count)
            print(f'invoiceflowmodulesinvoiceflowmodules {invoiceflowmodules}')
            if Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflowmodules,user=user_id,project_id=contract_details.projects_id,bank_user_verification=0,status=0).exists():
                get_data=True
            elif Invoiceflowmodulesusers.objects.filter(Invoiceflowmodules__in=invoiceflowmodules,user=user_id,project_id=contract_details.projects_id,bank_user_verification=1,status=0).exists():
                get_data=True
            return get_data
    return get_data

@register.simple_tag
def partial_payment_percentage(invoice_id):
    try:
        payment_instructions = PaymentInstruction.objects.filter(invoicecost_id=invoice_id, status=True)
        payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_instructions)
        return payment_percentage_sum
       
    except PaymentInstruction.DoesNotExist:
        return None
    except Exception as e:
        return None
    
@register.simple_tag
def check_payment_spit_module(cost_id, paycount):
    try:
        payment_instructions = PaymentInstruction.objects.filter(invoicecost_id=cost_id, status=True, payment_count=paycount)
        return payment_instructions.exists()
    except PaymentInstruction.DoesNotExist:
        return False


@register.simple_tag
def track_payment_status(cost_id, paycount):
    try:
        payment_instructions = PaymentInstruction.objects.filter(invoicecost_id=cost_id, status=True, payment_count__lte=paycount)
        payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_instructions)
        return payment_percentage_sum
    except PaymentInstruction.DoesNotExist:
        return False
    

from decimal import Decimal
@register.simple_tag
def check_payment_pending_amount(pk, counting, cost_id):
    percentage = Decimal('0')
    costInvoice = InvoiceCostInvoice.objects.filter(id=cost_id, status=1).first()
    if costInvoice:
        # Remove commas from net_payable and convert it to a Decimal
        net_payable = Decimal(costInvoice.new_netpayable.replace(',', ''))

        for count in range(1, counting + 1):  
            payment_instructions = PaymentInstruction.objects.filter(
                invoicecost__invoice_id=pk,
                status=True,
                payment_count=count,
                invoicecost_id=cost_id
            ).first()
            if payment_instructions:
                percentage += Decimal(payment_instructions.payment_percentage)
        print("percentage",percentage)
        # Calculate payment amount based on percentage
        payment_amount = net_payable * percentage / Decimal('100')
        print("payment_amount",payment_amount)
        # Calculate and return the remaining net payable amount
        remaining_net_payable = net_payable - payment_amount
        print("remaining_net_payable",remaining_net_payable)
        return remaining_net_payable
    else:
        return Decimal('0')

@register.simple_tag
def trackpaidstatus(pk, paycount):
    payment_status = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk, status=True, payment_count=paycount).values_list('payment_status', flat=True))
    print('payment',payment_status)
    paid_status = 2
    if 1 in payment_status and 2 in payment_status and 3 in payment_status :
        paid_status = 2
    elif 2 in payment_status and 3 in payment_status:
        paid_status = 2
    elif 1 in payment_status:
        paid_status = 2
    elif 2 in payment_status:
        paid_status = 2
    elif 3 in payment_status:
        paid_status = 3
    return paid_status
    
@register.simple_tag
def check_bankuser_status(pk,paycount):
    bankuser=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk, status=True, payment_count=paycount)
    generate_otp = True
    for bank in bankuser:
        if bank.verification_code == None or bank.verification_code =="" :
            generate_otp = False

    return generate_otp

@register.simple_tag
def payment_generate_split_percentage(invoice_id , paycount):
    try:
        payment_instructions = PaymentInstruction.objects.filter(invoicecost_id=invoice_id, status=True,payment_count=paycount)
        payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_instructions)
        
        return payment_percentage_sum
       
    except PaymentInstruction.DoesNotExist:
        return None
    except Exception as e:
        return None
    
    
@register.simple_tag
def paid_payment_percentage(invoice_id,payment_percentage):
    try:
        payment_instructions = PaymentInstruction.objects.filter(invoicecost_id=invoice_id, status=True)
        payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_instructions)
        already_paid_percentage=payment_percentage_sum-payment_percentage
        return already_paid_percentage
       
    except PaymentInstruction.DoesNotExist:
        return None
    except Exception as e:
        return None
    
    
@register.simple_tag
def paid_payment_amount(invoice_id,payment_percentage,netamount):
    payment=paid_payment_percentage(invoice_id,payment_percentage)
    if payment == None :
        payment=0
    remove_comma=str(netamount).replace(",", "")
    payment_percentage_sum = (float(remove_comma) * float(payment)) / 100 
    if payment_percentage_sum == 0 :
        return 0
    else :
        return new_round_of_two_values(payment_percentage_sum)
       
@register.simple_tag
def paid_payment(invoice_id,netamount):
    payment=partial_payment_percentage(invoice_id)
    if payment == None :
        payment=0
    remove_comma=str(netamount).replace(",", "")
    payment_percentage_sum = (float(remove_comma) * float(payment)) / 100 
    return new_round_of_two_values(payment_percentage_sum)
           
@register.simple_tag
def split_by_newline(value):
    if value == None:
        return 
    """Split the value by newline character and print each line."""
    values = value.split(',')
    print(values)
    poa = []
    for i in values:
        print('#', i)    
        poa.append(i.replace('"', ''))  # Replace double quotes for each element
    return poa


@register.simple_tag
def split_credit_newline(queryset):
    """Split the value by newline character and print each line."""
    values = set()
    new=[]
    for item in queryset:
        values.update(item.strip('[]"').split(','))
    for value in values:
        print(value.strip())
        new.append(value)
    return new


@register.filter
def convert_decimal(amount):
    float_amount = float(amount)
    return "{:,.2f}".format(float_amount)


@register.simple_tag
def payment_receipt_file(pk,pay_count):
    file =[]
    file_values = list(PaymentReceiptFile.objects.filter(payment_receipt__invoice_id=pk,status=True,payment_receipt__payment_instruct__payment_count=pay_count).values_list('payment_receipt', flat=True).distinct())
    for files in file_values:
            file_values = PaymentReceiptFile.objects.filter(payment_receipt__invoice_id=pk,status=True,payment_receipt__payment_instruct__payment_count=pay_count,payment_receipt_id=files).first()
            file.append(file_values)
    file_length = len(file)
    return file,file_length

@register.simple_tag
def payment_receipt_file_values(pk,pay_count,receipt_id):
    file = PaymentReceiptFile.objects.filter(payment_receipt__invoice_id=pk,status=True,payment_receipt__payment_instruct__payment_count=pay_count,payment_receipt_id=receipt_id)
    return file

@register.simple_tag
def check_vendor(cin):
    try:
        vendor_id = ContractMasterVendor.objects.filter(vin=cin).first()
        if vendor_id:
            return False
        else:
            return True
    except ObjectDoesNotExist:
        return True

@register.simple_tag
def getEncoded(image):
    with open(image.path, "rb") as f:
        img = Image.open(f)
        img_resized = img.resize((120, 80))  # Resize the image
        buffered = BytesIO()
        img_resized.save(buffered, format="PNG")  # Save the resized image to a buffer
        encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Encode the resized image
    return mark_safe(f"data:image/png;base64,{encoded_string}")


@register.simple_tag
def exchange_netamount(value1, exchagerate):
    try:
        value1=remove_symbol(value1)
        if exchagerate == 'N/A':
            exchagerate=1
        multiple = float(value1) * float(exchagerate)
        return new_round_of_two_values(multiple)
    except (ValueError, TypeError):
        return ''
    
    
@register.simple_tag
def exchange_grossamount(value1, exchagerate):
    try:
        if exchagerate == 'N/A':
            exchagerate=1
        multiple = float(value1) * float(exchagerate)
        return new_round_of_two_values(multiple)
    except (ValueError, TypeError):
        return ''



@register.simple_tag
def complete_module_track(pk, splitcount):
    try:
        invoice_details=Invoice.objects.get_by_id(pk)
        costinvoice=getinvoices(invoice_details).first()
        new_costinvoice=(InvoiceCostInvoice.objects.filter(invoice_id=invoice_details,status=1).values_list('id', flat=True))
        approved_users=Invoiceflowmodules.objects.filter(invoice=pk,status=1,module_id__lte=3 ,invoicecost_id=costinvoice.id)
        checked_invoice = list(Invoiceflowmodules.objects.filter(invoice=pk,status=1,payment_instruct__payment_count=splitcount , invoicecost__in=new_costinvoice).exclude(module=None).values_list('invoicecost', flat=True).distinct())
        
        if checked_invoice: 
            completed_invoice = Invoiceflowmodules.objects.filter(invoice=pk,status=1,payment_instruct__payment_count=splitcount , invoicecost_id=checked_invoice[0]).exclude(module=None)

            merged_queryset = (approved_users | completed_invoice).distinct()
            return merged_queryset
        else :
            merged_queryset = approved_users
            return merged_queryset
    except ObjectDoesNotExist:
        return None
    
    
@register.simple_tag
def exchage_rate_currency_symbol(pk, vendor_id):    
    currency_symbol = InvoiceCostInvoice.objects.filter(invoice_id=pk,vendor_invoice_id=vendor_id).first()
    return currency_symbol


@register.simple_tag
def find_fully_paid(pk):
    fullypaid=True
    invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=pk,status=1)
    for cost in invoice_cost :
        payment_percentage=PaymentInstruction.objects.filter(invoicecost_id=cost.id,invoicecost__invoice_id=pk,status=True )
        payment_percentage_sum = sum(instruction.payment_percentage for instruction in payment_percentage)
        if payment_percentage_sum != 100:
            fullypaid=False
            
    return fullypaid




@register.simple_tag
def find_payment_spit_value(pk, paycount):
    try:
        payment_instructions = PaymentInstruction.objects.filter(invoicecost__invoice_id=pk, status=True, payment_count=paycount)
        return payment_instructions
    except PaymentInstruction.DoesNotExist:
        return False
            
@register.simple_tag
def find_signatories_user(pk,project_id,request,email):
    new_list=[]
    contractcostinvoice=InvoiceCostInvoice.objects.get_invoice_id(pk,1)
    get_project_signatories=SignatoriesSettings.objects.filter_by_project(project_id,request.company.id,2,1)
    if (get_project_signatories.count() > 0):
        filtered_data=get_project_signatories
    else:
        filtered_data=SignatoriesSettings.objects.filter_by_project(None,request.company.id,1,1)
    for costinvoice in contractcostinvoice:
        invoice_cost_amount=int(float(remove_symbol(costinvoice.invoice_total_amount)))
        data=filtered_data.filter(currency_id=costinvoice.currency.id ,invoice_type=1 , project_id=project_id , max_amount__gte=invoice_cost_amount) 
        if (data.count() > 0):
            sign_data=data.first()
        else:
            get_value=costinvoice.invoice_total_amount
            split_val=get_value.split(' ')
            convert_val=float(split_val[1].replace(',',''))
            sign_data=filtered_data.filter(currency_id=costinvoice.currency.id,invoice_type=1).filter(Q(min_amount__lte=convert_val) & Q(max_amount__gte=convert_val)).first()
        
        if sign_data == None :
            sign_data=filtered_data.filter(currency_id=costinvoice.currency.id ,invoice_type=2 , status=1,signatory_type=1).first()
        if sign_data:
            sign_users=SignatoriesUsers.objects.get_by_signatoryId(sign_data.id)
            for sign in sign_users:
                if sign.user.email== email :
                    new_list.append(costinvoice.id)    
    return new_list


@register.simple_tag
def reasonfor_queryhistory(pk,status):
    invoice_exceptional_instance = InvoiceExceptional.objects.filter(invoice_id=pk,return_status=status).first()
    if invoice_exceptional_instance:
        checked_messages = invoice_exceptional_instance.checked_messages
    else:
        checked_messages = None  
    return checked_messages