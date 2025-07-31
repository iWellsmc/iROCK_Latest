from statistics import mode
from django.db import models
from django.forms import CharField
from custom_auth.models import Companies,User,Countries,States


class RoleManager(models.Manager):
    def getprojectdiscipline(self):
        return self.all()
    
    def get_discipline_byid(self,id):
        return self.get(id=id)


class ProjectDiscipline(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,verbose_name="Project Discipline",blank=True,null=True)
    objects=RoleManager()
    def __str__(self):
        return self.name

class ProjectDisciplineSubtype(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,verbose_name="Project Discipline Subtype",blank=True,null=True)
    project_discipline=models.ForeignKey("ProjectDiscipline",verbose_name="Project Discipline",on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.name

class DisciplineSubtypelist(models.Model):  
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    discipline_subtype=models.ForeignKey("ProjectDisciplineSubtype",verbose_name="Project Discipline Subtype",on_delete=models.CASCADE,blank=True, null=True)
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)

class ProjectDevelopmentType(models.Model):
    id=models.AutoField(primary_key=True)
    environment=models.ForeignKey("ProjectEnvironment",verbose_name="ProjectEnvironment",on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    development=models.ForeignKey("MasterDevelopmentType",verbose_name="Master DevelopmentType",on_delete=models.CASCADE,null=True,blank=True)
    cluster=models.ForeignKey("ProjectCluster",verbose_name="ProjectCluster",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)


class ProjectDevelopmentDisciplineManager(models.Manager):
    def getdevelopment_details(self,id):
        return self.get(id=id)
    


class ProjectDevelopmentDiscipline(models.Model):
    id=models.AutoField(primary_key=True)
    cluster=models.ForeignKey("ProjectCluster",verbose_name="ProjectCluster",on_delete=models.CASCADE,null=True,blank=True)
    project_discipline=models.CharField(max_length=255,verbose_name="Discipline",blank=True,null=True)
    development_type=models.ForeignKey("ProjectDevelopmentType",verbose_name="Development Type",on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=ProjectDevelopmentDisciplineManager()
#main

class ProjectDevelopmentSubTypeManager(models.Manager):
    def filter_by_project(self,project_id,status):
        return self.filter(project_id=project_id,status=status)
    def getdetails_byid(self,id):
        return self.get(id=id)
        
class ProjectDevelopmentSubType(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    project_discipline=models.ForeignKey("ProjectDevelopmentDiscipline",verbose_name="Project Development Discipline",on_delete=models.CASCADE,null=True,blank=True)
    discipline_subtype=models.ForeignKey("DisciplineSubtype",verbose_name="Discipline SubType",on_delete=models.CASCADE,blank=True,null=True)
    development_type=models.ForeignKey("ProjectDevelopmentType",verbose_name="Development Type",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)
    objects=ProjectDevelopmentSubTypeManager()

class DevelopmentSubSubType(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    discipline_subtype=models.ForeignKey("ProjectDevelopmentSubType",verbose_name="Development Type",on_delete=models.CASCADE,null=True,blank=True)
    disciplinesub_subtype=models.ForeignKey("DisciplineSubSubTypes",verbose_name="Discipline SubSubTypes",on_delete=models.CASCADE,null=True,blank=True)
    project_discipline=models.ForeignKey("ProjectDevelopmentDiscipline",verbose_name="Project Development Discipline",on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)

class DisciplineLastData(models.Manager):
    def filter_by_project(self,project_id,status):
        return self.filter(project_id=project_id,status=status)
    

class DevelopmentSubTypeSub(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projectcreation",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    disciplinesub_subtype=models.ForeignKey("DevelopmentSubSubType",verbose_name="Discipline SubType",on_delete=models.CASCADE,null=True,blank=True)
    sub_subtype_sub=models.ForeignKey("Subtypes",verbose_name="Subtypes",on_delete=models.CASCADE,null=True,blank=True)
    project_discipline=models.ForeignKey("ProjectDevelopmentDiscipline",verbose_name="Project Development Discipline",on_delete=models.CASCADE,null=True,blank=True)
    wellname=models.ForeignKey("ProjectWellName",verbose_name="ProjectWellName",on_delete=models.CASCADE,null=True,blank=True)
    objects= DisciplineLastData()
    other_type=models.ForeignKey("ProjectDevelopmentSubType",verbose_name="Development Type",on_delete=models.CASCADE,null=True,blank=True)
    discipline_type=models.CharField(max_length=255,verbose_name="Development Subtype",blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True, null=True,default=1)

class DisciplineSubSubtype(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,verbose_name="Discipline Sub Subtype",blank=True,null=True)
    discipline_subtype=models.ForeignKey("ProjectDisciplineSubtype",verbose_name="Project Discipline Subtype",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.name

class DisciplineSubSubtypeList(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    discipline_sub_subtype=models.ForeignKey("DisciplineSubSubtype",verbose_name="Discipline Sub Subtype",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class DevelopmentTypeManager(models.Manager):
    def getall_development_type(self):
        return self.all()
    def getall_development_byid(self,id):
        return self.get(id=id)

class DevelopmentType(models.Model):
    id=models.AutoField(primary_key=True)
    development_type=models.CharField(max_length=255,verbose_name="Development Type",blank=True,null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    objects=DevelopmentTypeManager()
    
    def __str__(self):
        return self.development_type

class DevelopmentTypeList(models.Model):
    id=models.AutoField(primary_key=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    development_type=models.ForeignKey("DevelopmentType",verbose_name="Development Type",on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class DisciplineSubtypeManager(models.Manager):
    def getdiscipline_bydevelopment(self,development_id):
        return self.filter(project_discipline_id=development_id).values()
    
    def filter_by_status(self,status):
        return self.filter(status=status)
    
    def get_discipline(self,name,status):
        return self.filter(discipline_subtype__iexact=name,status=status)
    
    def get_disciplinesubtype_byid(self,id):
        return self.get(id=id)

class DisciplineSubtype(models.Model):
    id=models.AutoField(primary_key=True)
    discipline_subtype=models.CharField(max_length=255,verbose_name="Discipline Subtype",blank=True,null=True)
    project_discipline=models.ForeignKey("ProjectDiscipline",verbose_name="Project Discipline",on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    objects=DisciplineSubtypeManager()
    def __str__(self):
        return self.discipline_subtype

class DisciplineSubtypeLists(models.Model):
    id=models.AutoField(primary_key=True)
    discipline_subtype=models.ForeignKey("DisciplineSubtype",verbose_name="Discipline Subtype",on_delete=models.CASCADE,null=True,blank=True)    
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False) 

class DisciplineSubSubTypes(models.Model):
    id=models.AutoField(primary_key=True)   
    discipline_subtype=models.ForeignKey("DisciplineSubtype",verbose_name="Discipline Subtype",on_delete=models.CASCADE,null=True,blank=True)
    sub_subtype_name=models.CharField(max_length=255,verbose_name="Sub Subtype",blank=True,null=True)    
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.sub_subtype_name

class DisciplineSubSubTypeslist(models.Model):
    id=models.AutoField(primary_key=True)
    sub_subtype=models.ForeignKey("DisciplineSubSubTypes",verbose_name="Discipline SubSubTypes",on_delete=models.CASCADE,null=True,blank=True)
    development_type=models.ForeignKey("DevelopmentType",verbose_name="Development Type",on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey("Projects",verbose_name="Projects",on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)

class Subtypes(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,verbose_name="Sub Types Subtype",blank=True,null=True)
    discipline_subtype=models.ForeignKey("DisciplineSubtype",verbose_name="Discipline Subtype",on_delete=models.CASCADE,null=True,blank=True)        
    status = models.IntegerField(blank=True, null=True,default=1)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name