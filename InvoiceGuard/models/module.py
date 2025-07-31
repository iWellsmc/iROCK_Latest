from django.db import models

class ModuleManager(models.Manager):
    def get_by_id(self, module_id):
        """
        Return Sigle Object by ID from Module Model
        """
        return self.get(id=module_id)
    
    def get_all_module(self):
        """
        Retun all Objects from Module Model
        """
        return self.all()
    
    def module_count(self):
        """ 
        Return Count of Module Model
        """
        return self.count()
    
    def get_by_processID(self,process_id):
        """ 
        Return Process of Module Model
        """
        return self.filter(processmodule__process_id=process_id)
    
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=ModuleManager()

    def __str__(self):
        return self.module_name