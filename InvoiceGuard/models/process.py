from django.db import models

class ProcessManager(models.Manager):

    def get_by_id(self,id):
        """
        Retun Single object by ID from Process Model
        """
        return self.get(pk=id)

    def company_process(self,company):
        """
        Return Company related Process Queryset 
        """
        return self.filter(company=company)
    
    def process_and_company(self,process,company):
        """
        Return Company related Process Queryset 
        """
        return self.filter(process_name__iexact=process,company=company)
    def search_by_process(self,company,process):
        """
        Return Process related Search 
        """
        return self.filter(company=company,process_name__icontains=process)
    
    def create_process(self,process,company):
        """
        Creating Process  
        """
        return self.create(process_name=process,company=company)

class Process(models.Model):
    id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=100)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProcessManager()