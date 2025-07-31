from django.db import models
from datetime import datetime,date
class WccApprovalManager(models.Manager):
   now=datetime.now()
   def create_data(self,wcc_id,wcc_flow,user,station_id,calculate_time,now):
      return self.create(wcc_id=wcc_id,wcc_flow_id=wcc_flow,user_id=user,wcc_per_station_id=station_id,created_at=now,notification_at=calculate_time)
   
   def create_override_user(self,wcc_id,wcc_flow,user,station_id,calculate_time,now=now):
      return self.create(wcc_id=wcc_id,wcc_flow_id=wcc_flow,user_id=user,wcc_per_station_id=station_id,created_at=now,notification_at=calculate_time,invoice_override=1)
   
   def filter_by_user_wcc(self,wcc_id,user_id):
      return self.filter(wcc_id=wcc_id,user_id=user_id)
   
   def get_by_user_wcc(self,user,wcc_id):
      return self.filter(user_id=user,wcc_id=wcc_id)
   
   def filter_by_station_status(self,station_id,approval_status):
      return self.filter(wcc_per_station=station_id,approval_status=approval_status)

   def filter_by_station_not_approve(self,wcc_id,station_id):
      return self.filter(wcc_id=wcc_id,wcc_per_station_id=station_id).exclude(approval_status=1)

   def update_user_data(self,user,wcc_id,approval_status,comments,curent_date):
      get_last_record=self.filter(wcc_id=wcc_id,user_id=user).last()
      get_last_record.approval_status=approval_status
      get_last_record.comment=comments
      get_last_record.wcc_approval_submit_date=curent_date
      return get_last_record.save()
    
   def track_station_data(self,wcc_id,wcc_per_station):
      return self.filter(wcc_id=wcc_id,wcc_per_station_id=wcc_per_station).exclude(approval_status=1)
   
   def station_data_app_status(self,wcc_id,wcc_per_station,approval_status):
      return self.filter(wcc_id=wcc_id,wcc_per_station_id=wcc_per_station,approval_status=approval_status)
    
   def filter_by_user(self,user,status):
      return self.filter(user=user,approval_status=status)

   def filter_by_wcc(self,wcc_id):
      return self.filter(wcc_id=wcc_id)

    
class WccApproval(models.Model):
   id = models.AutoField(primary_key=True)
   user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
   wcc_flow=models.ForeignKey("WccFlow",verbose_name="Wcc Flow",on_delete=models.CASCADE,null=True,blank=True)
   #approval status (1= pending,2=approved,0=rejected,3=return)
   approval_status=models.IntegerField(blank=True, null=True,default=1)
   wcc=models.ForeignKey("WorkCompletionCost",on_delete=models.CASCADE,blank=True, null=True)
   wcc_per_station=models.ForeignKey("WccPerStation",verbose_name="wcc Per Station",on_delete=models.CASCADE,null=True,blank=True)
   comment=models.TextField(blank=True, null=True)
   wcc_approval_submit_date=models.DateTimeField(editable=True,blank=True, null=True)
   created_at=models.DateTimeField(editable=True,null=True)
   notification_at=models.DateTimeField(editable=True,null=True)
   invoice_override=models.IntegerField(blank=True, null=True,default=0)
   objects=WccApprovalManager()


                             
class WccReturnTrack(models.Model):
  id = models.AutoField(primary_key=True)
  user=models.ForeignKey('custom_auth.User',on_delete=models.CASCADE,blank=True, null=True)
  wcc=models.ForeignKey('WorkCompletionCost',on_delete=models.CASCADE,blank=True, null=True)
  stage=models.IntegerField(default=1,blank=True,null=True)
  status=models.BooleanField(default=True,blank=True,null=True)
  reason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
  module=models.ForeignKey('InvoiceGuard.Module',on_delete=models.CASCADE,blank=True,null=True)
  created_at=models.DateTimeField(editable=True,blank=True, null=True)
  vendor_confirmation=models.IntegerField(default=0,blank=True,null=True)
  returned_count=models.IntegerField(default=0,blank=True,null=True)



class AddwccQueryManager(models.Manager):
    def create_wcc_query(self,pk,deniedreason,user,time_stamp,vendor,file,returned_count,file_name):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,file=file,returned_count=returned_count,original_file_name=file_name)
    
    def create_wccdisputed_query(self,pk,deniedreason,user,time_stamp,vendor,file):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=8,file=file)
    
    def reason_for_wccdispute(self,pk,deniedreason,user,time_stamp,vendor,module_id,returned_count):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id,returned_count=returned_count)
    
    def reason_for_wcc(self,pk,deniedreason,user,time_stamp,vendor,module_id,returncount):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id,returned_count=returncount)


class WccQuery(models.Model):
    id = models.AutoField(primary_key=True)
    wcc=models.ForeignKey('WorkCompletionCost',on_delete=models.CASCADE,blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    date=models.CharField(max_length=255)
    file=models.FileField(blank=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("InvoiceGuard.Module",on_delete=models.CASCADE,blank=True,null=True)
    highlighted_content=models.BooleanField(default=False,blank=True,null=True)
    #if query_status == 0, query not yet closed elif query_status == 1 ,query closed
    query_status=models.IntegerField(blank=True,null=True,default=0)
    #wcc returned- n times
    returned_count=models.IntegerField(blank=True,null=True,default=1)
    original_file_name = models.CharField(max_length=255, blank=True, null=True)  # New column to store original file name
    objects=AddwccQueryManager()



class BackTowccQueryManager(models.Manager):
    def create_wcc_query(self,pk,deniedreason,user,time_stamp,vendor,file,file_name):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,file=file,original_file_name=file_name)
    
    def reason_for_dispute(self,pk,deniedreason,user,time_stamp,vendor,module_id):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id)
    
    def reason_for_wcc(self,pk,deniedreason,user,time_stamp,vendor,module_id):
        return self.create(wcc_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id)

class BackTowccQuery(models.Model):
    id = models.AutoField(primary_key=True)
    wcc=models.ForeignKey('WorkCompletionCost',on_delete=models.CASCADE,blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    date=models.CharField(max_length=255)
    file=models.FileField(blank=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("InvoiceGuard.Module",on_delete=models.CASCADE,blank=True,null=True)
    objects=BackTowccQueryManager()