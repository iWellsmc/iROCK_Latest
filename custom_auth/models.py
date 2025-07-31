
# from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import Group

# class Roles(models.Model):
#     id = models.AutoField(primary_key=True)
#     roles=models.CharField(max_length=75,verbose_name="Roles", blank=True, null=True)
#     status=models.IntegerField(blank=True, null=True,default=1)


# class CustomUserManager(BaseUserManager):
#     """custom user manager class"""
#     use_in_migration = True

#     def _create_user(self, email, password, **extra_fields):
#         print(self)
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(email, password, **extra_fields)

# # Create your models here.
# class User(AbstractBaseUser, PermissionsMixin):
#     """ Custom user model class"""
#     id = models.AutoField(primary_key=True)
#     hidden_username=models.CharField(_('Hidden User Name'),unique=True, max_length=50, blank=True, null=True)
#     email = models.EmailField(_('email'),default='')
#     Title = models.CharField(_('Title'), max_length=10, blank=True,null=True)
#     name = models.CharField(_('first Name'), max_length=50, blank=False)
#     areacode=models.CharField(_('Area Code'), max_length=50,blank=True, null=True)
#     phone = models.CharField(_('Official Phone Number (Land Line)'), max_length=50, blank=True, null=True)
#     phone_countrycode = models.CharField(_('Country Code'), max_length=50, blank=True,null=True)
#     mobile_countrycode = models.CharField(_('Country Code'), max_length=50, blank=True,null=True)
#     mobile = models.CharField(_('Official Phone Number (Mobile Line)'), max_length=50,blank=True, null=True)
#     middlename=models.CharField(_('Middle Name'), max_length=50,blank=True, null=True)
#     lastname=models.CharField(_('last Name'), max_length=50,blank=True, null=True)
#     designation_role = models.CharField(_('designation'), max_length=50, blank=True, null=True)
#     roles=models.ForeignKey("Roles",on_delete=models.CASCADE,blank=True, null=True)
#     is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
#     is_active = models.BooleanField(_('is_active'), default=True)
#     is_staff = models.BooleanField(default=True)
#     #"primary vendor approver"
#     is_primary=models.IntegerField(blank=True,default=0)
#     #"secondary vendor approver"
#     is_secondary=models.IntegerField(blank=True,default=0)
#     #"active or inactive"
#     primary_active_status=models.IntegerField(blank=True,default=0)
#     #first_time_login
#     userfirsttimelogin=models.IntegerField(blank=True,default=0)
#     contactpersonstatus=models.IntegerField(blank=True,default=0)
#     image = models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)
#     phone_number_extenstion= models.CharField(_('Phone Number Extension'), max_length=50, blank=True, null=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     cin_number= models.CharField(max_length=255,blank=True,null=True)
#     status = models.IntegerField(blank=True,default=1)
#     user_department = models.ForeignKey("UserDepartment",on_delete=models.CASCADE,blank=True, null=True)
#     user_group = models.ForeignKey("UserGroup",on_delete=models.CASCADE,blank=True, null=True)
#     signature_type = models.CharField(_('signature_type'), max_length=50,blank=True, null=True)
#     signature_image = models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)
#     signature_draw = models.CharField(_('signature_draw'), max_length=50,blank=True, null=True)
#     USERNAME_FIELD = 'hidden_username'
#     REQUIRED_FIELDS = ['name']
#     # REQUIRED_FIELDS = ['email']
#     objects = CustomUserManager()

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def __str__(self):
#         """stirng representation"""
#         return self.name
#         # return self.name+''+self.lastname

# class CompaniesManager(models.Manager):
#     def get_by_id(self,id):
#         return self.get(id=id)


# class Companies(models.Model):  
#     id = models.AutoField(primary_key=True)
#     company_name= models.CharField(max_length=255)
#     cin_number= models.CharField(max_length=255,blank=True,null=True)
#     first_name= models.CharField(max_length=255)
#     last_name= models.CharField(max_length=255)
#     email= models.CharField(max_length=255)
#     mobile= models.CharField(max_length=255)
#     phonenumber=models.CharField(max_length=255,blank=True, null=True)
#     country=models.ForeignKey("Basecountries",on_delete=models.CASCADE,verbose_name="Country Name",blank=True, null=True)
#     phone_countrycode=models.CharField(max_length=255,blank=True, null=True)
#     mobile_countrycode=models.CharField(max_length=255,blank=True, null=True)
#     areacode=models.CharField(max_length=20,blank=True, null=True)
#     category_entity=models.CharField(max_length=50,blank=True, null=True)
#     image = models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)
#     address = models.CharField(max_length=500,blank=True, null=True)
#     website = models.CharField(max_length=255,blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     status = models.IntegerField(blank=True,default=1)
#     contact_person=models.CharField(max_length=255,blank=True, null=True)
#     designation=models.CharField(max_length=255,blank=True, null=True)
#     type_of_license=models.CharField(max_length=255,blank=True, null=True)
#     package=models.CharField(max_length=255,blank=True, null=True)
#     number_of_users=models.IntegerField(blank=True, null=True)
#     concurent_users=models.IntegerField(blank=True, null=True)
#     cloud_server=models.CharField(max_length=255,blank=True, null=True)
#     customisation=models.CharField(max_length=255,blank=True, null=True)
#     support_services=models.CharField(max_length=255,blank=True, null=True)
#     licensekey=models.CharField(max_length=255,blank=True, null=True)
#     licencestatus=models.IntegerField(blank=True,default=0)
#     currency=models.CharField(max_length=255,blank=True, null=True)
#     amount=models.CharField(max_length=255,blank=True, null=True)
#     checkkeystatus=models.IntegerField(blank=True,default=0)
#     invoicedate=models.CharField(max_length=255,blank=True, null=True)
#     invoicenumber=models.CharField(max_length=255,blank=True, null=True)
#     updated_at=models.DateTimeField(auto_now_add=True,blank=True, null=True, editable=False)
#     objects=CompaniesManager()

#     def __str__(self):
#         return self.company_name 

# #  Chennai@01





# class Settings(models.Model):
#     id = models.AutoField(primary_key=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     dateformat=models.CharField(max_length=255,blank=True, null=True)
#     timeformat=models.CharField(max_length=255,blank=True, null=True)
#     timezone=models.CharField(max_length=255,blank=True, null=True)
#     currency=models.CharField(max_length=255,blank=True, null=True)
#     unit=models.CharField(max_length=255,blank=True, null=True)
#     vendor_invite_time=models.CharField(max_length=255,blank=True, null=True)
#     vendor_invite_unit=models.CharField(max_length=255,blank=True, null=True)
#     vendor_registartion_time=models.CharField(max_length=255,blank=True, null=True)


# #general settings
    
# class Countries(models.Model):  
#     id = models.AutoField(primary_key=True)
#     iso= models.CharField(max_length=255)
#     name= models.CharField(max_length=255)
#     nicename= models.CharField(max_length=255)
#     iso3= models.CharField(max_length=255)
#     numcode= models.CharField(max_length=255)
#     phonecode= models.CharField(max_length=255)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     status = models.IntegerField(blank=True,default=1)
#     def __str__(self):
#         """stirng representation"""
#         return self.nicename

# class Basecountries(models.Model):
#     id = models.AutoField(primary_key=True)
#     name=models.CharField(max_length=255)
#     iso3=models.CharField(max_length=255)
#     numeric_code=models.CharField(max_length=255)
#     iso2=models.CharField(max_length=255)
#     phonecode=models.CharField(max_length=255)
#     capital=models.CharField(max_length=255)
#     currency=models.CharField(max_length=255)
#     currency_name=models.CharField(max_length=255)
#     currency_symbol=models.CharField(max_length=255)
#     tld=models.CharField(max_length=255)
#     native=models.CharField(max_length=255)
# ftcjhnftjregion=models.CharField(max_length=255)
#     subregion=models.CharField(max_length=255)
#     timezones=models.TextField()
#     translations=models.TextField()
#     flag=models.IntegerField(blank=True, null=True,default=1)
#     latitude=models.DecimalField(max_digits=10, decimal_places=8)
#     longitude=models.DecimalField(max_digits=11, decimal_places=8)
#     emoji=models.CharField(max_length=255)
#     emojiU=models.CharField(max_length=255,blank=True, null=True)
#     created_at=models.DateTimeField(auto_now_add=True, editable=False)
#     updated_at=models.DateTimeField(auto_now_add=True, editable=False)
#     wikiDataId=models.CharField(max_length=255,blank=True, null=True)
    
#     def __str__(self):
#         """stirng representation"""
#         return self.name
# Basecountries.objects.all().distinct('currency_symbol')

# class States(models.Model):

#     id= models.AutoField(primary_key=True)
#     name=models.CharField(max_length=255)
#     country=models.ForeignKey("Basecountries",on_delete=models.CASCADE,related_name="states",blank=True, null=True)
#     country_code=models.CharField(max_length=255)
#     fips_code=models.CharField(max_length=255)
#     iso2=models.CharField(max_length=255)
#     type=models.CharField(max_length=255)
#     latitude=models.DecimalField(max_digits=10, decimal_places=8)
#     longitude=models.DecimalField(max_digits=11, decimal_places=8)
#     created_at=models.DateTimeField(auto_now_add=True, editable=False)
#     updated_at=models.DateTimeField(auto_now_add=True, editable=False)
#     flag=models.IntegerField(blank=True, null=True,default=1)
#     wikiDataId=models.CharField(max_length=255)


# class zone(models.Model):
#     id= models.AutoField(primary_key=True)
#     country_code=models.CharField(max_length=255,blank=True, null=True)
#     zone_name =models.CharField(max_length=255,blank=True, null=True)
#     created_by =models.CharField(max_length=255,blank=True, null=True)
#     updated_by =models.CharField(max_length=255,blank=True, null=True)
#     deleted_by =models.CharField(max_length=255,blank=True, null=True)
#     created_at =models.DateTimeField(auto_now_add=True, editable=False)
#     updated_at =models.DateTimeField(auto_now_add=True, editable=False)
#     deleted_at =models.DateTimeField(auto_now_add=True, editable=False)
#     lock =models.IntegerField(blank=True, null=True,default=1)


# class Enquiryusers(models.Model):
#     id= models.AutoField(primary_key=True)
#     title=models.CharField(max_length=255,blank=True, null=True)
#     username=models.CharField(max_length=255,blank=True, null=True)
#     email_id=models.CharField(max_length=255,blank=True, null=True)
#     message=models.TextField(blank=True, null=True)
#     status=models.IntegerField(blank=True, null=True,default=1)
#     proposalstatus=models.IntegerField(blank=True, null=True,default=0)
#     # //for proposal form 


# class companylicensekey(models.Model):
#     id=models.AutoField(primary_key=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     created=models.DateTimeField(auto_now_add=True, editable=False)
#     status=models.IntegerField(blank=True,default=0)
#     type_of_license=models.CharField(max_length=255,blank=True, null=True)
#     package=models.CharField(max_length=255,blank=True, null=True)
#     number_of_users=models.IntegerField(blank=True, null=True)
#     concurent_users=models.IntegerField(blank=True, null=True)
#     licensekey=models.CharField(max_length=255,blank=True, null=True)
#     currency=models.CharField(max_length=255,blank=True, null=True)
#     amount=models.CharField(max_length=255,blank=True, null=True)
#     invoicedate=models.CharField(max_length=255,blank=True, null=True)
#     invoicenumber=models.CharField(max_length=255,blank=True, null=True)

# class PaymentHistory(models.Model):
#     id=models.AutoField(primary_key=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     status=models.IntegerField(blank=True,default=1)
#     currency=models.ForeignKey("Basecountries",on_delete=models.CASCADE,blank=True, null=True)
#     amount=models.CharField(max_length=255,blank=True, null=True)
#     invoicedate=models.CharField(max_length=255,blank=True, null=True)
#     invoicenumber=models.CharField(max_length=255,blank=True, null=True)
#     file=models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)

# class PaymentHistoryFile(models.Model):
#     id=models.AutoField(primary_key=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     file=models.FileField(upload_to ='uploads/',blank=True,null=True)
#     status=models.IntegerField(blank=True,default=1)
#     payment_history = models.ForeignKey("PaymentHistory",on_delete=models.CASCADE,blank=True, null=True)

# class UserDepartment(models.Model):
#     id=models.AutoField(primary_key=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     department=models.CharField(max_length=255,blank=True, null=True)
#     status=models.IntegerField(blank=True,default=1)

#     def __str__(self):
#         """stirng representation"""
#         return self.department

# class UserGroup(models.Model):
#     id=models.AutoField(primary_key=True)
#     company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
#     group=models.CharField(max_length=255,blank=True, null=True)
#     status=models.IntegerField(blank=True,default=1)
#     type=models.CharField(max_length=255,blank=True, null=True)

#     def __str__(self):
#         """stirng representation"""
#         return self.group

