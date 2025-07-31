# Standard library imports
import base64
import io
import json
import re
from io import BytesIO
# Third-party imports
import pandas as pd
from PIL import Image
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from easy_pdf.rendering import render_to_pdf_response
from tablib import Dataset
from weasyprint import HTML, CSS
import xlsxwriter
from itertools import chain,groupby
# Local application/library-specific imports
from  .models import *
from  projects.models import *
from  projects.helpers import *
from cost_code.helpers import getcostcode_format_type,getcostcodepdf_css,getcostcodepdfvendor_css,sum_costcode,getcode_format,getlastcode_bymaster,check_previous_level_exists,getlevel1_level2,getlevel1_level2_components
from cost_code.templatetags.cost_code_tags import sum_costcode,get_sub_type,getLastValue , getcostcode_preview,getcostcode_string ,getcostcode_category  
from projects.helpers import getvendorcontracts
from invoice.models import Invoice
from invoice.helpers import getvendorcostcode_bycontracts

class listCostCodeMaster(ListView):
    model = CostCodeMaster
    template_name = 'cost_code_master_list.html'
    def get_context_data(self,**kwargs):
        self.request.session['mainmenu'] = 'cost_code'
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=17)
            context['rights']=userrights
        context['cost_code_list'] = CostCodeMaster.objects.filter_by_status(1,self.request.company).order_by('id')
        context['length']=CostCodeSub.objects.get_by_company(1,self.request.company.id).count()
        context['cost_code_len'] = len(context['cost_code_list'])

        print('countttttt',CostCodeMain.objects.getallcostcode(self.request.company).count())

        return context
import json
class CreateCostCodeMaster(View):    
    def get(self,request):
        request.session['mainmenu'] = 'cost_code'
        levels = LevelMaster.objects.get_all()
        code_format=['01-00-000-000-00','01.00.000.000.00','010000000000']
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        discipline_subtype = DisciplineSubtype.objects.filter(status=1).values_list('discipline_subtype', flat=True).distinct()
        types=json.dumps(list(discipline_subtype))
        # print('types',type(types))
        # subtype=[]
        # for sub in DisciplineSubtype.objects.filter(status=1):
        #     subtype.append(sub.discipline_subtype)
        return render(request,'create_cost_code_master.html',{'levels':levels,'code_format':code_format,'alldiscipline':discipline,'alldevelopment':development_type,'discipline_subtype':discipline_subtype,'subtype':types})
    
    def post(self,request):
        cost_code_format = request.POST.get('cost_code_format')
        level_list = request.POST.getlist('level_type')
        digit_list = request.POST.getlist('num_digits')
        input_list = request.POST.get('input_type')
        start_list = request.POST.getlist('start_with')
        leveltype = request.POST.getlist('leveltype')
        newlevel = request.POST.getlist('new_level')
        level_cls=request.POST.getlist('level_cls')
        Sequence_list = request.POST.getlist('Sequence_gap')
        for level,digit,input,start,sequence,leveltype,newlevel,first_level in zip(level_list,digit_list,input_list,start_list,Sequence_list,leveltype,newlevel,level_cls):
            if(leveltype=='new'):
                levelmaster=LevelMaster.objects.createlevelmaster(newlevel,request.company.id)
                CostCodeMaster.objects.create_costcode_masternew(cost_code_format,digit,input,start,sequence,leveltype,newlevel,levelmaster.id,request.company.id)
            else:
                CostCodeMaster.objects.create_costcode_masterold(cost_code_format,level,digit,input,start,sequence,leveltype,request.company.id,first_level)
        usercreate = request.user.roles_id     
        create_user_log(request,"Cost Code Master","Cost Code Master",'Create','Cost Code Master Created',usercreate) 
        return redirect('cost_code:costcodemasterlist')

class Editcostcodemaster(View):
    def get(self,request):
        levels = LevelMaster.objects.get_all()
        cost_code_format=CostCodeMaster.objects.getfirst_level(request.company.id,1)
        costcodeformat=cost_code_format.cost_code_format
        code_format=['01-00-000-000-00','01.00.000.000.00','010000000000']
        subtype_len=CostCodeSub.objects.get_by_company(1,request.company.id).count()
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        discipline_subtype = DisciplineSubtype.objects.filter(status=1).values_list('discipline_subtype', flat=True).distinct()
        types=json.dumps(list(discipline_subtype))
        #edit
        return render(request,'edit_cost_code_master.html',{'levels':levels,'code_format':code_format,'costcodeformat':costcodeformat,'company':request.company,'subtype_len':subtype_len,'alldiscipline':discipline,'alldevelopment':development_type,'discipline_subtype':discipline_subtype,'subtype':types})
    
    def post(self,request):
        print(f"post {request.POST}")
        costcodemasterid = request.POST.getlist('costcodemasterid')
        level_type= request.POST.getlist('level_type')
        new_level= request.POST.getlist('new_level')
        cost_code_format = request.POST.get('cost_code_format')
        digit_list = request.POST.getlist('num_digits')
        input_list = request.POST.get('input_type')
        start_list = request.POST.getlist('start_with')
        Sequence_list = request.POST.getlist('Sequence_gap')
        leveltype= request.POST.getlist('leveltype')
        # level_cls=request.POST.getlist('level_cls')
        for i in range(len(costcodemasterid)):
            if(costcodemasterid[i]):
                CostCodeMaster.objects.update_costcode_master(cost_code_format,digit_list[i],input_list,start_list[i],Sequence_list[i],costcodemasterid[i],level_type[i])
                new_data=CostCodeMaster.objects.filter(id=costcodemasterid[i]).first()
                LevelMaster.objects.filter(id=new_data.level_type_id).update(level_name=level_type[i])
                if(leveltype[i]=='new'):
                    levelmasterid = CostCodeMaster.objects.filter(id=costcodemasterid[i]).values('level_type_id').first()
                    LevelMaster.objects.filter(id=levelmasterid['level_type_id']).update(level_name=level_type[i])
            else:
                if i==1:
                    CostCodeMaster.objects.create_costcode_masterold(cost_code_format,2,digit_list[i],input_list[i],start_list[i],Sequence_list[i],leveltype[i],request.company.id,level_type[i])
                else:
                    levelmaster=LevelMaster.objects.createlevelmaster(level_type[i],request.company.id)
                    CostCodeMaster.objects.create_costcode_masternew(cost_code_format,digit_list[i],input_list,start_list[i],Sequence_list[i],leveltype[i],level_type[i],levelmaster.id,request.company.id)

        return redirect('cost_code:costcodemasterlist')


class listCostCodeType(ListView):
    model = CostCodeMaster
    template_name = 'cost_code_type_list.html'
    def get_context_data(self,**kwargs):
        self.request.session['mainmenu'] = 'cost_code'
        context = super().get_context_data(**kwargs)
        get_id=self.kwargs.get('pk')
        level = CostCodeMaster.objects.get_by_level_id(get_id)
        cost_code_type_list = CostCodeType.objects.filter_by_codemaster(level,1,self.request.company).order_by('component_cost_code')
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=17)
            context['rights']=userrights
        context['pk'] = get_id
        context['level'] =level
        context['get_id']=get_id
        context['company'] = self.request.company
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.GET.get('pageperdata',10)
        paginator = Paginator(cost_code_type_list, pageper_data)
        context['process_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()

        return context
  
    def post(self, request, *args, **kwargs):
        context = {}
        get_id=self.kwargs.get('pk')
        level = CostCodeMaster.objects.get_by_level_id(get_id)
        if request.FILES:
            dataset= Dataset()
            import_file =request.FILES.get('import_file',None)
            imported_data = dataset.load(import_file.read(),format='xlsx')
            i=0
            new_array=[]
            while i<len(imported_data):
                if (imported_data[i][1] != None):            
                    check=list(CostCodeType.objects.check_data(request.POST.get('cost_code_id'),imported_data[i][1],1))
                    if (len(check) == 0):
                        new_array.append(imported_data[i][1])
                i+=1
            request.session['costcodeid']=request.POST.get('cost_code_id')
            request.session['costcodearray']=new_array
            return redirect('cost_code:importcostcodecomponent')
        search_query = self.request.POST.get('q',False)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=17)
            context['rights']=userrights
        if search_query =='':
            cost_code_type_list = CostCodeType.objects.filter_by_codemaster(level,1,self.request.company).order_by('component_cost_code')
            
        else:
            cost_code_type_list = CostCodeType.objects.filter(company=self.request.user.company,status=True,component_name__icontains=search_query).order_by('component_cost_code')
        context['query'] = search_query
        page = request.POST.get('page', 1)
        pageper_data = request.POST.get('pageperdata',10)
        paginator = Paginator(cost_code_type_list, pageper_data)
        context['process_count'] =  cost_code_type_list.count()
        context['process_list'] = paginator.page(page)
        context['pageper_data'] = pageper_data
        context['scheme']=request.scheme
        context['gethost']=request.get_host()
        context['pk'] = get_id
        context['level'] =level
        context['get_id']=get_id
        context['company'] = request.company
        # render to template string
        html = render_to_string('search_CostCodeType.html',context,request)
        # print(html)
        return JsonResponse({'status':True,'html':html})
        


class CreateCostCodeType(View):    
    def get(self,request,level_id):
        set_val = getLastValue(level_id,request.company)
        costcodemasterid = CostCodeMaster.objects.filter(level_type=level_id).first()
        request.session['mainmenu'] = 'cost_code'
        return render(request,'create_cost_code_type.html',{'level':set_val[1],'level_id':level_id,'set_val':set_val[0],'costcodemasterid':costcodemasterid.id,'costcodemaster':costcodemasterid})
    
    def post(self,request,level_id):
        component_name_list = request.POST.getlist('component_name')
        # component_cost_code_list = request.POST.getlist('component_cost_code')
        level = CostCodeMaster.objects.get_by_level_id(level_id)
        for component_name in zip(component_name_list):
            CostCodeType.objects.create_costcode_type(component_name,None,level,request.company)
        return redirect('cost_code:costcodetypelist',pk=level_id)
    
def getLastValue(level_id,company):
    level = CostCodeMaster.objects.get_by_level_id(level_id)
    print('level',level)
    data=CostCodeType.objects.filter_by_codemaster(level,1,company).order_by('-component_cost_code').first()
    if (data != None):
        set_val = int(data.component_cost_code)+int(level.sequence_gap)+1
        data = str(set_val).zfill(int(level.no_digits))
        if len(str(set_val)) > int(level.no_digits):
            set_val=''
            data=str(set_val)        
    return data,level

class getmaxvalue(View):
    def get(self,request):
        level_id=request.GET.get('masterId')
        master_id=request.GET.get('current_id')
        print(level_id,master_id)
        set_val = getLastValue(int(level_id),request.company)[1]
        level = CostCodeMaster.objects.get_by_id(int(master_id))
        data=CostCodeType.objects.filter_by_codemaster(master_id,1,request.company).order_by('-component_cost_code').first()
        if (data != None):
            print(1)
            set_val = int(data.component_cost_code)+int(level.sequence_gap)+1
            data = str(set_val).zfill(int(level.no_digits))
        else:
            set_val = getLastValue(int(level_id),request.company)[1]
            data = set_val.start_with
        sequencegap = level.sequence_gap
        no_digits=level.no_digits
        response_data = {
        'data': data,
        'sequencegap':sequencegap,
        'no_digits':no_digits
        }
        return JsonResponse(response_data,safe=False)
        

class editCostCodeType(View):    
    def get(self,request,pk):
        data = CostCodeType.objects.get_by_id(pk,1)
        request.session['mainmenu'] = 'cost_code'
        return render(request,'edit_cost_code_type.html',{'cost_code_type':data,'cost_code_typeid':data.cost_code_id})
    
    def post(self,request,pk):
        component_name = request.POST.get('component_name')
        component_cost_code = request.POST.get('component_cost_code')
        data = CostCodeType.objects.get_by_id(pk,1)
        CostCodeType.objects.update_data(component_name,component_cost_code,pk)
        return redirect('cost_code:costcodetypelist',pk=data.cost_code.level_type_id)

class Displaycostcode(View):
    def get(self,request):
        allcost_code= json.loads(request.session['allcostcode'])
        total_length_code=request.session['total_length_code']
        total_length=range(3,total_length_code+1)
        cost_code_format=getcostcode_format_type(request.company.id)
        level1_development=allcost_code[0]['level1_split'][0]
        level1_discipline=allcost_code[0]['level1_split'][1]
        level2_id=allcost_code[0]['level2_split'][0]
        total_length_iteration=range(1,total_length_code-2)
        level1_master=CostCodeMaster.objects.getmaster_by_limit_offset(request.company.id,0)
        level2_master=CostCodeMaster.objects.getmaster_by_limit_offset(request.company.id,1)


        return render(request, "listcostcode.html",{'allcost_code':allcost_code,'total_length':total_length,'total_length_code':total_length_code,'cost_code_format':cost_code_format,'level1':allcost_code[0]['level1_discipline']+'('+allcost_code[0]['level1']+')','level2':allcost_code[0]['level2'],'first_row':allcost_code[0],'level1_discipline':level1_discipline,'level1_development':level1_development,'level2_id':level2_id,'total_length_iteration':total_length_iteration,'level1_master':level1_master,'level2_master':level2_master})
    
    def post(self,request):
        print(f"post {request.POST}")
        allcost_code= json.loads(request.session['allcostcode'])
        costcode_main=CostCodeMain.objects.getcostcode_level1_level2(request.POST.get('level1_development_id'),request.POST.get('level1_discipline_id'),request.company,request.POST.get('level2_code'))
        if(costcode_main==None):
            costcode_main=CostCodeMain.objects.create_costcode_main(request.POST.get('level1_discipline_id'),request.POST.get('level1_development_id'),request.POST.get('level2_id'),request.POST.get('level1_code'),request.POST.get('level2_code'),request.company)
            start=1
        else:
            costcodesub=CostCodeSub.objects.getlastcostcodesub(costcode_main.id)
            start=costcodesub.order+1
        allsubcode_list=[]
        for i in range(0,len(allcost_code)):
            cost_code=request.POST.get('cost_code'+str(i+1))
            remaining_levels=request.POST.getlist('remaininglevels'+str(i+1))
            remaining_levels_code=request.POST.getlist('code'+str(i+1))
            remaining_cost_code_type=request.POST.getlist('cost_code_type'+str(i+1))
            level_index=2
            if 'old' in remaining_cost_code_type:
                continue
            else:
                for j in range(len(remaining_levels)):
                    cost_code_master=CostCodeMaster.objects.getmaster_by_limit_offset(request.company,level_index)
                    costcode_type_id=CostCodeType.objects.check_component_exist_new(cost_code_master.id,request.company,remaining_levels[j],costcode_main.id)
                    if(not costcode_type_id):
                        costcode_type_id=CostCodeType.objects.create_costcode_type(remaining_levels[j],remaining_levels_code[j],cost_code_master,request.company,costcode_main.id)
                    allcostcode_sub_data=CostCodeSub(cost_code=remaining_levels_code[j],order=start,company=request.company,cost_type_id=costcode_type_id.id,costcode_main_id=costcode_main.id,costcode_preview=cost_code,costcode_master_id=cost_code_master.id)
                    allsubcode_list.append(allcostcode_sub_data)

         
                    level_index +=1
            start +=1
        CostCodeSub.objects.bulk_create(allsubcode_list)

            

        return redirect('cost_code:costcodelist')

def getcost_code(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
    costcode_sub=CostCodeSub.objects.getcostcodesub_by_limit_offset(start,length,request.company.id,search_value)
    costcode_sub_total=CostCodeSub.objects.getcostcodesub_total(request.company.id,search_value)
    non_zero_sequence_count=0
    for remaining_level in get_remaining_level:
        if(remaining_level.sequence_gap != '0'):
            non_zero_sequence_count +=1
    
    # print(f"non_zero_sequence_count {non_zero_sequence_count}")
    print(f"costcode_sub_total {costcode_sub_total.count()}")

    costcode_format=getcostcode_format_type(request.company)
    allcost_code=[]
    s_no=start+1
    for costcode in costcode_sub:
        costcode_main=CostCodeMain.objects.getcostcodemain_byid(costcode['costcode_main_id'])
        print(f"costcode_main {costcode_main}")

        # level1_discipline=ProjectDiscipline.objects.get_discipline_byid(costcode_main.level1_discipline_id)
        level1_discipline=ProjectDiscipline.objects.get_discipline_byid(costcode_main.level1_discipline_id)

        # level1_development=DevelopmentType.objects.getall_development_byid(costcode_main.level1_developmenttype_id)
        level1_development=DevelopmentType.objects.getall_development_byid(costcode_main.level1_developmenttype_id)

        level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(costcode_main.level2_discipline_id)
        codecode_component=level1_discipline.name+'('+level1_development.development_type+')/'+level2_name.discipline_subtype+'/'
        costcodesub_byorder=CostCodeSub.objects.getcostcodemain_byorder_costcodemain(costcode['order'],request.company.id,costcode['costcode_main_id'])
        costcode_view=costcode_main.level1_cost_code+costcode_format+costcode_main.level2_cost_code+costcode_format
        index=0
        for costcodesub in costcodesub_byorder:
            status=costcodesub.status
            costcodesub_componenttype=CostCodeSub.objects.getcostcodesub_component_details(costcodesub.id)
            # print(f"data {costcodesub_componenttype.cost_type.component_name}")
            codecode_component +=costcodesub_componenttype.cost_type.component_name
            costcode_view +=costcodesub.cost_code
            print(f"costcodesub.cost_code {costcodesub.cost_code}")
            if(index == 0):
                if costcodesub.cost_code == '':
                    costcodesub.cost_code = 00
                else:
                    orderby_costcode=int(costcodesub.cost_code)
            
            if index != len(get_remaining_level) - 1:
                costcode_view +=costcode_format
                codecode_component +='/'

            index +=1

        allcost_code.append({
            's_no':s_no,
            'codecode_component':codecode_component,
            'costcode':costcode_view,
            'order':costcode['order'],
            'costcode_main_id':costcode_main.id,
            'orderby_costcode':orderby_costcode,
            'status':status,
            'level1_code':costcode_main.level1_cost_code,
            'level2_code':costcode_main.level2_cost_code
        })
        s_no +=1
    
   
    sorted_allcost_code = sorted(allcost_code, key=lambda x: (x['level1_code'], x['level2_code']))

    sorted_allcost_code_with_serial = [
        {**item, 's_no': start+(index + 1)} for index, item in enumerate(sorted_allcost_code)
    ]
    response = {
        'draw': draw,
        'recordsTotal': costcode_sub_total.count(),
        'recordsFiltered': costcode_sub_total.count(),
        'data': sorted_allcost_code_with_serial,
        'extra_data': {
        'sequence_gap_level_count': non_zero_sequence_count
        }
    }

    return JsonResponse(response)


def getvendor_costcode(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    vendor_id=request.GET['vendor_id'] 
    contract_id=request.GET['contract_id'] 

    print(f"vendor_id {vendor_id}")
    contract_masters=ContractMaster.objects.getcontract(contract_id)
    get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
    costcode_main_set = set()
    costcode_format=getcostcode_format_type(request.company)
    allcost_code=[]
    if contract_masters:
        projectdevelopmentdiscipline=ProjectDevelopmentDiscipline.objects.getdevelopment_details(contract_masters.projectdiscipline_id)
        level1_discipline=projectdevelopmentdiscipline.project_discipline
        if projectdevelopmentdiscipline.development_type.development.development_type == 'Oil_Development':
            level1_development_type=1
        elif projectdevelopmentdiscipline.development_type.development.development_type == 'Gas_Development':
            level1_development_type=2
        elif projectdevelopmentdiscipline.development_type.development.development_type == 'Unconventional_Oil':
            level1_development_type=3
        else:
            level1_development_type=4

        level2_discipline=ProjectDevelopmentSubType.objects.getdetails_byid(contract_masters.projectdisciplinetype_id)
        level2_discipline=level2_discipline.discipline_subtype.id
        costcode_by_level1_level2=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_discipline,level1_development_type,level2_discipline,request.company)
        if costcode_by_level1_level2:
            costcode_main_set.add(costcode_by_level1_level2.id)
        allcostcode=list(costcode_main_set)
        
        # print(f"allcostcode_main_id {allcostcode}")
        costcodesub=CostCodeSub.objects.getcostcodesub_by_limit_offset_costcodemain(start,length,request.company.id,search_value,allcostcode)
        # print(f"costcodesub {costcodesub}")
        costcodesub_total=CostCodeSub.objects.getcostcodesub_by_total_costcodemain(request.company.id,search_value,allcostcode)

        s_no=start+1
        for costcode in costcodesub:
            costcode_main=CostCodeMain.objects.getcostcodemain_byid(costcode['costcode_main_id'])
            level1_discipline=ProjectDiscipline.objects.get_discipline_byid(costcode_main.level1_discipline_id)
            level1_development=DevelopmentType.objects.getall_development_byid(costcode_main.level1_developmenttype_id)
            level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(costcode_main.level2_discipline_id)
            codecode_component=level1_discipline.name+'('+level1_development.development_type+')/'+level2_name.discipline_subtype+'/'
            costcodesub_byorder=CostCodeSub.objects.getcostcodemain_byorder_costcodemain(costcode['order'],request.company.id,costcode['costcode_main_id'])
            costcode_view=costcode_main.level1_cost_code+costcode_format+costcode_main.level2_cost_code+costcode_format
            index=0
            for costcodesub in costcodesub_byorder:
                status=costcodesub.status
                costcodesub_componenttype=CostCodeSub.objects.getcostcodesub_component_details(costcodesub.id)
                # print(f"data {costcodesub_componenttype.cost_type.component_name}")
                codecode_component +=costcodesub_componenttype.cost_type.component_name
                costcode_view +=costcodesub.cost_code
                if(index == 0):
                    orderby_costcode=int(costcodesub.cost_code)
                
                if index != len(get_remaining_level) - 1:
                    costcode_view +=costcode_format
                    codecode_component +='/'

                index +=1
            check_vendor_costcode_exist=CostCodeVendor.objects.getcostcodevendor_bystatus_main_order(costcode['costcode_main_id'],costcode['order'],request.company.id,vendor_id,contract_id)
            print(f"check_vendor_costcode_exist {check_vendor_costcode_exist}")
        
            allcost_code.append({
                's_no':s_no,
                'codecode_component':codecode_component,
                'costcode':costcode_view,
                'order':costcode['order'],
                'costcode_main_id':costcode_main.id,
                'orderby_costcode':orderby_costcode,
                'status':status,
                'level1_code':costcode_main.level1_cost_code,
                'level2_code':costcode_main.level2_cost_code,
                'vendor_costcode_exists':True if check_vendor_costcode_exist else False
            })
            s_no +=1
        
    
        sorted_allcost_code = sorted(allcost_code, key=lambda x: (x['level1_code'], x['level2_code']))

        sorted_allcost_code_with_serial = [
            {**item, 's_no': start+(index + 1)} for index, item in enumerate(sorted_allcost_code)
        ]
        total_count=costcodesub_total.count()
    else:
        sorted_allcost_code_with_serial =[]
        total_count=0


    response = {
        'draw': draw,
        'recordsTotal': total_count,
        'recordsFiltered': total_count,
        'data': sorted_allcost_code_with_serial,
    }

    return JsonResponse(response)


def update_costcode_status(request):
    order=request.GET['order']
    costcode_mainid=request.GET['costcode_mainid']
    status=request.GET['status']
    checkcostcode_vendor=CostCodeVendor.objects.getcostcodevendor_bystatus_main_order(costcode_mainid,order,request.company.id)
    if(not checkcostcode_vendor):
        CostCodeSub.objects.deletecostcode(costcode_mainid,order,status)
        return JsonResponse({'status':True})
    else:
        return JsonResponse({'status':False})


def getcomponent(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '') 
    costcode_master_id=request.GET.get('costcode_master_id')
    costcodemaster=CostCodeMaster.objects.get_by_level_id(costcode_master_id)

    component=CostCodeType.objects.getcostcodetype_bymasterid_table(costcodemaster.id,1,start,length,search_value)
    allcomponent=CostCodeType.objects.getallcostcodetype_bymasterid(costcodemaster.id,1,search_value)

    allcostcode_component=[]
    s_no=start+1
    for sub_component in component:
        allcostcode_component.append({
            's_no':s_no,
            'name':sub_component.component_name,
        })
        s_no +=1

    response = {
        'draw': draw,
        'recordsTotal': allcomponent.count(),
        'recordsFiltered': allcomponent.count(),
        'data': allcostcode_component
    }

    return JsonResponse(response)






class Addsequence(View):
    def post(self,request):
        print(f"post {request.POST}")
        get_remaining_level=CostCodeMaster.objects.getremaining_level(self.request.company,1)
        totallevel=get_remaining_level.count()+2
        sequence_level=int(request.POST.get('sequence_level'))
        costcode_main_id=request.POST.get('costcode_main_id')
        costcodesub=CostCodeSub.objects.getcostcodemain_byorder(request.POST.get('order'),self.request.company.id,costcode_main_id).first()
        costcode_main=CostCodeMain.objects.getmaincostcode_byid(costcodesub.costcode_main_id)
        last_costcode_sub=CostCodeSub.objects.getlastorder(request.company.id)
        next_code=last_costcode_sub.order+1
        costcode_format=getcostcode_format_type(request.company)
        level_index=3
        costcode=costcode_main.level1_cost_code+costcode_format+costcode_main.level2_cost_code+costcode_format
        index=0
        for level in get_remaining_level:
            if(sequence_level == level_index):
                subcostcode=CostCodeSub.objects.getcostcodesub_by_master_order(request.POST.get('order'),request.company,level.id,costcodesub.costcode_main_id)
                last_code=sum_costcode(subcostcode.cost_code,1)
                create_costcode_type=CostCodeType.objects.create_costcode_type(request.POST.get('level'+str(level_index)),last_code,level,request.company)
                costcode_type_id=create_costcode_type.id
              
            else:
                last_code=level.start_with
                if 'level'+str(level_index) in request.POST:
                    create_costcode_type=CostCodeType.objects.create_costcode_type(request.POST.get('level'+str(level_index)),last_code,level,request.company)
                    costcode_type_id=create_costcode_type.id

                else:
                    subcoodes_by_level=CostCodeSub.objects.getcostcodesub_by_master_order(request.POST.get('order'),request.company,level.id,costcodesub.costcode_main_id)
                    last_code=subcoodes_by_level.cost_code
                    costcode_type_id=subcoodes_by_level.cost_type_id


            costcode +=last_code
            if index != len(get_remaining_level) - 1:
                costcode +=costcode_format
            
            CostCodeSub.objects.create_costcode_sub(last_code,next_code,costcode_type_id,costcodesub.costcode_main_id,request.company,None,level.id)

            level_index +=1
            index +=1
        CostCodeSub.objects.updatecostcode_preview_byorder(next_code,costcodesub.costcode_main_id,costcode)
        return redirect('cost_code:costcodelist')

def check_sequence_exist(request):
    order=request.GET['order']
    costcode_main_id=request.GET['costcode_main']

    getcostcodemain_from_sub=CostCodeSub.objects.getcostcodemain_byorder(order,request.company.id,costcode_main_id).first()
    costcode_main=CostCodeMain.objects.getmaincostcode_byid(getcostcodemain_from_sub.costcode_main_id)
    costcode_sub=CostCodeSub.objects.getcostcodemain_byorder(order,request.company.id,costcode_main_id)
    print(f"costcode_sub {costcode_sub}")

    level_index=3
    alllevel=[]
    for subcode in costcode_sub:
        costcode_master=CostCodeMaster.objects.get_by_id(subcode.costcode_master_id)
        next_code=int(subcode.cost_code)+1
        zerofill_code=str(next_code).zfill(int(costcode_master.no_digits))

        check_nextcode_exist=CostCodeSub.objects.check_nextcode_available(request.company.id,subcode.costcode_master_id,getcostcodemain_from_sub.costcode_main_id,zerofill_code)
        if(check_nextcode_exist.count() == 0):
            alllevel.append({'level_index':level_index,'name':'Level '+str(level_index)})
        level_index +=1
    return JsonResponse({"data":alllevel})



class listCostCode(View):
    def get(self, request):
        userrights=''
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        listcode_count1 = CostCodeSub.objects.filter(costcode_main__company=self.request.company,status=1).count()
        count1=CostCodeMaster.objects.filter(company_id=self.request.company.id,status=1).count()
        if(getlastlevel != None):
            lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        else:
            lastlevel=None
        all_costcode = CostCodeMain.objects.getallcostcode(self.request.user.company).order_by('-id')
        # sub_cost_list=[]
        count = CostCodeSub.objects.filter(costcode_main__company=request.company,status=1).count()
        scheme=self.request.scheme
        gethost=self.request.get_host()
        getlevel1=CostCodeMaster.objects.filter_by_level_id(request.company,1)
        # getlevel2=CostCodeMaster.objects.filter_by_level_id(request.company,2)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=17)
        alllevel1_data=[]
        total_length=''
        if(getlevel1 != None):
            previous_code=getlevel1.start_with
            for level1_discipline in discipline:
                for level1_development in development_type:
                    alllevel1_data.append({
                        'value':str(level1_discipline.id)+'_'+str(level1_development.id)+'_'+str(previous_code),
                        'name':level1_discipline.name+'('+level1_development.development_type+')'
                    })

                    previous_code=sum_costcode(previous_code,int(getlevel1.sequence_gap)+1)
            total_length=range(3,get_remaining_level.count()+3)
        print(f"total_length {total_length}")
        listcode_count1 = CostCodeSub.objects.filter(costcode_main__company=self.request.company,status=1).count()
        return render(request, "cost_code_list.html",{'company':request.company,'scheme':scheme,'gethost':gethost,'listcount':count,'rights':userrights,'alllevel1_data':alllevel1_data,'total_length':total_length,'totallevel':get_remaining_level.count()+2,"count1":count1})

    def post(self,request):
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        count = CostCodeSub.objects.filter(costcode_main__company=request.company,status=1).count()
        userrights=''
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=17)
        
        if (request.FILES):
            costcodefile=request.FILES.get('costcodefile',None)
            if (costcodefile):
                allcost_code=[]
                getlevel1_level2_list=getlevel1_level2_components()
                level1_split=request.POST.get('level1_category').split('_')
                level2_split=request.POST.get('level2_category').split('_')

                level1_discipline=ProjectDiscipline.objects.get_discipline_byid(level1_split[0])
                level1_development=DevelopmentType.objects.getall_development_byid(level1_split[1])
                level1_name=level1_discipline.name+'('+level1_development.development_type+')'
                level1_remaining_list = [level1 for level1 in getlevel1_level2_list['level1'] if level1 != level1_name]
                level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(level2_split[0])
                level2_remaining_list = [level2 for level2 in getlevel1_level2_list['level2'] if level2 !=level2_name.discipline_subtype]

                
                df = pd.read_excel(costcodefile)  

                is_level1_present = df.iloc[:, 0].isin(level1_remaining_list).any()
                is_level2_present = df.iloc[:, 1].isin(level2_remaining_list).any()

                if(is_level1_present == True or is_level2_present == True):
                    messages.error(request, "Invalid File")
                    return redirect(request.META.get('HTTP_REFERER'))

              
                df = df.iloc[:, 2:]
                df = df.dropna(how='any')
                getlevel1=CostCodeMaster.objects.filter_by_level_id(request.company,1)
                check_costcode_exists=CostCodeMain.objects.getallcostcode(request.company)
                if(check_costcode_exists.count() == 0):
                    level1_code=getlevel1.start_with
                else:
                    last_code=check_costcode_exists.last()
                    level1_code=sum_costcode(last_code.level1_cost_code,getlevel1.sequence_gap)
                
                getlevel2=CostCodeMaster.objects.filter_by_level_id(request.company,2)
                check_level2_code=CostCodeMain.objects.filter_by_development(level1_split[0],level1_split[1],1,request.company)
          
                costcode_main=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_split[0],level1_split[1],level2_split[0],request.company)
               

             
              
               
                if(costcode_main):
                    costcode_subs=CostCodeSub.objects.getallsubcode_bymainids(costcode_main.id)
                else:
                    costcode_subs=None 
                
                if(check_level2_code.count() == 0):
                    level2_code=getlevel2.start_with
                else:
                    last_code=check_level2_code.last()
                    level2_code=sum_costcode(last_code.level2_cost_code,getlevel2.sequence_gap)
                

                for index, row in df.iterrows():

                    data_append={'level1_code':level1_split[2],'level2_code':level2_split[1],'level1':level1_development.development_type,'level2':level2_name.discipline_subtype,'level1_discipline':level1_discipline.name,'level1_split':level1_split,'level2_split':level2_split}
                    level_index=3
                    for col in range(len(df.columns)):
                        # print(f"row[col] {row[col]}")
                        # print(f"level1_name {level1_name}")

                        getsequence_gap=CostCodeMaster.objects.getmaster_by_limit_offset(request.company.id,level_index-1)
                        start_with=getlastcode_bymaster(costcode_subs,level_index,getsequence_gap,request.company,row[col],row[col-1],costcode_main)
                        if(costcode_main):
                            check_component_exist=CostCodeType.objects.check_component_exist_new(getsequence_gap.id,request.company,row[col],costcode_main.id)
                        else:
                            check_component_exist=None
                        # print(f"check_component_exist {check_component_exist}")
                        
                        if(not check_component_exist):
                            if(index ==0):
                                if(col == 0):
                                    previous_code=start_with
                                else:
                                    previous_level_exists=check_previous_level_exists(getsequence_gap,data_append['level'+str(level_index-1)+'_code'],data_append['level'+str(level_index-1)],request.company)
                                    if(previous_level_exists):
                                        previous_code=start_with
                                    else:
                                        previous_code=getsequence_gap.start_with

                            else:
                                last_dict = allcost_code[-1]
                                last_code=last_dict['level'+str(level_index)+'_code']
                                if(col == len(df.columns)-1):

                                    if(row[col-1] == last_dict['level'+str(level_index-1)]):
                                        previous_code=sum_costcode(last_dict['level'+str(level_index)+'_code'],int(getsequence_gap.sequence_gap)+1)
                                    else:
                                        previous_code=start_with
                                elif(col == 0):
                                    if(row[col] == last_dict['level'+str(level_index)]):
                                        previous_code=last_dict['level'+str(level_index)+'_code']
                                    else:
                                        previous_code=sum_costcode(last_dict['level'+str(level_index)+'_code'],int(getsequence_gap.sequence_gap)+1)
                                else:
                                    if(row[col] == last_dict['level'+str(level_index)]):
                                        previous_code=last_dict['level'+str(level_index)+'_code']
                                    else:
                                        if(row[col-1] == last_dict['level'+str(level_index-1)]):
                                            previous_code=sum_costcode(last_dict['level'+str(level_index)+'_code'],int(getsequence_gap.sequence_gap)+1)
                                        else:
                                            previous_code=start_with

                            data_append['level'+str(level_index)+'_code']=previous_code
                            data_append['level'+str(level_index)]=row[col]
                        else:
                            # print(f"row[col] {row[col]}")
                            if(level_index == 3):
                                data_append['level'+str(level_index)+'_code']=check_component_exist.component_cost_code
                                data_append['level'+str(level_index)]=row[col]
                            else:
                                codecodesubs=CostCodeSub.objects.getcostcodesub_by_costtype_id(check_component_exist.id,request.company.id,costcode_main.id)
                                all_component=[]
                                if(codecodesubs.count() >0):
                                    for subcostcode in codecodesubs:
                                        previous_costcode_sub=CostCodeSub.objects.getprevious_costcode(subcostcode.id,subcostcode.order)
                                        if(previous_costcode_sub):
                                            component_type=CostCodeType.objects.get_by_id(previous_costcode_sub.cost_type_id,1)
                                            all_component.append(component_type.component_name)

                                # print(f"all_component {all_component}")
                                if row[col-1] in all_component:
                                    data_append['level'+str(level_index)+'_code']=check_component_exist.component_cost_code
                                    data_append['level'+str(level_index)]=row[col]
                                else:
                                    last_dict = allcost_code[-1]
                                    last_code=last_dict['level'+str(level_index)+'_code']
                                    if(row[col-1] == last_dict['level'+str(level_index-1)]):
                                        data_append['level'+str(level_index)+'_code']=sum_costcode(last_dict['level'+str(level_index)+'_code'],int(getsequence_gap.sequence_gap)+1)
                                        data_append['level'+str(level_index)]=row[col]
                                    else:
                                        data_append['level'+str(level_index)+'_code']=start_with
                                        data_append['level'+str(level_index)]=row[col]

                            # if(index ==0):
                            #     data_append['level'+str(level_index)+'_code']=check_component_exist.component_cost_code
                            #     data_append['level'+str(level_index)]=row[col]
                            # else:
                            #     previoussequence_gap=CostCodeMaster.objects.getprevious_costcode_master(getsequence_gap.id,request.company.id)
                            #     previous_component=CostCodeType.objects.check_component_exist(previoussequence_gap.id,request.company,row[col-1])
                            #     print(f"previous_component {previous_component}")
                            #     if(not previous_component):
                            #         if(row[col-1] == allcost_code[-1]['level'+str(level_index-1)]):
                            #             data_append['level'+str(level_index)+'_code']=sum_costcode(allcost_code[-1]['level'+str(level_index)+'_code'],int(getsequence_gap.sequence_gap)+1)
                            #             data_append['level'+str(level_index)]=row[col]

                            #         else:
                            #             data_append['level'+str(level_index)+'_code']=start_with
                            #             data_append['level'+str(level_index)]=row[col]
                            #     else:
                                    
                            #         data_append['level'+str(level_index)+'_code']=check_component_exist.component_cost_code
                            #         data_append['level'+str(level_index)]=row[col]

                        level_index +=1
                    allcost_code.append(data_append)
                cost_code_format=getcostcode_format_type(request.company.id)
                request.session['allcostcode']= json.dumps(allcost_code)
                request.session['total_length_code']= len(df.columns)+2

                return redirect('cost_code:displaycost_code')


class ImportCostCodeStepOne(View):
    def get(self,request):
        file_data=request.session['generate_cost_code']
        # print('file_data',file_data)
        get_level=LevelMaster.objects.filter_company(request.company.id,1)
        main_list=[]
        for index,my_level in enumerate(get_level):
            list_data=[]
            for i,file in enumerate(file_data):
                if file[index].strip() not in list_data:
                    list_data.append(file[index].strip())
            main_list.append({'key_id':my_level.id,'values':list_data})
        count=0
        for check_data in main_list:
            level_id=check_data.get('key_id')
            get_level_data = CostCodeMaster.objects.filter_by_level_id(request.company.id,check_data.get('key_id'))
            existent_records = CostCodeType.objects.filter(cost_code_id=get_level_data.id,company_id=request.company.id,status=1).values_list('component_name',flat=True)
            get_last_value=CostCodeType.objects.filter(cost_code_id=get_level_data.id,company_id=request.company.id,status=1).last()
            new_list_data=[data for data in check_data.get('values') if data not in existent_records]
            if (len(new_list_data) > 0):
                count +=1
            check_data['values']=new_list_data
            check_data['code_code_master_id']=get_level_data.id
            check_data['level_master_name']=get_level_data.level_type.level_name
            check_data['sequence_gap']=get_level_data.sequence_gap
            check_data['no_digits']=get_level_data.no_digits
            check_data['get_last_value']=get_last_value.component_cost_code if get_last_value else get_level_data.start_with
        if count == 0:
            return redirect('cost_code:ImportCostCodeGenerateType')
                # cost_type=CostCodeType.objects.filter(cost_code_id=get_level_data.id,company_id=request.company.id,status=1).first()
                # print('cost_type',cost_type)
        #     a=1
        #     b=""
        #     my_dict={}
        #     for data in file:
        #         my_dict.update({''})
        #         b +="a-"
        #     file.append(b)
        #     if (a == 1):
        #         break
        #check below code
        # sample_main_list=[]
        # for index,my_level in enumerate(get_level):
        #     list_data=[]
        #     for i,file in enumerate(file_data):
        #             get_level_data = CostCodeMaster.objects.filter_by_level_id(request.company.id,my_level.id)
        #             list_data.append({'id':my_level.id,'new_component':file[index],'code_master_id':get_level_data.id})
        #     sample_main_list.append({'key_id':my_level.id,'values':list_data})
        # print('sample_main_list',sample_main_list)
        # for check_data in sample_main_list:
        #     get_level_data = CostCodeMaster.objects.filter_by_level_id(request.company.id,check_data.get('key_id'))
        #     existent_records = list(CostCodeType.objects.filter(component_name__in=check_data.get('values'),cost_code_id=get_level_data.id,company_id=request.company.id,status=1).values_list('component_name','component_cost_code'))
        #     check_data['values']=existent_records
        # print("file_data",sample_main_list)
        # code above
        return render(request,'import_cost_code_generate_one.html',{'main_list':main_list})

    def post(self,request):
        # print('request',request.POST)
        code_code_master_ids=request.POST.getlist('code_code_master_id')
        for master_id in code_code_master_ids:
            new_level_datas=request.POST.getlist('new_level_'+master_id)
            cost_code_previews=request.POST.getlist('cost_code_preview_'+master_id)
            new_comp_data=[CostCodeType(component_name=name,cost_code_id=master_id,component_cost_code=code,company=request.company) for name,code in zip(new_level_datas,cost_code_previews)]
            CostCodeType.objects.bulk_create(new_comp_data)
        # return render(request,'import_cost_code_generate_one.html',{'main_list':''})
        return redirect('cost_code:ImportCostCodeGenerateType')
class ImportCostCodeGenerateType(View):
    def get(self,request):
        try:
            cost_code_id=request.session['cost_master']
            file_data=request.session['generate_cost_code']
            level1=request.session['level1']
            level_1_split=level1.split('_')
            level2=request.session['level2']
            get_sub_type=DisciplineSubtype.objects.filter(id=level2).first()
            get_project_discipline=DisciplineSubtype.objects.getdiscipline_bydevelopment(level_1_split[0])
            discipline=ProjectDiscipline.objects.getprojectdiscipline()
            development_type=DevelopmentType.objects.getall_development_type()

            level12=CostCodeMaster.objects.getfirst_level(request.company,1)
            check_costcode=CostCodeMain.objects.getcostcode_bydevelopment_discipline(level_1_split[0],level_1_split[1],request.company)
            check_costcode_main=CostCodeMain.objects.getallcostcode(request.company).count()
            # print('file_data',file_data)
            if(check_costcode_main==0):
                cost_code=level12.start_with
            else:
                if(check_costcode):
                    cost_code=check_costcode.level1_cost_code
                else:
                    costcode_main=CostCodeMain.objects.getallcostcode(request.company).order_by('-id').first()
                    cost_code_add=int(costcode_main.level1_cost_code)+int(level12.sequence_gap)
                    cost_code=''
                    cost_code_len=len(str(cost_code_add))
                    if(int(cost_code_len)<=int(level12.no_digits)):
                        remaining_length=int(level12.no_digits)-int(cost_code_len)
                        for k in range(remaining_length):
                            cost_code +='0'
                        cost_code +=str(cost_code_add)
                    else:
                        cost_code = cost_code_add

            second_level=CostCodeMaster.objects.getsecond_level(request.company,1)
            check_costcodes=CostCodeMain.objects.getcostcode_discipline(level2,request.company)
            check_costcode_mains=CostCodeMain.objects.getallcostcode(request.company).count()
            if(check_costcode_mains==0):
                cost_code2=second_level.start_with
            else:
                if(check_costcodes):
                    cost_code2=check_costcodes.level2_cost_code
                else:
                    costcode_main=CostCodeMain.objects.getallcostcode(request.company).order_by('-id').first()
                    cost_code_add=int(costcode_main.level2_cost_code)+int(second_level.sequence_gap)
                    cost_code2=''
                    cost_code_len=len(str(cost_code_add))
                    if(int(cost_code_len)<=int(second_level.no_digits)):
                        remaining_length=int(second_level.no_digits)-int(cost_code_len)
                        for k in range(remaining_length):
                            cost_code2 +='0'
                        cost_code2 +=str(cost_code_add)
                    else:
                        cost_code2 = cost_code_add
            if '-' in second_level.cost_code_format:
                cost_code_type='-'
            elif '.' in second_level.cost_code_format:
                cost_code_type='.'
            else:
                cost_code_type=''
        except KeyError:
            return HttpResponse('<h2 style="text-align:center">Session Expired</h2>')
        finally:
            sub_types=list(CostCodeType.objects.filter_by_company(1,request.company).values
            ('cost_code__level_type_id','id','component_name','component_cost_code','cost_code_id'))
            sequence_gap=CostCodeMaster.objects.filter(company_id=request.company,status=1).all()[2:]
            for i in sequence_gap:
                sequencegap=i.sequence_gap
        development=CostCodeMaster.objects.filter(company_id=request.company,status=1).first()
        disciplineseq = CostCodeMaster.objects.filter(company_id=request.company, status=1, level_type_id=2)
        disciplinestartwith = 0
        # print('disciplineseq',disciplineseq)
        for i in disciplineseq:
            disciplinestartwith = i.start_with
            disciplineseq = i.sequence_gap
        
        #new approach
        get_level=LevelMaster.objects.filter_company(request.company.id,1)
        sample_main_list=[]
        for file in file_data:
            code_preview=f'{cost_code}{cost_code_type}{cost_code2}{cost_code_type}'
            my_list=[]
            for index,comp_data in enumerate(file):
                get_level_data = CostCodeMaster.objects.filter_by_level_id(request.company.id,get_level[index].id)
                remove_spaces=comp_data.strip()
                cost_type_data=CostCodeType.objects.filter(component_name__contains=remove_spaces,cost_code_id=get_level_data.id,company_id=request.company.id,status=1).first()
                my_list.append(cost_type_data)
                code_preview +=cost_type_data.component_cost_code+cost_code_type
            model_exists = any(x.get('code_preview') == code_preview for x in sample_main_list)
            if model_exists == False:
                sample_main_list.append({'components':my_list,'code_preview':code_preview[:-1]})    
            # change cost master len len_master  cost_code_id
        return render(request,'import_cost_code_generate.html',{'cost_code_id':cost_code_id,'file_data':file_data,'sub_types':sub_types,'alldiscipline':discipline,'development_type':development_type,'get_project_discipline':get_project_discipline,'get_sub_type':get_sub_type,'level1':level1,'cost_code':cost_code,'cost_code2':cost_code2,'cost_code_type2':cost_code_type,'levelstartwith':development.start_with,'sequencegap':development.sequence_gap,'disciplinestartwith':disciplinestartwith,'disciplineseq':disciplineseq,'len_master':1,'sample_main_list':sample_main_list})
    
    def post(self,request):
        pattern = r'^[0-9]+$'
        level1 = request.POST.get('level1_category')
        level2 = request.POST.get('level2_category')
        level1_costcode = request.POST.get('level1_costcode')
        level2_costcode  = request.POST.get('level2_costcode')
        print(f"post {request.POST}")
        total_rows = request.POST.get('total_rows')
        level1_split=level1.split('_')
        discipline_id=level1_split[0]
        development_id=level1_split[1]
        costcode_main=CostCodeMain.objects.getcostcode_level1_level2(discipline_id,development_id,request.company,level2)
        if(costcode_main==None):
            costcode_main=CostCodeMain.objects.create_costcode_main(development_id,discipline_id,level2,level1_costcode,level2_costcode,request.company)
            start=0
            end=start+int(total_rows)+1
        else:
            costcodesub=CostCodeSub.objects.getlastcostcodesub(costcode_main.id)
            start=costcodesub.order+1
            # end=start+costcodesub.order+1
            end=start+int(total_rows)+1
        # print(f"start {start}")
        # print(f"end {end}")
        # rangedata = range(start, end)
        print(total_rows,'rangedata')

        for i in range(0,int(total_rows)+1):
            start_value=start+i
            leveldata=request.POST.getlist('remaining_levels'+str(i))
            new_level=request.POST.getlist('new_level'+str(i))
            maxcode=request.POST.getlist("maxcode"+str(i))
            masterId=request.POST.getlist("masterId"+str(i))
            cost_code=request.POST.getlist('costcode'+str(i))
            costcodepreview=request.POST.get('costcodepreview'+str(i))

            # leveldata=request.POST.getlist('remaining_levels'+str(int(i-start)))
            # new_level=request.POST.getlist('new_level'+str(int(i-start)))
            # maxcode=request.POST.getlist("maxcode"+str(int(i-start)))
            # masterId=request.POST.getlist("masterId"+str(int(i-start)))
            # cost_code=request.POST.getlist('costcode'+str(int(i-start)))
            # costcodepreview=request.POST.get('costcodepreview'+str(int(i-start)))
            for j in range(len(leveldata)):
                if (re.match(pattern, leveldata[j]) is not None): 
                    # print(start_value,'order',i,'old',leveldata[j])
                    costcode_sub=CostCodeSub.objects.create_costcode_sub(cost_code[j],start_value,leveldata[j],costcode_main.id,request.company,costcodepreview)
                else:
                    print('new',leveldata[j])
                    # new_type_costcode=CostCodeType.objects.create(component_name=leveldata[j],cost_code_id=masterId[j],company=request.company,component_cost_code=maxcode[j])
                    # new_type_id=new_type_costcode.id
                    # costcode_sub=CostCodeSub.objects.create_costcode_sub(cost_code[j],start_value,new_type_id,costcode_main.id,request.company,costcodepreview)

                # if(leveldata[j]=='create'):
                    # print('newlevel[i]',new_level[j])
                    # print('masterId[i]',masterId[j])
                #     print('maxcost',maxcode[j])
                #     new_type_costcode=CostCodeType.objects.create(component_name=new_level[j],cost_code_id=masterId[j],company=request.company,component_cost_code=maxcode[j])
                #     new_type_id=new_type_costcode.id
                #     costcode_sub=CostCodeSub.objects.create_costcode_sub(cost_code[j],i,new_type_id,costcode_main.id,request.company,costcodepreview)
                # else:
                #     costcode_sub=CostCodeSub.objects.create_costcode_sub(cost_code[j],i,leveldata[j],costcode_main.id,request.company,costcodepreview)
                
        del request.session['cost_master']
        del request.session['generate_cost_code']
        del request.session['level1']
        del request.session['level2']
        return redirect('cost_code:costcodelist')
    


class EditCostCode(View):
    def get(self, request,order,maincode):
        costcodemain=CostCodeMain.objects.getmaincostcode_byid(maincode)
        print('costcodemain',costcodemain)
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        level2_discipline=DisciplineSubtype.objects.getdiscipline_bydevelopment(costcodemain.level1_discipline_id)
        costcode_type=getcostcode_format_type(request.company)

        data={
            'alldiscipline':discipline,
            'alldevelopment':development_type,
            'get_remaining_levels':get_remaining_level,
            'costcodemain':costcodemain,
            'level2_discipline':level2_discipline,
            'order':order,
            'company':request.company,
            'costcode_type':costcode_type
        }
        return render(request, "edit_cost_code.html",data)
    
    def post(self,request,order,maincode):
        print(f"post {request.POST}")
        level1 = request.POST.get('level_1_type')
        level2 = request.POST.get('level_2_type')
        level1_costcode = request.POST.get('level1_costcode')
        level2_costcode  = request.POST.get('level2_costcode')
        costtype_id = request.POST.getlist('oldcostcode')

        level1_split=level1.split('_')
        discipline_id=level1_split[0]
        development_id=level1_split[1]
        subcostcodeids = request.POST.getlist('costcodesubid')
        costcode_main=CostCodeMain.objects.updatemain_costcode(level1_costcode,level2_costcode,development_id,discipline_id,level2,maincode)
        remaining_levels= request.POST.getlist('remaining_levels')
        costcode=request.POST.getlist('costcode')
        costcodepreview=request.POST.get('costcodepreview')
        print(f"post {request.POST}")
        i=0
        for subcodedata in subcostcodeids:
            CostCodeType.objects.update_data(remaining_levels[i],costcode[i],costtype_id[i])
            costcode_sub=CostCodeSub.objects.update_costcode_sub(subcodedata,costtype_id[i],costcode[i],costcodepreview,maincode)
            i += 1
        usercreate = request.user.roles_id     
        create_user_log(request,"Cost Code",'Cost Code','Create','Cost Code has been Edited',usercreate)     
        return redirect('cost_code:costcodelist')

class ExportCostCode(View):
    def get(self, request):
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        getremaining_level=CostCodeMaster.objects.getremaining_level(request.company.id,1)
        data={
            'getremaining_levels':getremaining_level,
            'alldiscipline':discipline,
            'alldevelopment':development_type
        }
        return render(request, "export_cost_code.html",data)
    def post(self, request):
        print(f"post {request.POST}")
        level1 = request.POST.get('level1_category')
        level2 = request.POST.get('level2_category')
        remaining_levels = request.POST.getlist('remaining_levels')
        level1_split=level1.split('_')
        discipline_id=level1_split[0]
        development_id=level1_split[1]
        maincost_code=CostCodeMain.objects.getcostcode_level1_level2(discipline_id,development_id,request.company,level2)
        print
        for data in remaining_levels:
            print(f"data {data}")


class ImportCostCode(View):
    def get(self, request):
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        print('ghavdyjfgjkgv')
        data={
            'alldiscipline':discipline,
            'alldevelopment':development_type,
            'get_remaining_levels':get_remaining_level
        }
        return render(request, "import_cost_code.html",data)
    def post(self, request):
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        print('get_remaining_level',get_remaining_level)
        costcodefile=request.FILES.get('costcodefile',None)
        level1 = request.POST.get('level1_category')
        level2 = request.POST.get('level2_category')
        level1_costcode = request.POST.get('level1_costcode')
        level2_costcode  = request.POST.get('level2_costcode')
        level1_split=level1.split('_')
        discipline_id=level1_split[0]
        development_id=level1_split[1]
        costcode_format=getcostcode_format_type(request.company)

        if (costcodefile != None):
            dataset= Dataset()
            imported_data = dataset.load(costcodefile.read(),format='xlsx')
            i=0
            allleveldata=[]
            while i<len(imported_data):
                leveldata={}
                checknone=False
                for j in range(get_remaining_level.count()):
                    leveldata['level'+str(j)]=imported_data[i][j]
                    leveldata['levelmaster'+str(j)]=get_remaining_level[j].id
                    if(imported_data[i][j]==None):
                        checknone=True
                if(checknone==False):
                    allleveldata.append(leveldata)
                i+=1
            if(len(allleveldata)>0):
                costcode_main=CostCodeMain.objects.create_costcode_main(development_id,discipline_id,level2,level1_costcode,level2_costcode,request.company)
                m=0
                for data in allleveldata:
                    codecode=str(level1_costcode)+str(costcode_format)+str(level2_costcode)+str(costcode_format)
                    costcodesubid=[]
                    for k in range(get_remaining_level.count()):
                        costcode_type=CostCodeType.objects.getcostcodetype_name_masterid(data['level'+str(k)],data['levelmaster'+str(k)])
                        codecode +=str(costcode_type.component_cost_code)
                        codecode +=str(costcode_format)
                        costcode_sub=CostCodeSub.objects.create_costcode_sub(costcode_type.component_cost_code,m,costcode_type.id,costcode_main.id,request.company)
                        costcodesubid.append(costcode_sub.id)

                    m +=1
                    CostCodeSub.objects.filter(id__in=costcodesubid).update(costcode_preview=codecode.rstrip('-'))
        return redirect('cost_code:costcodelist')
          
def downloadcostcode_template(request):
    level_master=LevelMaster.objects.filter_company(request.company,1)
    get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    locked   = workbook.add_format({'locked': True})  
    unlocked = workbook.add_format({'locked': False})
    worksheet.protect()
    i=2
    level1=request.GET['level1']
    level2=request.GET['level2']
    level1_split=level1.split('_')
    discipline_id=level1_split[0]
    development_id=level1_split[1]
    level1_discipline=ProjectDiscipline.objects.get_discipline_byid(level1_split[0])
    level1_development=DevelopmentType.objects.getall_development_byid(level1_split[1])
    level2_split=level2.split('_')
    level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(level2_split[0])

    worksheet.write(0,0,'Level 1- Development Type',locked)
    first_column_range = f'A:A'
    worksheet.set_column(first_column_range, 50)

    worksheet.write(0,1,'Level 2- Discipline',locked)
    second_column_range = f'B:B'
    worksheet.set_column(second_column_range, 50)

    allcostcodetype={}
    albhabet='C'
    get_level=LevelMaster.objects.filter_company(request.company.id,1)
    for level,get_levl in zip(level_master,get_level):
      
        costcodetype=CostCodeType.objects.filter(cost_code__level_type_id=level.id,status=1).values_list('component_name',flat=True)
        allcostcodetype[i]=list(costcodetype)
        worksheet.write(0,i,'Level '+str(int(i+1))+ ' - '+get_levl.level_name,locked)
        column_range = f'{albhabet}:{albhabet}'
        worksheet.set_column(column_range, 70)
        albhabet = chr(ord(albhabet) + 1) 
        i +=1
    
    for range_value in range(2,2001):
        index_albhabet='C'
        j=2
        worksheet.write('A'+str(range_value),level1_discipline.name+'('+level1_development.development_type+')', locked)
        worksheet.write('B'+str(range_value),level2_name.discipline_subtype, locked)

        for level in get_remaining_level:
            print(f"index_albhabet {index_albhabet}")
            worksheet.write(index_albhabet+str(range_value),'', unlocked)
    #         worksheet.data_validation(index_albhabet+str(range_value)+'', {'validate': 'list',
    #                               'source': allcostcodetype[j]})
            index_albhabet = chr(ord(index_albhabet) + 1) 
            j +=1
        
      

        # worksheet.write_string(range_value, 1, 'Level 2', locked)  
        # worksheet.set_column('A:B', 90)  

    workbook.close()
    output.seek(0)
    filename = 'CostCode.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

class DeleteCostCode(View):
    def get(self, request,order,maincode):
        print(f'order {order} maincode {maincode}')
        CostCodeSub.objects.deletecostcode(maincode,order,0)
        # CostCodeMain.objects.filter(id=maincode).update(status=0)
        # return redirect('cost_code:costcodelist')
        return JsonResponse({"status":True})
    



def list_sub_costcode(costcode_main,company):
    costcodesub=CostCodeSub.objects.getgroup_costcode_sub(costcode_main).order_by('costcode_preview')
    getdiscipline=ProjectDiscipline.objects.get(id=costcode_main.level1_discipline_id)
    getdevelopmenttype=DevelopmentType.objects.get(id=costcode_main.level1_developmenttype_id)
    getlevel2discipline=DisciplineSubtype.objects.get(id=costcode_main.level2_discipline_id)
    costcode_type=getcostcode_format_type(company)
    costcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
    allcost_code=[]
    for costcode in costcodesub:
        allcostcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
        allcostcode_string=getdiscipline.name+'('+getdevelopmenttype.development_type+')'+'/'+getlevel2discipline.discipline_subtype+'/'
        allcostcodesub_order=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order'])
        allcostcodesub_value=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order']).last()
        type_name=CostCodeType.objects.get(id=allcostcodesub_value.cost_type_id)
        lastcategory=CostCodeType.objects.get(id=allcostcodesub_value.cost_type_id)
        for index, costcodesub_order in enumerate(allcostcodesub_order):
           allcostcode +=costcodesub_order.cost_code
           if index != len(allcostcodesub_order) - 1:
            allcostcode +=costcode_type
            costtype=CostCodeType.objects.getcostcodetype_id(costcodesub_order.cost_type_id).first()
            allcostcode_string +=costtype.component_name
            allcostcode_string +='/'
        get_values=get_sub_type(costcode['order'],costcode_main.id)                                 
        geting_value=get_values.replace('-', '').replace('.', '').replace('..', '')
        if geting_value == '':
            geting_value=000000
        else:
            geting_value=geting_value
            
        allcost_code.append({
            'allcostcode':allcostcode.rstrip(costcode_type),
            'allcostcode_string':allcostcode_string.rstrip('/'),
            'order':costcode['order'],
            'type_name':type_name,
            'lastcategory':lastcategory,
            'main_costcode_id':costcode_main.id,
            'sort_value':int(geting_value) if get_values else 000000
        })
    return allcost_code


def getcostcode_sub(costcode_main,company):
    costcodesub=CostCodeSub.objects.getgroup_costcode_sub(costcode_main)
    getdiscipline=ProjectDiscipline.objects.get(id=costcode_main.level1_discipline_id)
    getlevel2discipline=DisciplineSubtype.objects.get(id=costcode_main.level2_discipline_id)
    getdevelopmenttype=DevelopmentType.objects.get(id=costcode_main.level1_developmenttype_id)
    costcode_type=getcostcode_format_type(company)
    costcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
    allcost_code=[]
    
    for costcode in costcodesub:
        allcostcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
        allcostcode_string=getdiscipline.name+'('+getdevelopmenttype.development_type+')'+'/'+getlevel2discipline.discipline_subtype+'/'
        allcostcodesub_order=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order'])
        allcostcodesub_value=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order']).last()
        if '-' in allcostcodesub_value.costcode_preview:
            cost_code_type='-'
        elif '.' in allcostcodesub_value.costcode_preview:
            cost_code_type='.'
        else:
            cost_code_type=''
        type_name=CostCodeType.objects.get(id=allcostcodesub_value.cost_type_id)
        lastcategory=CostCodeType.objects.get(id=allcostcodesub_value.cost_type_id)
        # print('type_name',type_name.component_name)
        for index, costcodesub_order in enumerate(allcostcodesub_order):
           allcostcode +=costcodesub_order.cost_code
           allcostcode +=costcode_type
           if index != len(allcostcodesub_order) - 1:
            costtype=CostCodeType.objects.getcostcodetype_id(costcodesub_order.cost_type_id).first()
            allcostcode_string +=costtype.component_name
            allcostcode_string +='/'
            # print('costcodesub_order--',allcostcode_string)
            # print('lastcategory',lastcategory)
        allcost_code.append({
            'allcostcode':allcostcode.rstrip(cost_code_type),
            'allcostcode_string':allcostcode_string.rstrip('/'),
            'order':costcode['order'],
            'type_name':type_name.component_name,
            # 'lastcategory':lastcategory
        })
    # print('allcostcode---',allcost_code)    
   
    return allcost_code

    
class  GenerateCostCode(View):
    def get(self, request):
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        masters=LevelMaster.objects.filter_company(request.company.id,1).count()
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)
        development=CostCodeMaster.objects.filter(company_id=request.company,status=1).first()
        disciplineseq = CostCodeMaster.objects.filter(company_id=request.company, status=1, level_type_id=2)

        # master_count=disciplineseq.count()
        disciplinestartwith=0
        if masters!= 0:
            levelstartwith=development.start_with
            sequencegap=development.sequence_gap
          
            for i in disciplineseq:
                disciplinestartwith = i.start_with
                disciplineseq = i.sequence_gap
        else:
            disciplinestartwith=disciplineseq=sequencegap=levelstartwith=0
        
        getlevel1=CostCodeMaster.objects.filter_by_level_id(request.company,1)
        alllevel1_data=[]
        previous_code=getlevel1.start_with
        for level1_discipline in discipline:
            for level1_development in development_type:
                alllevel1_data.append({
                    'value':str(level1_discipline.id)+'_'+str(level1_development.id)+'_'+str(previous_code),
                    'name':level1_discipline.name+'('+level1_development.development_type+')'
                })
                previous_code=sum_costcode(previous_code,int(getlevel1.sequence_gap)+1)
        
        data={
            'levelstartwith':levelstartwith,
            'sequencegap':sequencegap,
            'disciplinestartwith':disciplinestartwith,
            'disciplineseq':disciplineseq,
            'alldiscipline':discipline,
            'alldevelopment':development_type,
            'get_remaining_levels':get_remaining_level,
            'count_of_remaining_levels':get_remaining_level.count(),
            'master_count':masters,
            'alllevel1_data':alllevel1_data,
        }
        return render(request, "generate_cost_code.html",data)
    
    def post(self,request):
        print(f"post {request.POST}")
        level1 = request.POST.get('level1_category')
        level2 = request.POST.get('level2_category')
        level1_costcode = request.POST.get('level1_costcode')
        level2_costcode  = request.POST.get('level2_costcode')
        total_rows = request.POST.get('total_rows')
        
        level1_split=level1.split('_')
        discipline_id=level1_split[1]
        development_id=level1_split[0]
        level1_costcode=level1_split[2]

        level2_split=level2.split('_')
        level2_id=level2_split[0]
        level2_costcode=level2_split[1]

        costcode_main=CostCodeMain.objects.getcostcode_level1_level2(development_id,discipline_id,request.company,level2_id)
       
        if(costcode_main==None):
            costcode_main=CostCodeMain.objects.create_costcode_main(discipline_id,development_id,level2_id,level1_costcode,level2_costcode,request.company)
            start=0
            end=start+int(total_rows)+1
        else:
            costcodesub=CostCodeSub.objects.getlastcostcodesub(costcode_main.id)
            start=costcodesub.order+1
            end=start+costcodesub.order+1
      
        rangedata = range(start, end)
        for i in rangedata:
            leveldata=request.POST.getlist('remaining_levels'+str(int(i-start)))
            new_level=request.POST.getlist('new_level'+str(int(i-start)))
            maxcode=request.POST.getlist("maxcode"+str(int(i-start)))
            masterId=request.POST.getlist("masterId"+str(int(i-start)))
            cost_code=request.POST.getlist('costcode'+str(int(i-start)))
            costcodepreview=request.POST.get('costcodepreview'+str(int(i-start)))
            for j in range(len(leveldata)):
                check_component_exists=CostCodeType.objects.check_component_exist(masterId[j],request.company,leveldata[j])
                if(not check_component_exists):
                    check_component_exists=CostCodeType.objects.create(component_name=leveldata[j],cost_code_id=masterId[j],company=request.company,component_cost_code=cost_code[j])
                costcode_sub=CostCodeSub.objects.create_costcode_sub(cost_code[j],i,check_component_exists.id,costcode_main.id,request.company,costcodepreview,masterId[j])
        usercreate = request.user.roles_id     
        create_user_log(request,"Cost Code Generated",'Cost Code','Create','Cost Code has been Generated',usercreate) 
        return redirect('cost_code:costcodelist')

        
def check_costcode_exists(request):
    cost_code=request.GET.get("cost_code")  
    print('cost_code',cost_code)
    check_costcode=CostCodeSub.objects.getcostcodesub_codecode(cost_code,request.company)
    print(f"check_costcode {check_costcode}")
    if(check_costcode.count() > 0):
        status=True
    else:
        status=False
    return JsonResponse({"status":status})

def check_costcode(request):
    component_name=request.GET.get("component_name")  
    level_id=request.GET.get("level_id")  
    level_index=request.GET.get("level_index")  
    level1=request.GET.get("level1")  
    level2=request.GET.get("level2")  
    costcode_master=CostCodeMaster.objects.get_by_id(level_id)
    check_component_exists=CostCodeType.objects.check_component_exist(level_id,request.company,component_name)
    level1_split=level1.split('_')
    level2_split=level2.split('_')

    costcode_main=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_split[0],level1_split[1],level2_split[0],request.company)
    print(f"check_component_exists {check_component_exists}")
    print(f"level_index {level_index}")


    if(not check_component_exists):
        if(not costcode_main):
            last_code=costcode_master.start_with
        else:
            print("gfdgh")

            if(level_index == '3'):
                costcode_sub = list(CostCodeSub.objects.getallcode_by_masterid_mainid(request.company.id,level_id,costcode_main.id).annotate(cost_code_int=Cast('cost_code', IntegerField())).values_list('cost_code_int', flat=True).distinct())
                last_code_list=costcode_sub[-1]
                next_costcode=last_code_list+int(costcode_master.sequence_gap)+1
                final_costcode=str(next_costcode).zfill(int(costcode_master.no_digits))
                last_code=final_costcode
            else:
                pre_cost_code=request.GET.get("pre_cost_code")  
                pre_component_name=request.GET.get("pre_component_name")  
                previous_costcode=CostCodeMaster.objects.getprevious_costcode_master(level_id,request.company.id)
                costcode_type=CostCodeType.objects.getcostcodetype_name_masterid(pre_component_name,previous_costcode.id)
                if(not costcode_type):
                    last_code=costcode_master.start_with
                else:
                    costcode_subs=CostCodeSub.objects.getallsubcode_bymainids(costcode_main.id)

                    getprevious_costcodes=costcode_subs.filter(costcode_master_id=previous_costcode.id,cost_type_id=costcode_type.id)
                    print(f"getprevious_costcodes {getprevious_costcodes}")
                    allnext_costcode=[]
                    for previous_costcodes in getprevious_costcodes:
                        nextcostcode=CostCodeSub.objects.getnext_costcode(previous_costcodes.id,previous_costcodes.order)
                        allnext_costcode.append(nextcostcode.cost_code)
                    
                    max_number = max(allnext_costcode, key=lambda x: int(x))
                    last_code=sum_costcode(max_number,int(costcode_master.sequence_gap)+1)

                    print(f"max_number {max_number}")



                    





        code_type='new'
    else:
        last_code=check_component_exists.component_cost_code
        code_type='old'
    
    data={
        'last_code':last_code,
        'code_type':code_type,
        'sequence_gap':costcode_master.sequence_gap,
        'no_digits':costcode_master.no_digits

    }
    return JsonResponse(data)



def level1costcode(request):
    discipline_id=request.GET.get("discipline_id")  
    development_id=request.GET.get("development_id")  
    costcodemain=CostCodeMain.objects.getcostcode_bydevelopment_discipline(discipline_id,development_id,request.company)
    get_project_discipline=DisciplineSubtype.objects.getdiscipline_bydevelopment(discipline_id)

    if(costcodemain):
        cost_code=costcodemain.level1_cost_code
    else:
        first_level=CostCodeMaster.objects.getfirst_level(request.company.id,1)
        costcodemain=CostCodeMain.objects.getallcostcode(request.company).order_by('-id').first()
        cost_code_add=int(costcodemain.level1_cost_code)+int(first_level.sequence_gap)
        cost_code=''
        cost_code_len=len(str(cost_code_add))
        if(int(cost_code_len)<=int(first_level.no_digits)):
            remaining_length=int(first_level.no_digits)-int(cost_code_len)
            for k in range(remaining_length):
                cost_code +='0'
            cost_code +=str(cost_code_add)
        else:
            cost_code = cost_code_add
    return JsonResponse({"data":list(get_project_discipline),"cost_code":cost_code})



    

def getlevel2_costcode(request):
    discipline_id=request.GET.get("discipline_id")  
    second_level=CostCodeMaster.objects.getsecond_level(request.company,1)
    check_costcode=CostCodeMain.objects.getcostcode_discipline(discipline_id,request.company)
    check_costcode_main=CostCodeMain.objects.getallcostcode(request.company).count()
    if(check_costcode_main==0):
        cost_code=second_level.start_with
    else:
        if(check_costcode):
            cost_code=check_costcode.level2_cost_code
        else:
            costcode_main=CostCodeMain.objects.getallcostcode(request.company).order_by('-id').first()
            cost_code_add=int(costcode_main.level2_cost_code)+int(second_level.sequence_gap)
            cost_code=''
            cost_code_len=len(str(cost_code_add))
            if(int(cost_code_len)<=int(second_level.no_digits)):
                remaining_length=int(second_level.no_digits)-int(cost_code_len)
                for k in range(remaining_length):
                    cost_code +='0'
                cost_code +=str(cost_code_add)
            else:
                cost_code = cost_code_add
    if '-' in second_level.cost_code_format:
        cost_code_type='-'
    elif '.' in second_level.cost_code_format:
        cost_code_type='.'
    else:
        cost_code_type=''
    return JsonResponse({"cost_code":cost_code,"cost_code_type":cost_code_type})

class CheckCostComponent(View):
    def post(self,request):
        print(f'req {request.POST}')
        cost_code_type= request.POST.get('cost_code_type')
        cost_id=request.POST.get('cost_id')
        check=CostCodeType.objects.filter(cost_code_id=cost_id,component_name=cost_code_type,status=1).count()
        print('check',check)
        print(f'cost_code_type {cost_code_type} cost_id {cost_id}  ')
        data={'data':check}
        return JsonResponse(data)
    
class CheckCostcodeNumber(View):
    def post(self,request):
        print(f'req {request.POST}')
        cost_code_type= request.POST.get('cost_code_type')
        cost_id=request.POST.get('cost_id')
        check=CostCodeType.objects.filter(cost_code_id=cost_id,component_cost_code=cost_code_type,status=1).count()
        print(f'cost_code_type {cost_code_type} cost_id {cost_id}  ')
        data={'data':check}
        return JsonResponse(data)

class CheckCostCodetype(View):
    def post(self,request):
        cost_code_type= request.POST.get('cost_code_type')
        cost_id=request.POST.get('cost_id')
        cost_type_id=request.POST.get('costypeid')
        if(cost_type_id):
            check=list(CostCodeType.objects.check_data_costtypeid(cost_id,cost_code_type,1,cost_type_id))
            data={'status':True}
            if (len(check) > 0):
                data={'status':False}
        else:
            if (cost_code_type):
                check=list(CostCodeType.objects.check_data(cost_id,cost_code_type,1))
                data={'status':True}
                if (len(check) > 0):
                    data={'status':False}
            else:
                CostCodeType.objects.getcostcodetype_id(cost_id).update(status=0)
                data={'status':True}
        return JsonResponse(data)

class CreateCostCompxl(View):
    def get(self,request,**kwargs):
        pk=kwargs.get('pk')
        get_level=LevelMaster.objects.getlevel_byid(pk).first()
        get_count=LevelMaster.objects.filter_company(request.company.id,1)
        level_name='Level '
        for count,level in zip(range(3,get_count.count()+3),get_count):
            if get_level.id == level.id:
                level_name += str(count)
        component_name=f'{level_name} - {get_level.level_name}'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        locked   = workbook.add_format({'locked': True})
        unlocked = workbook.add_format({'locked': False})
        worksheet.protect()
        worksheet.write(0,0,'S/N',locked )
        worksheet.write('B1',component_name,locked)
        # worksheet.write('C1','Title',locked)
        worksheet.set_column('B:B', 60)
        trim_format = workbook.add_format({'text_wrap': True,
        'align': 'left',
        'valign': 'top'})
        trim_format.set_text_wrap()
        format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                'font_color': '#9C0006'})
        worksheet.conditional_format('B2:B1000', {'type':   'duplicate','format': format1})
        for i in range(2,1001):
            worksheet.write('A'+str(i),'', unlocked)
            worksheet.write('B'+str(i),'', unlocked)
            # worksheet.write('C'+str(i),'', unlocked)
        worksheet.conditional_format('B2:B1000', {'type': 'text','criteria': 'containsBlanks',
                                        'format': trim_format})
        workbook.close()
        output.seek(0)
        filename = f'{component_name}.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

class ImportCostCodeType(View):
    def get(self,request):
        try:
            file_data=request.session['costcodearray']
            print('file_data',file_data)
            cost_code_id=request.session['costcodeid']
            get_types=CostCodeMaster.objects.filter_by_level_id(request.company.id,cost_code_id)
        except KeyError:
            return HttpResponse('<h2 style="text-align:center">Session Expired</h2>')
        set_val=getLastValue(cost_code_id,request.company)
        print('set_val',set_val)
        return render(request,'import_cost_code_type.html',{'datas':file_data,'cost_code_id':cost_code_id,'set_val':set_val[0],'level':set_val[1],'get_types':get_types})
    
    def post(self,request):
        print('req2',request.POST)
        cost_code_id=request.session['costcodeid']
        print('cost_code_id',cost_code_id)
        component_name_list = request.POST.getlist('component_name')
        component_cost_code_list = request.POST.getlist('component_cost_code')
        level = CostCodeMaster.objects.get_by_level_id(cost_code_id)
        for component_name,component_cost_code in zip(component_name_list,component_cost_code_list):
            CostCodeType.objects.create_costcode_type(component_name,component_cost_code,level,request.company)
        return redirect('cost_code:costcodetypelist',pk=cost_code_id)

class deletevendorcostcode(View):
    def post(self,request):
        id=request.POST.get('pk')
        CostCodeVendor.objects.get_vendor_company(id,1,request.company).update(status=0)
        return JsonResponse({'status':True})

class listCostCodeVendor(ListView):
    model = CostCodeVendor
    template_name = 'costcodevendor.html'
    def get_context_data(self,**kwargs):
        self.request.session['mainmenu'] = 'cost_code_vendor'
        context = super().get_context_data(**kwargs)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=19)
            context['rights']=userrights
        cost_code_vendor_list = CostCodeVendor.objects.filter_by_comapny(self.request.company,1).values('vendor_id','vendor__vendor_name','vendor__vin').distinct()
        listcode_count = CostCodeSub.objects.filter(costcode_main__company=self.request.company,status=1).count()
        
        page = self.request.GET.get('page', 1)
        pageper_data = self.request.GET.get('pageperdata',10)
        paginator = Paginator(cost_code_vendor_list, pageper_data)
        context['listcode_count']=listcode_count
        context['count_val']=cost_code_vendor_list.count()
        context['pageper_data']=pageper_data
        context['flow'] = paginator.page(page)
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        return context
    def post(self,request):
        # call get context data
        context = {}
        search_query = self.request.POST.get('q',False)
        if (self.request.user.roles_id == 3):
            userrights=UserRights.objects.get(user_id=self.request.user.id,module_id=17)
            context['rights']=userrights
        if search_query =='':
            cost_code_vendor_list = CostCodeVendor.objects.filter_by_comapny(self.request.company,1).values('vendor_id','vendor__vendor_name','vendor__vin').distinct()
            context['query'] = search_query
         
        else:
           cost_code_vendor_list = CostCodeVendor.objects.select_related('vendor').filter(company=self.request.user.company,status=True,vendor__vendor_name__icontains=search_query).values('vendor_id','vendor__vendor_name','vendor__vin').distinct()
           context['query'] = search_query
        # print('cost_code_vendor_list--',cost_code_vendor_list[0].vendor.vin)
        page = self.request.POST.get('page', 1)
        pageper_data = self.request.POST.get('pageperdata',10)  
        paginator = Paginator(cost_code_vendor_list, pageper_data)
        context['count_val']=cost_code_vendor_list.count()
        context['flow'] = paginator.page(page)
        context['scheme']=self.request.scheme
        context['gethost']=self.request.get_host()
        context['pageper_data'] = pageper_data
        # render to template string
        html = render_to_string('search_costcodevendor.html',context,request)
        # print(html)
        return JsonResponse({'status':True,'html':html})
        

class CreateCostCodeVendor(View):
    def get(self,request):
        vendors_list=ContractMasterVendor.objects.filter_company(request.company,1)
        # genertae_cost_code_list =CostCodeMain.objects.getallcostcode(request.company)
        # sub_cost_list=[]
        # for i in genertae_cost_code_list:
        #     sub_data=list_sub_costcode(i,request.company.id)
        #     sub_cost_list.extend(sub_data)
        # sorted_list = sorted(sub_cost_list, key=lambda value: value["sort_value"])
        # getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        # lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        # return render(request,'create_cost_code_vendor.html',{'vendors_list':vendors_list,'cost_code_main':genertae_cost_code_list,'company':request.company,'lastlevel':lastlevel,'costcode_list':sorted_list})
        return render(request,'create_cost_code_vendor.html',{'vendors_list':vendors_list})
    
    def post(self,request):
        vendor = request.POST.get('vendor')
        maincode = request.POST.getlist('maincode')
        vendor_name = request.POST.get('vendor_name_for_user_log')
        data_list=[]
        selected_costcode=request.POST.get('selected_costcode')
        contract_id=request.POST.get('contract_id')
        selected_costcode_array=selected_costcode.split(',')
        for main in selected_costcode_array:
            split_val=main.split("-")
            vendor_data = CostCodeVendor.objects.get_match_data(vendor,split_val[0],split_val[1],request.company.id,contract_id)
            if vendor_data.exists():
                data_list.append(vendor_data[0].id)
                vendor_data.update(status=1)
            else:
                create_data= CostCodeVendor.objects.createCostCodeVendor(vendor,split_val[0],split_val[1],request.company.id,contract_id)
                data_list.append(create_data.id)
        CostCodeVendor.objects.filter(vendor_id=vendor,company_id=request.company.id,contractid=contract_id).exclude(id__in=data_list).update(status=0)
        usercreate = request.user.roles_id     
        create_user_log(request,"Cost Code Assigned",'Cost Code','Create',f'Cost Code has been assigned to {vendor_name} ',usercreate) 
        return redirect('cost_code:listcostcodevendor')

class GetVendorCostCode(View):
    def post(self,request):
        vendor_id= request.POST.get('vendor_id')
        data=CostCodeVendor.objects.get_vendor_data(vendor_id,1).values()
        return JsonResponse({'data':list(data)})
    
class CostCodeVendorView(View):
    def get(self,request,vendor):
        vendor_detail=ContractMasterVendor.objects.get_byid(vendor,request.company)
        contract_id=request.GET.get('contract',0)

        if contract_id:
            costcode_main_set = set()
            contract_masters=ContractMaster.objects.getcontract(contract_id)
            projectdevelopmentdiscipline=ProjectDevelopmentDiscipline.objects.getdevelopment_details(contract_masters.projectdiscipline_id)
            level1_discipline=projectdevelopmentdiscipline.project_discipline
            if projectdevelopmentdiscipline.development_type.development.development_type == 'Oil_Development':
                level1_development_type=1
            elif projectdevelopmentdiscipline.development_type.development.development_type == 'Gas_Development':
                level1_development_type=2
            elif projectdevelopmentdiscipline.development_type.development.development_type == 'Unconventional_Oil':
                level1_development_type=3
            else:
                level1_development_type=4

            level2_discipline=ProjectDevelopmentSubType.objects.getdetails_byid(contract_masters.projectdisciplinetype_id)
            level2_discipline=level2_discipline.discipline_subtype.id
            costcode_by_level1_level2=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_discipline,level1_development_type,level2_discipline,request.company)
            if costcode_by_level1_level2:
                costcode_main_set.add(costcode_by_level1_level2.id)
            allcostcode=list(costcode_main_set)
            vendors_list=CostCodeVendor.objects.get_vendor_data(vendor,1,allcostcode)
        else:
            vendors_list=CostCodeVendor.objects.get_vendor_data(vendor,1)

        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        allcontract=getvendorcontracts(vendor)
        return render(request,'vendorcostcodeview.html',{'vendor':vendor_detail,'vendor_list':vendors_list,'company':request.company,'lastlevel':lastlevel,'allcontract':allcontract,'contract_id':int(contract_id)})



class Generatecostcodevendor_excel(View):
    template_name = 'costcodevendor_pdf.html'
    def get(self,request):
        cost_code_vendor_list = CostCodeVendor.objects.filter_by_comapny(self.request.company,1).values('vendor_id','vendor__vendor_name','vendor__vin').distinct().order_by('vendor__vin')
        allcostcode_vendor=getcostcode_vendor_forreport(request.company)
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)

        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB') 
            image = image.resize((120, 80))  
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            imageurl = None
        data={
            'allcostcode_vendor':allcostcode_vendor,
            'lastlevel':lastlevel,
            'get_remaining_level_count':get_remaining_level.count()
        }
        output_coversheet = render_to_string(self.template_name,data,request)
        css = CSS(string=getcostcodepdfvendor_css(encoded_image))
        pdf_buffer = BytesIO()
        HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="CostCodevendor PDF.pdf"'
        return response

def generateVendorReport(request,pk):
    template = 'generateVendorReport.html'
    vendormasterlist=CostCodeVendor.objects.filter(vendor_id=pk,status=1,company_id=request.company.id)
    # totalcount=contractmasterlist.count()
    allcostcode_vendor=getcostcode_vendor_forreport(request.company,pk)
    contracts_ids=list(CostCodeVendor.objects.filter(vendor_id=pk,status=1,company_id=request.company.id).values_list('contractid', flat=True).distinct())
    allcontract=getvendorcontracts(pk)
    get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)

    companyImage= Companies.objects.filter(id=request.company.id).first()
    if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB') 
            image = image.resize((120, 80))  
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    else:
        imageurl = None
    getcompanyname=request.company.company_name
    filename=getcompanyname+' generate Vendor report.pdf'
    context = {'company': request.company, 'imageurl': imageurl,'vendormasterlist':vendormasterlist,'request':request,'vendor_name':vendormasterlist.first(),'allcostcode_vendor':allcostcode_vendor,'get_remaining_level_count':get_remaining_level.count() , 'contracts_ids':contracts_ids , 'pk':pk , 'allcontract':allcontract}
    output_coversheet = render_to_string(template,context,request)
    css = CSS(string=getcostcodepdf_css(encoded_image))
    pdf_buffer = BytesIO()
    HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename='+filename+''
    return response

def getcostcode_vendor_forreport(company,vendor_id=None):
    if(vendor_id):
        costcodevendor=CostCodeVendor.objects.getcostcodevendor_groupby_costcodemain_vendor(company.id,vendor_id)
        print(f"costcodevendor {costcodevendor}")
    else:
        costcodevendor=CostCodeVendor.objects.getcostcodevendor_groupby_costcodemain(company.id)
    allcodes_data=[]
    costcode_type=getcostcode_format_type(company.id)

    for costcode_vendor in costcodevendor:
        if(vendor_id):
            costcode_vendor_bycostcodemain=CostCodeVendor.objects.getcostcode_vendor_bycostcodemain(costcode_vendor['costcode_main_id'],company.id,vendor_id)
        else:
            costcode_vendor_bycostcodemain=CostCodeVendor.objects.getcostcode_vendor_bycostcodemain(costcode_vendor['costcode_main_id'],company.id)
        allcost_code=[]

        costcode_main_details=getlevel1_level2(costcode_vendor['costcode_main_id'],company.id)
        for costcodemain in costcode_vendor_bycostcodemain:
            allcostcode=costcode_main_details['level1_2_code']

            vendor_details=ContractMasterVendor.objects.get_byid(costcodemain.vendor_id,company.id)
            # print(f"vendor_details {vendor_details}")
            getcostcode_sub_by_order_main=CostCodeSub.objects.getallcostcodesub_order(costcodemain.costcode_main_id,costcodemain.order)
            # print(f"getcostcode_sub_by_order_main {getcostcode_sub_by_order_main[0].status}")
            if getcostcode_sub_by_order_main[0].status == 1:
                remaining_levels=[]
                index=0
                for index, costcodesub in enumerate(getcostcode_sub_by_order_main):
                    if costcodesub.costcode_master is not None:
                        remaining_levels.append({costcodesub.costcode_master.level_type_name:costcodesub.cost_type.component_name})
                        allcostcode +=costcodesub.cost_code
                        if index != len(getcostcode_sub_by_order_main) - 1:
                            allcostcode +=costcode_type
                            print(f"allcostcode {allcostcode}")
                
                allcost_code.append({
                    'allcostcode':allcostcode.rstrip(costcode_type),
                    'remaining_levels':remaining_levels,
                    'level1':costcode_main_details['level1'],
                    'level2':costcode_main_details['level2'],
                    'vin':vendor_details.vin,
                    'vendor_name':vendor_details.vendor_name,
                })
        allcodes_data.append(allcost_code)
    
    return allcodes_data 








class GetLevelbyId(View):
    def get(self,request):
        level=self.request.GET.get('level_id')
        costcodetypes=CostCodeType.objects.filter(cost_code__level_type_id=level,status=1,company_id=request.company.id)
        serialized_data = serialize('json', costcodetypes)
        json_data = json.loads(serialized_data)
        return JsonResponse(json_data,safe=False)

class GetMasterId(View):
    def get(self,request):
        data_id=self.request.GET.get('data_id')
        master_data=CostCodeMaster.objects.filter_by_company(request.company.id,data_id)
        serialized_data = serialize('json', master_data)
        json_data = json.loads(serialized_data)
        return JsonResponse(json_data,safe=False)
    
    
    
class GetCostCodeValues(View):
    def get(self,request):
        contract_id=self.request.GET.get('contract_id')
        vendorId=self.request.GET.get('vendorId')
        vendors_list=CostCodeVendor.objects.filter(vendor_id=vendorId,status=1 ,contractid=contract_id)
        all_costcode_data=[]
        number=1
        for cost in vendors_list:
            costcode_preview=getcostcode_preview (cost.costcode_main, cost.order,request.company.id)
            costcode_string=getcostcode_string( cost.costcode_main ,cost.order,request.company.id)
            costcode_category=getcostcode_category(  cost.costcode_main, cost.order ,request.company.id)
            cost_value=f'{costcode_string}/{costcode_category.cost_type.component_name}'
            datas={ "serial_number": number, "costcode_preview": costcode_preview, "code_category_paths":cost_value }
            all_costcode_data.append(datas)
            number+=1
        
        json_data={'data':all_costcode_data}
        return JsonResponse(json_data,safe=False)
    


class GetCodeGenerate(View):
    def get(self,request):
        component_id=self.request.GET.get('component_id')
        print('component_id',component_id)
        component_cost_code=CostCodeType.objects.getcostcodetype_id(component_id)
        serialized_data = serialize('json', component_cost_code) 
        json_data = json.loads(serialized_data)
        return JsonResponse(json_data,safe=False)
    
class GenerateVendorPdf(View):
    template_name = 'generateCostCodeVendorPdf.html'
    def get(self,request,vendor):
        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')  # Convert the image to RGB mode
            image = image.resize((120, 80))  # Resize the image to 150x100 pixels
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        vendor_detail=ContractMasterVendor.objects.get_byid(vendor,request.company)
      
        allcostcode_vendor=getcostcode_vendor_forreport(request.company,vendor)
        print(f"allcostcode_vendor {allcostcode_vendor}")

        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)

        contracts_ids=list(CostCodeVendor.objects.filter(vendor_id=vendor,status=1,company_id=request.company.id).values_list('contractid', flat=True).distinct())
        allcontract=getvendorcontracts(vendor)
        vendors_list=CostCodeVendor.objects.get_vendor_data(vendor,1)
        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        context = {'vendor':vendor_detail,'vendor_list':vendors_list,'company':request.company,'companyid':request.company.id,'lastlevel':lastlevel,'allcostcode_vendor':allcostcode_vendor,'get_remaining_level_count':get_remaining_level.count(), 'contracts_ids':contracts_ids , 'pk':vendor , 'allcontract':allcontract}
        output_coversheet = render_to_string(self.template_name,context,request)
        coversheet_style = getcostcodepdfvendor_css(encoded_image)
        css = CSS(string=coversheet_style)
        pdf_buffer = BytesIO()
        HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])

        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')

        response['Content-Disposition'] = 'inline; filename="CostCode-VendorPDF.pdf"'

        return response


class DeleteMaster(View):
    def post(self, request):
        id=request.POST.get('id')
        CostCodeMaster.objects.filter_by_id(int(id)).update(status=0)
        LevelMaster.objects.getlevel_byid(CostCodeMaster.objects.filter_by_id(int(id)).first().level_type_id).update(status=0)
        return JsonResponse({'status':True})


class GetCostTypeValue(View):
    def get(self,request):
        data_id=request.GET.get('data_id')
        cost_type=list(CostCodeType.objects.filter(cost_code__level_type_id=data_id,status=1).values())
        return JsonResponse({"data":cost_type})
    
class validatecclevel(View):
    def post(self,request):
        currentval = request.POST.get('currentval')
        levelid = request.POST.get('levelid')
        levelnameexits=CostCodeType.objects.filter(cost_code_id=levelid,component_name=currentval,status=1).exists()
        print('levelnameexits',levelnameexits) 
        # print('actno----',actno,actno_id)
        # if actno_id:
          
        #     if CompanyBank.objects.filter(account_number=actno,company=request.company,status=True).exclude(id=actno_id).exists():
        #        return JsonResponse({'status':True})
        #     else:
        #         return JsonResponse({'status':False})
        # else:
        #     if CompanyBank.objects.filter(account_number=actno,company=request.company,status=True).exists():
        #        print('val',CompanyBank.objects.filter(account_number=actno,company=request.company,status=True))
        #        return JsonResponse({'status':True})
        #     else:
        return JsonResponse({'status':levelnameexits})



class DuplicateCostTypeCheck(View):
    def get(self,request):
        value=request.GET.get('value')
        masterId=request.GET.get('masterId')
        types=CostCodeType.objects.filter(cost_code_id=masterId,component_name=value,status=1).first()
        if types != None:
            duplicate=1
        else:
            duplicate=0
        return JsonResponse({"duplicate":duplicate})
    
class CreateCostCodeRangeType(View):    
    def get(self,request,level_id,id):
        set_val = getLastValue(level_id,request.company)
        costcodemasterid = CostCodeMaster.objects.filter(level_type=level_id).first()
        request.session['mainmenu'] = 'cost_code'
        return render(request,'create_cost_code_range_type.html',{'level':set_val[1],'level_id':level_id,'set_val':set_val[0],'costcodemasterid':costcodemasterid.id,'costcodemaster':costcodemasterid,'id':id})
    
    def post(self,request,level_id,id):
        component_name_list = request.POST.getlist('component_name')
        component_cost_code_list = request.POST.getlist('component_cost_code')
        level = CostCodeMaster.objects.get_by_level_id(level_id)
        for component_name,component_cost_code in zip(component_name_list,component_cost_code_list):
            CostCodeType.objects.create_costcode_type(component_name,component_cost_code,level,request.company)
        return redirect('cost_code:costcodetypelist',pk=level_id)
    
class validatecostcoderange(View):
    def post(self,request):
        pk = request.POST.get('pk')
        CostCodeTypeval = CostCodeType.objects.get(id=pk)
        lastval=CostCodeType.objects.filter(cost_code_id=CostCodeTypeval.cost_code_id,component_cost_code__gt=CostCodeTypeval.component_cost_code).exists()
        if(lastval == True):
            rangeval = CostCodeType.objects.filter(cost_code_id=CostCodeTypeval.cost_code_id,component_cost_code__gt=CostCodeTypeval.component_cost_code).exclude(id=CostCodeTypeval.id).order_by('component_cost_code').first()
            return JsonResponse({'fromrange':CostCodeTypeval.component_cost_code,'torange':rangeval.component_cost_code})
        else:
            return JsonResponse({'fromrange':CostCodeTypeval.component_cost_code,'torange':0})




class Generatecostcode_excel(View):
    template_name = 'costcode_pdf.html'
    def get(self,request):
        cost_code_main=CostCodeMain.objects.getallcostcode(request.company)
        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB') 
            image = image.resize((120, 80))  
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            imageurl = None
            encoded_image = None
        getlastlevel=CostCodeMaster.objects.filter_by_status(1,request.company).order_by('-id').first()
        print('cost_code_main',cost_code_main)
        lastlevel=LevelMaster.objects.getlevel_byid(getlastlevel.level_type_id).first()
        data={'cost_code_main':cost_code_main,'company':request.company,'lastlevel':lastlevel}
        allcostcode=[]
        s_no=1
       
        for costcodemain in cost_code_main:
            sorted_list=costcode_report(costcodemain,request.company.id)
            allcostcode.append(sorted_list) 
            # getsubcode=getcostcode_sub(costcodemain,request.company)
            # for costcodesub in getsubcode:
            #     print('type_name--',costcodesub['type_name'])
            #     allcostcode.append({
            #         's_no':s_no,
            #         'cost_code':costcodesub['allcostcode'],
            #         'last_level':lastlevel.level_name,
            #         'cost_string':costcodesub['allcostcode_string'],
            #         'type_name':costcodesub['type_name'],
            #         })
                # s_no +=1
        # sorted_list = sorted(allcostcode, key=lambda value: value["cost_code"])
        print(f"allcostcode {allcostcode}")
        get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)

        data={
            'allcostcode':allcostcode,
            'get_remaining_level_count':get_remaining_level.count()

        }
        output_coversheet = render_to_string(self.template_name,data,request)
        css = CSS(string=getcostcodepdf_css(encoded_image))
        pdf_buffer = BytesIO()
        HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="CostCode PDF.pdf"'
        return response


class SelectCodeCategory(View):
    def get(self,request):
        discipline=ProjectDiscipline.objects.getprojectdiscipline()
        development_type=DevelopmentType.objects.getall_development_type()
        count = CostCodeSub.objects.get_by_company(1,request.company.id).count()
        discipline_subtype = DisciplineSubtype.objects.filter_by_status(1).values_list('discipline_subtype', flat=True).distinct()
        company_image=Companies.objects.filter(id=request.company.id).filter(Q(image__isnull=True) | Q(image=None) | Q(image='')).count()
        return render(request,'selectcodecategory.html',{'listcount':count,'alldiscipline':discipline,'alldevelopment':development_type,'discipline_subtype':discipline_subtype,'company_image':company_image})
    
    def post(self,request):
        level1=str(request.POST.get('level_1'))
        level1_split=level1.split('_')
        
        level1_discipline_id=level1_split[0]
        level1_development_id=level1_split[1]
        level2=request.POST.get('level_2')
        level2_split=level2.split('_')
        level2_discipline_id=level2_split[0]



        companyImage= Companies.objects.filter(id=request.company.id).first()
        if companyImage.image:
            imageurl = companyImage.image.url
            with open(companyImage.image.path, 'rb') as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB') 
            image = image.resize((120, 80))  
            buffered = BytesIO()
            image.save(buffered, format="JPEG")      
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            imageurl = None

        costcode_main=CostCodeMain.objects.getallcostcode_by_level1_level2(level1_discipline_id,level1_development_id,level2_discipline_id,request.company)

        if(not costcode_main):
            messages.error(request, "No Data found")
            return redirect(request.META.get('HTTP_REFERER'))
          

        else:
            sorted_list=costcode_report(costcode_main,request.company.id)
            list_len=len(sorted_list)
            get_remaining_level=CostCodeMaster.objects.getremaining_level(request.company,1)

            data={
                'costcode_list':sorted_list,
                'list_len':list_len,
                'get_remaining_level_count':get_remaining_level.count()
            }
            output_coversheet = render_to_string('filtereddatas.html',data,request)
            css = CSS(string=getcostcodepdf_css(encoded_image))
            pdf_buffer = BytesIO()
            HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="CostCode Generate.pdf"'
            return response


def costcode_report(costcode_main,company_id):
    print(f"costcode_main {costcode_main}")
    costcodesub=CostCodeSub.objects.getgroup_costcode_sub(costcode_main).order_by('costcode_preview')
    costcode_type=getcostcode_format_type(company_id)
    level1_discipline=ProjectDiscipline.objects.get_discipline_byid(costcode_main.level1_discipline_id)
    level1_development=DevelopmentType.objects.getall_development_byid(costcode_main.level1_developmenttype_id)
    level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(costcode_main.level2_discipline_id)


    allcost_code=[]
    for costcode in costcodesub:
        allcostcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
        allcostcodesub_order=CostCodeSub.objects.getallcostcodesub_order(costcode_main,costcode['order'])
        remaining_levels=[]
        for index, costcodesub_order in enumerate(allcostcodesub_order):
            if costcodesub_order.costcode_master is not None:
                remaining_levels.append({costcodesub_order.costcode_master.level_type_name:costcodesub_order.cost_type.component_name})
                allcostcode +=costcodesub_order.cost_code
                if index != len(allcostcodesub_order) - 1:
                    allcostcode +=costcode_type
        # print(f"allcostcode {allcostcode}")
            

        allcost_code.append({
            'allcostcode':allcostcode.rstrip(costcode_type),
            'remaining_levels':remaining_levels,
            'level1':'Development Type: '+level1_development.development_type+'('+level1_discipline.name+')',
            'level2':'Discipline Type: '+level2_name.discipline_subtype
        })
    return allcost_code

def getvendorcostcode_bycontract(request,pk):
    invoice_detail = Invoice.objects.filter_by_id(pk).get()
    vendor_costcode=getvendorcostcode_bycontracts(invoice_detail.contractid,request,invoice_detail.vendor_id , invoice_detail.contracttype)
    return render(request,'vendorcostcode_contract.html',{'vendor_costcode':vendor_costcode})

