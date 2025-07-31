from django.db import models
from django.utils import timezone
class WorkCompletionCostManager(models.Manager):
    def filter_by_status(self,status,company):
        return self.filter(status=status,company_id=company)
    
    def get_wcc_approval_check(self,status,wcc_status,company=None):
        queryset=self.filter(status=status,wcc_status=wcc_status)
        if company is not None:
            queryset=queryset.filter(company_id=company)
        return queryset
    
    def filter_by_company(self,company):
        return self.filter(company_id=company)
    
    def filter_all_data(self,vendor_id,company):
        return self.filter(vendor_id=vendor_id,company_id=company)
    
    def filter_submiited_data(self,vendor_id,company):
        return self.filter(vendor_id=vendor_id,company_id=company,status=1,wcc_status=2)
    def get_by_id(self,pk):
        return self.get(id=pk)

    def update_by_id(self,pk,status):
        return self.filter(id=pk).update(status=status)
    
    def approve_wcc(self,pk,approve_status,date):
        return self.filter(id=pk).update(wcc_status=approve_status,wcc_status_date=date)
    
    def createworkcompletioncost(self,from_datetime_object,todate_datetime_object,contractid,contract_type,contractnameservice,contractservicetype,service_rendered,location_service,project,block,field,well,company,vendorid,block_not,field_not,well_not,costcode,project_hdn):
        return self.create(fromdate=from_datetime_object,todate=todate_datetime_object,contractid=contractid,contracttype=contract_type,name_service=contractnameservice,types_service=contractservicetype,description_service=service_rendered,location_service=location_service,project_name=project,block_id=block,field_id=field,well_id=well,company=company,vendor_id=vendorid,block_not_applicable=block_not,field_not_applicable=field_not,well_not_applicable=well_not,costcodevendor_id=costcode,project_id=project_hdn)
    
    def updateworkcompletioncost(self,pk,from_datetime_object,todate_datetime_object,contractid,contract_type,contractnameservice,contractservicetype,service_rendered,location_service,project,block,field,well,block_not,field_not,well_not,costcode):
        return self.filter(id=pk).update(fromdate=from_datetime_object,todate=todate_datetime_object,contractid=contractid,contracttype=contract_type,name_service=contractnameservice,types_service=contractservicetype,description_service=service_rendered,location_service=location_service,project_name=project,block_id=block,field_id=field,well_id=well,block_not_applicable=block_not,field_not_applicable=field_not,well_not_applicable=well_not,costcodevendor_id=costcode)

    def filter_by_project(self,project_id,wcc_status,submit_status):
        return self.filter(project_id=project_id,wcc_status=wcc_status,status=submit_status)
    
    def filter_by_project_ids(self,project_ids,wcc_status,submit_status):
        return self.filter(project_id__in=project_ids).filter(wcc_status=wcc_status,status=submit_status)
    
    def updatelast_notification(self,wcc_id,current_timestamp):
        self.filter(id=wcc_id).update(last_notification=current_timestamp)

class WorkCompletionCost(models.Model):
    id = models.AutoField(primary_key=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    wcc_submit_date=models.DateTimeField(editable=True,blank=True, null=True,auto_now_add=True)
    fromdate=models.DateTimeField(editable=True,null=True)
    todate=models.DateTimeField(editable=True,null=True)
    contractid=models.CharField(max_length=255,verbose_name="contractid", blank=True, null=True)
    contracttype=models.CharField(max_length=255,verbose_name="contract type", blank=True, null=True)
    name_service=models.CharField(max_length=255,verbose_name="name service", blank=True, null=True)
    types_service=models.CharField(max_length=255,verbose_name="types service", blank=True, null=True)
    description_service=models.CharField(max_length=255,verbose_name="description service", blank=True, null=True)
    location_service=models.CharField(max_length=255,verbose_name="location service", blank=True, null=True)
    project_name=models.CharField(max_length=255,verbose_name="project name", blank=True, null=True)
    project=models.ForeignKey("projects.Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    block=models.ForeignKey("projects.ProjectBlock",on_delete=models.CASCADE,blank=True, null=True)
    field=models.ForeignKey("projects.ProjectField",on_delete=models.CASCADE,blank=True, null=True)
    well=models.ForeignKey("projects.ProjectWellName",on_delete=models.CASCADE,blank=True, null=True)
    block_not_applicable=models.CharField(max_length=20,blank=True, null=True)
    field_not_applicable=models.CharField(max_length=20,blank=True, null=True)  
    well_not_applicable=models.CharField(max_length=20,blank=True, null=True)
    wcc_status=models.IntegerField(blank=True, null=True,default=0)
     # wcc_status 0 = unapproved, 1 = approved
    costcodevendor=models.ForeignKey("cost_code.CostCodeVendor",on_delete=models.CASCADE,blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=0)
    # status 1 = submitted,status 2 = delete,status 0 = draft
    wcc_status_date=models.DateTimeField(editable=True,blank=True, null=True)
    wcc_query_status=models.IntegerField(blank=True, null=True,default=0)
    dispute_status=models.IntegerField(blank=True, null=True,default=0)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    last_notification=models.BigIntegerField(blank=True, null=True)
    objects=WorkCompletionCostManager()
 
    