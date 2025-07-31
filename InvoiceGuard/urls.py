from .views import (listRole,listModule,getModule,addRole,assignRights,editRole,validateRole,deleteRole,listRolesAndRights,Addprocess,listProcess,editProcess,viewProcess,addFlow,listFlow,editFlow,viewFlow,getRights,listModuleBasedRole,listCompanySignatory,addUpdateSignatory,deleteSignatoryUser,ajaxPostViewSignatory,deleteSignatory,deleteProcess,deleteFlow,validateProcess,validateFlow,GetProjectSignatory,GetSignatoryUser)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name = 'InvoiceGuard'
urlpatterns = [
    path('addusergroup/', addRole.as_view(), name='add-usergroup-form'),
    path('editrole/<int:pk>/', editRole.as_view(), name='edit-role-form'),
    path('listrolesandrights/', listRole.as_view(), name='list-rolesandrights-form'),
    path('listmodules/', listModule.as_view(), name='list-modules-form'),
    path('assignrights/<int:pk>', assignRights.as_view(), name='assign-rights-form'),
    path('validaterole/', validateRole.as_view(), name='validate-role-form'),
    path('deleterole/', deleteRole.as_view(), name='delete-role-form'),
    path('getrolebasedrights/', getRights.as_view(), name='role-base-rights'),
    path('rolewithrightsview/', listModuleBasedRole.as_view(), name='role-withrights-view'),
    path('rolerightview/<int:pk>', listRolesAndRights.as_view(), name='role-right-view'),
    path('addprocess/',Addprocess.as_view(),name='add-process-form'),
    path('listprocess/',listProcess.as_view(),name='list-process-form'),
    path('editprocess/<int:pk>/',editProcess.as_view(),name='edit-process-form'),
    path('viewprocess/<int:pk>/',viewProcess.as_view(),name='view-process-form'),
    path('deleteprocess/',deleteProcess.as_view(),name='delete-process-view'),
    path('addflow/',addFlow.as_view(),name='add-flow-form'),
    path('listflow/',listFlow.as_view(),name='list-flow-form'),
    path('editflow/<int:pk>/',editFlow.as_view(),name='edit-flow-form'),
    path('viewflow/<int:pk>/',viewFlow.as_view(),name='view-flow-form'),
    path('signatoryview/',listCompanySignatory.as_view(),name='signatory-view-form'),
    path('addupdatesignatory/',addUpdateSignatory.as_view(),name='add-update-signatory-form'),
    path('deletesignatoryuser',deleteSignatoryUser.as_view(),name='delete-signatory-user-form'),
    path('ajaxpostviewsignatory',ajaxPostViewSignatory.as_view(),name='ajax-post-view-signatory-form'),
    path('deletesignatory',deleteSignatory.as_view(),name='delete-signatory-form'),
    path('deleteflow/',deleteFlow.as_view(),name='delete-flow-form'),
    path('validateprocess/',validateProcess.as_view(),name='validate-process-form'),
    path('validatflow',validateFlow.as_view(),name='create-flow-form'),
    path('getModule/',getModule.as_view(),name='get-module-form'),
    path('getsignatoryproject/',GetProjectSignatory.as_view(),name="get-signatory-project"),
    path('getsignatoryuser',GetSignatoryUser.as_view(),name='get-signatory-users'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)