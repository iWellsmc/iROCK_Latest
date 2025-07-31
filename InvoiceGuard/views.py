from django.shortcuts import render,redirect
from .models import (Module,Role,RoleRight,Right,Process,ProcessModule,Flow,FlowProcess,SignatoriesSettings,SignatoriesUsers)
from projects.models import Projects
from custom_auth.models import Companies,User,Basecountries,Settings
from django.views import View
from django.views.generic import ListView,UpdateView
from django.http import JsonResponse
# from django.db.models import F
from ast import literal_eval
from django.urls import reverse_lazy as rev
from projects.models import UserRights
from django.core.paginator import Paginator
from django.template.loader import render_to_string
# Create your views here.

class addRole(View):    
    def get(self,request):
        modules = Module.objects.get_all_module()
        return render(request,'add_role.html',{'modules':modules})
    
    def post(self,request):
        module_id = request.POST.get('module_id')
        role_id = request.POST.getlist('role_id')
        modules = Module.objects.get_by_id(module_id)
        companyId = Companies.objects.get_by_id(request.company.id)
        roleIds = []
        for role in role_id:
            roleId = Role.objects.create_role(role,companyId,modules)
            roleIds.append(roleId.id)
        request.session['roleIds'] = roleIds
        request.session['createview'] = True
        return redirect('InvoiceGuard:assign-rights-form',pk=modules.id)

class editRole(UpdateView):
    model = Role
    fields = ['role_name']
    context_object_name = 'role'
    template_name = 'edit_role.html'
    success_url = rev('InvoiceGuard:assign-rights-form')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = Role.objects.get_by_id(self.kwargs['pk'])
        return context
    def get_success_url(self):
        pk = self.kwargs['pk']
        self.request.session['roleIds'] = [pk]
        self.request.session['createview'] = False
        success_url = rev('InvoiceGuard:assign-rights-form', kwargs={'pk': pk})
        return success_url
    
    
class assignRights(View):
    def get(self,request,pk):
        sessionRoleIds = request.session.get('roleIds',None)
        if sessionRoleIds is not None:
            # getRole = Role.objects.filter(id__in=sessionRoleIds)
            getRole = Role.objects.filter_by_id(sessionRoleIds)
        else:
            # getRole = Role.objects.filter(module=pk)
            getRole = Role.objects.filter_by_id(pk)
        role_data=getRole.first()

        if (role_data.module.module_name == "WCC Approval Rights"):
            self.getRight = Right.objects.filter_only_wcc(request.user.company)
        else:
            self.getRight = Right.objects.filter_without_wcc(request.user.company) if role_data.module.id == 1 else Right.objects.filter_without_wcc(request.user.company).exclude(slug="invoice-proceed")
        return render(request,'assign_rights.html',{'getRole':getRole,'getRight':self.getRight,'pk':pk})
    def post(self,request,pk):
        self.getRight = Right.objects.filter_by_companyId(request.user.company)
        for role in request.POST.getlist('role_id'):
            for right in self.getRight:
                # get or create
                roleRight, created = RoleRight.objects.get_or_create(
                    right=right,role=Role.objects.get_by_id(role),company=request.user.company)
            right_id = request.POST.getlist(f'right_id{role}')
            assign_right = RoleRight.objects.filter_by_id(role,right_id,self.request.company).update(status=True)
            unassign_right = RoleRight.objects.filter_by_role1(role=role).exclude(right__in=right_id,company=self.request.company).update(status=False)       
        return redirect('InvoiceGuard:list-rolesandrights-form')
    
class listModule(ListView):
    model = Module
    template_name = 'list_module.html'
    context_object_name = 'modules'
    def get_queryset(self):
        return Module.objects.get_all_module()

class listRole(ListView):
    model = Module
    template_name = 'list_role.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=10)
            context['rights']=userrights
        context['modules_data'] =  Module.objects.get_all_module()
        context['userrights_count'] = Module.objects.module_count()
        return context

class listModuleBasedRole(ListView):
    model = Role
    template_name = 'modulebasedrole.html'
    def get_context_data(self,**kwargs):
        module_id=self.request.GET['module_id']
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get_by_module(self.request.user.id,10)
            context['rights']=userrights
        context['roles'] =  Role.objects.filter_by_module_id(module_id,self.request.user.company)
        context['roles_count'] =  Role.objects.filter_by_module_id(module_id,self.request.user.company).count()
        return context


    
class validateRole(View):
    def post(self,request):
        role_name = request.POST.get('role_name')
        role_id = request.POST.get('role_id')
        if role_id:
            if Role.objects.filter_by_rolename(role_name,request.company,True).exclude(id=role_id).exists():

                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            if Role.objects.filter_by_rolename(role_name,request.company,True).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
            
class deleteRole(View):
    def post(self,request):
        pk = request.POST.get('pk')
        role=Role.objects.delete_by_id(pk,request.company)
        role.status = False
        role.save()
        return JsonResponse({'status':True})

class getRights(View):
    def post(self,request):
        pk = request.POST.get('role_id')
        get_rights = RoleRight.objects.filter_by_role_with_name(pk,True)
        return JsonResponse({'datas':list(get_rights)})
    
    
class listRolesAndRights(View):
    def get(self,request,pk):
        getModuleRole = Role.objects.get_by_id(pk)
        get_right = RoleRight.objects.filter_by_role(pk,True)
        data = {'getModuleRole':getModuleRole,'get_right':get_right}
        return render(request,'role_right_detail.html',data)

class Addprocess(View):
    def get(self,request):
        modules = Module.objects.get_all_module()
        return render(request,'add_process.html',{'modules':modules})
    def post(self,request):
        process = request.POST.get('process_name')
        module_id = request.POST.getlist('module_id')
        company = Companies.objects.get_by_id(request.company.id)
        process = Process.objects.create_process(process,company)
        for module in module_id:
            ProcessModule.objects.create_process_module(process,Module.objects.get_by_id(module))
        return redirect('InvoiceGuard:list-process-form')
    
class listProcess(ListView):
    model = Process
    template_name = 'list_process.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get_by_module(self.request.user.id,6)
            context['rights']=userrights
        search_query = self.request.POST.get('q',False)
        if search_query:
            process_list = Process.objects.search_by_process(self.request.company,search_query).order_by('-id')
            context['query'] = search_query
        else:
            process_list = Process.objects.company_process(self.request.user.company).order_by('-id')
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.POST.get('pageperdata',10)
        paginator = Paginator(process_list, pageper_data)
        context['process_count'] =  process_list.count()
        context['process_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
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
            process_list = Process.objects.company_process(request.company).order_by('-id')
            context['query'] = search_query
        else:
            process_list = Process.objects.search_by_process(self.request.company,search_query).order_by('-id')
            context['query'] = search_query
        page = request.POST.get('page', 1)
        pageper_data = request.POST.get('pageperdata',10)
        paginator = Paginator(process_list, pageper_data)
        context['process_count'] =  process_list.count()
        context['process_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=request.scheme
        context['gethost']=request.get_host()
        # render to template string
        html = render_to_string('search_process.html',context,request)
        return JsonResponse({'status':True,'html':html})
    
class editProcess(View):
    def get(self,request,pk):
        process = Process.objects.get_by_id(pk)
        modules = Module.objects.get_all_module()
        process_module = ProcessModule.objects.filter_by_company(pk,request.company.id)
        return render(request,'edit_process.html',{'process':process,'process_module':process_module,'modules':modules})
    def post(self,request,pk):
        # upadte process name
        process = Process.objects.get_by_id(pk)
        process.process_name = request.POST.get('process_name')
        process.save()
        # update old process related modules
        process_module = ProcessModule.objects.filter_by_company(pk,request.company.id)
        for module in process_module:
            exists= request.POST.get(f'module_id{module.id}',False)
            if exists:
                old_module = ProcessModule.objects.get_by_id(module.id)
                old_module.module = Module.objects.get_by_id(request.POST.get(f'module_id{module.id}'))
                old_module.save()
            else:   
                module.delete()
        # add new modules
        new_module_exists = request.POST.getlist('module_id',False)
        if new_module_exists:
            new_process_module = [ProcessModule(process=process,module=Module.objects.get_by_id(i)) for i in new_module_exists]
            ProcessModule.objects.bulk_create(new_process_module)
        return redirect('InvoiceGuard:list-process-form')
    
class deleteProcess(View):
    def post(self,request):
        pk = request.POST.get('pk')
        process = Process.objects.get_by_id(pk)
        process.delete()
        return JsonResponse({'status':True})

class validateProcess(View):
    def post(self,request):
        process_name = request.POST.get('process_name')
        process_id = request.POST.get('process_id')
        if process_id:
            if Process.objects.process_and_company(process_name,request.company).exclude(id=process_id).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            if Process.objects.process_and_company(process_name,request.company).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
            
class viewProcess(View):
    def get(self,request,pk):
        process = Process.objects.get_by_id(pk)
        process_module = ProcessModule.objects.filter_by_company(pk,request.company.id)
       
        return render(request,'view_process.html',{'process':process,'process_module':process_module})
    
class addFlow(View):
    def get(self,request):
        process = Process.objects.company_process(request.company)
        return render(request,'add_flow.html',{'process':process})
    def post(self,request):
        process_id = request.POST.getlist('process')
        flow_name = request.POST.get('flow_name')
        create_flow = Flow.objects.create_flow(flow_name,request.company)
        for process in process_id:
            FlowProcess.objects.create_flow_process(create_flow,Process.objects.get(id=process))
        return redirect('InvoiceGuard:list-flow-form')

    
class listFlow(ListView):
    model = Flow
    template_name = 'list_flow.html'
    # context_object_name = 'flow'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get_by_module(self.request.user.id,7)
            context['rights']=userrights
        search_query = self.request.GET.get('q',False)
        if search_query:
            flow_list = Flow.objects.filter_by_company(self.request.user.company,True,search_query).order_by('-id')
            context['query'] = search_query
        else:
            flow_list = Flow.objects.get_company(self.request.user.company,True).order_by('-id')
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.GET.get('pageperdata',10)
        paginator = Paginator(flow_list, pageper_data)
        context['count_val']=flow_list.count()
        context['pageper_data']=pageper_data
        context['flow'] = paginator.page(page)
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
            flow_list = Flow.objects.get_company(self.request.user.company,True).order_by('-id')
            context['query'] = search_query
         
        else:
          flow_list = Flow.objects.filter_by_company(self.request.user.company,True,search_query).order_by('-id')
          context['query'] = search_query
       
        page = self.request.POST.get('page', 1)
        pageper_data = self.request.POST.get('pageperdata',10)
        paginator = Paginator(flow_list, pageper_data)
        context['count_val']=flow_list.count()
        context['flow'] = paginator.page(page)
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        context['pageper_data'] = pageper_data
        # render to template string
        html = render_to_string('search_flow.html',context,request)
        # print(html)
        return JsonResponse({'status':True,'html':html})
    
class editFlow(View):
    def get(self,request,pk):
        flow = Flow.objects.get_by_id(pk)
        process = Process.objects.company_process(request.company)
        flow_process = FlowProcess.objects.get_by_company(pk,request.company.id)
        return render(request,'edit_flow.html',{'flow':flow,'flow_process':flow_process,'process':process})
    def post(self,request,pk):
        # upadte flow name
        flow = Flow.objects.get_by_id(pk)
        flow.flow_name = request.POST.get('flow_name')
        flow.save()
        # update old flow related process
        flow_process = FlowProcess.objects.get_by_company(pk,request.company.id)
        for process in flow_process:
            exists= request.POST.get(f'process_id{process.id}',False)
            if exists:
                old_process = FlowProcess.objects.get_by_id(process.id)
                old_process.process = Process.objects.get_by_id(request.POST.get(f'process_id{process.id}'))
                old_process.save()
            else:   
                process.delete()
        # add new process
        new_process_exists = request.POST.getlist('new_process',False)
        if new_process_exists:
            new_flow_process = [FlowProcess(flow=flow,process=Process.objects.get_by_id(i)) for i in new_process_exists]
            FlowProcess.objects.bulk_create(new_flow_process)
        return redirect('InvoiceGuard:list-flow-form')
    
class deleteFlow(View):
    def post(self,request):
        pk = request.POST.get('pk')
        flow = Flow.objects.get_by_id(pk)
        flow.delete()
        return JsonResponse({'status':True})
    
class validateFlow(View):
    def post(self,request):
        flow_name = request.POST.get('flow_name')
        flow_id = request.POST.get('flow_id')
        if flow_id:
            if Flow.objects.filter_by_flow(flow_name,request.company).exclude(id=flow_id).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        else:
            if Flow.objects.filter_by_flow(flow_name,request.company).exists():
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
            
class viewFlow(View):
    def get(self,request,pk):
        flow = Flow.objects.get_by_id(pk)
        flow_process = FlowProcess.objects.get_by_company(pk,request.company.id)
        return render(request,'view_flow.html',{'flow':flow,'flow_process':flow_process})
    
class listCompanySignatory(View):
    def get(self,request):
        if (self.request.user.roles_id == 3):
            rights=UserRights.objects.get_by_module(self.request.user.id,12)
        else:
            rights = None
        company_signatory = SignatoriesSettings.objects.get_by_company(request.company,True,'1').count()
        with_invoice = SignatoriesSettings.objects.get_by_company_type(request.company,True,'1','1')
        without_invoice = SignatoriesSettings.objects.get_by_company_type(request.company,True,'2','1')
        projects=Projects.objects.filter(company=request.company,status=0)
        user = User.objects.get_by_company(request.company,[2,3],1)
        get_settings = Settings.objects.get_company(request.company).values_list('currency',flat=True).first()
        print('get_settings',get_settings)
        if get_settings!=None:
            currency = Basecountries.objects.get_by_id(literal_eval(get_settings))
            currency_count=currency.count()
        else:
            currency_count=0
            currency=[]
        return render(request,'list_signatories.html',{'user':user,'with_invoice':with_invoice,'currency':currency,'without_invoice':without_invoice,'signatory_count':company_signatory,'rights':rights,'projects':projects,'currency_count':currency_count})
    
class addUpdateSignatory(View):
    def get(self,request):
        projects=Projects.objects.filter_by_company(request.company,0)
        company_signatory = SignatoriesSettings.objects.get_by_company(request.company,True,'1')
        user = User.objects.get_by_company(request.company,[2,3],1)
        get_settings = Settings.objects.get_company(request.company).values_list('currency',flat=True).first()
        currency = Basecountries.objects.get_by_id(literal_eval(get_settings))
        return render(request,'add_update_signatory.html',{'user':user,'company_signatory':company_signatory,'currency':currency,'company_signatory_count':company_signatory.count(),'projects':projects})

class deleteSignatoryUser(View):
    def post(self,request):
        pk = request.POST.get('pk')
        signatory_user = SignatoriesUsers.objects.get_by_id(pk)
        signatory_value=signatory_user.signatory_id
        signatory_user.delete()
        count_values=SignatoriesUsers.objects.get_by_signatoryId(signatory_value).count()
        SignatoriesSettings.objects.filter_by_id(signatory_user.signatory_id).update(no_of_signatories=count_values)
        return JsonResponse({'status':True})
    

class ajaxPostViewSignatory(View):
    def post(self,request):
        get_type=request.POST.get('set_signatory')
        print('req',request.POST)
        if get_type == '1':
            for i in request.POST.getlist('signatory_id'):
                signatory, created = SignatoriesSettings.objects.update_or_create(
                    id=i,
                    defaults={
                        'min_amount': None if request.POST.get(f'min_amount{i}') == '' else request.POST.get(f'min_amount{i}').replace(',',''),
                        'max_amount': None if request.POST.get(f'max_amount{i}') == '' else request.POST.get(f'max_amount{i}').replace(',',''),
                        'currency': None if request.POST.get(f'currency{i}') == '' else Basecountries.objects.get(id=request.POST.get(f'currency{i}')),
                    }
                )
                if created:
                    signatory.company = request.company
                    signatory.save()
                signatory_user_exists = SignatoriesUsers.objects.get_by_signatory(signatory)
                if signatory_user_exists.exists():
                    user_type=1
                    for k in signatory_user_exists:
                        update_signatory_user = SignatoriesUsers.objects.get_by_id(k.id)
                        update_signatory_user.user = User.objects.get_by_id(request.POST.get(f'user{k.id}').replace(',',''))
                        update_signatory_user.usertype=user_type
                        update_signatory_user.save()
                        user_type+=1
                new_user = request.POST.getlist(f'newuser{i}',False)
                if new_user:
                    user_type=1
                    for new in new_user:
                        SignatoriesUsers.objects.create(signatory=SignatoriesSettings.objects.get_by_id(i),user=User.objects.get_by_id(new.replace(',','')),usertype=user_type) if new!='' else False
                        user_type+=1
            new_tr = request.POST.getlist('newtr',False)
            if new_tr:
                for i in range(len(new_tr)):
                    signatory_create = SignatoriesSettings.objects.create(
                        currency=None if request.POST.get(f'new_currency{i+1}') == '' else Basecountries.objects.get(id=request.POST.get(f'new_currency{i+1}')),
                        min_amount=None if request.POST.get(f'new_min_amount{i+1}') == '' else request.POST.get(f'new_min_amount{i+1}').replace(',',''),
                        max_amount=None if request.POST.get(f'new_max_amount{i+1}') == '' else request.POST.get(f'new_max_amount{i+1}').replace(',',''),
                        company = request.company,
                        invoice_type = request.POST.get(f'new_invoice_type{i+1}') if request.POST.get(f'new_invoice_type{i+1}') else request.POST.get(f'new_invoice_type{i+2}'),
                    )
                    new_user = request.POST.getlist(f'new_newuser{i+1}',False)
                    if new_user:
                        user_type=1
                        for new in new_user:
                            SignatoriesUsers.objects.create(signatory=signatory_create,user=User.objects.get_by_id(new.replace(',','')),usertype=user_type) if new!='' else False
                            user_type+=1
        elif get_type == '2':
            project=request.POST.get('get_project')
            print('qqq',request.POST.getlist('signatory_id_project'))
            for i in request.POST.getlist('signatory_id_project'):
                # print('project_id = int(project)',request.POST.get(f'max_amount_project{i}'))
                # print(i)
                # print(SignatoriesSettings.objects.filter(id=i,project_id = int(project)))
                signatory, created = SignatoriesSettings.objects.update_or_create(
                    id=i,project_id = int(project),
                    defaults={
                        'min_amount': None if request.POST.get(f'min_amount_project{i}') == '' else request.POST.get(f'min_amount_project{i}').replace(',',''),
                        'max_amount': None if request.POST.get(f'max_amount_project{i}') == '' else request.POST.get(f'max_amount_project{i}').replace(',',''),
                        'currency': None if request.POST.get(f'currency_project{i}') == '' else Basecountries.objects.get(id=request.POST.get(f'currency_project{i}')),
                    }
                )
                if created:
                    signatory.company = request.company
                    signatory.save()
                signatory_user_exists = SignatoriesUsers.objects.get_by_signatory(signatory)
                if signatory_user_exists.exists():
                    user_type=1
                    for k in signatory_user_exists:
                        update_signatory_user = SignatoriesUsers.objects.get_by_id(k.id)
                        update_signatory_user.user = User.objects.get_by_id(request.POST.get(f'user_project{k.id}').replace(',',''))
                        update_signatory_user.usertype=user_type
                        update_signatory_user.save()
                        user_type+=1

            new_tr = request.POST.getlist('newtr_project',False)
            print('new_tr',new_tr)
            if new_tr:
                for i in range(len(new_tr)):    
                    signatory_create = SignatoriesSettings.objects.create(
                        currency=None if request.POST.get(f'new_currency_project{i+1}') == '' else Basecountries.objects.get(id=request.POST.get(f'new_currency_project{i+1}')),
                        min_amount=None if request.POST.get(f'new_min_amount_project{i+1}') == '' else request.POST.get(f'new_min_amount_project{i+1}').replace(',',''),
                        max_amount=None if request.POST.get(f'new_max_amount_project{i+1}') == '' else request.POST.get(f'new_max_amount_project{i+1}').replace(',',''),
                        company = request.company,
                        invoice_type = None if request.POST.get(f'new_invoice_type_project{i+1}') == '' else request.POST.get(f'new_invoice_type_project{i+1}'),
                        signatory_type='2',
                        project_id = int(project),
                    )
                    new_user = request.POST.getlist(f'new_newuser_project{i+1}',False)
                    if new_user:
                        user_type=1
                        for new in new_user:
                            SignatoriesUsers.objects.create(signatory=signatory_create,user=User.objects.get_by_id(new.replace(',','')),usertype=user_type) if new!='' else False
                            user_type+=1

            print(3)
        return JsonResponse({'signatory_user':True})
    

class GetProjectSignatory(View):
    def get(self,request):
        pk=request.GET.get('pk')
        get_sign=SignatoriesSettings.objects.filter_by_project(int(pk),request.company.id,'2',True).values()
        # currency_type=Basecountries.objects.filter(id__in=SignatoriesSettings.objects.filter(project_id=int(pk),company_id=request.company.id,signatory_type='2',status=True).values_list('currency_id'))
        signatories=[]
        for sign in get_sign:
            currency_type=Basecountries.objects.filter_by_id(int(sign['currency_id']))
            currency_name=f'{currency_type.currency_symbol}-{currency_type.currency} ({currency_type.name})'
            get_name=SignatoriesUsers.objects.get_by_signatoryId(sign['id']).values_list('user',flat=True)
            users_name=User.objects.filter_by_userid(get_name).values('name','lastname')
            users_list=list(SignatoriesUsers.objects.get_by_signatoryId(sign['id']).values())
            sign['users']=users_list
            sign['currency_name']=currency_name
            sign['users_name']=list(users_name)
            signatories.append(sign)
            print('signatories',signatories)
        return JsonResponse(signatories, safe=False)
    

class GetSignatoryUser(View):
    def get(self,request):
        pk=request.GET.get('pk')
        SignatoriesUser= list(SignatoriesUsers.objects.get_by_signatoryId(pk).values())
        return JsonResponse(SignatoriesUser, safe=False)

class deleteSignatory(View):
    def post(self,request):
        pk = request.POST.get('pk')
        signatory = SignatoriesSettings.objects.get_by_id(pk)
        signatory.status = False
        signatory.save()
        return JsonResponse({'status':True})
    
class getModule(View):
    def post(self,request):
        pk = request.POST.get('process_id')
        print(pk,'pk')
        get_modules = Module.objects.get_by_processID(pk).values()
        return JsonResponse({'datas': list(get_modules)})