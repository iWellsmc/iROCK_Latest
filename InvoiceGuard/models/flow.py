from django.db import models

# class Flow(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     start = models.BooleanField(default=False)
#     end = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

class FlowManager(models.Manager):

    def get_by_id(self,id):
        """
        Return Single Object by id from Flow Model
        """
        return self.get(pk=id)
    
    def filter_by_company(self,company,status,flow_name):
        """
        Return Multiple Objects by company,status and flow name from Flow Model
        """
        return self.filter(company=company,status=status,flow_name__icontains=flow_name)
    
    def get_company(self,company,status):
        """
        Return Multiple Objects by company and status from Flow Model
        """
        return self.filter(company=company,status=status)
    
    def filter_by_flow(self,flow_name,company):
        """
        Return Multiple Objects by flow name and company from Flow Model
        """
        return self.filter(flow_name__iexact=flow_name,company=company)
    
    def getallflows(self,company):
        return self.filter(company=company,status=1)
    
    def create_flow(self,flow,company):
        """
        Create flow
        """
        return self.create(flow_name=flow,company=company)

class Flow(models.Model):
    id = models.AutoField(primary_key=True)
    flow_name = models.CharField(max_length=100)
    company = models.ForeignKey('custom_auth.Companies', on_delete=models.CASCADE, null=True,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FlowManager()