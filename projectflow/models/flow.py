from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
from django.db.models import F


class ProjectFlowlevelManager(models.Manager):
    def createprojectflowlevel(self,project_id,level_id,no_of_stations,process_id,company,flow_level,flow):
        return self.create(project_id=project_id,process_id=process_id,no_of_stations=no_of_stations,company=company,level_id=level_id,flow_level=flow_level,flow_id=flow)
    
    def createprojectflowlevelwellbased(self,project_id,level_id,no_of_stations,process_id,company,flow_level,flow):
        return self.create(project_id=project_id,process_id=process_id,no_of_stations=no_of_stations,company=company,level_id=level_id,flow_level=flow_level,flow_id=flow,well_based=1)
    

    def getprojectflowlevel_by_project_id(self,project_id):
        return self.filter(project_id=project_id,status=1)
    
    def get_by_level_main(self,level_id,level_type,comapny,project_id):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,status=1)
    
    def getprojectflowlevel(self,process_id,level_id,project_id):
        return self.filter(process_id=process_id,level_id=level_id,project_id=project_id,status=1).first()
    
    def checklevel(self,level_id,flow_level,project_id):
        projectflowlevel=self.filter(project_id=project_id,level_id=level_id,flow_level=flow_level,status=1,well_based=0)
        return projectflowlevel
    
    def checkwellbasedlevel(self,level_id,flow_level,project_id):
        projectflowlevel=self.filter(project_id=project_id,level_id=level_id,flow_level=flow_level,well_based=1,status=1)
        return projectflowlevel

    def updateprojectflowlevel(self,projectflow_level_id,no_of_stations):
        return self.filter(id=projectflow_level_id).update(no_of_stations=no_of_stations)

    def getprojectflow_bylevel(self,level_id,level_type,comapny,project_id,process):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,status=1,process_id=process).first()
    
    def filterprojectflow_bylevel(self,level_id,level_type,comapny,project_id,flow):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,flow_id=flow,status=1)

    def projectflow_bylevel_main(self,level_id,level_type,comapny,project_id):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,status=1).first()
        
    #wellbased discipline
    def filterprojectflow_bylevelwellbased(self,level_id,level_type,comapny,project_id,flow):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,flow_id=flow,well_based=1,status=1)
    # def getprojectflow_bywellbasedlevel(self,level_id,level_type,comapny,project_id):
    #     return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,well_based=1).first()
    
    def projectflow_bywellbasedlevel_main(self,level_id,level_type,comapny,project_id):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,status=1,well_based=1).first()
    
    def get_by_wellbasedlevel_main(self,level_id,level_type,comapny,project_id):
        return self.filter(level_id=level_id,company=comapny,flow_level=level_type,project_id=project_id,status=1,well_based=1)
    
    def deleteprojectlevel_by_levelid(self,level_id,company,project_id):
        return self.filter(id=level_id,project_id=project_id,company=company).delete()
    
    # def updateprojectlevel_by_levelid(self,level_id,no_of_stations):
    #     return self.filter(id=level_id).update(no_of_stations=no_of_stations,status=1)
    
    def updateprojectlevel_by_levelid(self,level_id,process_data,no_of_stations):
        return self.filter(id=level_id,process_id=process_data).update(no_of_stations=no_of_stations,status=1)
    
    def updateprojectlevel_by_level_wellbased_id(self,level_id,process_data,no_of_stations):
        return self.filter(id=level_id,process_id=process_data,well_based=1).update(no_of_stations=no_of_stations,status=1)
    
    def filter_id_process(self,flow_level,process_data):
        return self.filter(id=flow_level,process_id=process_data)
    
    def filter_id_process_wellbased(self,flow_level,process_data):
        return self.filter(id=flow_level,process_id=process_data,well_based=1)

    def remove_level_status(self,company,pk,project_level_list,flow):
        # print('remove_level_status',project_level_list)
        return self.filter(company=company,project_id=pk,well_based=0).exclude(id__in=project_level_list).update(status=0)
    
    def remove_level_wellbased_status(self,company,pk,project_level_list,flow):
        return self.filter(company=company,project_id=pk,well_based=1).exclude(id__in=project_level_list).update(status=0)
    
    def update_flow_level_name(self,pk,flow_name):
        return self.filter(project_id=pk).exclude(flow_level=flow_name).update(status=0)
    
    def update_flow_level_name_wellbased(self,pk,flow_name):
        return self.filter(project_id=pk).exclude(flow_level=flow_name).update(status=0)
    
class ProjectFlowlevel(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    project=models.ForeignKey("projects.Projectcreation",on_delete=models.CASCADE,blank=True, null=True)
    level_id=models.IntegerField(blank=True, null=True) #cluster id or discipline id or well id based on level selection in flow creation
    process=models.ForeignKey("InvoiceGuard.FlowProcess",on_delete=models.CASCADE,blank=True, null=True)
    no_of_stations=models.IntegerField(blank=True, null=True)
    flow_level=models.CharField(max_length=30,verbose_name="Levels", blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    well_based=models.IntegerField(blank=True, null=True,default=0)# this field used for data involved with well discipline ,1 = well discipline,0=not well discipine 
    flow=models.ForeignKey("InvoiceGuard.Flow",on_delete=models.CASCADE,blank=True, null=True)
    objects=ProjectFlowlevelManager()
    # created = models.DateTimeField(auto_now_add=True, editable=False)

class ProjectFlowModulesManager(models.Manager):
    def createprojectflowmodules(self,no_of_users,company,module_id,project_id,projectflow_level,role_id):
        return self.create(project_id=project_id,no_of_users=no_of_users,module_id=module_id,company=company,projectflow_level=projectflow_level,role_id=role_id)
    
    def getprojectmodules_by_levelid(self,project_flow_id,offset):
        projectmodules=self.filter(projectflow_level_id=project_flow_id,status=0).order_by('id')[offset:offset+1].first()
        return projectmodules

    def deleteprojectmodules_by_levelid(self,level_id,company,project_id):
        return self.filter(projectflow_level_id=level_id,project_id=project_id,company=company).delete()

    def getprojectmodules_by_level_module_role(self,project_flow_id,module_id,role_id):
        projectmodules=self.filter(projectflow_level_id=project_flow_id,module_id=module_id,role_id=role_id,status=0).first()
        return projectmodules
    
    
    def updateprojectflowmodules(self,no_of_users,module_id,role_id,projectflow_module_id):
        return self.filter(id=projectflow_module_id).update(no_of_users=no_of_users,module_id=module_id,role_id=role_id)
    
    def getactiveflow_level(self,id):
        projectmodules=self.filter(projectflow_level_id=id,status=0).first()
        return projectmodules
     
    def getnextactivelevel(self,flowlevel_id,flowmodule_id):
        projectmodules=self.filter(projectflow_level_id=flowlevel_id,id__gt=flowmodule_id,status=0).order_by('id').first()
        return projectmodules
    
    def getnxtprocessactlevel(self,flowlevel_id,project_id,level_id):
        projectmodules=self.filter(projectflow_level__level_id=level_id,project_id=project_id).filter(projectflow_level_id__gt=flowlevel_id,status=0).order_by('id').first()
        return projectmodules
    
    def getallactiveflow_level(self,id):
        projectmodules=self.filter(projectflow_level_id=id,status=0)
        return projectmodules

    def getallactiveflow_level_mul_id(self,id):
        projectmodules=self.filter(projectflow_level_id__in=id,status=0)
        return projectmodules
    
    def update_projectflowmodules(self,flow_level,projectflowmodule_id,module_id,no_of_users,role_id):
        return self.filter(projectflow_level=flow_level,id=projectflowmodule_id).update(module_id=module_id,no_of_users=no_of_users,role_id=role_id,status=0)  
    
    def get_project_flowmodule(self,flow_level,projectflowmodule_id):
        return self.get(projectflow_level_id=flow_level,id=projectflowmodule_id,status=0)
    
    def remove_modules_status(self,flow_level,project_module_list):
        self.filter(projectflow_level=flow_level).exclude(id__in=project_module_list).update(status=1)

    def get_data_ids(self,project_flow_ids):
        return self.filter(id__in=project_flow_ids,status=0)
    
    def getprojectflow_modules_byprojectid(self,project_id):
        return self.filter(project_id=project_id,status=0)


class ProjectFlowModules(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    project=models.ForeignKey("projects.Projectcreation",on_delete=models.CASCADE,blank=True, null=True)
    projectflow_level=models.ForeignKey("ProjectFlowlevel",on_delete=models.CASCADE,blank=True, null=True)
    module=models.ForeignKey("InvoiceGuard.ProcessModule",on_delete=models.CASCADE,blank=True, null=True)
    no_of_users=models.IntegerField(blank=True, null=True)
    role=models.ForeignKey("InvoiceGuard.Role",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=0)
    objects=ProjectFlowModulesManager()


class ProjectFlowModuleUsersManager(models.Manager):
    def createProjectFlowModuleUsers(self,project_flow_modules,company,user_id,project_id,projectflowlevel_id):
        return self.create(project_id=project_id,ProjectFlowModules=project_flow_modules,company=company,user_id=user_id,projectflow_level=projectflowlevel_id)
    
    def getflowusers(self,flowmodule_id,offset):
        return self.filter(ProjectFlowModules_id=flowmodule_id,status=0).order_by('id')[offset:offset+1].first()
    
    def deleteprojectflowusers_by_levelid(self,level_id,company,project_id):
        return self.filter(projectflow_level_id=level_id,project_id=project_id,company=company).delete()
    
    def getflowusers_by_user_module(self,flowmodule_id,user_id,projectflowlevel_id):
        return self.filter(ProjectFlowModules_id=flowmodule_id,user_id=user_id,projectflow_level_id=projectflowlevel_id,status=0).first()
    
    def getflowusers_by_user(self,flowmodule_id,user_id,projectflowlevel_id):
        return self.filter(ProjectFlowModules_id=flowmodule_id,user_id=user_id,projectflow_level_id=projectflowlevel_id)
    
    def getflowusers_active(self,id,projectflowlevel_id):
        return self.filter(ProjectFlowModules_id=id,projectflow_level_id=projectflowlevel_id,status=0)
    
    def update_user_status(self,flowmodule_id,user_id,projectflowlevel_id):
        return self.filter(ProjectFlowModules_id=flowmodule_id,user_id=user_id,projectflow_level_id=projectflowlevel_id).update(status=0)

    def remove_users_status(self,flowmodule_id,projectflowlevel_id,users_list):
        return self.filter(ProjectFlowModules_id=flowmodule_id,projectflow_level_id=projectflowlevel_id).exclude(id__in=users_list).update(status=1)

    def remove_users_flowlevel(self,flow_level,project_module_list):
        return self.filter(projectflow_level_id=flow_level).exclude(ProjectFlowModules_id__in=project_module_list).update(status=1)
    
    def get_data_user_ids(self,user_id_list):
        ## single user id in project user list
        return self.filter(user_id__in=user_id_list,status=0)
    
    def getusers_bymodule_id(self,flow_module_id):
        query=self.filter(ProjectFlowModules_id=flow_module_id,status=0)
        # print(f"{query.query}")
        return query


class ProjectFlowModuleUsers(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    project=models.ForeignKey("projects.Projectcreation",on_delete=models.CASCADE,blank=True, null=True)
    ProjectFlowModules=models.ForeignKey("ProjectFlowModules",on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("projects.ProjectUser",on_delete=models.CASCADE,blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=0)
    projectflow_level=models.ForeignKey("ProjectFlowlevel",on_delete=models.CASCADE,blank=True, null=True)
    objects=ProjectFlowModuleUsersManager()
    # created = models.DateTimeField(auto_now_add=True, editable=False)







   