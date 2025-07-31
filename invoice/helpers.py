from django.core import mail
from invoice.models import *
from django.db.models import Q
from custom_auth.models import *
from datetime import datetime,date
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
from datetime import timedelta
from .templatetags.invoice_custom_tags import find_fully_paid

# Local application/library-specific imports
from InvoiceGuard.models import RoleRight
from projects.models import ContractMaster,ProjectDevelopmentDiscipline,ProjectDevelopmentSubType,Amendment
from cost_code.models import CostCodeMain,CostCodeVendor



def getDocumentlist():
    document_list=[{'name':'Invoice','data':'1'},{'name':'Work Completion Cert.','data':'2'},{'name':'Call off Instructions','data':'3'},{'name':'Mobilization Notices','data':'4'},{'name':'Material Delivery Tickets/Cert.','data':'5'},{'name':'Timesheets','data':'6'},{'name':'Third Party Invoices','data':'7'},{'name':'Other Documents','data':'8'},{'name':'Contracts','data':'9'},{'name':'Price Table','data':'10'}]
    return document_list

def other_documents():
    document_list=[{'name':'Work Completion Cert.','data':'2'},{'name':'Call off Instructions','data':'3'},{'name':'Mobilization Notices','data':'4'},{'name':'Material Delivery Tickets/Cert.','data':'5'},{'name':'Timesheets','data':'6'},{'name':'Third Party Invoices','data':'7'},{'name':'Other Documents','data':'8'}]
    return document_list

def getinvoiceDate(companydateformat,date):
    print(f'companydateformat {companydateformat}')
    if (date != ""):
        if (companydateformat == 'dd-M-yy'):
            convert_date=datetime.strptime(date,"%d-%b-%Y").date()
        elif (companydateformat == 'dd-mm-yy'):
            try:
                convert_date=datetime.strptime(date,"%d-%b-%Y").date()
            except:
                convert_date=datetime.strptime(date,"%d-%m-%Y").date()
        elif (companydateformat == 'dd/mm/yy'):
            print('yead',date)
            convert_date=datetime.strptime(date,"%d/%m/%Y").date()
        elif (companydateformat == 'mm-dd-yy'):
            convert_date=datetime.strptime(date,"%m-%d-%Y").date()
        elif (companydateformat == 'mm/dd/yy'):
            convert_date=datetime.strptime(date,"%m/%d/%Y").date()
        elif (companydateformat == 'yy-mm-dd'):
            convert_date=datetime.strptime(date,"%Y-%m-%d").date()
        elif (companydateformat == 'yy/mm/dd'):
            convert_date=datetime.strptime(date,"%Y/%m/%d").date()
        else:
            convert_date=datetime.strptime(date,"%d-%b-%Y").date()
    else:
        convert_date=''
    return convert_date


def invoive_submission_mail(request,company,vendor):
    subject = 'Invoice Received'
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    context ={'company': company,'date':date_today,'vendor':vendor}
    comp_data=company_details(request)
    context.update(comp_data)
    print('context',context)
    html_message = render_to_string('invoicesubmissionmail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor.email
    print('to',to)
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_conform_costcode_mail(request,vendor_details,all_invoice,invoice_details,email):
    subject = 'Cost Code Updated'
    context ={'all_invoice': all_invoice,'service_name':invoice_details.name_service,'vendor_details':vendor_details,'company_name':request.company.company_name,'conform_costcode_comments':invoice_details.conform_costcode_comments}
    html_message = render_to_string('conformcostcodemail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def mail_send_to_verified_bank_user(request,pi_number,check_data,all_invoice,name_of_service):
    
    subject = 'Payment Code Verified'
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    bank_user_mail = check_data.verified_bank_user.email
    bank_user_name = check_data.verified_bank_user.name +" "+ check_data.verified_bank_user.lastname
    vendor_name = check_data.invoicecost.vendor.vendor_name
    context = {'bank_user_mail':bank_user_mail,
    'all_invoice':all_invoice,'pi_number':pi_number,
    'name_of_service':name_of_service,'bank_user_name':bank_user_name,
    'vendor_name':vendor_name,'request':request}
    comp_data=company_details(request)
    context.update(comp_data)
    print('context',context)
    html_message = render_to_string('otpconfirmationmail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = bank_user_mail
    print('to',to)
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    




def invoice_submission_fpoc(company,user,invoice,vendor,request):
    subject='Invoice Received'
    context={'user':user,'company':company,'invoice':invoice,'vendor':vendor,'request':request}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('invoicesubmissionfpoc.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def invoive_approval_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,invoiceflow_modules):
    subject='Invoice for Approval'
    context={'recipientuser':recipientuser,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'approved_users':approved_users,'invoiceflow_modules':invoiceflow_modules,'user_count':approved_users.count()}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('invoiceapprovedfpoc.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def invoive_approval_mail_step2(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,invoiceflow_modules):
    subject='Invoice for Payment Approval'
    context={'recipientuser':recipientuser,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'approved_users':approved_users,'invoiceflow_modules':invoiceflow_modules}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('taxconfirmationmail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def tax_confirmation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users):
    subject='Invoice for Payment Approval'
    context={'recipientuser':recipientuser,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'approved_users':approved_users,'approved_users_count':approved_users.count()}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('taxconfirmationmail_step2.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def payment_generation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users):
    subject='Invoice for Payment Approval'
    context={'recipientuser':recipientuser,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'approved_users':approved_users,'approved_users_count':approved_users.count()}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('payment_generation_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def payment_confirmation_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,pi_number):
    subject='Instructions For Payment Approval'
    total_amount=InvoiceCostInformation.objects.filter(invoice_id=invoice_detail.id).first()
    payment_details=PaymentInstruction.objects.get_by_payment(invoice_detail.id)
    context={'recipientuser':recipientuser,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'approved_users':approved_users,'total_amount':total_amount,'pi_number':pi_number,'payment_details':payment_details}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('payment_confirmation_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def invoice_payment_mail(request,recipientuser,vendor,invoice_detail,all_invoice,approved_users,comments,pi_number):
    subject='Approved Payment Instructions'
    total_amount=InvoiceCostInformation.objects.filter(invoice_id=invoice_detail.id).first()
    context={'recipientuser':recipientuser,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'approved_users':approved_users,'total_amount':total_amount,'comments':comments,'approved_users_count':approved_users.count(),'pi_number':pi_number}
    comp_data=company_details(request)
    context.update(comp_data)
    #chnage other html page
    html_message = render_to_string('payment_confirmation_mail2.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = recipientuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def payment_receipt_vendor(request,vendor,invoice_detail,all_invoice,pk,payment_count):
    subject='Payment on Invoices'
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    paid_status=find_fully_paid(pk)
    if paid_status :
        payment_status='Paid'
    else :
        payment_status= 'Partially paid'
    total_invoice=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True,payment_count=payment_count)
    payment_split = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
    paid_invoice_cost=PaymentReceipt.objects.filter(invoice_id=invoice_detail.id)
    unpaid_invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=invoice_detail.id).exclude(id__in=paid_invoice_cost.values_list('invoice_cost_id',flat=True))
    context={'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'date_today':date_today,'paid_invoice_cost':paid_invoice_cost,'unpaid_invoice_cost':unpaid_invoice_cost,'total_invoice':total_invoice, 'payment_status ':payment_status ,"payment_split":len(payment_split)}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('payment_receipt_vendor.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def payment_receipt_confirmation(request,get_user,vendor,invoice_detail,all_invoice,pk,payment_count):
    subject='Payment on Invoices'
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    paid_status=find_fully_paid(pk)
    if paid_status :
        payment_status='Paid'
    else :
        payment_status= 'Partially paid'

    payment_split = list(PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True).values_list('payment_count',flat=True).distinct())
    total_invoice=PaymentInstruction.objects.filter(invoicecost__invoice_id=pk,status=True,payment_count=payment_count)
    paid_invoice_cost=PaymentReceipt.objects.filter(invoice_id=invoice_detail.id)
    unpaid_invoice_cost=InvoiceCostInvoice.objects.filter(invoice_id=invoice_detail.id).exclude(id__in=paid_invoice_cost.values_list('invoice_cost_id',flat=True))
    context={'user':get_user,'vendor':vendor,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'date_today':date_today,'paid_invoice_cost':paid_invoice_cost,'unpaid_invoice_cost':unpaid_invoice_cost,'total_invoice':total_invoice , 'payment_status':payment_status ,"payment_split":len(payment_split)}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('receiptconfirmation.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = get_user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def invoive_return_mail(request,vendor_data,vendor,submit_name,invoice_data,comments,all_invoice,submit_type):
    subject=f'Invoice {submit_name}'
    if submit_type =='3':
        subject=f'Invoice {submit_name} for Clarification'
    url='https://irockinfo.mo.vc/vendorlogin' 
    context={'vendor':vendor,'submit_name':submit_name,'invoice_data':invoice_data,'comments':comments,'request':request,'all_invoice':all_invoice,'url':url}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('invoicereturnmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor_data.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def invoice_Settlement_mail(request,vendor_data,vendor,submit_name,invoice_detail,comments,all_invoice,disputed,approved):
    subject=f'Invoice Disputed'
    context={'vendor':vendor,'submit_name':submit_name,'invoice_data':invoice_detail,'comments':comments,'request':request,'all_invoice':all_invoice,'approved':approved,'disputed':disputed}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('invoicesettlementmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor_data.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def bank_verification_mail(request,user,bank_name,code):
    subject='Payment Instruction Received'
    today = date.today()
    date_today = today.strftime("%d-%b-%Y")
    context={'user':user,'bank_name':bank_name,'request':request,'date_today':date_today,'code':code}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('bankverificationmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def disputed_invoice_mail(request,vendor,submit_name,invoice_data,comments,all_invoice,vendor_name):
    subject=f'Invoice {submit_name}'
    context={'vendor':vendor,'submit_name':submit_name,'invoice_data':invoice_data,'comments':comments,'request':request,'all_invoice':all_invoice,'vendorname':vendor_name}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('disputeinvoicemail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message) 

def response_to_vendor_mail(request,vendor,all_invoice,url,invoice,team):
    subject=f'Response to Returned Invoice'
    context={'request':request,'vendor':vendor,'all_invoice':all_invoice,'url':url,'invoice':invoice,'team':team}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('responsemail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor.email
    print(f'{all_invoice}--- all_invoice,vendor---{vendor},url {url}, invoice {invoice}, team {team}')
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message) 


def moved_as_dispute_mail(request,user,all_invoice,url,invoice,vendor,comments):
    subject=f'Recommendation for Invoice Dispute'
    context={'request':request,'user':user,'all_invoice':all_invoice,'url':url,'invoice':invoice,'vendor':vendor,'comments':comments}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('moved_as_dispute.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    print(f'user {user},all_invoice {all_invoice},url {url}, invoice {invoice}')
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def dispute_vendor_acceptmail(request,user,all_invoice,invoice_detail,vendor):
    url='https://irockinfo.mo.vc/vendorlogin' 
    subject=f'Disputed Invoice Accepted and Resolved'
    context={'request':request,'user':user,'all_invoice':all_invoice,'url':url,'invoice_detail':invoice_detail,'vendor':vendor}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('dispute_vendor_acceptmail.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def dispute_vendor_acceptmail_touser(request,user,all_invoice,invoice_detail,vendor):
    url='https://irockinfo.mo.vc/' 
    subject=f'Disputed Invoice accepted by {request.user.name}'
    context={'request':request,'user':user,'all_invoice':all_invoice,'url':url,'invoice_detail':invoice_detail,'vendor':vendor}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('dispute_vendor_acceptmail_touser.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    print(f'to {to}')
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def bank_user_approvalmail(request,get_user,instruction_number,vendor,invoice_detail,all_invoice,comments):
    subject='Approved Payment Instructions'
    context={'user':get_user,'instruction_number':instruction_number,'request':request,'all_invoice':all_invoice,'invoice_detail':invoice_detail,'company':request.company,'vendor':vendor,'comments':comments}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('bankuserapprovalmail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = get_user.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def dispute_vendor_declinemail_touser(request,user,all_invoice,invoice_detail,vendor,comments):
    url='https://irockinfo.mo.vc/' 
    subject=f'Disputed Invoice Contested by {request.user.name}'
    context={'request':request,'user':user,'all_invoice':all_invoice,'url':url,'invoice_detail':invoice_detail,'vendor':vendor,'comments':comments}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('declinemail_touser.html',context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    print(f'to {to}')
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def invoiceflowapprovemail():
    return


def company_details(request):
    if Companies.objects.filter(id=request.company.id).filter(Q(image__isnull=True) | Q(image='')):
        imageurl=''
    else:
        imageurl=request.company.image.url
    company=Companies.objects.get(id=request.company.id)
    companyusername=company.first_name+' '+company.last_name
    url=f'{request.scheme}://{request.get_host()}'
    data={'areacode':company.areacode,'landline_countrycode':company.phone_countrycode,'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,'mobile':company.mobile,'website':company.website,'address':company.address,'image':imageurl,'companyname':company.company_name,'cin':company.cin_number,'email':company.email,'url':url,'companyusername':companyusername,'role':'Client Administrator'}
    return data




def get_payment_detail(invoice,invoice_cost): 
    get_len=0
    payment_term=list(PaymentInstruction.objects.filter(invoicecost_id=invoice_cost,invoicecost__invoice_id=invoice,status=True).values_list('bankuser_verification',flat=True))
    if 1 in payment_term:
        get_len=1
    return get_len

def add_invoice_time(now,company_invoice_time):
    if company_invoice_time.time_unit == 2:
        calculate_time=now+timedelta(minutes=company_invoice_time.time_allotted)
    elif company_invoice_time.time_unit == 0:
        calculate_time=now+timedelta(hours=company_invoice_time.time_allotted)
    else :
        calculate_time=now+timedelta(days=company_invoice_time.time_allotted)
    return calculate_time

def getreport_css(encoded_image):
    pdfsheet_style = """
        .head-inv-pre {
            color: #AF2B50;
            font-weight: 600;
            font-size:15px;
        }
        @page  {
            size: A4 landscape; /* can use also 'landscape' for orientation */
            margin-right:1cm !important;
            margin-left:1cm !important;

        }
        @page {
            margin-top:150px !important;
            margin-bottom:100px !important;

            @top-center{
                content: element(header);
                align-items: center;
                line-height: 1.3;
                width: 100%;
                margin-top: 40px;
                justufy-content: center;
                text-align: center;
            }
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10px;
                width: 20% !important;
                margin-right: 0px;
                padding:20px 0px; 
            }

            @bottom-left {
                content: element(footer);
                width: 100% !important;
                margin-top:-50px; 
            }
        }
        footer {
            position: running(footer);
            font-size:10px !important;
            /*height: 150px;*/
        }
        
        header{
            position: running(header);
            font-size:10px !important;
        }
        * {
            font-family: Arial, Helvetica, sans-serif;
        }

        

        .logo {
            margin: 10px 0px 10px 10px !important;
            background-image: url('data:image/png;base64,"""+encoded_image+"""');
            background-repeat: no-repeat; 
            width: 150px !important;
            height: 75px !important;
            object-fit: cover;
            text-align: left !important;
        }

        .from-head {
            color: #AF2B50;
            font-weight: 600;
            font-size:20px;
            text-align: center;
            margin: 10px 10px;
            width: 100% !important;
        }

        .company-details {
            margin: auto;
            text-align: center;
            width: 80% !important;
        }

        .company-details h4 {
            margin-bottom: 5px;
        }

        .company-details p {
            color: #000;
            font-size: 12px;
            font-weight: 500;
            margin-top: 0px;
            display: inline-block;
        }

        .parent {
            justify-content: center;
            width: 100%;
            margin: auto;
        }
       
        .row_border_header {
            border-bottom: none;
        }

        .d-flex {
            display: flex;
        }

        .justify-content-center {
            justify-content: center;
        }

        .align-items-center {
            align-items: center;
        }

        .justify-content-end {
            justify-content: end;
        }

        .col-2 {
            
        }

        .col-6 {
            width: 50%;
        }

        .col-4 {
            width: 33.33%;
        }

        .col-10 {
            width:83.33333333%;
        }

        .col-12 {
            width: 100%;
        }

        .vendorpdf-table {
            width: 100%;
            border-collapse: collapse;
        }
        .vendorpdf-table th {
            color: #000;
            font-size: 14px !important;
            font-weight: 600 !important;
            text-align: center;
        }
        .vendorpdf-table td {
            color: #000;
            font-size: 14px;
            text-align: center;
        }
        .vendorpdf-table th, td {
            padding: 5px 5px;
            border: 1px solid #e3e3e3;
        }
        .text-left {
            text-align: left !important;
        }

        
        /**************** Vendor login PDF ***************/
         .head-inv-pre-vend {
            color: #AF2B50;
            font-weight: 600;
            font-size:20px;
            margin-top: 0px;
        }
        .vin-no {
    margin: 10px auto;
}

.vin-table td {
     padding: 5px 5px 5px 0px;  

}

.vin-no td {
    border: none !important;
}

.ven-name td {
    border: none !important;
}

.vin-no label {
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 0px;
}

.dot-colon {
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
}

.vin-no span {
    color: #000 !important;
    font-size: 15px;
    font-weight: 500;
}

.ven-name {
    margin: 10px auto;
}

.ven-name label {
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 0px;
}

.ven-name span {
    color: #000 !important;
    font-size: 15px;
    font-weight: 500;
}

.ccv-table {
    width: 100%;
    border: 1px solid #e3e3e3 !important;
    border-collapse: collapse;
    margin-top: 15px;
}

.ccv-table th {
    text-align: center;
    color: #000;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 5px 5px;
}

.ccv-table th, td {
    border: 1px solid #e3e3e3 !important;
    border-collapse: collapse;
}

.ccv-table td {
    text-align: center;
    color: #000;
    font-size: 14px;
    padding: 5px 5px;
}
.wcc-name td {
    padding: 5px 5px;
}

.wcc-name td:nth-child(1){
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
    width: 100px;
}

.wcc-name td:nth-child(2){
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
}

.wcc-name td:nth-child(3){
    color: #017474;
    font-size: 15px;
    font-weight: 600;
    /* width: 250px; */
    /* padding-left: 25px; */
}

.wcc-flow {
    width: 35%;
}

.wcc-flow td {
    padding: 5px 5px;
}

.wcc-flow td:nth-child(1){
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
    width: 100px;
}
.wcc-flow td:nth-child(2){
    color: #AF2B50;
    font-size: 15px;
    font-weight: 600;
    width: 0px;
}

.wcc-flow td:nth-child(3){
    position: relative;
}

.down-arrow-sig img {
    position: absolute;
    right: 10px;
    top: 15px;
    transform: translateX(-50%);
}

        /**************** Vendor login PDF ****************/


      /**************** Invoice Register Report Page ****************/

.report-invoice-table {
    width: 100%;
    border-collapse: collapse;
}

.report-invoice-table th {
    padding: 8px 4px;
    font-size: 12px;
    text-align:center;
    border: 1px solid #c7c7c7;
}

.report-invoice-table td {
    padding: 8px 4px;
    font-size: 12px;
    border: 1px solid #c7c7c7;
}

            """
    
    return pdfsheet_style


def getInvoiceModule(module,pk,payment_count=None):
    urls=f"invoice/vendorbasedinvoice"
    if (module != ""):
        if (module == 1):
            urls=f"invoice/checklist/{pk}"
        elif (module == 2):
            urls=f"invoice/invoiceapproval/{pk}"
        elif (module == 3):
            urls=f"invoice/exchangerate/{pk}"
        elif (module == 4):
            urls=f"invoice/generatepayment/{pk}"
        elif (module == 5):
            urls=f"invoice/signatory/{pk}/{payment_count}"
        elif (module == 6):
            urls=f"invoice/accountpayable/{pk}/{payment_count}"
        else:
            urls=f"invoice/getinvoicesplit/{pk}"
    return urls

def getinvoiceroute(module):
    urls=f'invoicequeryhistory'
    if (module != ""):
        if (module == 1):
            urls=f"checklist"
        elif (module == 2):
            urls=f"invoiceapproval"
    return urls

def returned_count_invoice_credit(pk,invoice_type):
    if invoice_type == 1: #invoice
        try:
            return AddNewDisputedQuery.objects.filter(query_id=pk).last().returned_count
        except:
            return 1
    else:
        #creditnote
        return

def getrights_by_name(rights_name,role):
    check_rights=RoleRight.objects.check_module_rights(role.id,rights_name)
    return check_rights 


def getvendorcostcode_bycontracts(contract_id,request,vendor , contracttype=None ):
    costcode_main_set = set()
    if contracttype == 'original':
        contract_masters=ContractMaster.objects.getcontract(contract_id)
        projectdevelopmentdiscipline=ProjectDevelopmentDiscipline.objects.getdevelopment_details(contract_masters.projectdiscipline_id)
        contract_ids=contract_masters.id
    else:
        contract_masters=Amendment.objects.filter(id=contract_id ,status=1).first()
        projectdevelopmentdiscipline=ProjectDevelopmentDiscipline.objects.getdevelopment_details(contract_masters.service.projectdiscipline_id)
        contract_ids=contract_masters.service.id

    level1_discipline=projectdevelopmentdiscipline.project_discipline
    
    if projectdevelopmentdiscipline.development_type.development.development_type == 'Oil_Development':
        level1_development_type=1
    elif projectdevelopmentdiscipline.development_type.development.development_type == 'Gas_Development':
        level1_development_type=2
    elif projectdevelopmentdiscipline.development_type.development.development_type == 'Unconventional_Oil':
        level1_development_type=3
    else:
        level1_development_type=4

    if contracttype == 'original':
        level2_discipline=ProjectDevelopmentSubType.objects.getdetails_byid(contract_masters.projectdisciplinetype_id)
    else :
        level2_discipline=ProjectDevelopmentSubType.objects.getdetails_byid(contract_masters.service.projectdisciplinetype_id)
    level2_discipline=level2_discipline.discipline_subtype.id
    costcode_by_level1_level2=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_discipline,level1_development_type,level2_discipline,request.company)
    if costcode_by_level1_level2:
        costcode_main_set.add(costcode_by_level1_level2.id)
    allcostcode=list(costcode_main_set)
    vendors_list=CostCodeVendor.objects.get_vendor_data(vendor,1,allcostcode).filter(contractid=contract_ids)
    return vendors_list
