from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static #import this
from django.contrib.auth.decorators import login_required

app_name = 'custom_auth'

urlpatterns = [
    path('signup/<int:pk>/', views.SignupView.as_view(), name='signup'),


    path('', views.LoginView.as_view(), name='login'),
    path('forgotpasscode', views.forgotpasscode,name='forgotpasscode'),
    path('resetpasscode/<int:id>/',views.resetpasscode,name='resetpasscode'),
    path('forgotpasscodevin',views.forgotpasscode,name='forgotpasscodevin'),
    path('checkcompanyuseremail',views.checkcompanyuseremail,name='checkcompanyuseremail'),
    path('checkcompanyuseremailexists',views.checkcompanyuseremailexists,name='checkcompanyuseremailexists'),
    path('enquiry', views.enquiry, name='enquiry'),
    path('vendorlogin', views.Vendorlogin, name='vendorlogin'),
    path('logout/', views.Logout, name='logout'),
    path('adminlogin/', views.AdminLoginView.as_view(), name='adminlogin'),
    path('company/list/',views.Companieslist, name='companies'),
    path('company/view/<int:id>/', views.Companiesview, name='companyview'),
    path('company/approve/<int:id>/', views.Companiesapprove, name='companyapprove'),
    path('company/reject/<int:id>/', views.Companiesreject, name='companyreject'),
    path('checkemail/',views.checkemail,name="checkemail"),
    path('viewcompany/<int:pk>/',views.viewcompaniesdetails,name="viewcompany"),
    path('editcompany/<int:pk>/',views.editcompaniesdetails,name="editcompany"),
    path('editcompany/<int:pk>/getcountrycode',views.getcountrycode,name="getcountrycodes"),
    path('generalsetting/<int:companyid>/',views.Generalsetting,name="generalsetting"),
    path('generalsettingsview/<int:pk>',views.generalsettingview,name="generalsettingsview") ,
    path('userpasswordreset/<int:pk>',views.Userpasswordreset,name="userpasswordreset"),
    path('usereditdetails/<int:pk>',views.EditUserDetails,name='usereditdetails'),
    path('userdetails/<int:pk>',views.UserSpecificDetailsView,name='userdetails'),
    path('editclientadmindetails/<int:pk>',views.editclientadmindetails,name='editclientadmindetails'),
    path('clientadminview/<int:pk>',views.clientadminview,name='clientadminview'),    
    path('downloadbrochure',views.downloadbrochure,name='downloadbrochure'),  
    path('enquiryusers',views.enquiryusers,name='enquiryusers'),  
    path('proposalformsend/<int:pk>',views.proposalformsend,name='proposalformsend'),  
    path('keygenerator/<int:id>/<str:status>',views.keygenerator,name='keygenerator'),  
    path('keyactivationpage/',views.keyactivationpage,name='keyactivationpage'),
    path('seckeychecking/',views.seckeychecking,name='seckeychecking'),
    path('proposal_check/<int:id>/',views.proposal_check,name='proposal_check'),
    path('passwordrestcheck/',views.passwordrestcheck,name='passwordrestcheck'),
    path('notifications/', views.Notifications, name='notifications'),
    path('markallread/', views.markallread,name="markallread"),   
    path('checkinvoicenumduplicate', views.checkinvoicenumduplicate,name="checkinvoicenumduplicate"),   
    path('userdatetime', views.GetClientDatetime.as_view(),name="userdatetime"),
    # path('adduserdepartment/', views.addUserDepartmentForm, name='add-userdepartment-form'),
        # path('adduserdepartment/', views.UserAddView.as_view(), name='add-userdepartment-form'),
        # path('adduserdepartment/', views.add_form, name='add-userdepartment-form'),
    path('adduserdepartment/', views.addUserDepartment.as_view(), name='add-userdepartment-form'),
    path('listuserdepartment/', views.listUserDepartment.as_view(), name='list-userdepartment-form'),
    path('edituserdepartment/<int:pk>/', views.editUserDepartment.as_view(), name='edit-userdepartment-form'),
    path('deleteuserdepartment/<int:pk>/', views.deleteUserDepartment.as_view(), name='delete-userdepartment-form'),
    path('addusergroup/', views.addUserGroup.as_view(), name='add-usergroup-form'),
    path('listusergroup/', views.listUserGroup.as_view(), name='list-usergroup-form'),
    path('editusergroup/<int:pk>/', views.editUserGroup.as_view(), name='edit-usergroup-form'),
    path('deleteusergroup/<int:pk>/', views.deleteUserGroup.as_view(), name='delete-usergroup-form'),
    path('validateusergroup/', views.validateUserGroup.as_view(), name='validateusergroup'),
    path('validateuserdepartment/', views.validateUserDepartment.as_view(), name='validateuserdepartment'),
    path('urlchkforiframe/',views.urlchkforiframe.as_view(),name='urlchkforiframe'),
    path('invoicetriggertime/<int:companyid>/',views.Invoicetriggertime.as_view(),name="Invoicetriggertime"),
    path('editinvoicetriggertime/<int:companyid>/',views.EditInvoicetriggertime.as_view(),name="EditInvoicetriggertime"),
    path('wcctriggertime/<int:companyid>/',views.Wcctriggertime.as_view(),name="Wcctriggertime"),
    path('editwcctriggertime/<int:companyid>/',views.EditWcctriggertime.as_view(),name="EditWcctriggertime"),
    path('listdisputemembers',views.ListDisputeMembers.as_view(),name='listdisputemembers'),
    path('addcommitteemembers',views.AddCommitteMembers.as_view(),name='add-committee-form'),
    path('deletedisputeuser',views.DeleteDisputeUser,name='deletedisputeuser'),
    path('duplicateusercheck',views.DuplicateUserCheck,name='duplicateusercheck'),
    path('editusercommittee/<int:pk>',views.EditUserCommittee.as_view(),name='editusercommittee'),
    path('user_log/',views.user_log,name='user_log'),
    path('user_log_datatable',views.user_log_datatable,name='user_log_datatable'),
    path('dashbord/dash_country_view',views.dash_country_view,name='dash_country_view'),
    path('markallread1/', views.mark_all_read, name="markallread1")
]

# for urlpattern in urlpatterns:
#     urlpattern.callback = login_required(
#         urlpattern.callback,
#         redirect_field_name=None,
#         # LOGIN_REDIRECT_URL = 'dashboard:dashboard'        

#         # login_url='dashboard:dashboard'
#     )
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
