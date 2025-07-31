from django.db import models
from datetime import datetime
class InvoiceflowmodulesManager(models.Manager):
    def createinvoiceflowmodules(self,project_id,company_id,flowlevel_id,flowmodule_id,invoice_id,module_id,create_date,notify_date):
        return self.create(project_id=project_id,company=company_id,flowlevel_id=flowlevel_id,flowlevel_module_id=flowmodule_id,invoice_id=invoice_id,module_id=module_id,created_at=create_date,notification_at=notify_date)
    
    def createcreditflowmodules(self,project_id,company_id,flowlevel_id,flowmodule_id,credit_id,module_id,create_date,notify_date):
        return self.create(project_id=project_id,company=company_id,flowlevel_id=flowlevel_id,flowlevel_module_id=flowmodule_id,creditnote_id=credit_id,module_id=module_id,created_at=create_date,notification_at=notify_date)

    def createbankinvoiceflowmodules(self,project_id,company_id,flowlevel_id,flowmodule_id,invoice_id,module_id,create_date,notify_date):
        return self.create(project_id=project_id,company=company_id,flowlevel_id=flowlevel_id,flowlevel_module_id=flowmodule_id,invoice_id=invoice_id,module_id=module_id,created_at=create_date,notification_at=notify_date,bank_user_status=1)
    
    def getinvoiceflowmodules_byinvoice(self,invoice_id,module_id):
        return self.filter(invoice_id=invoice_id,status=0,module_id=module_id).last()
    
    def getcreditflowmodules_byinvoice(self,credit_id,module_id):
        return self.filter(creditnote_id=credit_id,status=0,module_id=module_id).first()
    
    def getinvoiceflowmodules_only_byinvoice(self,invoice_id,module_id):
        return self.filter(invoice_id=invoice_id,module_id=module_id).first()
    
    def get_by_module_id(self,invoice_id,status,module_id):
        return self.filter(invoice_id=invoice_id,status=status,module_id=module_id).last()

    def filter_by_module_id(self,invoice_id,status,module_id):
        return self.filter(invoice_id=invoice_id,status=status,module_id=module_id)
    
    def filter_by_module_id_with_invoicecostinvoice(self,invoicecost_id,status,module_id):
        return self.filter(invoicecost_id=invoicecost_id,status=status,module_id=module_id)
    
    def updateinvoiceflowmodules(self,id):
        return self.filter(id=id).update(status=1)
    
    def getinvoiceflowmodules(self,flowlevel_id,flowlevel_module_id):
        return self.filter(flowlevel=flowlevel_id,flowlevel_module=flowlevel_module_id)
    
    def getinvoiceflowmodules_invoice(self,invoice_id,flowlevel_id,flowlevel_module_id):
        return self.filter(invoice=invoice_id,flowlevel=flowlevel_id,flowlevel_module=flowlevel_module_id)
    
    def getinvoiceflowmodules_credit(self,credit_id,flowlevel_id,flowlevel_module_id):
        return self.filter(creditnote_id=credit_id,flowlevel=flowlevel_id,flowlevel_module=flowlevel_module_id)
    
    def getinvoiceflowmodules_by_invoice_id(self,invoice_id):
        return self.filter(invoice=invoice_id)
    
    def getinvoiceflowmodules_by_credit_id(self,creditnote_id):
        return self.filter(creditnote_id=creditnote_id)
    
    def get_by_only_module_id(self,invoice_id,module_id):
        return self.filter(invoice_id=invoice_id,module_id=module_id).first()
    
    def get_disputed_querys(self,invoice,module):
        return self.filter(invoice_id=invoice,status=1,module_id=module).first()
    
    def getall_activeinvoiceflowmodules(self):
        return self.filter(status=0,invoice__status=1,company_id=225)
    
    def getinvoiceflowmodules_byinvoiceids(self,invoice_id,module_id):
        return self.filter(invoice_id=invoice_id,status=0,module_id=module_id)



class Invoiceflowmodules(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=0)  #0- inprogress 1-completed 2-rejected
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    creditnote=models.ForeignKey("credit_note.CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    project_id=models.IntegerField(blank=True, null=True)
    flowlevel=models.ForeignKey("projectflow.ProjectFlowlevel",on_delete=models.CASCADE,blank=True, null=True)
    flowlevel_module=models.ForeignKey("projectflow.ProjectFlowModules",on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("InvoiceGuard.Module",on_delete=models.CASCADE,blank=True, null=True)
    created_at=models.DateTimeField(editable=True,null=True)
    notification_at=models.DateTimeField(editable=True,null=True)
    bank_user_status=models.IntegerField(blank=True, null=True,default=0)
    exchangerate_confirm_status=models.IntegerField(blank=True, null=True,default=0)
    tax_confirm_status=models.IntegerField(blank=True, null=True,default=0) 
    invoicecost=models.ForeignKey('InvoiceCostInvoice',on_delete=models.CASCADE,blank=True,null=True)
    payment_instruct=models.ForeignKey('PaymentInstruction',on_delete=models.CASCADE,blank=True,null=True)
    objects=InvoiceflowmodulesManager()


class InvoiceflowmodulesusersManager(models.Manager):
    current_date=datetime.now()
    def createinvoiceflowmodulesusers(self,project_id,project_user,Invoiceflowmodules_id,projectflow_user_id,user_id,current_date=current_date):
        return self.create(project_id=project_id,project_user=project_user,Invoiceflowmodules_id=Invoiceflowmodules_id,projectflow_user_id=projectflow_user_id,user=user_id,active_date=current_date)
    
    def createoverrideinvoiceusers(self,project_id,project_user,Invoiceflowmodules_id,user_id,override_status,current_date=current_date):
        return self.create(project_id=project_id,project_user=project_user,Invoiceflowmodules_id=Invoiceflowmodules_id,user=user_id,active_date=current_date,invoice_override=override_status)
    
    def creatbankinvoiceusers(self,project_id,invoiceflowmodules_id,user_id,instruction_id,instruction_companybank_id,bank_user_status,current_date=current_date):
        return self.create(project_id=project_id,Invoiceflowmodules_id=invoiceflowmodules_id,user=user_id,active_date=current_date,bank_user_status=bank_user_status,payment_instruction_id=instruction_id,company_bank_user_id=instruction_companybank_id)
    # projectflow_user_id=projectflow_user_id
    
    def getinvoiceflowmodulesusers_byuser(self,user_id,project_id,invoiceflowmodule_id=None):
        if invoiceflowmodule_id:
            return self.filter(user=user_id,project_id=project_id,status=0,Invoiceflowmodules_id=invoiceflowmodule_id)
        else:
            return self.filter(user=user_id,project_id=project_id,status=0)
    
    def getinvoiceflowmodulesusers_by_only_user(self,user_id,project_id,invoiceflowmodule_id):
        return self.filter(user=user_id,project_id=project_id,Invoiceflowmodules_id=invoiceflowmodule_id)
    
    def getinvoiceflowmodulesusers_payins(self,project_id,invoiceflowmodule_id,pay_instruction):
        return self.filter(project_id=project_id,Invoiceflowmodules_id=invoiceflowmodule_id,payment_instruction_id=pay_instruction,status=1)
    
    def getinvoiceoverrideflowmodulesusers_byuser(self,user_id,project_id,invoiceflowmodule_id):
        return self.filter(user=user_id,project_id=project_id,status=0,Invoiceflowmodules_id=invoiceflowmodule_id,invoice_override=1)

    def updateinvoicelowusers(self,Invoiceflowmodules_id,user_id,date,status,comments=None):
        return self.filter(Invoiceflowmodules_id=Invoiceflowmodules_id,user=user_id).update(status=status,comments=comments,created_at=date)
    
    def getapprovedusersinvoice(self,invoice):
        return self.filter(Invoiceflowmodules__invoice_id=invoice).exclude(status=0)
        
    def get_approved_users(self,Invoiceflowmodules_id):
        return self.filter(Invoiceflowmodules_id=Invoiceflowmodules_id).exclude(status=0)
    
    def get_invflow_users(self,Invoiceflowmodules_id):
        return self.filter(Invoiceflowmodules_id=Invoiceflowmodules_id)
    
    def getusers_by_invoiceflow_ids(self,all_invoiceflowmodules_id):
        return self.filter(Invoiceflowmodules_id__in=all_invoiceflowmodules_id)

    def get_bankuser_invoicefloemodule(self,Invoiceflowmodules_id,user,bank_user_status):
        try:
            return self.get(Invoiceflowmodules_id=Invoiceflowmodules_id,user=user,bank_user_status=bank_user_status)
        except:
            return self.filter(Invoiceflowmodules_id=Invoiceflowmodules_id,user=user,bank_user_status=bank_user_status).last()
    
    def filter_bankuser_invoice(self,user,bank_user_status):
        return self.filter(user=user,bank_user_status=bank_user_status)
    
    def createinvflowsignuser(self,project_id,invoiceflow_id,user_id,pay_instruction_data_id,current_date=current_date):
        return self.create(project_id=project_id,Invoiceflowmodules_id=invoiceflow_id,user=user_id,active_date=current_date,payment_instruction_id=pay_instruction_data_id)
    
    def getinvoiceflowmodulesusers_payapp(self,invoiceflowmodule_id,pay_instruction):
        return self.filter(Invoiceflowmodules_id=invoiceflowmodule_id,payment_instruction_id=pay_instruction,status=1)
    
    def get_payins_ids(self,invoiceflowmodule_id,pay_instruction_list):
        return self.filter(Invoiceflowmodules_id__in=invoiceflowmodule_id,payment_instruction_id__in=pay_instruction_list).filter(status=1)
    
    def getallinvoiceflow_byuserid(self,user,role_id=None, company=None):
        queryset=self.select_related('Invoiceflowmodules','Invoiceflowmodules__invoice').prefetch_related('Invoiceflowmodules__invoice__invoicecostinvoice_set')
        queryset=queryset.filter(status=0,Invoiceflowmodules__status=0 , Invoiceflowmodules__company=company)
        if(role_id != 2):
            queryset=queryset.filter(user=user)
        
        return queryset
    
    def getinvoiceoverride_users(self,invoice_id):
        return self.filter(Invoiceflowmodules__invoice_id=invoice_id,invoice_override=1)

    def checkuserexist_in_invoiceflowmodules(self,invoiceflow_module_id,user_id):
        self.filter(Invoiceflowmodules_id=invoiceflow_module_id,user=user_id)

    def updatemultipleinvoiceflowusers(self,Invoiceflowmodules_id,user_id,date,status,comments=None):
        return self.filter(Invoiceflowmodules_id__in=Invoiceflowmodules_id,user=user_id).update(status=status,comments=comments,created_at=date)

    
class Invoiceflowmodulesusers(models.Model):
    id = models.AutoField(primary_key=True)
    Invoiceflowmodules=models.ForeignKey("Invoiceflowmodules",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=0)
    user_status=models.IntegerField(blank=True, null=True,default=0)
    # status 1 = approved,status 2 = proceed,status 3 = return,status 4 = reject
    projectflow_user=models.ForeignKey("projectflow.ProjectFlowModuleUsers",on_delete=models.CASCADE,blank=True, null=True)
    project_id=models.IntegerField(blank=True, null=True)
    project_user=models.IntegerField(blank=True, null=True)
    user=models.IntegerField(blank=True, null=True)
    comments=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(editable=True,blank=True, null=True)
    active_date=models.DateTimeField(editable=True,null=True)
    invoice_override=models.IntegerField(blank=True, null=True,default=0)
    payment_instruction=models.ForeignKey("PaymentInstruction",on_delete=models.CASCADE,blank=True, null=True)
    company_bank_user=models.ForeignKey('finance.CompanyBankUser',on_delete=models.CASCADE,blank=True,null=True)
    bank_user_status=models.IntegerField(blank=True, null=True,default=0)
    bank_user_verification=models.IntegerField(blank=True, null=True,default=0)
    returned = models.IntegerField(blank=True,null=True,default=0)
    returned_date =models.DateTimeField(editable=True,blank=True,null=True)
    invoice_costinvoice=models.CharField(max_length=255,blank=True, null=True)
    objects=InvoiceflowmodulesusersManager()

class InvoiceFlowChecklistManager(models.Manager):
    def createinvoicechecklist(self,invoice_id,checklist,checked_status,comments):
        return self.create(invoice_id=invoice_id,checklist=checklist,confirm_status=checked_status,comments=comments)
    
    def createcreditchecklist(self,credit_id,checklist,checked_status,comments):
        return self.create(credit_id=credit_id,checklist=checklist,confirm_status=checked_status,comments=comments)
    
class InvoiceFlowChecklist(models.Model):
    id = models.AutoField(primary_key=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    invoice=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    credit=models.ForeignKey("credit_note.CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    checklist=models.CharField(max_length=10,blank=True, null=True)
    confirm_status=models.IntegerField(blank=True, null=True,default=0)
    comments=models.TextField(blank=True, null=True)
    objects=InvoiceFlowChecklistManager()

  