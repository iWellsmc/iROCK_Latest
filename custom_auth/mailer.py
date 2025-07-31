from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.http import HttpResponse,BadHeaderError
# from django.contrib.auth.forms import PasswordResetForm
# from django.utils.http import urlsafe_base64_encode
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes

# from notifications.signals import notify
from custom_auth.models import User
from django.conf import settings

def send_confirmation_mail(company,url):
    subject = 'iROCK Proposal Form Acknowledgement'
    html_message = render_to_string('mail/confirmtemplate2.html', {'name': company.company_name,'url':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = company.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def send_approvel_mail(company,request):
    subject = 'iROCK – Approval Confirmation'
    # url='http://127.0.0.1:8000'
    # url='https://irockinfo.mo.vc/'
    url=f'{request.scheme}://{request.get_host()}'
    print('company.licensekey',company.licensekey)
    html_message = render_to_string('mail/approvetemplate2.html', {'cin_number':company.cin_number,'name': company.company_name,'request':request,'licenseingkey':company.licensekey,'email':company.email,'url':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = company.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def send_reject_mail(company):
    subject = 'Reject Email From iROCK Team'
    html_message = render_to_string('mail/rejecttemplate2.html', {'name': company.company_name,})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = company.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)



def email_enquiry(title,name,email,url):
    print('mailer',title,name,email)
    subject = 'iROCK Enquiry Acknowledgement'
    # pdf='http://127.0.0.1:8000/downloadbrochure'
    # pdf='https://irockinfo.mo.vc/downloadbrochure'
    pdf = f'{url}/downloadbrochure'
    html_message = render_to_string('mail/enquiryemail.html',{'title':title,'name': name,'url':pdf,'current_url':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    
def email_proposal(name,title,email_id,id,current_url):
    print('mailer',title,name,email_id)
    subject = 'iROCK Proposal Form'
    # url='http://127.0.0.1:8000/proposal_check/'+str(id)
    # url='https://irockinfo.mo.vc/proposal_check/'+str(id)
    url = f'{current_url}/proposal_check/{str(id)}'
    html_message = render_to_string('mail/proposalform-mail.html', {'title':title,'name': name,'link':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email_id
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def email_forgotpassword(urls,name,lastname,email_id,id):
    # print('mailer',title,name,email_id)
    subject = 'iROCK Reset Password'
    # url='http://127.0.0.1:8000/proposal_check/'+str(id)
    url = f'{urls}/resetpasscode/{id}/'
    # url=f'https://facebook.com{email_id}{id}{cinnum}'
  
    html_message = render_to_string('mail/email-templates.html', {'title':'Dear','name': name,'lastname':lastname,'link':url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email_id
    status = mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    if status:
        print('sent')
    else:
        print('there any problem')