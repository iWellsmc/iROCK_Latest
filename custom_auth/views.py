# from turtle import update
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView,ListView,UpdateView,View
from projects.models import ContractMasterVendor,UserRights,Projectcreation
from projects.models import *
from custom_auth.models import FontFamily
# from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
import requests
from custom_auth.forms import Usercreationform,EnquiryFrom
# from django.contrib.auth.hashers import make_password
# from .forms import Generalsettingform
from django.urls import reverse_lazy
from custom_auth.models import *
import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
# from django.views.decorators.cache import cache_controlfrom 
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache
from django.db.models import Q
import os
from django.utils import timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from custom_auth.mailer import send_confirmation_mail,send_approvel_mail,send_reject_mail,email_enquiry,email_proposal,email_forgotpassword
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from custom_auth.helpers import companygeneratecin,markas_read_status
from django.template.loader import render_to_string
from notifications.models import Notification
from notifications.signals import notify
from django.core.paginator import Paginator
from django.views.generic import View
import mimetypes
# from django.views.decorators.csrf import csrf_protect
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime,timedelta
from django.contrib.auth.models import Group
import uuid
from invoice.models import *
from projects.helpers import create_user_log

from .fixtures.UserData import user_data
import base64 
from django.core.files.base import ContentFile
import string    
import random  
from wcc.models import *
from invoice.templatetags.invoice_custom_tags import custom_range_func
 
from .helpers import userlog
from custom_auth.models import userlog
from django.conf import settings



def Vendorlogin(request):
    if (request.POST):
        print(request.POST)
        vin=request.POST.get('vin')
        email=request.POST.get('email')
        password=request.POST.get('password')
        vendoruser=''
        if (ContractMasterVendor.objects.filter(vin=vin,contactpersonemail=email,status=1).exists()):
            vendoruser= ContractMasterVendor.objects.filter(vin=vin,contactpersonemail=email,status=1).first()
            print('a')
        elif (ContractMasterVendor.objects.filter(vin=vin,official_primary_email=email,status=1).exists()):
            vendoruser= ContractMasterVendor.objects.filter(vin=vin,official_primary_email=email,status=1).first()
        elif (ContractMasterVendor.objects.filter(vin=vin,official_secondary_email=email,status=1).exists()):
            vendoruser= ContractMasterVendor.objects.filter(vin=vin,official_secondary_email=email,status=1).first()
        print('a',vendoruser)
        if vendoruser is None or vendoruser == '':
            messages.add_message(request, messages.ERROR, 'Vendor does not exist or Invalid Vin number')
            return HttpResponseRedirect(reverse_lazy('custom_auth:vendorlogin'))
        # if vendoruser.vin != vin:
        #     messages.add_message(request, messages.ERROR, 'Invalid Vin number')
        #     return HttpResponseRedirect(reverse_lazy('custom_auth:vendorlogin'))
        get_vendoruser=User.objects.get(email=email,company_id=vendoruser.company_id,cin_number=vin,status=1)
        # print('get_vendoruser',get_vendoruser)
        userpassword=get_vendoruser.password
        print('pa',userpassword)
        matchcheck= check_password(password, userpassword)
        if matchcheck:
            vendorlogin = authenticate_vendoruser(vin=vin,email=email,password=password,vendor=vendoruser)
            login(request, vendorlogin)
            return redirect('dashboard:dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Email ID or Password')
            return HttpResponseRedirect(reverse_lazy('custom_auth:vendorlogin')) 
    return render(request,'vendorlogin.html')

def authenticate_vendoruser(vin,email, password,vendor):
    try:
        get_vendor=ContractMasterVendor.objects.filter(id=vendor.id,vin=vin,status=1).first()
        if (get_vendor != None):
            user = User.objects.get(email=email,company_id=get_vendor.company_id,cin_number=vin,status=1)
            if user.loginstatus == 0:
                User.objects.filter(email=email,company_id=get_vendor.company_id,cin_number=vin,status=1).update(loginstatus=1)
            elif user.loginstatus == 1:
                User.objects.filter(email=email,company_id=get_vendor.company_id,cin_number=vin,status=1).update(loginstatus=2)
            print(user)
        else:
            return None
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

        return None

class LoginView(FormView):
    
    """login view"""
    login_required = True
    form_class = forms.LoginForm
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'login.html'
    # success_url = reverse_lazy('custom_auth:keyactivationpage')
    # @method_decorator(csrf_exempt,name='dispatch')
    # @csrf_exempt
    # def dispatch(self,request,*args,**kwargs):
    #     return super(LoginView,self).dispatch(request,*args,**kwargs)

        # if self.request.method == 'POST':
        #     dispatch_method = method_decorator(csrf_exempt)(dispatch_method)

        # return dispatch_method(request,*args, **kwargs)
        
    def form_valid(self, form):
        print('data')
        """ process user login"""
        credentials = form.cleaned_data
        current_timestamp = int(datetime.now().timestamp())

        print("credentials",credentials)
        if User.objects.filter(cin_number=credentials['cin'],email=credentials['email'],roles_id=3,status=1).exists():
            # user=User.objects.filter(email=credentials['email'],roles_id=3,status=1).first()
            user=User.objects.filter(cin_number=credentials['cin'],email=credentials['email'],roles_id=3,status=1).first()
            if user is None:
                messages.add_message(self.request, messages.ERROR, 'User does not exists')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            if user.cin_number != credentials['cin']:
                messages.add_message(self.request, messages.ERROR, 'Invalid CIN number')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            userpassword=user.password
            p=credentials['password']
            matchcheck= check_password(p, userpassword)
            if matchcheck:
                login(self.request, user)
                previous_login_date=user.previous_login_date
                User.objects.update_login_date(user.id,previous_login_date)
                User.objects.update_previous_login_date(user.id,current_timestamp)
                if user.loginstatus == 0:
                    User.objects.filter(email=credentials['email'],roles_id=3,status=1).update(loginstatus=1)
                elif user.loginstatus == 1:
                    User.objects.filter(email=credentials['email'],roles_id=3,status=1).update(loginstatus=2)
                if (Settings.objects.filter(company_id=self.request.user.company.id).exists()):
                    companytimezone=Settings.objects.filter(company=self.request.user.company.id).first()
                    if (companytimezone != None):
                        self.request.session['companytimezone']=companytimezone.timezone
                        # print("session",self.request.session.get('companytimezone'))
                else:
                    self.request.session['companytimezone']=''
                return HttpResponseRedirect(self.success_url)
            else:
                messages.add_message(self.request, messages.ERROR, 'Invalid Email ID or Password')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login')) 
        elif User.objects.filter(cin_number=credentials['cin'] ,email=credentials['email'],bankuserstatus=1,status=1).exists():
            user=User.objects.filter(email=credentials['email'],bankuserstatus=1,status=1).first()
            if user is None:
                messages.add_message(self.request, messages.ERROR, 'User does not exists')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            if user.cin_number != credentials['cin']:
                messages.add_message(self.request, messages.ERROR, 'Invalid CIN number')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            userpassword=user.password
            p=credentials['password']
            print('asd')
            print('p',p)
            matchcheck= check_password(p, userpassword)
            print('p',matchcheck)
            if matchcheck:
                login(self.request, user)
                previous_login_date=user.previous_login_date
                User.objects.update_login_date(user.id,previous_login_date)
                User.objects.update_previous_login_date(user.id,current_timestamp)
                if user.loginstatus == 0:
                    User.objects.filter(email=credentials['email'],bankuserstatus=1,status=1).update(loginstatus=1)
                elif user.loginstatus == 1:
                    User.objects.filter(email=credentials['email'],bankuserstatus=1,status=1).update(loginstatus=2)
                if (Settings.objects.filter(company_id=self.request.user.company.id).exists()):
                    companytimezone=Settings.objects.filter(company=self.request.user.company.id).first()
                    if (companytimezone != None):
                        self.request.session['companytimezone']=companytimezone.timezone
                else:
                    self.request.session['companytimezone']=''
                return HttpResponseRedirect(self.success_url)
            else:
                messages.add_message(self.request, messages.ERROR, 'Invalid Email ID or Password')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login')) 
            
        else:   
            try:
                company =  Companies.objects.get(cin_number=credentials['cin'],email=credentials['email'],status=1)
            except Companies.DoesNotExist:
                company = None
            if company is None:
                messages.add_message(self.request, messages.ERROR, 'Company does not exist')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
            if company.cin_number != credentials['cin']:
                messages.add_message(self.request, messages.ERROR, 'Invalid Cin number')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))

            user = authenticate_user(cin=credentials['cin'],email=credentials['email'],
                                password=credentials['password'],company=company)
            if user is not None:
                login(self.request, user)
                previous_login_date=user.previous_login_date
                User.objects.update_login_date(user.id,previous_login_date)
                User.objects.update_previous_login_date(user.id,current_timestamp)
                # print("check",company)
                if (Settings.objects.filter(company=company).exists()):
                    companytimezone=Settings.objects.filter(company=company).first()
                    if (companytimezone != None):
                        self.request.session['companytimezone']=companytimezone.timezone
                        # print("session",self.request.session.get('companytimezone'))
                else:
                    self.request.session['companytimezone']=''
                return HttpResponseRedirect(self.success_url)

            else:
                messages.add_message(self.request, messages.ERROR, 'Invalid Email ID or Password')
                return HttpResponseRedirect(reverse_lazy('custom_auth:login'))
        

    def form_invalid(self, form, **kwargs):
        messages.add_message(self.request, messages.ERROR, 'Invalid Email ID or Password')
        return HttpResponseRedirect(reverse_lazy('custom_auth:adminlogin'))

def authenticate_user(cin,email, password,company):
    try:
        get_company=Companies.objects.filter(id=company.id,cin_number=cin).first()
        if (get_company != None):
            user = User.objects.get(email=email,company=company,roles_id=2)
            if user.loginstatus == 0:
                User.objects.filter(email=email,company=company,roles_id=2).update(loginstatus=1)
            elif user.loginstatus == 1:
                User.objects.filter(email=email,company=company,roles_id=2).update(loginstatus=2)
            print("get_comp",user)
        else:
            return None
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

        return None

def user_log(request):
    request.session['submenu'] = 'userlog'
    create_user_log=userlog.objects.filter(company_id = request.company) 
    data={'create_user_log':create_user_log}
    return render(request,'company/userlog.html',data) 
    # return render(request,'company/userlog.html')

def user_log_datatable(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    # user_log_datas = userlog.objects.filter(company_id = request.company)

        # Apply search filter
    # company_id = request.GET.get('company_id', None)
    
    # Assuming you have a company_id field in your UserLog model, adjust it accordingly
    user_log_datas = userlog.objects.filter(company_id=request.company)

    # Apply search filter
    if search_value:
        search_fields = ['source_id', 'source_type', 'message', 'username', 'created']

        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f'{field}__icontains': search_value})

        user_log_datas = user_log_datas.filter(q_objects)

    total_count = user_log_datas.count()

    total_count = user_log_datas.count()

    # Apply pagination
    paginator = Paginator(user_log_datas, length)
    page_number = (start // length) + 1
    user_log_datas = paginator.page(page_number)

    data = []
    for serial_number, user_log in enumerate(user_log_datas, start=1):
        data.append({
            'S/N': serial_number,
            'Message': user_log.message,
            'Source Name': user_log.source_id,
            'Source Type': user_log.source_type,
            'Created By': user_log.username.name,
            'Date': user_log.created.strftime('%d-%b-%Y at %I:%M %p'),
            
        })

    response = {
        'draw': draw,
        'recordsTotal': total_count,
        'recordsFiltered': total_count,
        'data': data
    }

    return JsonResponse(response)    

def enquiry(request):
    form=EnquiryFrom()
    
    # print(form)
    if request.method == 'POST':
        postvalues=request.POST
        title=postvalues.get('title')
        username=postvalues.get('companyname')
        email_id=postvalues.get('email')
        message=postvalues.get('message')
        print(title,username,email_id,message)
        createenquiry=Enquiryusers.objects.create(title=title,username=username,email_id=email_id,message=message)
        email_enquiry(title,username,email_id,f'{request.scheme}://{request.get_host()}')
        sender = User.objects.get(is_superuser=1)
        recipient = User.objects.filter(is_superadmin=1)
        scheme=request.scheme
        gethost=request.get_host()
        url=f"{scheme}://{gethost}/enquiryusers"
        notify.send(sender, recipient=recipient,data=url, verb='Enquiry Received', description=f'New Enquiry received from {username}')
        return redirect('custom_auth:login')
    data={'form':form}
    return render(request,'enquiry.html',data)

class SignupView(FormView):
    """sign up user view"""
    print('in signup form')


    def get_context_data(self, **kwargs):
        getenquiryid=self.kwargs['pk']
        context = super(FormView, self).get_context_data(**kwargs)
        countries=Basecountries.objects.all().values('name','id','phonecode')
        enquirydata=Enquiryusers.objects.filter(id=getenquiryid).first()
        context=({'countries':countries,'enquiryid':getenquiryid})
        # print('basecountry',countries)
        # context=({'countries':countries,})
        return context
    
    form_class = forms.SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('dashboard:dashboard')
    def form_invalid(self,form):
        
        print(form.errors)
        return (super().form_invalid(form))

        
    def form_valid(self, form):
        """ process user signup"""
        postvalues=self.request.POST
        print(postvalues)
        print(f"form {form}")
        
        
        # get_email=postvalues.get('email')
        # if User.objects.filter(email__exact=get_email,status=1).exists():
        #     print("email already exists")
        # else:
        company_name=postvalues.get('company_name')
        
        cin_num=companygeneratecin(company_name)
        genlicensekey= uuid.uuid4()

        # Enquiryusers.objects.filter(id=pk).update

        company=Companies.objects.create(
        company_name=postvalues.get('company_name'),
        first_name=postvalues.get('name'),
        last_name=postvalues.get('last_name'),
        email=postvalues.get('email'),
        mobile=postvalues.get('contact_no'),
        mobile_countrycode=postvalues.get('code'),
        phone_countrycode=postvalues.get('code'),
        cin_number=cin_num,
        status=0,
        country_id=postvalues.get('country_select'),
        contact_person=postvalues.get('contactperson'),
        designation=postvalues.get('designation'),
        type_of_license=postvalues.get('type_of_license'),
        package=postvalues.get('package'),
        number_of_users=postvalues.get('number_of_users'),
        concurent_users=postvalues.get('concurrent_user'),
        cloud_server=postvalues.get('cloudserver'),
        customisation=postvalues.get('customization'),
        support_services=postvalues.get('support'),
        licensekey=genlicensekey

        )
        predifined_data = user_data(Companies.objects.get(id=company.id))
        print(postvalues.get('email'))
        # Enquiryusers.objects.filter(email_id=postvalues.get('email')).update(proposalstatus=2)
        Enquiryusers.objects.filter(id=postvalues.get('enquiry')).update(proposalstatus=2,status=2)
        company.image=None

        company.save()
        current_url=f'{self.request.scheme}://{self.request.get_host()}'
        send_confirmation_mail(company,current_url)
        sender = User.objects.get(is_superuser=1)
        recipient = User.objects.filter(is_superadmin=1)
        # scheme='https'
        # gethost='irockinfo.mo.vc'
        url=f"{current_url}/company/list"
        notify.send(sender, recipient=recipient,data=url, verb='Proposal Form Received', description=f'Proposal form received from {company.first_name} {company.last_name}')
        user = form.save(commit=False)
        user.lastname=postvalues.get('last_name')
        user.company_id=company.id
        user.roles_id=2
        user.mobile=postvalues.get('contact_no')
        user.mobile_countrycode_id=postvalues.get('code')
        user.designation_role='Client Administrator'
        user.set_password('Hello@123')
        user.save()
        # group = Group.objects.get(id=1)
        # user.groups.add(group)
    
        # login(self.request, user)
        messages.success(self.request, "Licensing Proposal Form Submitted Successfully, Please wait for Admin’s Feedback.")
        if user is not None:
            #return HttpResponseRedirect(self.success_url)
            return redirect('custom_auth:login')

        return super().form_valid(form)

 
#check email
def checkemail(request):
    email=request.GET.get('email')
    data={}
    if Companies.objects.filter(email__exact=email,status=1).exists() or User.objects.filter(email__exact=email,status=1).exists():
        data={'exists':'email already exists'}
        return JsonResponse(data)
    else:
        data={'new':'new mail'}
        return JsonResponse(data)

@login_required
def Userpasswordreset(request,pk):
    currentuser=request.user
    if (request.user.contactpersonstatus == 1):
        if (request.user.userfirsttimelogin == 0):
            User.objects.filter(id=currentuser.id).update(userfirsttimelogin=1)
    else:
        if (request.user.userfirsttimelogin == 0):
            User.objects.filter(id=currentuser.id).update(userfirsttimelogin=1)
        if (request.user.userfirsttimelogin == 1):
            User.objects.filter(id=currentuser.id).update(userfirsttimelogin=2)
    form = PasswordChangeForm(currentuser)

    if request.method == 'POST':
        form = PasswordChangeForm(currentuser, request.POST)
        if form.is_valid():
            print('success')
            user = form.save()
            update_session_auth_hash(request, user)
            # User.objects.filter(id=currentuser.id).update(userfirsttimelogin=1)
            if (request.user.roles_id == 4):
                if (request.user.userfirsttimelogin == 1):
                    return redirect('projects:vendordetailpage')
                else:
                    return redirect('custom_auth:vendorlogin')
            elif (request.user.roles_id == 2):
                if (request.user.userfirsttimelogin == 1):
                    return redirect('custom_auth:login')
                else:
                    return redirect('custom_auth:login')
                # return redirect('custom_auth:clientadminview',pk=pk)
            else:
                if (request.user.userfirsttimelogin == 1):
                    return redirect('custom_auth:userdetails',pk=pk)
                 
                else:
                    return redirect('custom_auth:login')
                # return redirect('custom_auth:userdetails',pk=pk)
        else:
            print(form.errors)

    data={'form':form,'userid':currentuser}

    return render(request,'userpasswordreset.html',data)


def EditUserDetails(request,pk):
    currentuser=request.user
    phonecodelist=[]
    phonecode = Basecountries.objects.all().values('iso3','id','phonecode').order_by('phonecode').distinct()
    fontfamilylist = FontFamily.objects.filter(status=1)
   
    for codes in phonecode:
        id=codes.get('id')
        num=codes.get('phonecode')
        iso=codes.get('iso3')
        x = re.findall("\+",num)
        if x:
            phonecodelist.append({'id':str(id),'phonecode':str(num),'iso':iso})
        else:
            phonecodelist.append({'id':str(id),'phonecode':'+'+str(num),'iso':iso})
    newlist=sorted(phonecodelist, key = lambda i:  (i['phonecode']))

    userdatas=User.objects.get(id=pk)
    form=Usercreationform(instance=userdatas)
    
    titles=['Mr','Mrs','Ms']
    userimage=''
    if User.objects.filter(id=pk).filter(Q(image__isnull=True) | Q(image='')):
        print('yes')
        userimage='images/icons/Character_icon.svg'
    else:
        user_detail=User.objects.get(id=pk)
        userimage=user_detail.image.url
        print('no',user_detail.image)

    if request.method == 'POST':
        print(f'POST Data {request.POST}')
        phone=request.POST.get('phone')
        phone_countrycode=request.POST.get('phone_countrycode')
        mobile_countrycode=request.POST.get('mobile_countrycode')
        mobile=request.POST.get('mobile')
        areacode=request.POST.get('areacode')
        phone_number_extenstion=request.POST.get('phone_number_extenstion')
        inputfield=request.POST.get('inputfield')
        font=request.POST.get('fontfamily')

        # print('phone_number_extenstion',phone_number_extenstion)
        # email=request.POST.get('email')
        # print('request',request)
        if (currentuser.is_primary == 1):
            vendor_primary = ContractMasterVendor.objects.filter(company=request.company.id,vin=request.user.cin_number).update(contact_primary_phone_code=phone_countrycode,contact_primary_phone=phone,contact_primary_area_code=areacode,contact_primary_mobile_code=mobile_countrycode,contact_primary_mobile=mobile,contact_primary_phone_number_extenstion=phone_number_extenstion)
            # print(f'vendor_primary {vendor_primary}')
        if (currentuser.is_secondary == 1):
            vendor_secondary = ContractMasterVendor.objects.filter(company=request.company.id,vin=request.user.cin_number).update(contact_secondary_phone=phone,contact_secondary_mobile=mobile,contact_secondary_phone_code=phone_countrycode,contact_secondary_mobile_code=mobile_countrycode,contact_secondary_area_code=areacode,contact_secondary_phone_number_extenstion=phone_number_extenstion)
            # print(f'vendor_secondary {vendor_secondary}')
        sender = User.objects.get(id=request.user.id)
        # get roles id from sender
        senderrolesid = request.user.roles_id
        recipient = User.objects.filter(company=request.company.id,roles_id=2).first()
        scheme=request.scheme
        gethost=request.get_host()  
        if senderrolesid == 3:
            urls=f"{scheme}://{gethost}/projects/userview/{pk}"
            notify.send(sender, recipient=recipient,data=urls, verb='User Details Updated', description=f'{sender.name} {sender.lastname if sender.lastname != None else ""} updated their details')
        else:
            urls=f"{scheme}://{gethost}/projects/vendormasterlist"
            notify.send(sender, recipient=recipient,data=urls, verb='Vendor Details Updated', description=f'{sender.name} {sender.lastname if sender.lastname != None else ""} updated their details')
        title=request.POST.get('title')
        image=request.FILES.get('image')
        sign_type = request.POST.get('sign_type')
        sign_file=request.FILES.get('sign_file')
        sign_draw=request.POST.get('sign_draw')
        font=request.POST.get('fontfamily')
        print('sign_type--',sign_type)
        form = Usercreationform(request.POST,instance=userdatas)
        
        if form.is_valid():
            print('form Valid')
            user = form.save(commit=False)
            user.Title=title
            user.signature_type = sign_type
            
            if (sign_type == "file"):
                print("sign_file",sign_file)
                if (sign_file != None):
                    user.signature_image = sign_file
            elif(sign_type == "signature"):
                if (sign_draw != ''):
                    format, imgstr = sign_draw.split(';base64,') 
                    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))  
                    ext = format.split('/')[-1] 
                    data = ContentFile(base64.b64decode(imgstr))
                    file_name =request.user.name+str(ran)+'signature.' + ext
                    user.signature_image.save(file_name,data, save=True)
       
            else:
                    print('else')
                    print(f'inputfield {inputfield}')
                    print(f'font {font}')
                    user.signature_fontname = inputfield
                   
                    if (font != 'None'):
                        user.signature_fontfamily_id = font

            if (image != None):
                user.image=image
            user.save()
            return redirect('custom_auth:userdetails',pk=pk)
        else:
            print(f'form Error {form.errors}')
            
    
    data={'form':form,
          'phone':newlist,
          'datas':userdatas,
          'titles':titles,
          'image':userimage,
          'fontfamily':fontfamilylist,
          }
    return render(request,'usereditdetails.html',data)



def UserSpecificDetailsView(request,pk):
    if (request.user.roles_id == 4 and request.user.userfirsttimelogin == 1):
            vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
            if(request.user.is_primary == 0 and request.user.is_secondary == 0) :
                return redirect('projects:editinsidevendorbasicinfo',pk=vendorid.id)
    # Notification read status 
    markas_read_status(request.get_full_path())
    print(request.user)
    userdata=User.objects.get(id=pk)
    project_user = ProjectUser.objects.filter(user_id = pk , company_id = request.company.id)
    # for project_user_instance in project_user:
    #     project_name = project_user_instance.project.projectname.name  # Access the related project name
    #     print("Project Name:", project_name)
    # print(project_name,"PROJECT USERS")
    data={'user':userdata,'project_user':project_user,'project_user_count':project_user.count()}
    return render(request,'userspecificdetails.html',data)

# @cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/')
def Logout(request):
    """logout logged in user"""
    if(request.user.is_superadmin==1):
        logouturl="custom_auth:adminlogin"
    elif(request.user.roles_id==4):
        logouturl="custom_auth:vendorlogin"
    else:
        logouturl="custom_auth:login"
    now = datetime.now()
    if request.user.is_superadmin!=1:
        current_timestamp = int(datetime.now().timestamp())

        User.objects.filter(id=request.user.id).update(login_date=current_timestamp)
    logout(request)
    return HttpResponseRedirect(reverse_lazy(logouturl))


# @cache_control(no_cache=True, must_revalidate=True)
# def func():
#   check="Login Must"
#   return check

class AdminLoginView(FormView):
    """login view"""
    login_required = True
    form_class = forms.AdminLoginForm
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'adminlogin.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate_admin(email=credentials['email'],
                            password=credentials['password'], is_superadmin=1)

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Invalid Email ID or Password')
            return HttpResponseRedirect(reverse_lazy('custom_auth:adminlogin'))

    def form_invalid(self, form, **kwargs):
        messages.add_message(self.request, messages.INFO, 'Invalid Email ID or Password')
        return HttpResponseRedirect(reverse_lazy('custom_auth:adminlogin'))



def authenticate_admin(email, password,is_superadmin):
    try:
        user = User.objects.get(email=email,is_superadmin=1)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None


#company
def Companieslist(request):
    # Notifcation read status
    markas_read_status(request.get_full_path())    
    companies=Companies.objects.all().order_by('-id')
    title="Registered Companies"
    return render(request,'company/list.html',{'companies':companies,'title':title})


 
def Companiesview(request, id):  
    print('viewpage')
    try:
        data = Companies.objects.get(id=id)
        paymenthistory = PaymentHistory.objects.filter(company_id=id,status=1)
        print('paymenthistorys',paymenthistory)
        print('data',data)
        if data.image =='':
            print("yes")
        else:
            print('No')
    except Companies.DoesNotExist:
        messages.error(request, "Company Does Not Exists")
        return redirect("/company/list/all")
    return render(request,'company/view.html', {'data':data,'paymenthistorys':paymenthistory,'paymenthistorycount':paymenthistory.count()})


def Companiesapprove(request,id):
    companyupdate =  Companies.objects.filter(pk=id).update(status= 1)
    company =  Companies.objects.get(id=id)
    update_user = User.objects.filter(company_id=id).update(status= 1)
    print('company',company)
    send_approvel_mail(company,request)
    # print('companies approval')
    messages.success(request, "Company Approved Successfully")
    return redirect('custom_auth:companies')

def Companiesreject(request, id):  
    company =  Companies.objects.filter(pk=id).update(status= 2)
    company =  Companies.objects.get(id=id)
    User.objects.filter(company_id=company.id).update(status=0)
    # send_reject_mail(company)
    messages.error(request, "Company Rejected Successfully")
    return redirect("custom_auth:companies")

def viewcompaniesdetails(request,pk):
    request.session['mainmenu'] = 'settings'
    request.session['submenu']='profile'
    companyupdate =  Companies.objects.get(pk=pk)


    data={'company':companyupdate}
    # messages.success(request, 'Form submission successful')
    
    # messages.add_message(request, messages.INFO, 'Form Submitted successfully.')
    print('jsdfpjsojs')
    return render(request,'company/viewcompanydetails.html',data)

def editclientadmindetails(request,pk):
    userdata=User.objects.get(id=pk)
    fontfamilylist = FontFamily.objects.filter(status=1)
    userimage=''
    if User.objects.filter(id=pk).filter(Q(image__isnull=True) | Q(image='')):
        print('yes')
    else:
        userimage=userdata.image.url
        print('no',userimage)
    print('userimage----',userimage)
    if request.method == 'POST':
        image=request.FILES.get('image',None)
        inputfield=request.POST.get('inputfield')
        font=request.POST.get('fontfamily')
        sign_type = request.POST.get('sign_type')
        sign_file=request.FILES.get('sign_file')
        sign_draw=request.POST.get('sign_draw')
        font=request.POST.get('fontfamily')
        print('inputfield,font,sign_type,image------',image)
        # print(image)
        # form = Usercreationform(request.POST,instance=userdata)
        # if form.is_valid():
        userdata.signature_type = sign_type
        if (sign_type == "file"):
                print("sign_file",sign_file)
                if (sign_file != None):
                    userdata.signature_image = sign_file
        elif(sign_type == "signature"):
                if (sign_draw != ''):
                    format, imgstr = sign_draw.split(';base64,') 
                    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))  
                    ext = format.split('/')[-1] 
                    data = ContentFile(base64.b64decode(imgstr))
                    file_name =request.user.name+str(ran)+'signature.' + ext
                    userdata.signature_image.save(file_name,data, save=True)
       
        else:
                    print('else')
                    print(f'inputfield {inputfield}')
                    print(f'font {font}')
                    userdata.signature_fontname = inputfield
                   
                    if (font != 'None'):
                        userdata.signature_fontfamily_id = font
        if (image != None):
                userdata.image=image
        userdata.save()
        # else:
        #     print(f'form Error {form.errors}')
        return redirect('custom_auth:clientadminview',pk=pk)
    print('userdata',userdata.signature_image) 
    data={'userdata':userdata,'userimage':userimage,'fontfamily':fontfamilylist}
    return render(request,'editclientadmindetails.html',data)

def clientadminview(request,pk):
    return render(request,'clientadmindetails.html')

def editcompaniesdetails(request,pk):
    phonecodelist=[]
    entitytypelist=['Oil_and_Gas_Operators','Oil_and_Gas_Servicing_Companies','Other_Industry']
    countries=Basecountries.objects.all()
    request.session['mainmenu'] = 'settings'
    request.session['submenu'] = 'profile'
    companyupdate =  Companies.objects.get(pk=pk)

    print(companyupdate)
    imagedata=''
    imagevalue=''
    if Companies.objects.filter(pk=pk).filter(Q(image__isnull=True) | Q(image=None) | Q(image='')):
        imagedata=''
        imagevalue=''
    else:
        companyupdatedata = Companies.objects.get(pk=pk)
        imagedata=companyupdatedata.image.url
        imagevalue=companyupdatedata.image
    if (request.POST):
        # print(request.POST)
        get_value=request.POST
        # first_name=get_value.get('firstname')
        # last_name=get_value.get('lastname')
        mobile=get_value.get('mobile_no')
        phonenumber=get_value.get('phone_no')
        website=get_value.get('website')
        address=get_value.get('address')
        country=get_value.get('country')
        image=request.FILES.get('image',None)
        phone_countrycode=get_value.get('phone_countrycode')
        areacode=get_value.get('phone_areacode')
        mobile_countrycode=get_value.get('mobile_countrycode')
        entity=get_value.get('projecttype')
        print('address',address)
        companies=Companies.objects.get(id=pk)
        if len(request.FILES) != 0:
            companies.image = image
            companies.save()
            # save without folder
            # if (companies.image != '' or companies.image != None):
            #     if len(companies.image) > 0:
            #         os.remove(companies.image.path)
            # else:
            #     companies.image = image
            #     companies.save(
        Companies.objects.filter(id=pk).update(phone_countrycode=phone_countrycode,areacode=areacode,mobile_countrycode=mobile_countrycode,category_entity=entity,mobile=mobile,phonenumber=phonenumber,website=website,address=address,country=country)
        return redirect('custom_auth:viewcompany', pk=pk)
    data={'company':companyupdate,
          'countries':countries,
          'entitytype':entitytypelist,
          'image':imagedata,
          'imagevalue':imagevalue,
          }
    return render(request,'company/editcompany.html',data)



def getcountrycode(request,pk):
    countryid=request.GET.get('countryid',None)
    data={}

    countries=Basecountries.objects.get(id=countryid)
    code=countries.phonecode
    x = re.findall("\+",code)
    if x:
        data={'countrycode':code}
    else:
        data={'countrycode':'+'+str(code)}
    return JsonResponse({'data':data})

def Generalsetting(request,companyid):
    request.session['mainmenu'] = 'Generalsetting'
    request.session['submenu'] = 'Generalsettingcreate'
    # form=Generalsettingform()
    countries=Basecountries.objects.all()
    zones=zone.objects.all()
    basecountry=Basecountries.objects.all().values_list('timezones',flat=True)
    # print(basecountry)
    timezonelist=[]
    # for country in basecountry:
    #     convert_list=ast.literal_eval(country)
    #     for time_zone in convert_list:
    #         timezonelist.append({'zoneName':time_zone['zoneName'],'gmtOffsetName':time_zone['gmtOffsetName']})
    general_settings={}
    if  Settings.objects.filter(company=request.company).exists():
        general_settings= Settings.objects.filter(company=request.company).first()
        
    else:
        general_settings
    print(f'general_settings {general_settings}')
    if (request.POST):
        postvalues=request.POST
        dateformat=postvalues.get('dateformat')
        timezone=postvalues.get('timezone')
        units=postvalues.get('units')
        timeformat=postvalues.get('timeformat')
        currency=postvalues.getlist('currency')
        vendoremailtime=postvalues.get('vendoremailtime')
        vendoremailtimeunit=postvalues.get('vendoremailtimeunit')
        vendor_registartion_time=postvalues.get('vendor_registartion_time')
        bankuser=postvalues.get('bank_user_check')
        user_check=0
        if bankuser:
           user_check= bankuser
        print(f'bankuser {bankuser}')
        urlfield=postvalues.get('urlfield')
        # convert_list=json.dumps(currency)
        if  Settings.objects.filter(company=request.company).exists():
            general=Settings.objects.filter(company_id=request.company).first()
            Settings.objects.filter(company=request.company).update(vendor_registartion_time=vendor_registartion_time,currency=currency,dateformat=dateformat,timeformat=timeformat,timezone=timezone,unit=units,vendor_invite_time=vendoremailtime,vendor_invite_unit=vendoremailtimeunit,urlfield=urlfield,bank_user=user_check)
            request.session['companytimezone']=timezone
        else:
            general=Settings.objects.create(vendor_registartion_time=vendor_registartion_time,currency=currency,company=request.company,dateformat=dateformat,timeformat=timeformat,timezone=timezone,unit=units,vendor_invite_time=vendoremailtime,vendor_invite_unit=vendoremailtimeunit,urlfield=urlfield,bank_user=user_check)
            request.session['companytimezone']=timezone
        return redirect('custom_auth:generalsettingsview',pk=general.id)
    
    # all_dateformat=['dd-mm-yy','dd/mm/yy','mm-dd-yy','mm/dd/yy','yy-mm-dd','yy/mm/dd','dd-M-yy'] 
    Units=['API','SI','MIXED_UNIT']
    timeformat=['12','24']
    date_units=['Hours','Days']
    data={'timezones':zones,
          'basecountry':countries,
          'general_settings':general_settings,
        #   'all_dateformat':all_dateformat,
          'Units':Units,
          'timeformat':timeformat,
          'date_units':date_units,         
          }
    return render(request,"company/generalsetting.html",data)


def generalsettingview(request,pk):
    request.session['mainmenu'] = 'Generalsetting'
    request.session['submenu'] = 'Generalsettingcreate'
    general=Settings.objects.filter(id=pk).first()
    data={'general':general,'length':len(general.urlfield)}
    return render(request,'company/generalsettingview.html',data)

class urlchkforiframe(View):
    def post(self,request):
       url = request.POST.get('url')
      
    #    url = "https://www.google.com/"
       print('url--',url)
       response = requests.head(url)
       headers = response.headers

        # Iterate over the headers
    #    for key, value in headers.items():
    #         print(f'{key}: {value}')
        
       if 'X-Frame-Options' in headers:
            xframe_options = response.headers['X-Frame-Options']
            print(f"The X-Frame-Options header value for {url} is: {xframe_options}")
            return JsonResponse({'status':True})
       else:
            print(f"No X-Frame-Options header found for {url}")
            return JsonResponse({'status':False})

        

def downloadbrochure(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'irock-brochure-new.pdf'
    # Define the full file path
    filepath = BASE_DIR + '/custom_auth/irock-enquiry/' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def enquiryusers(request):
    # Notifiaction read status for enquiry
    markas_read_status(request.get_full_path())
    enquiryuserslist=Enquiryusers.objects.all().order_by('-id')
    print(enquiryuserslist)
    
    return render(request,'company/enquiryusersllists.html',{'enquiryuserslist':enquiryuserslist})

def proposalformsend(request,pk): 
    print(pk)
    check = Enquiryusers.objects.filter(id=pk).update(proposalstatus=1)
    if check:
        print(f"proposalformsend: {check}")
    en=Enquiryusers.objects.get(id=pk)
    print(f'en{en}')
    name=en.username
    title=en.title
    email_id=en.email_id
    id=en.id
    print(name)
    email_proposal(name,title,email_id,id,f'{request.scheme}://{request.get_host()}')
    return redirect('custom_auth:enquiryusers')


def keygenerator(request,id,status):
    data = Companies.objects.get(id=id)
    currency=Basecountries.objects.all()
    print('currency',id,type(status))

    if(request.POST or request.FILES):
        print(request.POST)
        get_value=request.POST
        currency=get_value.get('currency')
        amount=get_value.get('amount')
        comapnyid=get_value.get('companyid')
        date=get_value.get('date')
        invoicenum=get_value.get('invoicenum')
        file=request.FILES.getlist('file')
        # print(file)
        print('status',status)
        if (status == '0'):
            update=Companies.objects.filter(id=data.id).update(currency=currency,amount=amount,licencestatus=1,invoicedate=date,invoicenumber=invoicenum,status=0)
            print(update)
        else:
            update=Companies.objects.filter(id=data.id).update(currency=currency,amount=amount,licencestatus=1,invoicedate=date,invoicenumber=invoicenum)
        create_file = PaymentHistory.objects.create(currency_id=currency,amount=amount,invoicedate=date,invoicenumber=invoicenum,status=1,company_id=comapnyid)
        print('master',create_file)
        for f in file:
            print('file',f)
            create_files =  PaymentHistoryFile.objects.create(company_id=comapnyid,file=f,payment_history=create_file)
            print('child',create_files)
        return redirect('custom_auth:companyview',id=comapnyid)
    return render(request,'company/keygenerationpage.html',{'data':data,'currency':currency,'pk':id})



def keyactivationpage(request): 
    print(request.POST)
    print('kjsdfksjhdfkj')
    print(request.POST.get('sec_key'))
    key=request.POST.get('sec_key')
    if request.method=='POST':
        if Companies.objects.filter(licensekey=key,id=request.company.id).exists():
            print('test')
            Companies.objects.filter(id=request.company.id).update(checkkeystatus=1)
            return redirect('custom_auth:userpasswordreset',pk=request.user.id)
        else:
            messages.success(request, "Invalid License Key")
            return redirect('custom_auth:keyactivationpage')
    return render(request,'company/companykeyactivationpage.html')



def seckeychecking(request): 
    print(request.GET['value'])
    keyvalue=request.GET['value']
    if Companies.objects.filter(licensekey=keyvalue,id=request.company.id).exists():
        data={'data':'true'}
    else:
        data={'data':'false'}
    return JsonResponse(data)




def proposal_check(request,id):
    print(id)
    getenquiryid=id
    # print('coming to proposal check function')
    
    enquirydata=Enquiryusers.objects.filter(id=getenquiryid).first()
    if (enquirydata.status == 2):
            # return super().dispatch(request, *args, **kwargs)
            # return redirect('custom_auth:linkexpired')
            # print('checking')
            return render (request,"linkexpired.html")
    else:
            # print('else dispatch')
            return redirect('custom_auth:signup',pk=getenquiryid)



def passwordrestcheck(request):

    userid=request.user.id
    # print("userid "+userid)
    check=User.objects.get(id=userid)
    password=request.GET.get('oldpass')
    print(password)
    hashed_password = check.password
    if check_password(password,hashed_password):
        data={'data':'true'}
    else:
        data={"data":'false'}
    return JsonResponse(data)
            
            
  
def forgotpasscode(request):
    print(f"current URL: {request.path}")
    print(type(str(request.path)))
    print(request.POST)
    current_url = request.path
    scheme=request.scheme
    gethost=request.get_host()
    url=f'{scheme}://{gethost}'
    print('url',url)
    if(request.POST):
        print('before send')
        email_forgotpassword(url,request.POST.get('name'),request.POST.get('lastname'),request.POST.get('email'),request.POST.get('id'))
        print('after send')
        print(f"Email: {request.POST.get('email')} ID: {request.POST.get('id')}")
        if str(current_url) == '/forgotpasscodevin':
            return redirect('custom_auth:vendorlogin')
        else:
            return redirect('custom_auth:login')
    if str(current_url) == '/forgotpasscodevin':
        return render(request,'forgotpasscodevin.html')
    else:
        return render(request,'forgotpasscode.html')


 
    

def checkcompanyuseremailexists(request):
    get_email=request.POST.get('email')
    get_cin=request.POST.get('cin_number')
    print(get_email, get_cin)
    dataexists = User.objects.filter(email=get_email,cin_number=get_cin,roles_id=4,status=1).first()
    if dataexists != None:
        data={'data':'exists','id':dataexists.id,'name':dataexists.name,'last_name':dataexists.lastname}
    else:
        data={'data':'failure'}
    return JsonResponse(data)

def checkcompanyuseremail(request):
    get_email=request.POST.get('email')
    # print(get_email)
    dataexists = User.objects.filter(Q(email=get_email),Q(roles_id=2) |Q(roles_id=3),Q(status=1)).first()
    if dataexists != None:
        data={'data':'exists','id':dataexists.id,'name':dataexists.name,'last_name':dataexists.lastname}
    else:
        data={'data':'failure'}
    return JsonResponse(data)

def resetpasscode(request,id):
    u = User.objects.get(id=id)
    roles_id = u.roles_id
    if(request.POST):
        u.set_password(request.POST.get('passcode'))
        u.save()
        if roles_id == 2:
            return redirect('custom_auth:login')
        elif roles_id == 4:
            return redirect('custom_auth:login')
    return render(request,'resetpasscode.html')

def Notifications(request):
    user = User.objects.get(pk=request.user.id)
    notifications=user.notifications.all()
    page = request.GET.get('page', 1)
    pageper_data = request.GET.get('pageperdata',10)
    paginator = Paginator(notifications, pageper_data)
    notifications = paginator.page(page)
    scheme=request.scheme
    gethost=request.get_host()
    hours = request.session.get('hours',0)
    minutes = request.session.get('minutes',0)
    return render(request, 'notifications.html',{'notifications':notifications,'scheme':scheme,'gethost':gethost,'hours':hours,'minutes':minutes})


def markallread(request):
    notifications=Notification.objects.filter(recipient=request.user)
    for notification in notifications:
        Notification.objects.get(pk=notification.id).mark_as_read()
    return redirect ("/notifications/")
def mark_all_read(request):
    notifications = Notification.objects.filter(recipient=request.user)
    
    for notification in notifications:
        notification.mark_as_read()

    # You can send a JSON response to indicate success
    return JsonResponse({'status': 'success'})

def checkinvoicenumduplicate(request):
    invoice_num=request.GET.get('invoice_num')
    if PaymentHistory.objects.filter(invoicenumber=invoice_num,status=1).exists():
        data={'data':'exists'}
    else:
        data={'data':'success'}
    return JsonResponse(data)



class GetClientDatetime(View):
    def get(self, request):
        hours = request.GET.get('hours')
        minutes = request.GET.get('minutes')
        data = {'hours': hours, 'minutes': minutes}
        request.session['hours'] = hours
        request.session['minutes'] = minutes
        return JsonResponse(data)
    
# class CreateUserDepartment(CreateView):
#     # multiple form add by using formset
#     model = UserDepartment
#     form_class = UserDepartmentForm
#     template_name = 'create_user_department.html'
#     success_url = reverse_lazy('custom_auth:department_list')
#     def get_context_data(self, **kwargs):
#         data = super(CreateUserDepartment, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['formset'] = UserDepartmentFormSet(self.request.POST)
#         else:
#             data['formset'] = UserDepartmentFormSet()
#         return data
#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']
#         with transaction.atomic():
#             self.object = form.save()
#             if formset.is_valid():
#                 formset.instance = self.object
#                 formset.save()
#         return super(CreateUserDepartment, self).form_valid(form)

def addUserDepartmentForm(request):
    form = forms.UserDepartmentForm()
    context = {
        "form": form
    }
    return render(request, "addUserDepartment.html", context)
@require_POST
def add_form(request):
    formset = forms.UserDepartmentFormSet(forms.UserDepartmentForm, extra=1)
    data = request.POST or None
    new_formset = formset(data=data)
    html = render(request, 'addUserDepartment.html', {'formset': new_formset}).content.decode('utf-8')
    return JsonResponse({'html': html})

class UserAddView(TemplateView):
    # template_name = "adddepartment.html"
    template_name = "addUserDepartment.html"
    # Define method to handle GET request
    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = forms.UserDepartmentFormSet(queryset=UserDepartment.objects.none())
        return self.render_to_response({'bird_formset': formset})
    
    def post(self, *args, **kwargs):

        formset = forms.UserDepartmentFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("dashboard:dashboard"))

        return self.render_to_response({'bird_formset': formset})


class addUserDepartment(View):
    def get(self, request):
        return render(request, "addUserDepartment.html")
    def post(self, request):
        if request.POST:
            for i in self.request.POST.getlist('departmentName'):
                department = UserDepartment.objects.create(department=i,company=request.user.company)
                usercreate = request.user.roles_id     
                create_user_log(request,department,'User Department','Create','User Department Created',usercreate)  
         
        return redirect(reverse_lazy("custom_auth:list-userdepartment-form"))

class listUserDepartment(ListView):
    model = UserDepartment
    template_name = "listUserDepartment.html"
    # context_object_name = 'departments'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=8)
            context['rights']=userrights
        search_query = self.request.POST.get('q',False)
        if search_query:
            dep_list = UserDepartment.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),department__icontains=search_query,status=1).order_by('-id')
            context['query'] = search_query
        else:
            dep_list = UserDepartment.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1).order_by('-id')
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.POST.get('pageperdata',10)
        paginator = Paginator(dep_list, pageper_data)
        context['dep_count'] =  dep_list.count()
        context['dep_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        context['departments'] =  UserDepartment.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1)
        return context


    def post(self,request):
        print('post',request.POST)
        # call get context data
        context = {}
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get_by_module(self.request.user.id,6)
            context['rights']=userrights
        search_query = self.request.POST.get('q',False)
        if search_query =='':
            dep_list = UserDepartment.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1).order_by('-id')
            context['query'] = search_query
        else:
            dep_list = UserDepartment.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),department__icontains=search_query,status=1).order_by('-id')
            context['query'] = search_query
        page = request.POST.get('page', 1)
        pageper_data = request.POST.get('pageperdata',10)
        paginator = Paginator(dep_list, pageper_data)
        context['dep_count'] =  dep_list.count()
        context['dep_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=request.scheme
        context['gethost']=request.get_host()
        # render to template string
        html = render_to_string('search_department.html',context,request)
        return JsonResponse({'status':True,'html':html})
    # def get_queryset(self):
    #     data={}
    #     if (request.user.roles_id == 3):
    #         userrights=UserRights.objects.get(user_id=request.user.id,module_id=5)
    #         data['rights']=userrights
    #     data.update({'alltaxes':alltaxes})
        # return UserDepartment.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1)

class editUserDepartment(UpdateView):
    model = UserDepartment
    template_name = "editUserDepartment.html"
    context_object_name = 'department'
    fields = ['department']
    success_url = reverse_lazy('custom_auth:list-userdepartment-form')
    def form_valid(self, form):
        # Get the usercreate information
        usercreate = self.request.user.roles_id

        # Log the update of the UserDepartment
        create_user_log(self.request, self.object, 'User Department', 'Edit', 'User Department Edited', usercreate)

        # Proceed with the default form validation
        return super().form_valid(form)

class deleteUserDepartment(View):
    def post(self, request, pk):
        print(f'pk {pk}')
        company_tax = UserDepartment.objects.filter(id=pk).first()
        if company_tax:
            company_tax.status = 0
            company_tax.save()
            usercreate = request.user.roles_id     
            create_user_log(request,company_tax,'User Department','Delete','User Department Deleted',usercreate)  
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
        
class addUserGroup(View):
    def get(self, request):
        return render(request, "addUserGroup.html")
    def post(self, request):
        if request.POST:
            for i in self.request.POST.getlist('groupName'):
                user_group = UserGroup.objects.create(group=i,company=request.user.company)
                usercreate = request.user.roles_id     
                create_user_log(request,user_group,'User Group','Create','User Group Created',usercreate)  
        return redirect(reverse_lazy("custom_auth:list-usergroup-form"))
    
class listUserGroup(ListView):
    model = UserGroup
    template_name = "listUserGroup.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=9)
            context['rights']=userrights
        search_query = self.request.POST.get('q',False)
        if search_query:
            group_data = UserGroup.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),group__icontains=search_query,status=1).order_by('company_id')
            context['query'] = search_query
        else:
            group_data = UserGroup.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1).order_by('company_id')
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.POST.get('pageperdata',10)
        paginator = Paginator(group_data, pageper_data)
        context['group_count'] =  group_data.count()
        context['group_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        return context
    
    def post(self,request):
        print('post',request.POST)
        # call get context data
        context = {}
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=9)
            context['rights']=userrights
        search_query = self.request.POST.get('q',False)
        if search_query =='':
            group_data = UserGroup.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1).order_by('company_id')
            context['query'] = search_query
        else:
            group_data = UserGroup.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),group__icontains=search_query,status=1).order_by('company_id')
            context['query'] = search_query
        page = request.POST.get('page', 1)
        pageper_data = request.POST.get('pageperdata',10)
        print('pageper_data',pageper_data)
        paginator = Paginator(group_data, pageper_data)
        print('paginator',paginator)
        context['group_count'] =  group_data.count()
        context['group_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=request.scheme
        context['gethost']=request.get_host()
        # render to template string
        html = render_to_string('search_usergroup.html',context,request)
        print('html',html)
        return JsonResponse({'status':True,'html':html})
    


    # context_object_name = 'groups'
    # def get_queryset(self):
    #     return UserGroup.objects.filter(Q(company_id=self.request.company.id) | Q(company_id=None),status=1).order_by('company_id')

   





    
class editUserGroup(UpdateView):
    model = UserGroup
    template_name = "editUserGroup.html"
    context_object_name = 'group'
    fields = ['group']
    success_url = reverse_lazy('custom_auth:list-usergroup-form')
    def form_valid(self, form):
        # Get the usercreate information
        usercreate = self.request.user.roles_id

        # Log the update of the UserDepartment
        create_user_log(self.request, self.object, 'User Group', 'Edit', 'User Group Edited', usercreate)

        # Proceed with the default form validation
        return super().form_valid(form)

class deleteUserGroup(View):
    def post(self, request, pk):
        company_group = UserGroup.objects.filter(id=pk).first()
        if company_group:
            company_group.status = 0
            company_group.save()
            usercreate = request.user.roles_id    
            create_user_log(request,company_group,'User Group','Delete','User Group Deleted',usercreate)  
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
        
class validateUserGroup(View):
    def post(self, request):
        if request.POST:
            group = request.POST.get('group')
            group_id = request.POST.get('group_id')
            if group_id:
                if UserGroup.objects.filter(group__iexact=group,company=request.company,status=1).exclude(id=group_id).exists():
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})
            else:
                if UserGroup.objects.filter(group__iexact=group,company=request.company,status=1).exists():
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})
                
class validateUserDepartment(View):
    def post(self, request):
        if request.POST:
            department = request.POST.get('department')
            department_id = request.POST.get('department_id')
            if department_id:
                if UserDepartment.objects.filter(department__iexact=department,company=request.company,status=1).exclude(id=department_id).exists():
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})
            else:
                if UserDepartment.objects.filter(department__iexact=department,company=request.company,status=1).exists():
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})

class Invoicetriggertime(View):
    def get(self,request,companyid):
        data={}
        masterinvoicetrigger = InvoiceTimeTrigger.objects.filter(status=1,company=companyid)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id='15')
            data['rights']=userrights
        data.update({'masterinvoicetrigger':masterinvoicetrigger,'companyid':companyid})
        return render(request,'invoicetriggertime.html',data)
    


class EditInvoicetriggertime(View):
     def get(self,request,companyid):
        masterinvoicetrigger = InvoiceTimeTrigger.objects.filter(status=1,company=companyid)
        invoice_check=custom_range_func("modules",request)
        dict_obj=[{'key':2,'value':'Minutes'},{'key':0,'value':'Hours'},{'key':1,'value':'Days'}]
        data={'masterinvoicetrigger':masterinvoicetrigger,'companyid':companyid,'invoice_check':len(invoice_check),'time_format':dict_obj}
        return render(request,'editinvoicetriggertime.html',data)
     def post(self,request,companyid):
         method=self.request
         pk = method.POST.getlist('pk')
         payment_terms_from = method.POST.getlist('payment_terms_from')
         payment_terms_to = method.POST.getlist('payment_terms_to')
         time_unit = method.POST.getlist('time_unit')
         time_allotted = method.POST.getlist('time_allotted')
                
         for i, _ in enumerate(pk):
             if(pk[i] == '0'):
                InvoiceTimeTrigger.objects.create(payment_terms_from=payment_terms_from[i],payment_terms_to=payment_terms_to[i],time_unit=time_unit[i],time_allotted=time_allotted[i],company_id=companyid,status=1)
             else:
                InvoiceTimeTrigger.objects.filter(status=1,company=companyid,id=pk[i]).update(
                payment_terms_from=payment_terms_from[int(i)],
                payment_terms_to=payment_terms_to[int(i)],
                time_unit=time_unit[int(i)],
                time_allotted=time_allotted[int(i)]
                )
         masterinvoicetrigger = InvoiceTimeTrigger.objects.filter(status=1,company=companyid)
         data={'masterinvoicetrigger':masterinvoicetrigger,'companyid':companyid}
         return render(request,'invoicetriggertime.html',data)
     
class Wcctriggertime(View):
     def get(self,request,companyid):
        data={}
        masterinvoicetrigger = WccTimeTrigger.objects.filter(status=1,company=companyid)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id='15')
            data['rights']=userrights
        data.update({'masterinvoicetrigger':masterinvoicetrigger,'companyid':companyid})
        return render(request,'wcctriggertime.html',data)
    
class EditWcctriggertime(View):
    def get(self,request,companyid):
        print('asd')
        get_project_ids=Projectcreation.objects.filter__by_company(request.company.id,0).values_list('id',flat=True)
        wcc_completion_data=WorkCompletionCost.objects.filter_by_project_ids(get_project_ids,0,1).count()
        masterinvoicetrigger = WccTimeTrigger.objects.filter(status=1,company=companyid) 
        dict_obj=[{'key':2,'value':'Minutes'},{'key':0,'value':'Hours'},{'key':1,'value':'Days'}]
        data={'masterinvoicetrigger':masterinvoicetrigger,'companyid':companyid,'time_format':dict_obj,'wcc_completion_data':wcc_completion_data}
        return render(request,'editwcctriggertime.html',data)
     
    def post(self,request,companyid):
        method=self.request
        pk = method.POST.getlist('pk')
        print(f"method.POST {method.POST}")
        # payment_terms_from = method.POST.getlist('payment_terms_from')
        # payment_terms_to = method.POST.getlist('payment_terms_to')
        time_unit = method.POST.getlist('time_unit')
        time_allotted = method.POST.getlist('time_allotted')
        for i, _ in enumerate(pk):
            if(pk[i] == '0'):
                WccTimeTrigger.objects.create(payment_terms_from=payment_terms_from[i],payment_terms_to=payment_terms_to[i],time_unit=time_unit[i],time_allotted=time_allotted[i],company_id=companyid,status=1)
            else:
                WccTimeTrigger.objects.filter(status=1,company=companyid,id=pk[i]).update(
                payment_terms_from=1,
                payment_terms_to=3,
                time_unit=time_unit[int(i)],
                time_allotted=time_allotted[int(i)]
                )

        masterinvoicetrigger = WccTimeTrigger.objects.filter(status=1,company=companyid)
        data={'masterinvoicetrigger':masterinvoicetrigger,'companyid':companyid}
        return render(request,'wcctriggertime.html',data)


class ListDisputeMembers(View):
    def get(self,request):
        users=list(User.objects.filter(company_id=request.company,roles_id=3,status=1).values_list('id',flat=True))
        total_users=list(UserRights.objects.filter(user_id__in=users,module_id=18,create='1').values_list('user_id',flat=True))
        dispute_handlers=User.objects.filter(company_id=request.company,roles_id=3,status=1,id__in=total_users).order_by('-id')
        usercount=dispute_handlers.count()
        data={"users":dispute_handlers,"usercount":usercount}
        return render(request,'listdisputemembers.html',data)
    
class AddCommitteMembers(View):
    def get(self,request):
        users=User.objects.filter(company_id=request.company,roles_id=3,status=1).order_by('-id')
        usercount=users.count()
        data={"users":users,"usercount":usercount}
        return render(request,'adddisputemembers.html',data)
    
    def post(self,request):
        print(f'form {self.request.POST}')
        users_list=self.request.POST.getlist('get_users')
        update_users=User.objects.filter(id__in=users_list).update(disputeuser=True)
        print(f'update_users {update_users}')
        return redirect('custom_auth:listdisputemembers')
    

def DeleteDisputeUser(request):
    user_id=request.POST.get('user_id')
    User.objects.filter(id=user_id).update(disputeuser=False)
    print(f'request {request.user.id}')
    return JsonResponse({'status':True})

def DuplicateUserCheck(request):
    user_id=request.POST.get('user_id')
    dispute_type=request.POST.get('type_dispute')
    status=False
    get_user=User.objects.filter(id=user_id)
    if dispute_type =='1': 
        if User.objects.filter(id=user_id,disputeuser=True).exists():
            status=True
            get_user=User.objects.filter(id=user_id,disputeuser=True)
        deparment=get_user.first().user_department.department if get_user.first().user_department != None else ''
        group=get_user.first().user_group.group if get_user.first().user_group != None else ''
    else:
        pk=request.POST.get('pk')
        if user_id != pk:
            if User.objects.filter(id=user_id,disputeuser=True).exists():
                status=True
                get_user=User.objects.filter(id=user_id,disputeuser=True)
    deparment=get_user.first().user_department.department if get_user.first().user_department != None else ''
    group=get_user.first().user_group.group if get_user.first().user_group != None else ''
    return JsonResponse({'status':status,'userlist':list(get_user.values()),'deparment':deparment,'group':group})


class EditUserCommittee(View):
    def get(self,request,pk):
        users=User.objects.filter(company_id=request.company,roles_id=3,status=1).order_by('-id')
        user_data=User.objects.filter(id=pk,disputeuser=True).first()
        data={'user_data':user_data,'users':users}
        return render(request,'editusercommittee.html',data)
    
    def post(self,request,pk):
        get_users=request.POST.get('get_users')
        if get_users != pk:
            update_users=User.objects.filter(id=get_users).update(disputeuser=True)
            update_users=User.objects.filter(id=pk).update(disputeuser=False)
        return redirect('custom_auth:listdisputemembers')
    
    
def dash_country_view(request):
    
    cin = request.GET.get('cin_number')
    
    company=Companies.objects.filter(cin_number=cin).first()
    company_id=company.id
    
    country_ids = list(Projectcreation.objects.filter(
        company_id=company_id, status=0
    ).values_list("country_id", flat=True).distinct())

    # Retrieve country objects based on the IDs obtained
    country_objects = Countries.objects.filter(id__in=country_ids)
    
    for country in country_objects:
    # Do something with each country object
        try:
            project=Projectcreation.objects.filter(company_id=company_id,country=country)
            for project_name in project: 
                 contract=ContractMaster.objects.filter(projects=project_name.id).values('types_service').distinct()
                 for contract_name in contract:
                    sub_contract=ContractMaster.objects.filter(projects=project_name.id, types_service=contract_name["types_service"])
                    for sub in sub_contract:
                        # print(f"{country} {project_name}  {sub.types_service } {sub.name_service }  ")
                        pass
        except:
            pass
        

    # print(country_objects)
    dataset = [{'id': '0.0', 'parent': '', 'name': 'Irock'}]

    current_id = 1 
    jun_id=current_id
    pro_id=jun_id
    sub_id=1
    def generate_pastel_color(used_colors):
        while True:
            # Generate random RGB values within the pastel range [180, 255]
            r = random.randint(120, 255)
            g = random.randint(120, 255)
            b = random.randint(120, 255)
            color = f"rgb({r}, {g}, {b})"
            if color not in used_colors:
                used_colors.add(color)
                return color
    used_colors = set()
    rgb=generate_pastel_color(used_colors)
    for country in country_objects:
          rgb=generate_pastel_color(used_colors)
          
          try:
              
            projects = Projectcreation.objects.filter(company_id=company_id, country=country)
            country_dict = {'id': f'1.{current_id}', 'parent': '0.0', 'name': str(country) ,'color':rgb}
            dataset.append(country_dict)

            try:
                for idx, project in enumerate(projects, start=1):
                    contract_type=ContractMaster.objects.filter(projects=project.id).values('types_service').distinct()
                    
                    project_dict = {'id': f'2.{jun_id}', 'parent': country_dict['id'], 'name': str(project), 'value':contract_type.count() if contract_type.count() else 1}
                    dataset.append(project_dict)
                    
                    try:
                        for contract in contract_type:
                            contract_name=ContractMaster.objects.filter(projects=project.id, types_service=contract["types_service"])

                            contract_dict = {'id': f'3.{pro_id}', 'parent': project_dict['id'], 'name': str(contract["types_service"]), 'value': contract_name.count() if contract_name.count() else 1}
                            dataset.append(contract_dict)
                           
                            try:
                                for sub in contract_name:
                                    sub_dict = {'id': f'4.{sub_id}', 'parent': contract_dict['id'], 'name': str(sub.name_service), 'value': 1}
                                    dataset.append(sub_dict)
                                    sub_id +=1
                            except:
                                pass
                            pro_id+=1
                    except:
                        pass
                        
                    jun_id+= 1
            except:
               pass
                
            
          except:
              pass
          current_id += 1    
    data = dataset
    # print(data)

    return JsonResponse({'data':data})

def error_404_view(request, exception):
    return render(request,'404.html', status=404)