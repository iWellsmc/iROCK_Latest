from django.shortcuts import render,redirect
from django.views import View
from .models import *
from custom_auth .models import *
from django.http import JsonResponse
from custom_auth.models import Settings,Basecountries
from django.views.generic import ListView,UpdateView
from django.urls import reverse_lazy
from ast import literal_eval
from projects .models import UserRights
from django.core.paginator import Paginator
from django.template.loader import render_to_string
import ast
from django.contrib.auth.hashers import make_password
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.core import mail
from django.db.models import Q
from django.conf import settings
# Create your views here.
class CreateCompanyBank(View):
    template_name='CompanyBankCreate.html'
    def get(self,request):
        banklist = UserBankMaster.objects.filter_company(request.company)
        get_settings = Settings.objects.get_company(request.company).values_list('currency',flat=True).first()
        currency = Basecountries.objects.get_by_id(literal_eval(get_settings))
        data = {'currency':currency,'banklist':banklist}
        return render(request,self.template_name,data)
    
    def post(self,request):
        method = request.POST
        bankname = method.get('select_bank')
        currency = method.getlist('currency')
        accountno = method.getlist('accountno')
        instructortitle = method.getlist('instructortitle')
        instructorfirstname = method.getlist('instructorfirstname')
        instructorlastname = method.getlist('instructorlastname')
        

        for i in range(len(currency)):
            usertitle = method.getlist('usertitle'+str(i))
            userfirstname = method.getlist('userfirstname'+str(i))
            userlastname = method.getlist('userlastname'+str(i))
            useremail = method.getlist('useremail'+str(i))
            userdesignation = method.getlist('userdesignation'+str(i))
            companybank = CompanyBank.objects.create_companybank(request.company,currency[i],accountno[i],instructortitle[i],instructorfirstname[i],instructorlastname[i],bankname)
            password = make_password("Hello@123")
            context_password="Hello@123"
            for title,firstname,lastname,email,designation in zip(usertitle,userfirstname,userlastname,useremail,userdesignation):
             
                if not User.objects.filter(email=email,status=True,company=request.company).exists():
                    userid = User.objects.create(Title=title,name=firstname,lastname=lastname,email=email,designation_role=designation,bankuserstatus=1,cin_number=request.company.cin_number,password=password,company=request.company)
                 
                else:
                  userid = User.objects.filter(email=email,bankuserstatus=1,company=request.company).first()
              
                CompanyBankUser.objects.create(companybank_id=companybank.id,user_id=userid.id)
                if Companies.objects.filter(id=request.company.id).filter(Q(image__isnull=True) | Q(image='')):
                    imageurl=''
                else:
                    imageurl=request.company.image.url
            
                company=Companies.objects.get(id=request.company.id)
                fullname=firstname+' '+lastname
                companyusername=company.first_name+' '+company.last_name
                url=f'{request.scheme}://{request.get_host()}'
                subject = 'iROCK Login Credentials'
        
                
                usercreate = request.user.roles_id
                print('usercreate',usercreate)

                context={'areacode':company.areacode,'userrole':designation,'role':request.user.designation_role,
                'landline_countrycode':company.phone_countrycode,
                'lanline':company.phonenumber,'mobile_countrycode':company.mobile_countrycode,
                'mobile':company.mobile,'website':company.website,
                'address':company.address,'image':imageurl,
                'companyname':company.company_name,
                'cin':company.cin_number,
                'email':company.email,'fullname':fullname,'password':context_password,'url':url,'title':title,'companyusername':companyusername,'useremail':email}
                html_message = render_to_string('bankuseremail.html', context)
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to = email

                msg=mail.send_mail(subject,plain_message, from_email, [to], html_message=html_message)  
          
               
        return redirect('finance:list_details')

class CompanyBankDelete(View):
    def post(self,request,pk):
        signatory_user = CompanyBank.objects.get_by_id(pk)
        signatory_user.status=False
        signatory_user.save()
        return JsonResponse({'status':True})
    
class list_details(ListView):
    model=CompanyBank
    template_name='list_bank.html'
    def get_context_data(self,**kwargs):
        self.request.session['mainmenu']='masters'
        self.request.session['submenu']='bank_information'
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get_by_module(self.request.user.id,11)
            context['rights']=userrights
        context['list_bank']= CompanyBank.objects.get_by_company(self.request.company).order_by('-id')
        
        search_query = self.request.GET.get('q',False)
        
        bank_list = CompanyBank.objects.get_by_company(self.request.user.company).order_by('-id')
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.GET.get('pageperdata',10)
        paginator = Paginator(bank_list, pageper_data)
        context['pageper_data']=pageper_data
        context['count_val']=bank_list.count()
        context['list_bank'] = paginator.page(page)
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        return context
    
    def post(self,request):
        # call get context data
        context = {}
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get_by_module(self.request.user.id,6)
            context['rights']=userrights
        search_query = self.request.POST.get('q',False)
        
        if search_query =='':
            bank_list = CompanyBank.objects.get_by_company(self.request.company).order_by('-id')
            context['query'] = search_query
        else:
            bank_list = CompanyBank.objects.filter(company=self.request.company,status=True,bank_name__bank_name__icontains=search_query).order_by('-id')

        context['query'] = search_query
        page = self.request.POST.get('page', 1)
        pageper_data = self.request.POST.get('pageperdata',10)
        paginator = Paginator(bank_list, pageper_data)
        context['count_val']=bank_list.count()
        context['pageper_data'] = pageper_data
        context['list_bank'] = paginator.page(page)
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        # render to template string
        html = render_to_string('search_bank.html',context,request)
        return JsonResponse({'status':True,'html':html})



class EditCompanyBank(View):
    template_name='CompanyBankEdit.html'
    def get(self,request,pk):
          bankdetails = CompanyBank.objects.get_by_id(pk)
          users = CompanyBankUser.objects.filter(companybank_id=pk,status=True)
          data={'bankdetails':bankdetails,'users':users}
          return render(request,self.template_name,data)
    def post(self,request,pk):
        print("Companybankedit post method")
        paymentinstructiontitle = request.POST.get('paymentinstructiontitle')
        paymentinstructionfirstname = request.POST.get('paymentinstructionfirstname')
        paymentinstructionlastname = request.POST.get('paymentinstructionlastname')
        CompanyBank.objects.filter(id=pk).update(instructortitle=paymentinstructiontitle,instructorfirstname=paymentinstructionfirstname,instructorlastname=paymentinstructionlastname)
        userid = request.POST.getlist('userid')
        usertitle = request.POST.getlist('usertitle')
        userfirstname = request.POST.getlist('userfirstname')
        userlastname = request.POST.getlist('userlastname')
        useremail = request.POST.getlist('useremail')
        userdesignation = request.POST.getlist('userdesignation')
       
        for i in range(len(usertitle)):
            if userid[i] != '':
                User.objects.filter(id__in=CompanyBankUser.objects.filter(user_id=userid[i]).values_list('user_id', flat=True)).update(Title=usertitle[i],name=userfirstname[i],lastname=userlastname[i],email=useremail[i],designation_role=userdesignation[i])
            else:
               userid = User.objects.create(Title=usertitle[i],name=userfirstname[i],lastname=userlastname[i],email=useremail[i],designation_role=userdesignation[i],bankuserstatus=1,password=make_password("Hello@123"),company=request.company)
               CompanyBankUser.objects.create(companybank_id=pk,user_id=userid.id)
        return redirect('finance:list_details')
    
class validateActno(View):
    def post(self,request):
        actno = request.POST.get('actno')
        actno_id = request.POST.get('actno_id')
        if actno_id:
          
            if CompanyBank.objects.filter(account_number=actno,company=request.company,status=True).exclude(id=actno_id).exists():
               return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            if CompanyBank.objects.filter(account_number=actno,company=request.company,status=True).exists():
               print('val',CompanyBank.objects.filter(account_number=actno,company=request.company,status=True))
               return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
            
            
class CreateBankUser(View):
    template_name='CreateUserBank.html'
    def get(self,request):
        request.session['mainmenu']='masters'
        request.session['submenu']='bank_user'
        currenctlist = []
        currency = Settings.objects.filter(company=request.company).first()
        separated_values = ast.literal_eval(currency.currency)
        for i in separated_values:
           currenctlist.append(Basecountries.objects.get(id=i))
        data={'currency':currenctlist}
        return render(request,self.template_name,data)
    def post(self,request):
        method = request.POST
        bankname = method.getlist('bankname')
        otherdetails = method.getlist('otherdetails')
        for j in range(len(bankname)): 
            print('otherdetails',otherdetails[j])
            currency = method.getlist('currency'+str(j))
            actno = method.getlist('actno'+str(j))
            newobj = UserBankMaster.objects.create(bank_name=bankname[j],currency=currency,otherdetails=otherdetails[j],company=request.company)
            for acc in actno:
                UserBankAccountno.objects.create(accountno=acc,userbank_id=newobj.id)
        return redirect('finance:listbankuser')
    
    

class ListBankUser(View):
    template_name='ListUserBank.html'
    def get(self,request):
        data={}
        companyid=request.company.id
        userbank = UserBankMaster.objects.filter_company(request.company).order_by('bank_name')
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=11)
            data['rights']=userrights
        get_settings = Settings.objects.get_company(request.company).values_list('currency',flat=True).first()
        if get_settings!=None:
            currency = Basecountries.objects.get_by_id(literal_eval(get_settings))
            currency_count=currency.count()
        else:
            currency_count=0
            currency=[]
        data.update({'userbank':userbank,'currency_count':currency_count,'currency':currency , 'companyid':companyid})
        return render(request,self.template_name,data)
    
class ViewBankInfo(View):
    template_name='viewbankinformation.html'
    def get(self,request,pk):
        bankinformation = CompanyBank.objects.get(id=pk)
        data={'id':pk,'bankinformation':bankinformation}
        return render(request,self.template_name,data)
    
class DeleteBankUser(View):
   def post(self,request,pk):
       print('pk--',pk)
       UserBankMaster.objects.delete_bankusers(pk)
       return JsonResponse({'status':True})
   
    
class ViewBankUser(View):
   template_name='ViewUserBank.html'
   def get(self,request,pk):
       currenctlist=[]
    #    userbank = UserBankMaster.objects.get(id=pk,company=request.company,status=1)
       userbank = UserBankMaster.objects.getbank(pk,request.company)
       separated_values = ast.literal_eval(userbank.currency) 
       for i in separated_values:
            currenctlist.append(Basecountries.objects.getone_by_id(i))
       userbankactno = UserBankAccountno.objects.filter(userbank=pk)
    #    bankusers = User.objects.getbankusers(pk)
       data={'userbank':userbank,'currency':currenctlist,'userbankactno':userbankactno,} 
       return render(request,self.template_name,data)
   
class EditBankUser(View):
   template_name='EditUserBank.html'
   def get(self,request,pk):
       currenctlist=[]
       bankcurrency=[]
       userbank = UserBankMaster.objects.get_company(pk,request.company)
       separated_values = ast.literal_eval(userbank.currency)
       for i in separated_values:
            currenctlist.append(Basecountries.objects.get(id=i))
       userbankactno = UserBankAccountno.objects.filter(userbank=pk)
    #    bankusers = User.objects.getbankusers(pk)   
       currency = Settings.objects.getcompany_settings(request.company)
       separated_values_company = ast.literal_eval(currency.currency)
       for i in separated_values_company:
           bankcurrency.append(Basecountries.objects.getone_by_id(i))
       data={'userbank':userbank,'currency':userbank.currency,'bankcurrency':bankcurrency,'userbankactno':userbankactno} 
       return render(request,self.template_name,data)
   def post(self,request,pk):
        method = request.POST
        bankname = method.get('bankname')
        currency = method.getlist('currency')
        actno = method.getlist('actno')
        actnodataid = method.getlist('actnodataid')
        otherdetails = method.get('otherdetails')
        
        UserBankMaster.objects.update_bank(pk,request.company,bankname,currency,otherdetails)
        for i in range(len(actno)):
            if actnodataid[i] != ' ':
                UserBankAccountno.objects.filter(id=actnodataid[i]).update(accountno=actno[i])
            else:
                UserBankAccountno.objects.create(accountno=actno[i],userbank_id=pk)

        
        return redirect('finance:listbankuser')
   

class GetBankInformation(View):
    def post(self,request):
        currency=[]
        bankid = request.POST.get('bankid')
        userbank = UserBankMaster.objects.get(id=bankid)
        currency = Basecountries.objects.filter(id__in=literal_eval(userbank.currency)).values('id','currency_symbol','currency','name')
        accountnumber = UserBankAccountno.objects.filter(userbank=bankid).values('id','accountno')
        
        return JsonResponse({'currency':list(currency),'accountnumber':list(accountnumber)})
    
class ValidateBankname(View):
    def post(self,request):
        bankname = request.POST.get('bankname')
        bankid = request.POST.get('bankid')
        print('validate',bankname,bankid)
        if bankid != '':
            print('count',UserBankMaster.objects.filter(bank_name__iexact=bankname,company=request.company,status=True).exclude(id=int(bankid)).count())
            if UserBankMaster.objects.filter(bank_name__iexact=bankname,company=request.company,status=True).exclude(id=int(bankid)).exists():
               return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            if UserBankMaster.objects.filter(bank_name__iexact=bankname,company=request.company,status=True).exists():
                 return JsonResponse({'status':True})
            else:
                 return JsonResponse({'status':False})
       
class ValidateDuplicateBank(View):
    def post(self,request):
        actnoid = request.POST.get('actnoid')
        currency = request.POST.get('currency')
        bankid = request.POST.get('bankid')
        if CompanyBank.objects.filter(bank_name_id=bankid,account_number_id=actnoid,currency_id=currency,company=request.company,status=True).exists():
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})
       
class validateDuplicateemail(View):
    def post(self,request):
        email = request.POST.get('email')
        userid = request.POST.get('userid',None)
        print('userid------',userid)
        if userid != '':
            if User.objects.filter(email=email,company=request.company,status=True).exclude(id=userid).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            if User.objects.filter(email=email,company=request.company,status=True).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
            
       
class RemoveBankUsers(View):
    def post(self,request):
        userid = request.POST.get('userid')
        dataid = request.POST.get('dataid')
        print('Userid',userid)
        print('dataid',dataid)
        CompanyBankUser.objects.filter(user_id=userid,id=dataid).update(status=False)
        if not CompanyBankUser.objects.filter(user_id=userid,status=True):
            User.objects.filter(id=userid).update(bankuserstatus=0)
        return JsonResponse({'status':True})