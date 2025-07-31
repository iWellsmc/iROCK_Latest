from django.core.management.base import BaseCommand
from invoice.models import Invoiceflowmodules,InvoiceCostInformation,Invoiceflowmodulesusers,InvoiceCostInvoice,Invoice
from datetime import datetime,timedelta
from custom_auth.models import InvoiceTimeTrigger,User
from django.utils import timezone
from invoice.helpers import add_invoice_time
from InvoiceGuard.models import RoleRight
from projectflow.models import ProjectFlowlevel,ProjectFlowModules,ProjectFlowModuleUsers
from projects.models import ContractMasterVendor
from notifications.signals import notify 






class Command(BaseCommand):
    help = 'check autoremainder'

    def handle(self, *args, **kwargs):
        self.checkoverride_invoice()
    
    def checkoverride_invoice(self):
        invoiceflow_modules=Invoiceflowmodules.objects.getall_activeinvoiceflowmodules()
        current_datetime = timezone.now()
        current_timestamp = datetime.now().timestamp()


        for invoiceflow_module in invoiceflow_modules:
            invoice_details=InvoiceCostInformation.objects.getinvoice_cost_information(invoiceflow_module.invoice_id)

            get_company_invoice_time=InvoiceTimeTrigger.objects.getinvoice_time_trigger_by_paymentday(invoice_details.payment_terms.payment_day,invoice_details.invoice.company_id)
            last_notification=invoiceflow_module.invoice.last_notification
            if last_notification:
                time_difference = current_timestamp - last_notification   
            
            
            if get_company_invoice_time.time_unit == 2:
                sequence_type='minutes'
            elif get_company_invoice_time.time_unit == 0:
                sequence_type='hours'
            else:
                sequence_type='days'
            notification_interval = timedelta(**{sequence_type: get_company_invoice_time.time_allotted})
            notification_interval_seconds = notification_interval.total_seconds()

            if not last_notification:
                time_difference = notification_interval_seconds

            if not last_notification or time_difference >= notification_interval_seconds:
                sender = User.objects.getclientadmin_by_companyid(invoiceflow_module.invoice.company_id)
                invoice_number=list(InvoiceCostInvoice.objects.get_invoice_id(invoiceflow_module.invoice_id,1).values_list('invoice_number',flat=True))
                all_invoice=', '.join(str(e) for e in invoice_number)
                vendor=ContractMasterVendor.objects.get_byid(invoiceflow_module.invoice.vendor_id,invoiceflow_module.invoice.company_id)

                if current_datetime > invoiceflow_module.notification_at:
            
                    get_all_modules=ProjectFlowModules.objects.getprojectflow_modules_byprojectid(invoiceflow_module.invoice.project_id)
                    for flow_module in get_all_modules:
                        check_invoice_override=RoleRight.objects.check_module_rights(flow_module.role_id,'Override Invoice Approval')

                        if (check_invoice_override):
                                projectflow_module_users=ProjectFlowModuleUsers.objects.getusers_bymodule_id(flow_module.id)
                                if(projectflow_module_users):
                                    for user in projectflow_module_users:
                                        checkuserexists=Invoiceflowmodulesusers.objects.checkuserexist_in_invoiceflowmodules(invoiceflow_module.id,user.user.user.id)
                                        print(f"checkuserexists {checkuserexists}")
                                        if(not checkuserexists):
                                            Invoiceflowmodulesusers.objects.createoverrideinvoiceusers(invoiceflow_module.invoice.project_id,user.user.id,invoiceflow_module.id,user.user.user.id,1)
                                    
                                        recipient_user=user.user.user
                                    
                                        recipient=recipient_user
                                        url="https:/irockinfo.mo.vc//invoice/vendorbasedinvoice"
                                    
                                        notify.send(sender, recipient=recipient,data=url, verb='Action Required: Invoice Override Approval Needed', description=f'Assign personnel for Invoice approval for Invoice {all_invoice} for Vendor {vendor.vendor_name}  for services {invoiceflow_module.invoice.name_service}')
                    Invoice.objects.updatelast_notification(invoiceflow_module.invoice.id,current_timestamp)
            
                
   




















        





    
