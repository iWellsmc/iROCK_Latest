from django.db import models
from .flow import Flow
from .process import Process
from django.db.models import F

# Create your models here.

class FlowProcessManager(models.Manager):

    def get_by_id(self,id):
        """
        Return Single Object by id from FlowProcess Model
        """
        return self.get(pk=id)
    
    def get_by_company(self,id,company):
        """
        Return Multiple Objects by company from FlowProcess Model
        """
        return self.filter(flow_id=id,flow__company=company)
    
    def getprocess_byflow(self,flow_id):
        return self.filter(flow_id=flow_id).select_related('process').values('id', 'process_id',process_name=F('process__process_name'))
    
    def create_flow_process(self,flow,process):
        """
        Create FlowProcess
        """
        return self.create(flow=flow,process=process)

class FlowProcess(models.Model):
    id = models.AutoField(primary_key=True)
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, null=True,blank=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True,blank=True)
    process_order = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FlowProcessManager()
    def __str__(self):
        return self.flow.flow_name