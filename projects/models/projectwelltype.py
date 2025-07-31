from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States

class ProjectWellTypeManager(models.Manager):
    def get_by_discipline(self,project_id,discipline_type,status):
        return self.get(project_id=project_id,discipline_type_id=discipline_type,status=status)
    def filter_by_discipline(self,project_id,discipline_type,status):
        return self.filter(project_id=project_id,discipline_type_id=discipline_type,status=status)
    
class ProjectWellType(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    project_discipline=models.ForeignKey("ProjectDevelopmentDiscipline",verbose_name="Project Development Discipline",on_delete=models.CASCADE,null=True,blank=True)
    discipline_type=models.ForeignKey("ProjectDevelopmentSubType",verbose_name="ProjectDevelopmentSubType",on_delete=models.CASCADE,null=True,blank=True)
    welltype=models.ForeignKey("Well",verbose_name="Well Name",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=ProjectWellTypeManager()

class ProjectWellNameManager(models.Manager):
    def filter_by_project(self,project_id,status):
        return self.filter(project_id=project_id,status=status)
    
    def filter_by_well_type(self,project_id,well_type,status):
        return self.filter(project_id=project_id,welltype_id=well_type,status=status)

class ProjectWellName(models.Model):
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    id=models.AutoField(primary_key=True)
    project_discipline=models.ForeignKey("ProjectDevelopmentDiscipline",verbose_name="Project Development Discipline",on_delete=models.CASCADE,null=True,blank=True)
    welltype=models.ForeignKey("ProjectWelltype",verbose_name="ProjectWelltype",on_delete=models.CASCADE,null=True,blank=True)
    wellname=models.ForeignKey("WellSub",verbose_name="WellSub",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=ProjectWellNameManager()

class Well(models.Model):
    id=models.AutoField(primary_key=True)
    well_name=models.CharField(max_length=255,verbose_name="Well Name",blank=True,null=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    development_type=models.ForeignKey("MasterDevelopmentType",verbose_name="Master DevelopmentType",on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    
    def __str__(self):
        return self.well_name


class WellSub(models.Model):
    id=models.AutoField(primary_key=True)
    well_subname=models.CharField(max_length=255,verbose_name="Well Name",blank=True,null=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    well=models.ForeignKey("Well",verbose_name="Well Name",on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.well_subname 