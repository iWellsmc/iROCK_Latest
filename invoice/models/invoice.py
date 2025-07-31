from django.db import models
from django.db.models import Q

class RoleManager(models.Manager):
    def get_by_id(self,invoice_id):
        return self.get(id=invoice_id)
    
    def get_by_id_status(self,invoice_id,status):
        return self.get(id=invoice_id,status=status)

    def createinvoice(self,invoicetype,from_datetime_object,todate_datetime_object,contractid,contract_type,contractnameservice,contractservicetype,service_rendered,location_service,project,block,field,well,company,vendorid,block_not,field_not,well_not,costcode,project_hdn,wcc_id):
        return self.create(invoice_type=invoicetype,fromdate=from_datetime_object,todate=todate_datetime_object,contractid=contractid,contracttype=contract_type,name_service=contractnameservice,types_service=contractservicetype,description_service=service_rendered,location_service=location_service,project_name=project,block_id=block,field_id=field,well_id=well,company=company,vendor_id=vendorid,block_not_applicable=block_not,field_not_applicable=field_not,well_not_applicable=well_not,costcodevendor_id=costcode,project_id=project_hdn,wcc_id=wcc_id)
    
    def getallinvoices(self,company):
        return self.filter(status=1,invoice_status=2,company=company).order_by('-id')
   
    def filter_by_company(self,status,invstatus,company):
        """
        Filter Multiple object by company from Invoice Model
        """
        return self.filter(status=status,invoice_status=invstatus,company=company)
    
    def exclude_approved_invoice_by_company(self,company):
        return self.filter(company=company,status=1).filter(Q(invoice_status=2) | Q(invoice_status=4) | Q(invoice_status=5)).order_by('-id')

    def filter_by_id(self,id):
        """
        Return Single object by Id from Invoice Model
        """
        return self.filter(id=id)
    
    def filter_by_wcc(self,wcc_id):
        return self.filter(wcc_id=wcc_id)

    # def filter_by_id(self,invoice_id,status):
    #     return self.get(id=invoice_id,status=status)
    
    # def delete_by_id(self,id,company_id):
    #     return self.get(id=id,company=company_id)
    
    # def get_by_company(self,company_name,status):
    #     return self.filter(company=company_name,status=status)
    
    # def filter_by_rolename(self,role_name,company,status):
    #     return self.filter(role_name__iexact=role_name,company=company,status=status)

    # def filter_by_module_id(self,module_id,company):
    #     return self.filter(module_id=module_id,company=company,status=1)

    def getinvoiceby_contract(self,contractid):
        return self.filter(contractid=contractid,status=1,invoice_status=2).order_by('-id')
    
    def exclude_approved_invoice(self,contractid):
        return self.filter(contractid=contractid,status=1).filter(Q(invoice_status=2) | Q(invoice_status=4) | Q(invoice_status=5)).order_by('-id')
    
    def getdisputedinvoiceby_contract(self,contractid):
        return self.filter(contractid=contractid,status=1,invoice_status=6).order_by('-id')
    
    def getinvoiceby_payment(self,contractid):
        return self.filter(contractid=contractid,status=1,invoice_status=3).order_by('-id')

    def get_invoice_by_list_ids(self,invoice_list):
        return self.filter(id__in=invoice_list).order_by('-id')
    
    def getapproved_invoice_byvendor(self,vendor_id):
        return self.filter(approval_status=1,vendor_id=vendor_id)
    
    def updatelast_notification(self,invoice_id,timestamp):
        return self.filter(id=invoice_id).update(last_notification=timestamp)

    def update_conform_costcode(self,invoice_id,costcode_vendor_id,comments):
        return self.filter(id=invoice_id).update(is_conform_costcode=1,costcodevendor_id=costcode_vendor_id,conform_costcode_comments=comments)
    
    def get_conform_costcode(self,invoice_id):
        try:
            return self.get(id=invoice_id,is_conform_costcode=1)
        except ObjectDoesNotExist:
            return ""

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    invoice_type=models.CharField(max_length=255,verbose_name="invoice type", blank=True, null=True)
    invoice_submit_date=models.DateTimeField(editable=True,blank=True, null=True)
    fromdate=models.DateTimeField(editable=True,null=True)
    todate=models.DateTimeField(editable=True,null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    contracttype=models.CharField(max_length=255,verbose_name="contract type", blank=True, null=True)
    name_service=models.CharField(max_length=255,verbose_name="name service", blank=True, null=True)
    types_service=models.CharField(max_length=255,verbose_name="types service", blank=True, null=True)
    description_service=models.CharField(max_length=255,verbose_name="description service", blank=True, null=True)
    location_service=models.CharField(max_length=255,verbose_name="location service", blank=True, null=True)
    project_name=models.CharField(max_length=255,verbose_name="project name", blank=True, null=True)
    block=models.ForeignKey("projects.ProjectBlock",on_delete=models.CASCADE,blank=True, null=True)
    field=models.ForeignKey("projects.ProjectField",on_delete=models.CASCADE,blank=True, null=True)
    well=models.ForeignKey("projects.ProjectWellName",on_delete=models.CASCADE,blank=True, null=True)
    block_not_applicable=models.CharField(max_length=20,blank=True, null=True)
    field_not_applicable=models.CharField(max_length=20,blank=True, null=True)  
    well_not_applicable=models.CharField(max_length=20,blank=True, null=True)
    invoice_status=models.IntegerField(blank=True, null=True,default=1)
    #costinvoice.approval_status == 6 and invoice.invoice_status == 6 (Disputed), costinvoice.approval_status == 1 and invoice.invoice_status == 2 (Awaiting Approval), costinvoice.approval_status == 1 and invoice.invoice_status == 1 (Not Yet Submitted),costinvoice.approval_status =3 and invoice.invoice_status = 3 Approved,costinvoice.approval_status =4 and invoice.invoice_status = 4 Returned,costinvoice.approval_status =5 and invoice.invoice_status = 5 Rejected,
    costcodevendor=models.ForeignKey("cost_code.CostCodeVendor",on_delete=models.CASCADE,blank=True, null=True)
    wcc=models.ForeignKey("wcc.WorkCompletionCost",on_delete=models.CASCADE,blank=True, null=True)
    project=models.ForeignKey("projects.Projectcreation",on_delete=models.CASCADE,blank=True, null=True)
    #to check whether the vendor closed the query for disputed invoice
    dispute_status=models.IntegerField(blank=True, null=True,default=0)
    tax_type=models.IntegerField(blank=True, null=True,default=0)
    created_at=models.DateTimeField(editable=True,null=True,blank=True)
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_modified = models.DateTimeField(auto_now=True, null=True)
    approval_status=models.IntegerField(blank=True, null=True,default=0)
    last_notification=models.BigIntegerField(blank=True, null=True)
    is_conform_costcode=models.BooleanField(blank=True, null=True,default=0)
    conform_costcode_comments=models.TextField(blank=True, null=True)
    query_status=models.IntegerField(blank=True, null=True,default=0)
    # return_reject_status=1 is return  , return_reject_status=2 is dispute
    return_dispute_status=models.IntegerField(blank=True, null=True,default=0)
    objects=RoleManager()