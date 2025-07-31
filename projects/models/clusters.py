from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States
#muliple field cluster #
class Clusters(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    field_environment=models.ForeignKey("FieldEnvironment",verbose_name="Field Environment",on_delete=models.CASCADE,null=True,blank=True)
    cluster_name=models.CharField(max_length=255,verbose_name="Cluster Name",null=True,blank=True)
    status = models.IntegerField(blank=True,default=1)
    def __str__(self):
        return self.cluster_name

# multiple cluster sub name #
class ClusterSubnames(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    cluster=models.ForeignKey("Clusters",verbose_name="Cluster Name",on_delete=models.CASCADE,null=True,blank=True)
    cluster_subname=models.CharField(max_length=255,verbose_name="Cluster SubName",null=True,blank=True)
    status = models.IntegerField(blank=True,default=1)
    def __str__(self):
        return self.cluster_subname

class MasterDevelopmentType(models.Model):
    id=models.AutoField(primary_key=True)
    clustersubname=models.ForeignKey("ClusterSubnames",verbose_name="Cluster Subnames",on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    development_type=models.CharField(max_length=255,verbose_name="Cluster SubName",null=True,blank=True)
    status = models.IntegerField(blank=True,default=1)
    def __str__(self):
        return self.development_type

class ProjectClusterManager(models.Manager):
    def filter_by_project(self,project_id,status):
        return self.filter(project_id=project_id,status=status)
    
class ProjectCluster(models.Model):
    id=models.AutoField(primary_key=True)
    field=models.ForeignKey("ProjectField",verbose_name="Project Field",on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    environment=models.ForeignKey("ProjectEnvironment",verbose_name="ProjectEnvironment",on_delete=models.CASCADE,null=True,blank=True)
    clustersubname=models.ForeignKey("ClusterSubnames",verbose_name="Cluster Subnames",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=ProjectClusterManager()