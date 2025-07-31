from credit_note.templatetags.credit_custom_tags import new_round_of_two_values, round_of_two_values
from invoice.helpers import company_details
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core import mail
from datetime import date


def getCreditNoteDocumentlist():
    document_list=[{'name':'Credit Note','data':'1'},{'name':'Other Documents','data':'2'},{'name':'Contracts','data':'3'},{'name':'Price Table','data':'4'},{'name':'Related Invoice Docs','data':'5'}] 
    # document_list=[{'name':'Other Documents','data':'2'},{'name':'Contracts','data':'3'},{'name':'Price Table','data':'4'},{'name':'Related Invoice Docs','data':'5'}] 
    return document_list 
def newCreditNoteDocumentlist():
    # document_list=[{'name':'Credit Note','data':'1'},{'name':'Other Documents','data':'2'},{'name':'Contracts','data':'3'},{'name':'Price Table','data':'4'},{'name':'Related Invoice Docs','data':'5'}] 
    document_list=[{'name':'Other Documents','data':'2'},{'name':'Contracts','data':'3'},{'name':'Price Table','data':'4'},{'name':'Related Invoice Docs','data':'5'}] 
    return document_list 

def credit_return_mail(request,vendor_data,vendor,submit_name,invoice_data,comments,credit_no):
    # def invoive_return_mail(request,vendor_data,vendor,submit_name,invoice_data,comments,all_invoice):
    subject=f'Credit Note {submit_name}'
    url='https://irockinfo.mo.vc/vendorlogin' 
    context={'vendor':vendor,'submit_name':submit_name,'invoice_data':invoice_data,'comments':comments,'request':request,'credit_no':credit_no,'url':url}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('creditreturnmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor_data.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def credit_submission_mail_vendor(request,vendor_data,vendor):
    subject=f'Credit Note Received'
    date_today=get_date()
    url='https://irockinfo.mo.vc/vendorlogin' 
    context={'vendor':vendor,'request':request,'url':url,'date_today':date_today}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('creditsubmissionmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor_data.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def credit_submission_mail_user(request,recipientuser,vendor,all_credit,all_invoice,invoice):
    subject=f'Credit Note Received'
    url='https://irockinfo.mo.vc/vendorlogin' 
    context={'vendor':vendor,'request':request,'url':url,'recipientuser':recipientuser,'all_credit':all_credit,'invoice':invoice,'all_invoice':all_invoice}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('creditsubmissionmailuser.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def credit_approval_mail(request,recipientuser,vendor,all_credit,all_invoice,invoice,all_users,invoiceflow_modules):
    subject=f'Credit Note for Approval'
    url='https://irockinfo.mo.vc' 
    context={'vendor':vendor,'request':request,'url':url,'recipientuser':recipientuser,'all_credit':all_credit,'invoice':invoice,'all_invoice':all_invoice,'all_users':all_users,'invoiceflow_modules':invoiceflow_modules,'user_count':all_users.count()}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('creditapprovalmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def get_date():
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    return date_today


def credit_applied_mail(request,user,invoice_number,numbers_credit,date_today,get_submission_date):
    subject=f'Credit Note Applied to Invoice'
    url='https://irockinfo.mo.vc' 
    context={'request':request,'url':url,'recipientuser':user,'all_credit':numbers_credit,'all_invoice':invoice_number,'date_today':date_today}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('creditappliedmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)





def get_netpayable(amount,exchange_rate,taxes,split):
    if exchange_rate == 'N/A' or exchange_rate.strip() == '':
        exchange_rate=1
    if not amount:
        gross_amount=0
    gross_amount=round_of_two_values(float(round_of_two_values(float(amount)*(float(split)/100)))*float(exchange_rate))
    tax_amount=0
    for i in taxes:
        if i['taxpercentage']:
            tax_amount+=float(round_of_two_values(float(gross_amount)*(float(i['taxpercentage'])/100)) )
    tax_amount=float(gross_amount)-float(tax_amount)
    return new_round_of_two_values(tax_amount)
