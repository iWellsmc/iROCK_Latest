from invoice.models import InvoiceCostInvoice
from projects.models import ContractMaster,Projectcreation,VendorCompanyTaxDetails
from custom_auth.models import Countries,Companies
from credit_note.models import CreditNoteContractInvoice


def getapprovedinvoice_summary(vendor_id):
    allinvoice=InvoiceCostInvoice.objects.groupinvoice_by_currency(vendor_id)
    allinvoice_gross_total=[]
    currencies=[]
    for invoice in allinvoice:
        currency_invoice=InvoiceCostInvoice.objects.getinvoice_by_currency(vendor_id,invoice['invoice_currency'])
        currencies.append(invoice['invoice_currency'])
        invoice_paid_amont=0
        invoice_unpaid_amount=0
        for currencyinvoice in currency_invoice:
            amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', currencyinvoice.invoice_total_amount)))
            if(currencyinvoice.payment_status==1):
                invoice_unpaid_amount +=amount_without_currency
            else:
                invoice_paid_amont +=amount_without_currency

        allinvoice_gross_total.append({
            'currency':invoice['invoice_currency'],
            'invoice_unpaid_amount':invoice_unpaid_amount,
            'invoice_paid_amont':invoice_paid_amont,

        })
    data={
       'allinvoice_gross_total':allinvoice_gross_total,
       'currencies':currencies 
    }
    return data

def getawaitinginvoice_summary(vendor_id):
    allinvoice=InvoiceCostInvoice.objects.groupawaitinginvoice_by_currency(vendor_id)
    allinvoice_gross_total=[]
    currencies=[]

    for invoice in allinvoice:
        currency_invoice=InvoiceCostInvoice.objects.getinvoice_by_currency(vendor_id,invoice['invoice_currency'])
        total_amount=0
        currencies.append(invoice['invoice_currency'])

        for currencyinvoice in currency_invoice:
            amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', currencyinvoice.invoice_total_amount)))
            total_amount +=amount_without_currency
           
        allinvoice_gross_total.append({
            'currency':invoice['invoice_currency'],
            'total_amount':total_amount,

        })
    data={
       'allinvoice_gross_total':allinvoice_gross_total,
       'currencies':currencies 
    }
    return data

def getdisputedinvoice_summary(vendor_id):
    allinvoice=InvoiceCostInvoice.objects.groupdisputedinvoice_by_currency(vendor_id)
    allinvoice_gross_total=[]
    currencies=[]

    for invoice in allinvoice:
        currency_invoice=InvoiceCostInvoice.objects.getinvoice_by_currency(vendor_id,invoice['invoice_currency'])
        currencies.append(invoice['invoice_currency'])
        total_amount=0
        for currencyinvoice in currency_invoice:
            amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', currencyinvoice.invoice_total_amount)))
            total_amount +=amount_without_currency
           
        allinvoice_gross_total.append({
            'currency':invoice['invoice_currency'],
            'total_amount':total_amount,
        })
    
    data={
       'allinvoice_gross_total':allinvoice_gross_total,
       'currencies':currencies 
    }
    return data

def getprojectby_countrywise(vendor_id,country_ids=[],is_poa=False):
    if(is_poa == False):
        allprojects=ContractMaster.objects.getproject_bycountrywise(1,vendor_id,country_ids)
    else:
        allprojects=ContractMaster.objects.getproject_bycountrywise(1,None,country_ids)
 
    country_wise_project=[]
    country_wise_project.append({"name":"Country Wise Projects","id":"0.0","parent":"","color": '#fff'})
    for project in allprojects:
        country_details=Countries.objects.getcountry_by_id(project['country'])
        if(is_poa == False):
            projects_by_country=ContractMaster.objects.getproject_bycountry(1,vendor_id,project['country'])
        else:
            projects_by_country=ContractMaster.objects.getproject_bycountry(1,None,project['country'])

        projectcount=0
        for countryproject in projects_by_country:
            project_details=Projectcreation.objects.getproject_byid(countryproject['projects'])
            country_wise_project.append({"name":project_details.projectname.name,"id":str(project_details.id),"parent":str(project['country']),'value':1})
            projectcount +=1
        country_wise_project.append({"name":country_details.name,"id":str(project['country']),"parent":"0.0","value":projectcount,"color": '#b70863'})

    return country_wise_project

def getinvoicesummarychartdata_byvendor(vendor_details):
    default_currency=getdefaultcurrency_company(vendor_details.company_id)
    vendorprojects=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_details.id,True)
    allprojects=[]
    unpaid_invoice_amount=[]
    paid_invoice_amount=[]
    allawaiting_invoices=[]
    alldisputed_invoices=[]

    for vendorproject in vendorprojects:
        invoice_paid_amont=0
        invoice_unpaid_amount=0
        invoice_awaiting_amount=0
        invoice_disputed_amount=0


        project_details=Projectcreation.objects.getproject_byid(vendorproject['projects_id'])
        allprojects.append(project_details.projectname.name)
        approvedinvoices=InvoiceCostInvoice.objects.getinvoice_by_currency(vendor_details.id,default_currency,vendorproject['projects_id'])
        for approvedinvoice in approvedinvoices:
            amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', approvedinvoice.invoice_total_amount)))
            if(approvedinvoice.payment_status == 1):
                invoice_unpaid_amount +=amount_without_currency
            else:
                invoice_paid_amont +=amount_without_currency
        unpaid_invoice_amount.append(invoice_unpaid_amount)
        paid_invoice_amount.append(invoice_paid_amont)
        awaiting_invoices=InvoiceCostInvoice.objects.getallawaiting_invoice_by_currency_and_projectid(vendor_details.id,default_currency,vendorproject['projects_id'])
        for awaiting_invoice in awaiting_invoices:
            amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', awaiting_invoice.invoice_total_amount)))
            invoice_awaiting_amount +=amount_without_currency

        allawaiting_invoices.append(invoice_awaiting_amount)
        disputed_invoices=InvoiceCostInvoice.objects.getalldisputed_invoice_by_currency_and_projectid(vendor_details.id,default_currency,vendorproject['projects_id'])
        for disputed_invoice in disputed_invoices:
            amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', disputed_invoice.invoice_total_amount)))
            invoice_disputed_amount +=amount_without_currency
        alldisputed_invoices.append(invoice_disputed_amount)
    
    data={
        'allprojects':allprojects,
        'unpaid_invoice_amount':unpaid_invoice_amount,
        'paid_invoice_amount':paid_invoice_amount,
        'allawaiting_invoices':allawaiting_invoices,
        'alldisputed_invoices':alldisputed_invoices,
        'currency':default_currency


    }
    return data

def getallprojects_byvendor(vendor_id):
    allprojects=ContractMaster.objects.getproject_bycountry(1,vendor_id)
    projects=[]
    for allproject in allprojects:
        project_details=Projectcreation.objects.getproject_byid(allproject['projects'])
        projects.append({"name":project_details.projectname.name,"id":project_details.id})
    
    return projects

def getallcountries_byvendor(vendor_id):
    allprojects=ContractMaster.objects.getproject_bycountrywise(1,vendor_id,[])
    countries=[]
    for project in allprojects:
        country_details=Countries.objects.getcountry_by_id(project['country'])
        countries.append({"name":country_details.name,"id":country_details.id})
    return countries

def getallcurrencies_byvendor(vendor_id):
    currencies=InvoiceCostInvoice.objects.getallcurrencies_by_vendor(vendor_id)
    allcurrencies=[]
    for currency in currencies:
        allcurrencies.append({'name':currency['invoice_currency']})
    return allcurrencies
    
def getcreditnote_details_byvendor(vendor_details):
    default_currency=list(getdefaultcurrency_company(vendor_details.company_id))
    approved_credit_notes=CreditNoteContractInvoice.objects.get_credit_notes_byvendor_currency_approvedstatus(vendor_details.id,default_currency,vendor_details.company_id,4)
    approved_creditnote_amount=0
    for approved_credit_note in approved_credit_notes:
        amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', approved_credit_note.payment_currency_amount)))
        approved_creditnote_amount +=amount_without_currency

    unapproved_credit_notes=CreditNoteContractInvoice.objects.get_credit_notes_byvendor_currency_approvedstatus(vendor_details.id,default_currency,vendor_details.company_id,1)
    unapproved_creditnote_amount=0
    for unapproved_credit_note in unapproved_credit_notes:
        amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', unapproved_credit_note.payment_currency_amount)))
        unapproved_creditnote_amount +=amount_without_currency

    returned_rejected_credit_notes=CreditNoteContractInvoice.objects.get_return_rejected_credit_notes_byvendor_currency(vendor_details.id,default_currency,vendor_details.company_id)
    returned_rejected_credit_note_amount=0
    for returned_rejected_credit_note in returned_rejected_credit_notes:
        amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', returned_rejected_credit_note.payment_currency_amount)))
        returned_rejected_credit_note_amount +=amount_without_currency

    data={
        'approved_creditnote_amount':approved_creditnote_amount,
        'unapproved_creditnote_amount':unapproved_creditnote_amount,
        'returned_rejected_credit_note_amount':returned_rejected_credit_note_amount
    }
    return data


def getdefaultcurrency_company(company_id):
    company_details=Companies.objects.get_by_id(company_id)
    val=company_details.country
    try:
        return company_details.country.currency_symbol
    except :
        return []

def getinvoice_summary_details_filter(vendor_id,currencies,project_id,country_ids,services,tax,company_id):
    default_currency=getdefaultcurrency_company(company_id)
    allinvoice_by_currency_vendor=InvoiceCostInvoice.objects.getallinvoice_by_currency_vendor(vendor_id,currencies,project_id,country_ids,default_currency)
    allinvoices=[]
    filtered_invoice=[]
    if len(services) > 0:
        for invoice in allinvoice_by_currency_vendor:
            contract_details=ContractMaster.objects.getcontract_byid(invoice.contractid,services)
            if not contract_details:
                continue
            allinvoices.append(invoice)
    else:
        allinvoices=allinvoice_by_currency_vendor
    
    if len(tax) > 0:
        for allinvoice in allinvoices:
            contracttax_details=VendorCompanyTaxDetails.objects.getcontracttax_by_contract_taxtype(allinvoice.contractid,tax)
            if not contracttax_details:
                continue
            filtered_invoice.append(allinvoice)
    else:
        filtered_invoice=allinvoices
    
    allfiltered_invoice=[]
    for filterinvoice in filtered_invoice:
        amount_without_currency = float(''.join(filter(lambda x: x.isdigit() or x == '.', filterinvoice.invoice_total_amount)))
        # print(f"amount_without_currency {amount_without_currency} {filterinvoice.id} {filterinvoice.invoice_currency} {filterinvoice.payment_status}")
        currency_exists = None
        for invoice_data in allfiltered_invoice:
            if invoice_data['currency'] == filterinvoice.invoice_currency:
                currency_exists = invoice_data
                break

        if(not currency_exists):
            invoice_data = {
                'currency': filterinvoice.invoice_currency,
                'paid_amount': 0,
                'unpaid_amount': 0,
                'awaiting_amount':0,
                'disputed_amount':0
            }
            if(filterinvoice.invoice.approval_status == 1 and filterinvoice.payment_status == 1):
                invoice_data['unpaid_amount'] = amount_without_currency
            
            elif(filterinvoice.invoice.approval_status == 1 and filterinvoice.payment_status != 1):
                invoice_data['paid_amount'] = amount_without_currency
            
            elif(filterinvoice.invoice.approval_status==0 and filterinvoice.invoice.invoice_status==2 and filterinvoice.approval_status==1):
                invoice_data['awaiting_amount'] = amount_without_currency
            elif(filterinvoice.invoice.invoice_status==6 and filterinvoice.approval_status==6):
                invoice_data['disputed_amount'] = amount_without_currency
            allfiltered_invoice.append(invoice_data)
        else:
            if(filterinvoice.invoice.approval_status == 1 and filterinvoice.payment_status == 1):
                currency_exists['unpaid_amount'] += amount_without_currency
            
            elif(filterinvoice.invoice.approval_status == 1 and filterinvoice.payment_status != 1):
                currency_exists['paid_amount'] += amount_without_currency
            elif(filterinvoice.invoice.approval_status==0 and filterinvoice.invoice.invoice_status==2 and filterinvoice.approval_status==1):
                invoice_data['awaiting_amount'] += amount_without_currency
            elif(filterinvoice.invoice.invoice_status==6 and filterinvoice.approval_status==6):
                invoice_data['disputed_amount'] += amount_without_currency

    return allfiltered_invoice

      
def getproject_summary_details_filter(vendor_id,country_ids,company_id):
    total_project=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_id,None,country_ids)
    active_project=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_id,True,country_ids)
    inactive_project=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_id,False,country_ids)
    data={
        'total_project':total_project.count(),
        'active_project':active_project.count(),
        'inactive_project':inactive_project.count()
    }
    return data







   