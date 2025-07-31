from typing import Any
from django.db import models

class AddNewDisputedQueryManager(models.Manager):
    def create_disputed_query(self,pk,deniedreason,user,time_stamp,vendor,file,returned_count,file_name):
        return self.create(query_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,file=file,returned_count=returned_count,original_file_name=file_name)
    
    def create_creditdisputed_query(self,pk,deniedreason,user,time_stamp,vendor,file):
        return self.create(credit_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,file=file)
    
    def reason_for_dispute(self,pk,deniedreason,user,time_stamp,vendor,module_id,returned_count):
        return self.create(query_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id,returned_count=returned_count)
    
    def reason_for_creditdispute(self,pk,deniedreason,user,time_stamp,vendor,module_id):
        return self.create(credit_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id)

class AddNewDisputedQuery(models.Model):
    id = models.AutoField(primary_key=True)
    query=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    credit=models.ForeignKey("credit_note.CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    date=models.CharField(max_length=255)
    file=models.FileField(blank=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("InvoiceGuard.Module",on_delete=models.CASCADE,blank=True,null=True)
    highlighted_content=models.BooleanField(default=False,blank=True,null=True)
    #if query_status == 0, query not yet closed elif query_status == 1 ,query closed
    query_status=models.IntegerField(blank=True,null=True,default=0)
    #invoice returned- n times
    returned_count=models.IntegerField(blank=True,null=True,default=1)
    objects=AddNewDisputedQueryManager()
    original_file_name = models.CharField(max_length=255, blank=True, null=True)  # New column to store original file name

class DisputedQueryFiles(models.Model):
    id = models.AutoField(primary_key=True)
    disputedquery=models.ForeignKey("AddNewDisputedQuery",on_delete=models.CASCADE,blank=True, null=True)
    file=models.FileField(blank=True)
    document_type=models.CharField(max_length=10, blank=True, null=True)
    document_name=models.CharField(max_length=1000, blank=True, null=True)
    original_file_name = models.CharField(max_length=255, blank=True, null=True)  # New column to store original file name

    # def save(self, *args, **kwargs):
    #     if self.file and not self.original_file_name:
    #         self.original_file_name = self.file.name
    #     super().save(*args, **kwargs)


class BackToDisputeQueryManager(models.Manager):
    def create_disputed_query(self,pk,deniedreason,user,time_stamp,vendor,file,file_name):
        return self.create(query_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,file=file,original_file_name=file_name)
    
    def reason_for_dispute(self,pk,deniedreason,user,time_stamp,vendor,module_id):
        return self.create(query_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id)
    
    def reason_for_creditdispute(self,pk,deniedreason,user,time_stamp,vendor,module_id):
        return self.create(credit_id=pk,deniedreason=deniedreason,user=user,date=time_stamp,vendor_id=vendor,module_id=module_id)

class BackToDisputeQuery(models.Model):
    id = models.AutoField(primary_key=True)
    query=models.ForeignKey("Invoice",on_delete=models.CASCADE,blank=True, null=True)
    credit=models.ForeignKey("credit_note.CreditNote",on_delete=models.CASCADE,blank=True, null=True)
    deniedreason=models.CharField(max_length=1000,verbose_name="Reason", blank=True, null=True)
    date=models.CharField(max_length=255)
    file=models.FileField(blank=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("InvoiceGuard.Module",on_delete=models.CASCADE,blank=True,null=True)
    objects=BackToDisputeQueryManager()