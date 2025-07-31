from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.http import HttpResponse,BadHeaderError
from custom_auth.models import *
from django.db.models import Q
from projects.models import *

from irock.settings import *
from django.conf import settings

def vendorprimaryapprovermail(companyid,primary,companyrole,current_url):
    # print("companyid",companyid)
    print("primary",primary)
    primaryuser=User.objects.get(id=primary)
    company=Companies.objects.get(id=companyid)
    if Companies.objects.filter(id=companyid,image__isnull=True):
        # print("no images")
        imageurl=''
    else:
        imageurl=company.image.url
    fname=company.first_name
    lname=company.last_name
    fullname=fname+' '+lname
    # print("email",company.email)
    context={'areacode':company.areacode,'role':companyrole,
        'landline_countrycode':company.phone_countrycode,
        'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,
        'mobile':company.mobile,'website':company.website,
        'address':company.address,'image':imageurl,'email':company.email,'companyusername':fullname,
        'companyname':company.company_name,'approve_role':'Primary','title':primaryuser.Title,'firstname':primaryuser.name,'lastname':primaryuser.lastname,'url':current_url
        }

    subject = 'Addition to Vendor Approval Panel'
    html_message = render_to_string('vendorapproversemail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = primaryuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

#del
def vendorsecondaryapprovermail(companyid,secondary,companyrole,current_url):
    # print("companyid",companyid)
    print("secondary",secondary)
    secondaryuser=User.objects.get(id=secondary)
    company=Companies.objects.get(id=companyid)
    if Companies.objects.filter(id=companyid,image__isnull=True):
        # print("no images")
        imageurl=''
    else:
        imageurl=company.image.url
    fname=company.first_name
    lname=company.last_name
    fullname=fname+' '+lname
    context={'areacode':company.areacode,'role':companyrole,
        'landline_countrycode':company.phone_countrycode,
        'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,
        'mobile':company.mobile,'website':company.website,
        'address':company.address,'image':imageurl,'email':company.email,'companyusername':fullname,
        'companyname':company.company_name,'approve_role':'Secondary','title':secondaryuser.Title,'firstname':secondaryuser.name,'lastname':secondaryuser.lastname,'url':current_url
        }

    subject = 'Addition to Vendor Approval Panel'
    html_message = render_to_string('vendorapproversemail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = secondaryuser.email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)



def vendorsemail(v_id,title,name,current_url,vendorid,companyid,email,vendorstatus):
    
    print('a',title,name,vendorid,companyid,email,vendorstatus)
    company=Companies.objects.get(id=companyid)
    get_company=User.objects.filter(company_id=companyid).first()
    vendoruser=User.objects.get(id=vendorid)
    vendormaster=ContractMasterVendor.objects.get(id=v_id)
    if Companies.objects.filter(id=companyid).filter(Q(image__isnull=True) | Q(image='')):
        imageurl=''
    else:
        imageurl=company.image.url
    fname=company.first_name
    lname=company.last_name
    if (lname != None):
        fullname=fname+' '+lname
    else:
        fullname=fname
    url=f'{current_url}/vendorlogin' 
    live_link_invoice_url=f'{current_url}/projects/Guidelines_For_Invoice/{str(companyid)}'
    context={'areacode':company.areacode,'role':get_company.designation_role,
        'landline_countrycode':company.phone_countrycode,
        'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,
        'mobile':company.mobile,'website':company.website,
        'address':company.address,'image':imageurl,'company_email':company.email,'companyusername':fullname,'url':url,
        'companyname':company.company_name,'title':title,'name':name,'vendorstatus':vendorstatus,'vendorcompanyname':vendormaster.vendor_name,'vin':vendormaster.vin,'email':email,'password':'Hello@123'
        ,'invoice_url':live_link_invoice_url,'current_url':current_url,'phone_number_extenstion':''}
    user_data = User.objects.get(id=vendormaster.created_by.id) if vendormaster.created_by else None
    context['vendorcompanyname'] = vendormaster.vendor_name
    if user_data:   
        print('user_data',user_data)
        if user_data.roles_id == 3:
            print(f'landline_countrycode {user_data.phone_countrycode} lanline {user_data.phone} mobile_countrycode {user_data.mobile_countrycode} mobile {user_data.mobile}')
            context['areacode'] = user_data.areacode
            if user_data.phone_countrycode!= '':
                context['landline_countrycode'] = f'+{Basecountries.objects.get(id=user_data.phone_countrycode).phonecode}' if Basecountries.objects.filter(id=user_data.phone_countrycode).exists() else ''
            if user_data.mobile_countrycode!= '':
                context['mobile_countrycode'] = f'+{Basecountries.objects.get(id=user_data.mobile_countrycode).phonecode}' if Basecountries.objects.filter(id=user_data.mobile_countrycode).exists() else ''
            context['lanline'] = user_data.phone
            context['mobile'] = user_data.mobile
            context['phone_number_extenstion'] = f'-{user_data.phone_number_extenstion}'
            context['companyusername'] = f'{user_data.name} {user_data.lastname}' if user_data.lastname else user_data.name
            context['company_email'] = user_data.email
            context['role'] = user_data.designation_role
    subject = 'iROCK Vendor Registration'
    html_message = render_to_string('vendorbasicinfoemail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def vendorloginmail(subject,company,companyrole,vendor_id,user,userroles , current_url):
    print(company.email,companyrole,vendor_id,user,userroles)
    
    vendor_master=ContractMasterVendor.objects.get(id=vendor_id)
    if Companies.objects.filter(id=company.id).filter(Q(image__isnull=True) | Q(image='')):
        imageurl=''
    else:
        imageurl=company.image.url
    fname=company.first_name
    lname=company.last_name
    fullname=fname+' '+lname
    companyusername=company.first_name+' '+company.last_name
    fname=user.name
    lname=user.lastname
    fullname1=fname+' '+lname
    username=user.name+' '+user.lastname
    # phone = user.phone_countrycode
    # mobile = user.mobile_countrycode
    # mobile = user. areacode
    user_data = User.objects.get(id=user.id)
    print('user',user_data.phone_countrycode)
    if user_data.phone_countrycode != '':
        phonecountrycode= Basecountries.objects.get(id=user_data.phone_countrycode).phonecode if Basecountries.objects.filter(id=user_data.phone_countrycode).exists() else ''
    else:
        phonecountrycode=''
    mobilecountrycode= Basecountries.objects.get(id=user_data.mobile_countrycode).phonecode if Basecountries.objects.filter(id=user_data.mobile_countrycode).exists() else ''
    # url='https://irockinfo.mo.vc/vendorlogin' 
    url=f'{current_url}/vendorlogin' 
    if(userroles == 3):
        context={'areacode':user_data.areacode,'role':companyrole,
        'landline_countrycode':f'+{phonecountrycode}',
        'lanline':user_data.phone,'mobile_countrycode':f'+{mobilecountrycode}',
        'mobile':user_data.mobile,'website':company.website,
        'address':company.address,'image':imageurl,'email':user.email,'fullname':fullname1,'url':url,
        'companyname':company.company_name,'vin':vendor_master.vin,'v_email':vendor_master.contactpersonemail,'v_password':'Hello@123','v_name':vendor_master.contactpersonname+' '+vendor_master.contactpersonlastname,'title':vendor_master.contactpersontitle,'companyusername':username,'phone_number_extenstion':f'-{user_data.phone_number_extenstion}'}    
    else:
        context={'areacode':company.areacode,'role':companyrole,
        'landline_countrycode':company.phone_countrycode,
        'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,
        'mobile':company.mobile,'website':company.website,
        'address':company.address,'image':imageurl,'email':company.email,'fullname':fullname,'url':url,
        'companyname':company.company_name,'vin':vendor_master.vin,'v_email':vendor_master.contactpersonemail,'v_password':'Hello@123','v_name':vendor_master.contactpersonname+' '+vendor_master.contactpersonlastname,'title':vendor_master.contactpersontitle,'companyusername':companyusername}
    subject = subject
    html_message = render_to_string('vendorloginmail.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = vendor_master.contactpersonemail
    return mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)