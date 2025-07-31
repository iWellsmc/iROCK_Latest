import re
from django.db.models import Q
from custom_auth.models import *
from projects.models import *
from invoice.models import *
from credit_note.models import *
from django import template


register = template.Library()

def convert_credit_date(value,companyid):
    if (value != None and value !=""):
        # convert_date=datetime.strptime(value ,"%Y-%m-%d").date()
        company_generalsetting=Settings.objects.filter(company_id=companyid).first()
        all_dateformat = {'dd-M-yy':"%d-%b-%Y",'dd-mm-yy':"%d-%m-%Y",'dd/mm/yy':"%d/%m/%Y",'mm-dd-yy':'%m-%d-%Y','mm/dd/yy':'%m/%d/%Y','yy-mm-dd':'%Y-%m-%d','yy/mm/dd':'%Y/%m/%d'}
        try:
            for key,values in all_dateformat.items():
                if (key == company_generalsetting.dateformat):
                    return value.strftime(values)
        except:
            return "N/A"
    else:
        return "N/A"



def credit_contract_invoices(credit_id,inv):
    contract_invoices=CreditNoteInvoice.objects.filter(credit_id=credit_id,status=1).values_list('invoice_id',flat=True)
    get_invoices_cost=InvoiceCostInvoice.objects.filter(invoice_id__in=contract_invoices).values_list('invoice_number',flat=True)
    return list(get_invoices_cost)

def credit_excluive_tax(value,percentage):
    if (value != ''):
        get_percentage=float(value)*float(percentage)/100
        RoundTax =("{:0,.2f}".format(get_percentage))
        return RoundTax
    else:
        return ''
    
    
@register.simple_tag
def credit_excluive_tax_with_exchangetype(value,percentage , exchangevalue):
    if (value != ''):
        if exchangevalue =='N/A':
            exchangevalue =1
        get_percentage=float(round_of_two_values(float(value)*float(percentage)/100))
        exchange=round_of_two_values(float(get_percentage)*float(exchangevalue))
        RoundTax =(new_round_of_two_values(exchange))
        return RoundTax
    else:
        return ''
    
@register.simple_tag
def credit_exclusive_value(value, percentage):
    if value:
        get_percentage = float(value) * float(percentage) / 100
        rounded_tax = new_round_of_two_values(get_percentage)
        return rounded_tax
    else:
        return ''
        
def convert_int(value):
    if (value != ""):
        # split_val=value.split(" ")
        # removed_symbols = ''
        # remove_comma=split_val[0].replace(",","")
        output_str = re.sub(r"[^0-9.]", "", value)
        removed_symbols = re.sub(r"[0-9.]", "", value.replace(",",""))
        convert_val=float(output_str)
        RoundTax =("{:0,.2f}".format(convert_val))
        return removed_symbols+' '+RoundTax
    else:
        return ''
# import re

# input_str = "12,345.678!90?"
# removed_symbols = ''
# # Replace any character that is not a number, dot or comma with an empty string
# output_str = re.sub(r"[^0-9.,]", "", input_str)
# # Find all characters that were removed
# removed_symbols = re.sub(r"[0-9.,]", "", input_str)


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


def get_credit_invoices(credit_id):
    credit_note_invoice=CreditNoteContractInvoice.objects.filter(credit_id=credit_id,status=1)
    return credit_note_invoice

def subcreditnote(credit_id,split_id):
    credit_notes=CreditNoteContractInvoice.objects.filter(credit_id=credit_id,vendor_split_invoice_id=split_id,status=1)
    return credit_notes

def add_separators(value):
    if (value != ""):
        return format(int(float(value)),",")
    else:
        return ""


def dateformat(value,companyid):
    if (value != None and value !=""):
        company_generalsetting=Settings.objects.filter(company_id=companyid).first()
        all_dateformat = {'dd-M-yy':"%d-%b-%Y",'dd-mm-yy':"%d-%m-%Y",'dd/mm/yy':"%d/%m/%Y",'mm-dd-yy':'%m-%d-%Y','mm/dd/yy':'%m/%d/%Y','yy-mm-dd':'%Y-%m-%d','yy/mm/dd':'%Y/%m/%d'}
        for key,values in all_dateformat.items():
            if (key == company_generalsetting.dateformat):
                return value.strftime(values)
    else:
        return ""
    
def convert_to_int(amount):
    convert_to = float(re.sub(r'[^\w\s.]|[a-zA-Z]+', '', amount))
    val = int(convert_to) if convert_to.is_integer() else float(convert_to)
    return val

@register.filter
def newamount_convertion(amount):
    if amount.strip() != '':
        base_amount=convert_to_int(amount)
        return new_round_of_two_values(base_amount)
    else:
        return '0'
        
@register.simple_tag
def calculate(totalvalue,percentage,exchange_value):
    get_total_value=re.findall(r'[0-9][0-9,.]+', totalvalue)
    if len(get_total_value)>0:
        if (exchange_value =="N/A" or exchange_value ==""):
            remove_comma = float(get_total_value[0].replace(',', ''))
            gross_amount = float(remove_comma)*float(percentage)/100
            return new_round_of_two_values(gross_amount)
        else:
            remove_comma = float(get_total_value[0].replace(',', ''))
            gross_amount1 = float(remove_comma)*float(percentage)/100*float(exchange_value)
            return new_round_of_two_values(gross_amount1)
    else:
        return 0
        
@register.simple_tag
def newcalculate(totalvalue,percentage,exchange_value):
    get_total_value=re.findall(r'[0-9][0-9,.]+', totalvalue)
    if len(get_total_value)>0:
        if (exchange_value =="N/A" or exchange_value ==""):
            remove_comma = float(get_total_value[0].replace(',', ''))
            gross_amount =float(remove_comma)*float(percentage)/100
            return new_round_of_two_values(gross_amount)
        else:
            remove_comma = float(get_total_value[0].replace(',', ''))
            gross=float(round_of_two_values(float(remove_comma)*float(percentage)/100))
            gross_amount1 = round_of_two_values(gross*float(exchange_value))
            return new_round_of_two_values(gross_amount1)
    else:
        return 0
    
    
    
@register.simple_tag
def creaditenote_gross_amount(totalvalue,percentage,exchange_value):
    get_total_value=re.findall(r'[0-9][0-9,.]+', totalvalue)
    if len(get_total_value)>0:
        if (exchange_value =="N/A" or exchange_value ==""):
            remove_comma = float(get_total_value[0].replace(',', ''))
            gross_amount =float(remove_comma)*float(percentage)/100
            return round_of_two_values(gross_amount)
        else:
            remove_comma = float(get_total_value[0].replace(',', ''))
            gross=float(round_of_two_values(float(remove_comma)*float(percentage)/100))
            gross_amount1 = round_of_two_values(gross*float(exchange_value))
            return gross_amount1
    else:
        return 0
    
    
@register.simple_tag
def newcalculate1(percentage,exclusive_value,exchange_value):
    if (exchange_value =="N/A" or exchange_value ==""):
        exchange_value=(float(exclusive_value)*float(percentage))/100
        final_value=round_of_two_values(exchange_value)
        return round_of_two_values(final_value)
    else:
        exchange_value=(float(exclusive_value)*float(percentage))/100
        addexchange=exchange_value*float(exchange_value)
        final_value1=round_of_two_values(addexchange)
        return round_of_two_values(final_value1)


@register.simple_tag
def calculate1(percentage,exclusive_value,exchange_value):
    if (exchange_value =="N/A" or exchange_value ==""):
        final_value=(float(exclusive_value)*float(percentage))/100
        return new_round_of_two_values(final_value)
    else:
        addexchange=round_of_two_values((float(exclusive_value)*float(percentage))/100)
        final_value1=float(addexchange)*float(exchange_value)
        return new_round_of_two_values(final_value1)

def remove_comma_and_convert(value):
    value=str(value)
    cleaned_value = value.replace(',', '')
    return float(cleaned_value)

def addvalue(totalvalue,exclusive_value):
    value1 = totalvalue
    value2 = float('{:.2f}'.format(exclusive_value))
    final_value = float(value1) + float(value2)
    return "{:,.2f}".format(final_value)

def newaddvalue(totalvalue,exclusive_value):
    value1=remove_comma_and_convert(totalvalue)
    value2=str(exclusive_value).replace(',', '')
    final_value = float(value1) + float(value2)
    return new_round_of_two_values(final_value)


@register.simple_tag
def addmorevalue(totalvalue,exclusive_value):
    totalvalue = totalvalue.replace(',', '')
    exclusive_value = str(exclusive_value).replace(',', '')
    value1 = remove_symbol(totalvalue)
    value2 = float(round_of_two_values(exclusive_value))
    final_value = float(value1) + float(value2)

    return new_round_of_two_values(final_value)

@register.simple_tag
def checkallcreditno(creditid,vendorsplitid):
    credit = CreditNoteContractInvoice.objects.filter(credit_id=creditid,vendor_split_invoice_id=vendorsplitid,status=1)
    inv_count=credit.filter(Q(credit_note_no__isnull=True) | Q(credit_note_no__iexact='') | Q(date__isnull=True) | Q(date__iexact='') | Q(date__iexact='') | Q(exchange_rate='')).count()
    return inv_count


def currencysymbol(value):
    if (value != ""):
        symbol=value.split("-")
        value1=symbol[0]
        return value1
    else:
        return""
@register.filter
def remove_symbol(value):
    removed_symbol = re.sub(r"[^0-9.]", "", value)
    return (round_of_two_values(float(removed_symbol)))


@register.filter
def credit_remove_symbol(value):
    removed_symbol = re.sub(r"[^0-9.]", "", value)
    return float(removed_symbol)

@register.filter
def new_remove_symbol(value):
    value=str(value)
    removed_symbol = re.sub(r"[^0-9.]", "", value)
    return ("{:,.2f}".format(float(removed_symbol)))

@register.filter
def remove_currency_symbol(value):
    removed_symbol = re.sub(r"[^0-9.]", "", value)
    if removed_symbol=='':
        removed_symbol=0
    return ("{:0.2f}".format(float(removed_symbol)))

@register.simple_tag
def get_creditapproved_users(credit_id,level_id,module_id):
    get_data=Invoiceflowmodules.objects.getinvoiceflowmodules_credit(credit_id,level_id,module_id).first()
    if (get_data):
        get_invoice_app_users=Invoiceflowmodulesusers.objects.get_approved_users(get_data.id)
        app_value=True
        if (get_invoice_app_users.count() == 0):
            get_invoice_app_users=Invoiceflowmodulesusers.objects.get_invflow_users(get_data.id)
            app_value=False
    else:
        get_invoice_app_users=[]
        app_value=False
    return get_data,get_invoice_app_users,app_value

register.filter('convert_credit_date',convert_credit_date)
register.filter('credit_contract_invoices',credit_contract_invoices)
register.filter('credit_excluive_tax',credit_excluive_tax)
register.filter('convert_int',convert_int)
register.filter('get_credit_invoices',get_credit_invoices)
register.filter('add_separators',add_separators)
register.filter('dateformat',dateformat)
register.filter('addvalue',addvalue)
register.filter('newaddvalue',newaddvalue)
register.filter('checkallcreditno',checkallcreditno)
register.filter('currencysymbol',currencysymbol)
register.filter('subcreditnote',subcreditnote)


@register.simple_tag
def getcreditsupportfiles(invoiceid, supportid, contract=None):
    print(invoiceid, supportid, contract)
    invoice_details = Invoice.objects.get_by_id(invoiceid)
    
    files = []  # Initialize files to an empty list
    
    # Check if contract is not None before accessing its id attribute
    if contract is not None:
        contract_id = contract.id
    else:
        contract_id = None
    
    if supportid == '10':
        if invoice_details.contracttype == 'original' and contract_id is not None:
            files = VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract_id, 2)

        else:
            if invoice_details.contracttype == 'amendment' or invoice_details.contracttype == "addendum":
                contracts = Amendment.objects.filter(id=invoice_details.contractid, status=1).first()
                files = VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contracts.service.id, 2)
        # print(f"files {files}")

    elif supportid == '9':
        if invoice_details.contracttype == 'original' and contract_id is not None:
            files = VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contract_id, 1)
        else:
            if invoice_details.contracttype == 'amendment' or invoice_details.contracttype == "addendum":
                contracts = Amendment.objects.filter(id=invoice_details.contractid, status=1).first()
                files = VendorContractPriceTable.objects.getallprice_tablefiles_contractid(contracts.service.id, 1)

    else:
        files = InvoiceFileUpload.objects.filter(invoice_id=invoiceid, support=supportid, status=1)
    
    
    print(files, files.count)
    return files, len(files)


@register.simple_tag
def getamendmentcontract_price_files1(contract, contracttype, file_type):
    if contract:
        contract_table_files = VendorContractPriceTable.objects.getallprice_tablefiles_amendment_addendum(contract.id, file_type).values()
        # print(f"contract_table_files {contract_table_files}")
        return contract_table_files
    else:
        return None

@register.simple_tag
def credit_base_amount(total, percentage):
    if total:
        get_total_value = credit_remove_symbol(total)
        if get_total_value:
            remove_comma =str(get_total_value).replace(",","")
            add_value = round_of_two_values((float(remove_comma) * float(percentage)) / 100)
            return add_value
    return ''