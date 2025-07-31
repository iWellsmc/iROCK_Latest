from django import forms 
from custom_auth.models import Countries,User
from projects.models import Projectcreation,DisciplineSubtypelist,ProjectDiscipline, ProjectType,Projects,ProjectDisciplineSubtype,ProjectType,ProjectTypeCompany,DisciplineSubSubtype,DisciplineSubSubtypeList,DevelopmentType,DevelopmentTypeList,DisciplineSubtype,DisciplineSubtypeLists,DisciplineSubSubTypeslist


class Usercreation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Usercreation, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label  

    class Meta:
        model=User
        fields= ['phone_number_extenstion','Title','areacode','name','lastname','email','phone','mobile','designation_role','phone_countrycode','mobile_countrycode','user_department','user_group'] 
        widgets={'password':forms.PasswordInput(),'company':forms.HiddenInput(),'is_active':forms.HiddenInput(),'is_staff':forms.HiddenInput()}


class ProjectForm(forms.ModelForm):
    country=forms.ModelChoiceField(widget=forms.Select,queryset=Countries.objects.all(),empty_label="---Select Country---")
    project_discipline=forms.ModelChoiceField(widget=forms.Select,queryset=ProjectDiscipline.objects.all(),empty_label="---Select Discipline---")
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)  

    class Meta:
        model=Projects
        fields= "__all__"  
        widgets={'company':forms.HiddenInput(),'status':forms.HiddenInput(),'project_environment_subtype':forms.HiddenInput()}

class ProjectCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectCreationForm, self).__init__(*args, **kwargs)  

    class Meta:
        model=Projectcreation
        fields= "__all__"  
        widgets={'company':forms.HiddenInput(),'status':forms.HiddenInput()}


  #del#
class DisciplineSubtypelistForm(forms.ModelForm):  
    discipline_subtype=forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple,queryset=ProjectDisciplineSubtype.objects.all(),initial="")
    def __init__(self, *args, **kwargs):
        super(DisciplineSubtypelistForm, self).__init__(*args, **kwargs)
    class Meta:  
        model = DisciplineSubtypelist  
        fields = "__all__"
        widget={'projects':forms.HiddenInput(),'status':forms.HiddenInput()}

#del#
class DisciplineSubSubTypeListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisciplineSubSubTypeListForm, self).__init__(*args, **kwargs)

    class Meta:
        model=DisciplineSubSubtypeList
        fields= "__all__"
        widget={'projects':forms.HiddenInput(),'status':forms.HiddenInput()}

###development form ###
class DevelopmentTypeListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DevelopmentTypeListForm, self).__init__(*args, **kwargs)

    class Meta:
        model=DevelopmentTypeList
        fields= "__all__"
        widget={'project':forms.HiddenInput(),'status':forms.HiddenInput()}

### DisciplineSubtypeLists form ##
class DisciplineSubtypeListsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisciplineSubtypeListsForm, self).__init__(*args, **kwargs)   
    class Meta:
        model = DisciplineSubtype
        fields = "__all__"
        widget={'project':forms.HiddenInput(),'status':forms.HiddenInput()} 

## Discipline sub subtye list form ##
class DisciplineSubSubTypeslistForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisciplineSubSubTypeslistForm, self).__init__(*args, **kwargs)  
    class Meta:
        model = DisciplineSubSubTypeslist
        fields = "__all__"
        widget={'project':forms.HiddenInput(),'status':forms.HiddenInput(),"development_type":forms.HiddenInput()} 
