from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name = 'finance'
urlpatterns = [
    path('createcompanybank/',CreateCompanyBank.as_view(),name='createcompanybank'),
    path('companybankdelete/<int:pk>/',CompanyBankDelete.as_view(),name='companybankdelete'),
    path('listdetails/',list_details.as_view(),name='list_details'),
    path('validateactno/',validateActno.as_view(),name='validate-actno-form'),
    path('createbankuser/',CreateBankUser.as_view(),name='createbankuser'),
    path('listbankuser/',ListBankUser.as_view(),name='listbankuser'),
    path('viewbankuser/<int:pk>/',ViewBankUser.as_view(),name='viewbankuser'),
    path('editbankuser/<int:pk>/',EditBankUser.as_view(),name='editbankuser'),
    path('deletebankuser/<int:pk>/',DeleteBankUser.as_view(),name='deletebankuser'),
    path('getbankinformation/',GetBankInformation.as_view(),name='getbankinformation'),
    path('editcompanybank/<int:pk>/',EditCompanyBank.as_view(),name='editcompanybank'),
    path('validatebankname/',ValidateBankname.as_view(),name='validatebankname'),
    path('validateduplicatebank/',ValidateDuplicateBank.as_view(),name='validateduplicatebank'),
    path('validateduplicateemail/',validateDuplicateemail.as_view(),name='validateduplicateemail'),
    path('viewbankinfo/<int:pk>/',ViewBankInfo.as_view(),name='viewbankinfo'),
    path('removebankusers/',RemoveBankUsers.as_view(),name='removebankusers'),
   
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)