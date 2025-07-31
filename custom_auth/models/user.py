
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy  as _
from django.db.models import Q
class CustomUserManager(BaseUserManager):
    """custom user manager class"""
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        print(self)
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def getUser(self,user_id):
        return self.filter(id=user_id,status=1).first()
    
    def get_by_company(self,company,roles,status):
        """
        Return Multiple Objects of company and roles in User Model
        """
        return self.filter(company=company,roles__in=roles,status=status)
    
    def get_by_id(self,id):
        """
        Return Single Object of id in User Model
        """
        return self.get(id=id)
    
    def getbankusers(self,id):
         """
        Return Single Object of Bankusers in User Model
        """
         return self.filter(bankuser=id,bankuserstatus=1)
    
    def filter_by_userid(self,id):
        """
        Return Single Object of id in User Model
        """
        return self.filter(id__in=id)

    def update_users_byid(self,userid,firstname,lastname,email,designation):
        """
        Update Multiple Object of User Details in User Model
        """
        return self.filter(id=userid).update(name=firstname,lastname=lastname,email=email,designation_role=designation)
    
    def search_by_user(company,name):
        """
        Return user related Search 
        """
        return filter(company=company,roles_id=3),Q(name__icontains=name) | Q(lastname__icontains=name)
    
    def update_previous_login_date(self,user_id,current_timestamp):
        self.filter(id=user_id).update(previous_login_date=current_timestamp)
    
    def update_login_date(self,user_id,previous_login_date):
        self.filter(id=user_id).update(login_date=previous_login_date)
    
    def getclientadmin_by_companyid(self,company_id):
        queryset=self.get(company_id=company_id,roles_id=2)
        print(f"queryset {queryset}")
        return queryset
    
    def getusers_by_cin(self,cin):
        return self.filter(cin_number=cin,status=1,is_active=1)
        


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model class"""
    id = models.AutoField(primary_key=True)
    hidden_username=models.CharField(_('Hidden User Name'),unique=True, max_length=50, blank=True, null=True)
    email = models.EmailField(_('email'),default='')
    Title = models.CharField(_('Title'), max_length=10, blank=True,null=True)
    name = models.CharField(_('first Name'), max_length=50, blank=False)
    areacode=models.CharField(_('Area Code'), max_length=50,blank=True, null=True)
    phone = models.CharField(_('Official Phone Number (Land Line)'), max_length=50, blank=True, null=True)
    phone_countrycode = models.CharField(_('Country Code'), max_length=50, blank=True,null=True)
    mobile_countrycode = models.CharField(_('Country Code'), max_length=50, blank=True,null=True)
    mobile = models.CharField(_('Official Phone Number (Mobile Line)'), max_length=50,blank=True, null=True)
    middlename=models.CharField(_('Middle Name'), max_length=50,blank=True, null=True)
    lastname=models.CharField(_('last Name'), max_length=50,blank=True, null=True)
    designation_role = models.CharField(_('designation'), max_length=50, blank=True, null=True)
    roles=models.ForeignKey("Roles",on_delete=models.CASCADE,blank=True, null=True)
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=True)
    #"primary vendor approver"
    is_primary=models.IntegerField(blank=True,default=0)
    #"secondary vendor approver"
    is_secondary=models.IntegerField(blank=True,default=0)
    #"active or inactive"
    primary_active_status=models.IntegerField(blank=True,default=0)
    #first_time_login
    userfirsttimelogin=models.IntegerField(blank=True,default=0)
    contactpersonstatus=models.IntegerField(blank=True,default=0)
    image = models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)
    phone_number_extenstion= models.CharField(_('Phone Number Extension'), max_length=50, blank=True, null=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    cin_number= models.CharField(max_length=255,blank=True,null=True)
    status = models.IntegerField(blank=True,default=1)
    user_department = models.ForeignKey("UserDepartment",on_delete=models.CASCADE,blank=True, null=True)
    user_group = models.ForeignKey("UserGroup",on_delete=models.CASCADE,blank=True, null=True)
    signature_type = models.CharField(_('signature_type'), max_length=50,blank=True, null=True)
    signature_image = models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)
    signature_draw = models.CharField(_('signature_draw'), max_length=50,blank=True, null=True)
    signature_fontname = models.CharField(max_length=50,null=True,blank=True)
    signature_fontfamily = models.ForeignKey('FontFamily',on_delete=models.CASCADE, null=True,blank=True)
    bankuserstatus = models.IntegerField(blank=True,default=0)
    disputeuser = models.BooleanField(blank=True,default=False,null=True)
    loginstatus=models.IntegerField(blank=True,default=0)
    login_date=models.BigIntegerField(blank=True, null=True)
    previous_login_date=models.BigIntegerField(blank=True, null=True)

    USERNAME_FIELD = 'hidden_username'
    REQUIRED_FIELDS = ['name']
    # REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.name
        # return self.name+''+self.lastname
class UserDepartment(models.Model):
    id=models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    department=models.CharField(max_length=255,blank=True, null=True)
    status=models.IntegerField(blank=True,default=1)

    def __str__(self):
        """stirng representation"""
        return self.department

class UserGroup(models.Model):
    id=models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    group=models.CharField(max_length=255,blank=True, null=True)
    status=models.IntegerField(blank=True,default=1)
    type=models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        """stirng representation"""
        return self.group