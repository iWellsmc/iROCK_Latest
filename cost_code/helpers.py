from cost_code.models import CostCodeType,CostCodeSub,CostCodeMaster,LevelMaster,CostCodeMain
from  projects.models import *


def getcostcode_format_type(companyid):
    costcode_master=CostCodeMaster.objects.filter_by_status(1,companyid).first()

    cost_code_type=''
    if(costcode_master != None):
        if '-' in costcode_master.cost_code_format:
            cost_code_type='-'
        elif '.' in costcode_master.cost_code_format:                            
            cost_code_type='.'
    
    return cost_code_type

def getcostcodepdf_css(encoded_images):
    encoded_image = ""
    if encoded_images is not None :
        encoded_image = encoded_images

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
                margin-top: 55px;
                /*font-size: 20px; 
                margin-left:30px !important;
                color: #AF2B50; 
                font-weight: 600;*/
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
            margin: 10px 10px !important;
            background-image: url('data:image/png;base64,"""+encoded_image+"""');
            background-repeat: no-repeat; 
            width: 200px !important;
            height: 90px !important;
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
            width: 100% !important;
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

        .bor-top {
            border-top: none !important;
        }

        .bor-ryt {
            border-right: 1px solid #c7c7c7;
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

        .cost-code-pdf-table {
            width: 100%;
            border-collapse: collapse;
        }
        .cost-code-pdf-table th {
            color: #000;
            font-size: 10px !important;
            font-weight: 600 !important;
            text-align: center;
        }
        .cost-code-pdf-table td {
            color: #000;
            font-size: 10px;
            text-align: center;
        }
        .cost-code-pdf-table th, td {
            padding: 5px 5px;
            border: 1px solid #e3e3e3;
        }
        .cost-code-pdf-table p {
            margin: 0px 0px;
        }
        .td-green {
            color: #017474 !important;
            font-weight: 600;
        }
        .text-left {
            text-align: left !important;
        }

        /******************** filterreddatas.html *******************/
        .filter-table {
            width: 100%;
            border-collapse: collapse;
        } 

        .filter-table th {
            color: #000;
            font-size: 10px !important;
            font-weight: 600 !important;
            text-align: center;
        }
        .filter-table td {
            color: #000;
            font-size: 10px;
            text-align: center;
        }
        .filter-table th, td {
            padding: 5px 5px;
            border: 1px solid #e3e3e3;
        }
        .filter-table p {
            margin: 0px 0px;
        }
        .td-filter-green {
            color: #017474 !important;
            font-weight: 600;
        }
        /******************** filterreddatas.html *******************/ 
            """
    return pdfsheet_style


def getcostcodepdfvendor_css(encoded_image):
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

        /*************** costcodevendor_pdf ***************/

        .vendorpdf-table {
            width: 100%;
            border-collapse: collapse;
        }
        .vendorpdf-table th {
            color: #000;
            font-size: 10px !important;
            font-weight: 600 !important;
            text-align: center;
        }
        .vendorpdf-table td {
            color: #000;
            font-size: 10px;
        }
        .vendorpdf-table th, td {
            padding: 5px 5px;
            border: 1px solid #e3e3e3;
        }
        .vendorpdf-table p {
            margin: 0px 0px;
        }
        .text-left {
            text-align: left !important;
        }
        .td-ccvendor-green {
            color: #017474 !important;
            font-weight: 600;
        }

     /*************** SA 3-11-2023 ***************/ 
        .titl-assign{
            font-size:15px;
            font-weight:600;
            text-align:center;
            margin:0px 0px;
            color:#AF2B50;
        }
        
        /**************** Vendor login PDF ***************/
         .head-inv-pre-vend {
            color: #AF2B50;
            font-weight: 600;
            font-size:20px;
            margin-top: 0px;
        }
        .vin-no {
            margin: 10px auto 0px;
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
            font-size: 10px;
            font-weight: 600;
            margin-bottom: 0px;
        }

        .dot-colon {
            color: #AF2B50;
            font-size: 10px;
            font-weight: 600;
        }

        .vin-no span {
            color: #000 !important;
            font-size: 10px;
            font-weight: 500;
        }

        .ven-name {
            margin: 10px auto;
        }

        .ven-name label {
            color: #AF2B50;
            font-size: 10px;
            font-weight: 600;
            margin-bottom: 0px;
        }

        .ven-name span {
            color: #000 !important;
            font-size: 10px;
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
            font-size: 10px !important;
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
            font-size: 10px;
            padding: 5px 5px;
        }

        /**************** Vendor login PDF ****************/
            """
    return pdfsheet_style

def sum_costcode(costcode,sequence_gap):
    new_costcode = str(int(costcode) + int(sequence_gap))
    return new_costcode.zfill(len(costcode))


def getcode_format(total_length,code,cost_code_format):
    allcode=''
    for i in range(1,total_length+1):
        if(i==total_length):
            allcode +=code['level'+str(i)+'_code']
        else:

            allcode +=code['level'+str(i)+'_code']+cost_code_format
    return allcode

def getlastcode_bymaster(costcode_subs,level_index,costcode_master,company,current_component,previous_component,costcode_main):
    previous_costcode=CostCodeMaster.objects.getprevious_costcode_master(costcode_master.id,company.id)
    if(costcode_main):
        costcode_type=CostCodeType.objects.check_component_exist_new(previous_costcode.id,company.id,previous_component,costcode_main.id)
    else:
        costcode_type=None
  

    if(not costcode_type):
        if(not costcode_subs):
            start_with=costcode_master.start_with

        else:
            getlevel_cost_codes=costcode_subs.filter(costcode_master_id=costcode_master.id)
            if(getlevel_cost_codes.count()==0):
                start_with=costcode_master.start_with
            else:
                cost_code_list=getlevel_cost_codes.values_list('cost_code',flat=True)
                cost_code_list = list(cost_code_list)
                max_number = max(cost_code_list, key=lambda x: int(x))
                start_with=sum_costcode(max_number,int(costcode_master.sequence_gap)+1)
    else:
        getprevious_costcodes=costcode_subs.filter(costcode_master_id=previous_costcode.id,cost_type_id=costcode_type.id)
        cost_code_list=getprevious_costcodes.values_list('cost_code',flat=True)
        cost_code_list = list(cost_code_list)
        max_number = max(cost_code_list, key=lambda x: int(x))
        start_with=sum_costcode(max_number,int(costcode_master.sequence_gap)+1)
    
    # if(current_component == 'Others'):
    #     print(f"start_with {start_with}")
    
    return start_with

def check_previous_level_exists(costcode_master,cost_code,component_name,company):
    previous_costcode=CostCodeMaster.objects.getprevious_costcode_master(costcode_master.id,company.id)
    costcode_type=CostCodeType.objects.getcostcodetype_name_masterid(component_name,previous_costcode.id)
    return costcode_type




def getcode_format(total_length,code,cost_code_format):
    allcode=''
    for i in range(1,total_length+1):
        if(i==total_length):
            allcode +=code['level'+str(i)+'_code']
        else:

            allcode +=code['level'+str(i)+'_code']+cost_code_format
    return allcode

def checklimit_exist(index,company_id,cost_code):
    costcode_master=list(CostCodeMaster.objects.filter_by_status(1,company_id))
    length_start_with=len(costcode_master[index-1].start_with)
    highest_number = 10 ** length_start_with - 1
    if(int(cost_code) <= highest_number):
        return False
    else:
        return True

def getlevel1_level2(costcode_mainid,company_id):
    costcode_main=CostCodeMain.objects.getcostcodemain_byid(costcode_mainid)
    costcode_type=getcostcode_format_type(company_id)
    level1_discipline=ProjectDiscipline.objects.get_discipline_byid(costcode_main.level1_discipline_id)
    level1_development=DevelopmentType.objects.getall_development_byid(costcode_main.level1_developmenttype_id)
    level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(costcode_main.level2_discipline_id)
    allcostcode=costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
    data={
        'level1':'Development Type: '+level1_development.development_type+'('+level1_discipline.name+')',
        'level2':'Discipline Type: '+level2_name.discipline_subtype,
        'level1_2_code':costcode_main.level1_cost_code+costcode_type+costcode_main.level2_cost_code+costcode_type
    }
    return data

def getlevel1_level2_components():
    level1=['Green Field Development(Oil Development)','Green Field Development(Gas Development)','Green Field Development(Unconventional Oil)','Green Field Development(Unconventional Gas)','Brown Field Development(Oil Development)','Brown Field Development(Gas Development)','Brown Field Development(Unconventional Oil)','Brown Field Development(Unconventional Gas)','Others(Oil Development)','Others(Gas Development)','Others(Unconventional Oil)','Others(Unconventional Gas)']

    level2=['Subsurface and Reservoir Engineering','Drilling and Completions','Facilities and Projects','Production and Operations','Human Resources and Administration','Legal','ICT','Finance','QHSE &amp; Community Development','Business Development &amp; Sales and Marketing','Insurance','Miscellaneous']
    level1_2={
        'level1':level1,
        'level2':level2,


    }
    return level1_2

def getcostcode_component_path(order,company_id,costcode_main_id,get_remaining_level,costcode_format):
    costcode_main=CostCodeMain.objects.getcostcodemain_byid(costcode_main_id)
    level1_discipline=ProjectDiscipline.objects.get_discipline_byid(costcode_main.level1_developmenttype_id)
    level1_development=DevelopmentType.objects.getall_development_byid(costcode_main.level1_discipline_id)
    level2_name=DisciplineSubtype.objects.get_disciplinesubtype_byid(costcode_main.level2_discipline_id)
    codecode_component=level1_discipline.name+'('+level1_development.development_type+')/'+level2_name.discipline_subtype+'/'

    costcodesub_byorder=CostCodeSub.objects.getcostcodemain_byorder_costcodemain(order,company_id,costcode_main_id)
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
    data ={
       'codecode_component':codecode_component,
       'costcode_view':costcode_view 
    }
    return data






