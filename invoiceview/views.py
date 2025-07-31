from django.shortcuts import render
from django.views.generic import View,DeleteView
from datetime import datetime
from invoice.models import Invoiceflowmodulesusers


class Calendarview(View):
    def get(self,request):
        # print(f"role_id {request.user.roles_id}")
        invoiceflowusers=Invoiceflowmodulesusers.objects.getallinvoiceflow_byuserid(request.user.id,request.user.roles_id , request.company.id)
        allinvoice_events=[]
        existing_invoice_ids = set()  
        print(f"invoiceflowusers {invoiceflowusers}")
        for invoiceflowuser in invoiceflowusers:
            try:
                invoice = invoiceflowuser.Invoiceflowmodules.invoice
                if(invoiceflowuser.Invoiceflowmodules.bank_user_status == 0):
                    module_name=invoiceflowuser.Invoiceflowmodules.flowlevel_module.module.module.module_name
                else:
                    module_name='Bank User'
                print(f"invoiceflowuser.Invoiceflowmodules {invoiceflowuser.Invoiceflowmodules}")
                if invoiceflowuser.Invoiceflowmodules.invoice.id not in existing_invoice_ids:
                    existing_invoice_ids.add(invoiceflowuser.Invoiceflowmodules.invoice.id)  

                    invoice_cost_information = invoice.invoicecostinvoice_set.all()
                    invoice_number_join=''
                    allinvoice_number=[]
                    for cost_info in invoice_cost_information:
                        allinvoice_number.append(cost_info.invoice_number)
                    invoice_number_join = ', '.join(allinvoice_number)

                    allinvoice_events.append({
                        'title': invoice_number_join, 
                        'start':invoiceflowuser.Invoiceflowmodules.notification_at, 
                        'end': invoiceflowuser.Invoiceflowmodules.notification_at,
                        'invoice_id':invoiceflowuser.Invoiceflowmodules.invoice.id,
                        'module_name':module_name
                    })
            except Exception as e:
                continue

        # print(f"allinvoice_events {allinvoice_events}")
        return render(request,'calendar.html',{'events': allinvoice_events})


class Listview(View):
    def get(self,request):
        invoiceflowusers=Invoiceflowmodulesusers.objects.getallinvoiceflow_byuserid(request.user.id,request.user.roles_id, request.company.id)
        allinvoice_events=[]
        existing_invoice_ids = set()  
        for invoiceflowuser in invoiceflowusers:
            try:
                invoice = invoiceflowuser.Invoiceflowmodules.invoice
                if(invoiceflowuser.Invoiceflowmodules.bank_user_status == 0):
                    module_name=invoiceflowuser.Invoiceflowmodules.flowlevel_module.module.module.module_name
                else:
                    module_name='Bank User'
                if invoiceflowuser.Invoiceflowmodules.invoice.id not in existing_invoice_ids:
                    existing_invoice_ids.add(invoiceflowuser.Invoiceflowmodules.invoice.id)  
                    invoice_cost_information = invoice.invoicecostinvoice_set.all()
                    invoice_number_join=''
                    allinvoice_number=[]
                    for cost_info in invoice_cost_information:
                        allinvoice_number.append(cost_info.invoice_number)
                    invoice_number_join = ', '.join(allinvoice_number)
                    invoice_submission_date=cost_info.invoice_submission_date  # Moved here

                    allinvoice_events.append({
                        'title': invoice_number_join, 
                        'start':invoiceflowuser.Invoiceflowmodules.notification_at, 
                        'end': invoiceflowuser.Invoiceflowmodules.notification_at,
                        'invoice_id':invoiceflowuser.Invoiceflowmodules.invoice.id,
                        'module_name':module_name,
                        'vendor_name':invoiceflowuser.Invoiceflowmodules.invoice.vendor.vendor_name,
                        'vin':invoiceflowuser.Invoiceflowmodules.invoice.vendor.vin,
                        'name_service':invoiceflowuser.Invoiceflowmodules.invoice.name_service,
                        'submitted_date':invoice_submission_date,
                        'company_id':invoiceflowuser.Invoiceflowmodules.invoice.company_id
                    })
            except Exception as e:
                continue

        return render(request,'list.html',{'allinvoice': allinvoice_events})

class Listview_date(View):
    def get(self,request):
        date_str = request.GET.get('date')



  