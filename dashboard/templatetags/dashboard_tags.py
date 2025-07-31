
from django import template
register = template.Library()


@register.simple_tag
def getinvoiceamount_by_currency(currency,invoice_summary,awaitedinvoice_summary,disputedinvoice_summary):
    data={}
    for approved_invoice in invoice_summary['allinvoice_gross_total']:
        if approved_invoice['currency'] == currency:
            data['approved_invoice_paid']=approved_invoice['invoice_paid_amont']
            data['approved_invoice_unpaid']=approved_invoice['invoice_unpaid_amount']
    
    for awaited_invoice in awaitedinvoice_summary['allinvoice_gross_total']:
        if awaited_invoice['currency'] == currency:
            data['awaited_invoice']=awaited_invoice['total_amount']
    
    for disputed_invoice in disputedinvoice_summary['allinvoice_gross_total']:
        if disputed_invoice['currency'] == currency:
            data['disputed_invoice']=disputed_invoice['total_amount']


    return data

   

