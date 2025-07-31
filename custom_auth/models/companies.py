from django.db import models

class CompaniesManager(models.Manager):
    def get_by_id(self,id):
        return self.get(id=id)


class Companies(models.Model):  
    id = models.AutoField(primary_key=True)
    company_name= models.CharField(max_length=255)
    cin_number= models.CharField(max_length=255,blank=True,null=True)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    mobile= models.CharField(max_length=255)
    phonenumber=models.CharField(max_length=255,blank=True, null=True)
    country=models.ForeignKey("Basecountries",on_delete=models.CASCADE,verbose_name="Country Name",blank=True, null=True)
    phone_countrycode=models.CharField(max_length=255,blank=True, null=True)
    mobile_countrycode=models.CharField(max_length=255,blank=True, null=True)
    areacode=models.CharField(max_length=20,blank=True, null=True)
    category_entity=models.CharField(max_length=50,blank=True, null=True)
    image = models.FileField(upload_to ='uploads/',blank=True,null=True,default=None)
    address = models.CharField(max_length=255,blank=True, null=True)
    website = models.CharField(max_length=255,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.IntegerField(blank=True,default=1)
    contact_person=models.CharField(max_length=255,blank=True, null=True)
    designation=models.CharField(max_length=255,blank=True, null=True)
    type_of_license=models.CharField(max_length=255,blank=True, null=True)
    package=models.CharField(max_length=255,blank=True, null=True)
    number_of_users=models.IntegerField(blank=True, null=True)
    concurent_users=models.IntegerField(blank=True, null=True)
    cloud_server=models.CharField(max_length=255,blank=True, null=True)
    customisation=models.CharField(max_length=255,blank=True, null=True)
    support_services=models.CharField(max_length=255,blank=True, null=True)
    licensekey=models.CharField(max_length=255,blank=True, null=True)
    licencestatus=models.IntegerField(blank=True,default=0)
    currency=models.CharField(max_length=255,blank=True, null=True)
    amount=models.CharField(max_length=255,blank=True, null=True)
    checkkeystatus=models.IntegerField(blank=True,default=0)
    invoicedate=models.CharField(max_length=255,blank=True, null=True)
    invoicenumber=models.CharField(max_length=255,blank=True, null=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True, null=True, editable=False)
    objects=CompaniesManager()

    def __str__(self):
        return self.company_name 


class companylicensekey(models.Model):
    id=models.AutoField(primary_key=True)
    company=models.ForeignKey("Companies",on_delete=models.CASCADE,blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True, editable=False)
    status=models.IntegerField(blank=True,default=0)
    type_of_license=models.CharField(max_length=255,blank=True, null=True)
    package=models.CharField(max_length=255,blank=True, null=True)
    number_of_users=models.IntegerField(blank=True, null=True)
    concurent_users=models.IntegerField(blank=True, null=True)
    licensekey=models.CharField(max_length=255,blank=True, null=True)
    currency=models.CharField(max_length=255,blank=True, null=True)
    amount=models.CharField(max_length=255,blank=True, null=True)
    invoicedate=models.CharField(max_length=255,blank=True, null=True)
    invoicenumber=models.CharField(max_length=255,blank=True, null=True)