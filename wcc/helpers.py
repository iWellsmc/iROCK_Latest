from custom_auth.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core import mail
from django.db.models import Q
def getsupportsdata():
    supports_docs=[{'id':3,'name':'Call off Instructions'},{'id':4,'name':'Mobilization Notices'},{'id':5,'name':'Material Delivery Tickets/Certificates'},{'id':6,'name':'Timesheets'},{'id':7,'name':'Third Party Invoices'},{'id':8,'name':'Other Supporting Documents'}]
    return supports_docs

def change_key_name(objects_list, old_key_name, new_key_name):
    for obj in objects_list:
        if old_key_name in obj:
            obj[new_key_name] = obj.pop(old_key_name)
    return objects_list

def wcccreatedmail(request,user,wcc_data,wcc_work,vendor,template_name,approver_name=''):
    title=f'{user.Title}.' if user.Title != None else ''
    lastname=f'{user.lastname}' if user.lastname != None else ''
    user_name=f"{title} {user.name} {lastname}"
    subject = 'iROCK - Work Completion Certificate (WCC) for Approval'
    context={'full_name':user_name,'wcc_data':wcc_data,'wcc_work':wcc_work,'vendor':vendor,'approver_name':approver_name}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string(template_name+'.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
    return msg

def wccsubmissionmail(request,user,wcc_data,wcc_work,template_name,approver_name,date,contract_data):
    approver=User.objects.filter(id=approver_name).first()
    title=f'{user.Title}.' if user.Title != None else ''
    lastname=f'{user.lastname}' if user.lastname != None else ''
    user_name=f"{title} {user.name} {lastname}"
    subject = 'Work Completion Certificate Received'
    context={'full_name':user_name,'wcc_data':wcc_data,'wcc_work':wcc_work,'approver_name':approver,'date':date,'request':request,'contract_data':contract_data}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string(template_name+'.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email
    msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
    return msg

def wccreturnrejectmail(request,user,wcc_data,wcc_work,approver_name,date, status, reasons):
    
    approver=User.objects.filter(id=approver_name).first()
    title=f'{user.Title}.' if user.Title != None else ''
    lastname=f'{user.lastname}' if user.lastname != None else ''
    user_name=f"{title} {user.name} {lastname}"
    subject = 'Work Completion Certificate (WCC) '+status
    context={'full_name':user_name,'wcc_data':wcc_data,'wcc_work':wcc_work,'approver_name':approver,'date':date,'request':request,'status':status,'reasons':reasons}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('returnrejectmail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to =user.email
    msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
    return msg

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

# def station_station_email(request,user,wcc_data,wcc_work,vendor,approver_name):
#     user_name=f"{user.Title}.{user.name} {user.lastname}"
#     if Companies.objects.filter(id=request.company.id).filter(Q(image__isnull=True) | Q(image='')):
#         imageurl=''
#     else:
#         imageurl=request.company.image.url
#     company=Companies.objects.get(id=request.company.id)
#     companyusername=company.first_name+' '+company.last_name
#     url=f'{request.scheme}://{request.get_host()}'
#     subject = 'Work Completion Certificate (WCC) for Approval'
#     context={'full_name':user_name,'wcc_data':wcc_data,'wcc_work':wcc_work,'vendor':vendor,'areacode':company.areacode,
#     'landline_countrycode':company.phone_countrycode,
#     'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,
#     'mobile':company.mobile,'website':company.website,
#     'address':company.address,'image':imageurl,
#     'companyname':company.company_name,
#     'cin':company.cin_number,
#     'email':company.email,'url':url,'companyusername':companyusername,'role':'Client Administrator','approver_name':approver_name}
#     html_message = render_to_string('station_to_station.html', context)
#     plain_message = strip_tags(html_message)
#     from_email = settings.EMAIL_HOST_USER
#     to = user.email
#     msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
#     return msg


def wcc_status_mail(request,wcc_data,wcc_work,vendor,status,comments):
    con_status=f'{status}'.capitalize()
    subject = 'iROCK - Work Completion Certificate (WCC) for '+con_status
    context={'wcc_data':wcc_data,'wcc_work':wcc_work,'vendor':vendor,'status':status,'comments':comments}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('wcc_status_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor.contactpersonemail
    msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
    return msg

def wcc_approve_mail(request,wcc_data,wcc_work,vendor):
    subject = ' Work Completion Certificate (WCC) Approved'
    context={'wcc_data':wcc_data,'wcc_work':wcc_work,'vendor':vendor}
    comp_data=company_details(request)
    context.update(comp_data)
    html_message = render_to_string('wcc_approve_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor.contactpersonemail
    msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
    return msg

def wcc_approve_mail_robust(request,wcc_data,wcc_work,vendor):
    for obj in vendor:
        subject = ' Work Completion Certificate (WCC) Approved'
        context={'wcc_data':wcc_data,'wcc_work':wcc_work,'vendor':obj}
        comp_data=company_details(request)
        context.update(comp_data)
        html_message = render_to_string('wcc_approve_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = obj.contactpersonemail
        msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)   
    return True