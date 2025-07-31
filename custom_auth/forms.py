from django import forms
from custom_auth.models import Companies,User,UserDepartment
from django.contrib.auth import get_user_model

from django.forms import ModelForm, Field, ValidationError, BooleanField, CharField
from django.forms.widgets import CheckboxInput, Select

class LoginForm(forms.Form):
    cin=forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(forms.ModelForm):
    """user signup form"""
    password = forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(SignupForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['password'].required = False

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password',)

class AdminLoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class Usercreationform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Usercreationform, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label 
            self.fields['phone_countrycode'].required = False

    class Meta:
        model=User
        fields= ['phone_number_extenstion','Title','areacode','name','lastname','email','phone','mobile','designation_role','phone_countrycode','mobile_countrycode','signature_fontname','signature_fontfamily'] 
        widgets={'password':forms.PasswordInput(),'company':forms.HiddenInput(),'is_active':forms.HiddenInput(),'is_staff':forms.HiddenInput()}
        

class EnquiryFrom(forms.Form):

    title = forms.ChoiceField(widget = forms.Select({'class':'form-control titlecls'}),choices = ([("","Select"), ("Mr", "Mr"),("Mr", "Mrs"),("Ms", "Ms"), ]), initial='Select', required = True,)
    companyname=forms.CharField(label='Name',max_length=200, 
                    widget=forms.TextInput(attrs={'placeholder': 'Name','class':'form-control comcls'}))
    email=forms.EmailField(label='Email',max_length=50, 
                    widget=forms.TextInput(attrs={'placeholder': 'Email','class':'form-control mailcls'}))
    # message=forms.CharField(label='Message',widget=forms.Textarea({'class':'msgcls'}))
    
    # def __init__(self, *args, **kwargs):
    #     super(EnquiryFrom, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         # print(visible)
    #         visible.field.widget.attrs['class'] = 'form-control'

# class UserDepartmentForm(forms.Form):
#     company=forms.ModelChoiceField(queryset=Companies.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
#     department=forms.CharField(label='Department',max_length=255, 
#                     widget=forms.TextInput(attrs={'placeholder': 'Department','class':'form-control'}))
#     status=forms.BooleanField(label='Status',required=False,widget=forms.CheckboxInput(attrs={'class':'form-control'}))

# class UserDepartmentForm(forms.ModelForm):
#     class Meta:
#         model = UserDepartment
#         fields = ('company','department','status')
#         widgets = {
#             'company': forms.Select(attrs={'class':'form-control'}),
#             'department': forms.TextInput(attrs={'placeholder': 'Department','class':'form-control'}),
#             'status': forms.CheckboxInput(attrs={'class':'form-control'}),
#         }

# UserDepartmentFormSet = forms.modelformset_factory(UserDepartment, form=UserDepartmentForm, extra=1)


class UserDepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(UserDepartmentForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['company'].initial = request.company.id
    
    class Meta:
        model = UserDepartment
        fields = ('company', 'department', 'status')
        labels = {
            'department': '',
        }
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        # exclude the company field from the widget definition since we are setting its value programmatically
        exclude = ('company','status')

UserDepartmentFormSet = forms.modelformset_factory(UserDepartment, form=UserDepartmentForm, extra=1)