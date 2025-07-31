from django.db import models
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
class WorkCompletionValueCostManager(models.Manager):
    def filter_by_status(self,status,company):
        return self.filter(status=status,company_id=company)
    
    def get_by_id(self,pk):
        return self.get(id=pk)
    
    def filter_by_id(self,pk):
        return self.filter(id=pk)
    
    def filter_by_wcc(self,pk):
        return self.filter(wcc_id=pk)
    
    def get_by_wcc(self,wcc_id):
        return self.filter(wcc_id=wcc_id).first()
    
    def create_wcc_value(self,vendor,wcc,wcc_number,wcc_date,wcc_amount,wcc_file,company):
        if (wcc_file ==  None or wcc_file ==''):
              wcc_name = wcc_file
        else:
              wcc_name = wcc_file.name
        return self.create(vendor=vendor,wcc_id=wcc,wcc_number=wcc_number,wcc_date=wcc_date,wcc_amount=wcc_amount,wcc_file=wcc_file,wcc_file_name=wcc_name,company=company)
    
    def update_data(self,pk,wcc_number,wcc_date,wcc_amount,wcc_file,wccfilehdnid):
        if (wccfilehdnid):
            data=self.filter(wcc_id=pk).update(wcc_number=wcc_number,wcc_date=wcc_date,wcc_amount=wcc_amount)
        else:
            data=self.filter(wcc_id=pk).update(wcc_number=wcc_number,wcc_date=wcc_date,wcc_amount=wcc_amount,wcc_file=wcc_file)
            if (wcc_file !=  None):
                fs = FileSystemStorage()
                fs.save(wcc_file.name, wcc_file)
        return data
    
    def check_data(self,**kwargs):
        if (kwargs['wcc_id'] != ''):
            return self.filter(company=kwargs['company'],wcc_number=kwargs['wcc_number']).exclude(id=kwargs['wcc_id'])
        else:
            return self.filter(company=kwargs['company'],wcc_number=kwargs['wcc_number'])

class WorkCompletionValue(models.Model):
    id = models.AutoField(primary_key=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    wcc=models.ForeignKey("WorkCompletionCost",on_delete=models.CASCADE,blank=True, null=True)
    wcc_number=models.CharField(max_length=255,verbose_name="wcc number", blank=True, null=True)
    wcc_date=models.DateTimeField(editable=True,blank=True,null=True)
    wcc_amount=models.CharField(max_length=255,verbose_name="wcc amount", blank=True, null=True)
    wcc_file=models.FileField(upload_to="wccfile",blank=True,null=True)
    wcc_file_name=models.CharField(max_length=255,blank=True,null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=WorkCompletionValueCostManager()

    
class WccFileUploadManager(models.Manager):
    def filter_by_status(self,status,company):
        return self.filter(status=status,company_id=company)
    
    def get_by_id(self,pk):
        return self.get(id=pk)
    
    def create_wcc_supportfile(self,vendor,wcc,support,wcc_file,company):
        return self.create(vendor=vendor,wcc_id=wcc,support=support,wcc_support_file=wcc_file,wcc_support_file_name=wcc_file.name,company=company)

    def get_by_support(self,wcc,status,support):
        return self.filter(support=support,status=status,wcc_id=wcc)
    
    def update_file_status(self,pk,file_ids):
        return self.filter(id=pk).exclude(id__in=file_ids).update(status=0)

class WccFileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    vendor=models.ForeignKey("projects.ContractMasterVendor",on_delete=models.CASCADE,blank=True, null=True)
    wcc=models.ForeignKey("WorkCompletionCost",on_delete=models.CASCADE,blank=True, null=True)
    support=models.CharField(max_length=10,blank=True, null=True)
    wcc_support_file=models.FileField(upload_to="wccfile",blank=True,null=True)
    wcc_support_file_name=models.CharField(max_length=255,blank=True,null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=WccFileUploadManager()


class WccQueryFiles(models.Model):
    id = models.AutoField(primary_key=True)
    disputedquery=models.ForeignKey("WccQuery",on_delete=models.CASCADE,blank=True, null=True)
    file=models.FileField(blank=True)
    document_type=models.CharField(max_length=10, blank=True, null=True)
    document_name=models.CharField(max_length=1000, blank=True, null=True)
    original_file_name = models.CharField(max_length=255, blank=True, null=True)