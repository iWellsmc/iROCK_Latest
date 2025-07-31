from django.db import models
from django.db.models import Q

class WccFlowManager(models.Manager):
    def filter_by_project(self,project_id):
      return self.filter(project_id=project_id)
    
    def get_by_project(self,project_id):
      return self.get(project_id=project_id)
    
    def create_flow(self,project_id,level_type,company):
      data=self.create(project_id=project_id,level_type=level_type,company=company)
      return data
    def update_data_project(self,pk,level_type):
      data=WccFlow.objects.filter(id=pk).update(level_type=level_type)
      return data


class WccFlow(models.Model):
    id = models.AutoField(primary_key=True)
    project=models.ForeignKey("projects.Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    level_type=models.CharField(max_length=255,verbose_name="Level Type", blank=True, null=True)
    # discipline=models.ForeignKey("projects.DevelopmentSubTypeSub",verbose_name="Discipline",on_delete=models.CASCADE,null=True,blank=True)
    # cluster=models.ForeignKey("projects.ProjectCluster",verbose_name="Cluster",on_delete=models.CASCADE,null=True,blank=True)
    # well=models.ForeignKey("projects.ProjectWellName",verbose_name="Well",on_delete=models.CASCADE,null=True,blank=True)
    # station=models.CharField(max_length=100,verbose_name="Station", blank=True, null=True)
    # status=models.BooleanField(blank=True, null=True,default=0)
    # # status 1 = submitted,status 2 = delete,status 0 = draft
    # wcc_status_date=models.DateTimeField(editable=True,blank=True, null=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    objects=WccFlowManager()

class WccFlowLevelManager(models.Manager):
    def filter_by_project(self,project_id):
        return self.filter(project_id=project_id)
    
    def filter_wcc_level(self,level_type,level_id,wcc_flow_id,status):
      if (level_type == "discipline"):
        data=self.filter(wcc_flow_id=wcc_flow_id,discipline_id=level_id,status=status,well_based=0)
      elif (level_type == "cluster"):
         data=self.filter(wcc_flow_id=wcc_flow_id,cluster_id=level_id,status=status)
      else:
         data=self.filter(wcc_flow_id=wcc_flow_id,well_id=level_id,status=status)
      return data
    
    def filter_wcc_levelbased(self,level_id,wcc_flow_id,status):
      return self.filter(wcc_flow_id=wcc_flow_id,discipline_id=level_id,status=status,well_based=1)
    
    def check_wcc_levelbased(self,level_id,wcc_flow_id):
      return self.filter(wcc_flow_id=wcc_flow_id,discipline_id=level_id,well_based=1)
    
    def check_wcc_level(self,level_type,level_id,wcc_flow_id):
      if (level_type == "discipline"):
        data=self.filter(wcc_flow_id=wcc_flow_id,discipline_id=level_id,well_based=0)
      elif (level_type == "cluster"):
         data=self.filter(wcc_flow_id=wcc_flow_id,cluster_id=level_id)
      else:
         data=self.filter(wcc_flow_id=wcc_flow_id,well_id=level_id)
      return data
    
    def update_levelbased(self,level_id,wcc_flow_id,station):
      return self.filter(wcc_flow_id=wcc_flow_id,discipline_id=level_id,well_based=1).update(station=station,status=1)
        
    def update_wcc_flowlevel(self,level_id,wcc_flow_id,station,level_type):
      if (level_type == 'discipline'):
        data=self.filter(wcc_flow_id=wcc_flow_id,discipline_id=level_id).update(station=station,status=1)
      elif (level_type == "cluster"):
        data=self.filter(wcc_flow_id=wcc_flow_id,cluster_id=level_id).update(station=station,status=1)
      else:
        data=self.filter(wcc_flow_id=wcc_flow_id,well_id=level_id).update(station=station,status=1)
      return data
    
    def update_all_well_based(self,wcc_flow_id,flow_level_list):
      return self.filter(wcc_flow_id=wcc_flow_id,well_based=1).exclude(id__in=flow_level_list).update(status=0)
    
    def update_all_flow_level(self,wcc_flow_id,flow_level_list):
      return self.filter(wcc_flow_id=wcc_flow_id).exclude(well_based=1).exclude(id__in=flow_level_list).update(status=0)
    
    def create_well_based_data(self,company,project_id,wcc_flow,level,station):
      data=self.create(company=company,project_id=project_id,wcc_flow=wcc_flow,station=station,discipline_id=level,well_based=1) 
      return data
    
    def create_flow_level(self,company,project_id,wcc_flow,level_type,level,station):
      if (level_type == 'discipline'):
        data=self.create(company=company,project_id=project_id,wcc_flow=wcc_flow,station=station,discipline_id=level) 
      elif (level_type == "cluster"):
        data=self.create(company=company,project_id=project_id,wcc_flow=wcc_flow,station=station,cluster_id=level) 
      else:
        data=self.create(company=company,project_id=project_id,wcc_flow=wcc_flow,station=station,well_id=level) 
      return data
    
    
class WccFlowLevel(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    project=models.ForeignKey("projects.Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    wcc_flow=models.ForeignKey("WccFlow",verbose_name="Wcc Flow",on_delete=models.CASCADE,null=True,blank=True)
    discipline=models.ForeignKey("projects.ProjectDevelopmentSubType",verbose_name="Discipline",on_delete=models.CASCADE,null=True,blank=True)
    cluster=models.ForeignKey("projects.ProjectCluster",verbose_name="Cluster",on_delete=models.CASCADE,null=True,blank=True)
    well=models.ForeignKey("projects.ProjectWellName",verbose_name="Well",on_delete=models.CASCADE,null=True,blank=True)
    station=models.CharField(max_length=100,verbose_name="Station", blank=True, null=True)
    well_based=models.IntegerField(blank=True, null=True,default=0)
    status=models.BooleanField(blank=True, null=True,default=1)
    objects=WccFlowLevelManager()

class WccPerStationManager(models.Manager):
    def filter_by_status(self,status,company):
      return self.filter(status=status,company_id=company)
    
    def filter_by_wcc(self,status,wcc):
      return self.filter(status=status,wcc_flow=wcc)
    
    def filter_by_project(self,project_id,status):
      return self.filter(status=status,project_id=project_id)
    
    def filter_by_station(self,station_id,status=1):
       return self.filter(id=station_id,status=status)

    def update_per_station(self,station_id,per_station):
       return self.filter(id=station_id).update(station_user=per_station)
    
    def get_by_id(self,station_id):
       return self.get(id=station_id)
    
    def get_next_data(self,station_id,wcc_flow_level_id ):
       return self.filter(id__gt=station_id,wcc_flow_level_id=wcc_flow_level_id )

    def create_wcc_per_station(self,wcc_flow_level,station_user,wcc_flow,project_id,user_role):
      return self.create(wcc_flow_level_id=wcc_flow_level,station_user=station_user,wcc_flow=wcc_flow,project_id=project_id,role_id=user_role)
    
    def edit_station(self,wcc_flow_id,station_list):
      return self.filter(wcc_flow_id=wcc_flow_id).exclude(id__in=station_list).update(status=0)
    
    def filter_by_flow_level(self,flow_level_id,status):
       return self.filter(wcc_flow_level_id=flow_level_id,status=status)
    
    def filter_by_flow_level_wcc(self,wcc_id,flow_level_id,status):
       return self.filter(wcc_id=wcc_id,wcc_flow_level_id=flow_level_id,status=status)
    
    def update_wcc_per_station(self,pk,station_user,user_role):
      return self.filter(id=pk).update(station_user=station_user,role_id=user_role) 
    
    def update_all_per_station(self,wcc_flow_id,flow_level_id,per_station_list):
      return self.filter(wcc_flow_id=wcc_flow_id,wcc_flow_level_id=flow_level_id).exclude(id__in=per_station_list).update(status=0) 

class WccPerStation(models.Model):
    id = models.AutoField(primary_key=True)
    project=models.ForeignKey("projects.Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    wcc_flow=models.ForeignKey("WccFlow",verbose_name="Wcc Flow",on_delete=models.CASCADE,null=True,blank=True)
    wcc_flow_level=models.ForeignKey("WccFlowLevel",verbose_name="Wcc FloLevel",on_delete=models.CASCADE,null=True,blank=True)
    station_user=models.CharField(max_length=100,verbose_name="Station User", blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    role = models.ForeignKey("InvoiceGuard.Role", on_delete=models.CASCADE,null=True,blank=True)
    objects=WccPerStationManager()

class WccStationUsersManager(models.Manager):
    def filter_by_user(self,user,status):
      return self.filter(user_id=user,status=status)
    
    def check_by_user(self,station_id,user):
      return self.filter(wcc_per_station_id=station_id,user_id=user)
    
    def update_user_status(self,station_id,user):
      return self.filter(wcc_per_station_id=station_id,user_id=user).update(status=1)
    
    def edit_station_users(self,station_id,userlist):
       return self.filter(wcc_per_station_id=station_id).exclude(id__in=userlist).update(status=0)
    
    def filter_by_station(self,station_id,status):
      return self.filter(wcc_per_station_id=station_id,status=status)
    
    def get_by_id(self,user):
      return self.get(user_id=user)
    
    def create_wcc_station_user(self,user_id,station_id,wcc_flow,project_id,wcc_flow_level):
      return self.create(user_id=user_id,wcc_per_station_id=station_id,wcc_flow_id=wcc_flow,project_id=project_id,wcc_flow_level_id=wcc_flow_level)
    
    def update_other_status(self,wcc_flow_id,flow_level_id,station_list):
       return self.filter(wcc_flow_id=wcc_flow_id,wcc_flow_level_id=flow_level_id).exclude(wcc_per_station_id__in=station_list).update(status=0)
       
class WccStationUsers(models.Model):
    id = models.AutoField(primary_key=True)
    project=models.ForeignKey("projects.Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    wcc_flow=models.ForeignKey("WccFlow",verbose_name="Wcc Flow",on_delete=models.CASCADE,null=True,blank=True)
    wcc_flow_level=models.ForeignKey("WccFlowLevel",verbose_name="Wcc FloLevel",on_delete=models.CASCADE,null=True,blank=True)
    wcc_per_station=models.ForeignKey("WccPerStation",verbose_name="wcc Per Station",on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    objects=WccStationUsersManager()

class WccExceptional(models.Model):
    id = models.AutoField(primary_key=True)
    wcc=models.ForeignKey("WorkCompletionCost",on_delete=models.CASCADE,blank=True, null=True)
    exceptional_type = models.IntegerField(blank=True, null=True)
    status=models.IntegerField(blank=True, null=True,default=1)
    confirm_dispute=models.IntegerField(blank=True, null=True,default=0)
    checked_messages=models.TextField(blank=True, null=True,default=0)
    return_status=models.IntegerField(blank=True, null=True,default=0)

