from django.db import models
from .process import *
from .module import Module
from django.db.models import F


class ProcessModuleManager(models.Manager):
    def get_by_id(self,id):
        """
        Return Single Object by id from ProcessModule Model
        """
        return self.get(pk=id)
    
    def filter_by_company(self,id,company):
        """
        Return Multiple Objects by Process Id from ProcessModule Model
        """
        return self.filter(process_id=id,process__company=company)
    
    def getmodule_byprocess(self,process_id):
        return self.filter(process=process_id).select_related('module').values('id', 'process_id','module_id',module_name=F('module__module_name'))
    
    def getmodule_byid(self,id):
        return self.get(id=id)
    
    def create_process_module(self,process,module):
        return self.create(process=process,module=module)

class ProcessModule(models.Model):
    id = models.AutoField(primary_key=True)
    process = models.ForeignKey(Process,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProcessModuleManager()