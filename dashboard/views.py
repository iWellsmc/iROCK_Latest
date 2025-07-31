# standard libraries
from django.http import JsonResponse
from django.views.generic import View
# third-party libraries
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# local libraries
from django.shortcuts import render,redirect
from custom_auth.helpers import markas_read_status
from projects.models import ContractMasterVendor,ContractMaster,ProjectUser,Projects,Projectcreation,UserRights
from invoice.models import InvoiceCostInvoice
from invoice.invoice_dashboard import getapprovedinvoice_summary,getawaitinginvoice_summary,getdisputedinvoice_summary,getprojectby_countrywise,getinvoicesummarychartdata_byvendor,getallprojects_byvendor,getallcountries_byvendor,getallcurrencies_byvendor,getcreditnote_details_byvendor,getdefaultcurrency_company,getinvoice_summary_details_filter,getproject_summary_details_filter
from custom_auth.models import Countries,Companies
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
import string    
import random  


@method_decorator(login_required(login_url='/'), name='dispatch')

class Dashboard(View):
    
    def get(self, request):
        markas_read_status(request.get_full_path())
        # rights=User
        # markas_read_status(request.get_full_path())
        projectviewrights=UserRights.objects.filter(user_id=request.user.id, status=1, view=1,module_id=1 ).count()
        contractmasterviewrights=UserRights.objects.filter(user_id=request.user.id, status=1, view=1,module_id=4 ).count()
        vendorviewrights=UserRights.objects.filter(user_id=request.user.id, status=1, view=1,module_id=2).count()
        data={'projectviewrights':projectviewrights ,'contractmasterviewrights':contractmasterviewrights, 'vendorviewrights':vendorviewrights, 'request':request}
        request.session['mainmenu'] = 'dashboard'
        if(request.user.is_superuser):
            return render(request, 'dashboardsuperuser.html')
        elif (request.user.roles_id == 3):
            if (request.user.userfirsttimelogin == 0):
                return redirect('custom_auth:userpasswordreset',pk=request.user.id)
            else:
                return render (request,"userdashboard.html" , data)
        elif (request.user.bankuserstatus == 1):
            return render (request,"userdashboard.html",data)
        elif (request.user.roles_id == 4):
                if (request.user.userfirsttimelogin == 0):
                    return redirect('custom_auth:userpasswordreset',pk=request.user.id)
                else:
                    if (request.user.userfirsttimelogin == 1) :
                        if(request.user.is_primary == 0 and request.user.is_secondary == 0) :
                            vendorid=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
                            return redirect('projects:editinsidevendorbasicinfo',pk=vendorid.id )
                    vendor=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
                    vendor_data=getvendor_dashboard(request)
                    getvendordetails=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
                    return render (request,"vendordashboard.html",{'data':vendor_data , 'vendor':vendor ,'getvendordetails':getvendordetails , 'request':request})
                
        else:
            company=Companies.objects.get(id=request.company.id)
            if company.checkkeystatus == 0:
                return redirect('custom_auth:keyactivationpage')
            
            else:
                if Companies.objects.filter(id=request.company.id,category_entity__isnull=True):
                    return redirect('custom_auth:editcompany',pk=request.company.id)
                else:
                    return render (request,"dashboard.html")
def getvendor_dashboard(request):
    vendor_details=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    # invoices=Invoice.objects,filter(vendor_id=vendorid.id,status=1)
    invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendor_details.id,status=1,approval_status=2,payment_status=2)
    paidinvoices=invoices.count()
    invoices=InvoiceCostInvoice.objects.filter(vendor_id=vendor_details.id,status=1,approval_status=2,payment_status=1)
    unpaidinvoices=invoices.count()
    data={'paidinvoices':paidinvoices,'unpaidinvoices':unpaidinvoices}
    if (request.user.userfirsttimelogin == 0):
        return redirect('custom_auth:userpasswordreset',pk=request.user.id)
    else:
        if (request.user.userfirsttimelogin == 1) :
            if(request.user.is_primary == 0 and request.user.is_secondary == 0) :
                return redirect('projects:editinsidevendorbasicinfo',pk=vendor_details.id)
        total_project=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_details.id,None)
        active_project=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_details.id,True)
        inactive_project=ContractMaster.objects.getprojectcount_by_vendor_status(vendor_details.id,False)

        total_contracts=ContractMaster.objects.gettotalcontracts(vendor_details.id)
        active_contracts=ContractMaster.objects.gettotalcontracts_bystatus(vendor_details.id,True)
        inactive_contracts=ContractMaster.objects.gettotalcontracts_bystatus(vendor_details.id,False)

        approvedinvoice_summary=getapprovedinvoice_summary(vendor_details.id)
        awaitedinvoice_summary=getawaitinginvoice_summary(vendor_details.id)
        disputedinvoice_summary=getdisputedinvoice_summary(vendor_details.id)
     
        currencies_list = list(set(approvedinvoice_summary['currencies'] + awaitedinvoice_summary['currencies'] + disputedinvoice_summary['currencies']))
        allprojects=getallprojects_byvendor(vendor_details.id)
        allcountries=getallcountries_byvendor(vendor_details.id)
        allcurrencies=getallcurrencies_byvendor(vendor_details.id)
        credit_note_details=getcreditnote_details_byvendor(vendor_details)

        

        data ={
            'total_project':total_project.count(),
            'active_project':active_project.count(),
            'inactive_project':inactive_project.count(),
            'total_contracts':total_contracts.count(),
            'active_contracts':active_contracts.count(),
            'inactive_contracts':inactive_contracts.count(),
            'invoice_summary':approvedinvoice_summary,
            'awaitedinvoice_summary':awaitedinvoice_summary,
            'disputedinvoice_summary':disputedinvoice_summary,
            'currencies_list':currencies_list,
            'vendor_id':vendor_details.id,
            'allprojects':allprojects,
            'allcountries':allcountries,
            'allcurrencies':allcurrencies,
            'credit_note_details':credit_note_details,
            'default_currency':getdefaultcurrency_company(request.company.id),
            'default_currency_list':list(getdefaultcurrency_company(request.company.id))
        }
        return data

def filtervendor_dashboard(request):
    vendor_details=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()

    country_ids = request.GET.getlist('country_id[]', []) 
    project_id = request.GET.getlist('project_id[]', []) 
    services = request.GET.getlist('services[]', []) 
    currencies = request.GET.getlist('currencies[]', []) 
    tax = request.GET.getlist('tax[]', []) 
    invoice_summary_details=getinvoice_summary_details_filter(vendor_details.id,currencies,project_id,country_ids,services,tax,vendor_details.company_id)
    project_summary_details=getproject_summary_details_filter(vendor_details.id,country_ids,vendor_details.company_id)

    allproject=getprojectby_countrywise(vendor_details.id,country_ids)


    data ={
       'invoice_summary_details':invoice_summary_details,
       'project_summary_details':project_summary_details,
       'allproject':allproject
    }
    return JsonResponse(data,safe=False)



def getcountry_wise_project(request):
    vendor_id=request.GET.get('vendor_id',None)
    
    is_poa = request.GET.get('is_poa', False)

    allproject=getprojectby_countrywise(vendor_id,[],is_poa)
    return JsonResponse(allproject,safe=False)
def getinvoicesummarychart_byvendor(request):
    vendor_details=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    chartdata=getinvoicesummarychartdata_byvendor(vendor_details)
    return JsonResponse(chartdata,safe=False)


def getunpaid_overdueinvoices(request):
    vendor_details=ContractMasterVendor.objects.filter(vin=request.user.cin_number).first()
    chartdata=getinvoicesummarychartdata_byvendor(vendor_details)
    return JsonResponse(chartdata,safe=False)
def dash_country_viewas(request):
    user_id = request.user.id

    assigned_projects = ProjectUser.objects.filter(user_id=user_id)
    project_details_list = []
    country_ids = []

    for project in assigned_projects:
        project_creation = Projectcreation.objects.get(id=project.project_id)
        project_name = project_creation.projectname  # Assuming projectname is the name field
        project_details_list.append(project_name)
        country_id = project_creation.country.id
        country_ids.append(country_id)

    # Retrieve country objects based on the IDs obtained
    country_objects = Countries.objects.filter(id__in=country_ids)

    # Define a function to generate random pastel colors
    def generate_pastel_color(used_colors):
        while True:
            r = random.randint(180, 255)
            g = random.randint(180, 255)
            b = random.randint(180, 255)
            color = f"rgb({r}, {g}, {b})"
            if color not in used_colors:
                used_colors.add(color)
                return color

    # Initialize dataset with a root node representing the company
    dataset = [{'id': '0.0', 'parent': '', 'name': 'Irock'}]
    used_colors = set()

    # Iterate over each country
    for country in country_objects:
        # Generate a random pastel color for the country
        rgb = generate_pastel_color(used_colors)

        try:
            # Get projects associated with the country
            # Get project IDs associated with the user
            project_ids = ProjectUser.objects.filter(user_id=user_id).values_list('project_id', flat=True)

            # Get projects associated with the user's project IDs and country
            projects = Projectcreation.objects.filter(id__in=project_ids, country=country)


            # Create a dictionary entry for the country
            country_dict = {'id': f'1.{country.id}', 'parent': '0.0', 'name': str(country), 'color': rgb}
            dataset.append(country_dict)

            # Create dictionary entries for each project
            for project in projects:
                project_dict = {'id': f'2.{project.id}', 'parent': country_dict['id'], 'name': str(project), 'value': 1}
                dataset.append(project_dict)

        except Exception as e:
            print(f"Error processing country {country}: {e}")

    data = dataset

    return JsonResponse({'data': data})