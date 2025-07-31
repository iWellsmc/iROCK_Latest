from . import views
from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name = 'wcc'
urlpatterns = [
    path('wcclist',WccList.as_view(),name='wcclist'),
    path('createwcc',CreateWccMaster.as_view(),name='createwcc'),
    path('createwccsteptwo/<int:pk>',CreateWccFormTwo.as_view(),name='createwccsteptwo'),
    path('wccpreview/<int:pk>',WccPreview.as_view(),name='wccpreview'),
    path('getsupportfiles',views.getsupportfiles,name='wccpreview'),
    path('wccview/<int:pk>',WccView.as_view(),name='wccview'),
    path('wcceditformone/<int:pk>',WccEditFormOne.as_view(),name='wcceditformone'),
    path('wcceditformtwo/<int:pk>',WccEditFormTwo.as_view(),name='wcceditformtwo'),
    path('checkwccnumber',CheckWccNumber.as_view(),name='CheckWccNumber'),
    path('wccflow/<int:project_id>',ProjectWccFlow.as_view(),name='wccflow'),
    path('projectwccview/<int:project_id>',ProjectWccView.as_view(),name='projectwccview'),
    path('wccprojectlevels',WccProjectLevels.as_view(),name='wccprojectlevels'),
    path('approvalwcclist',ApprovalWccList.as_view(),name='approvalwcclist'),
    path('wccapprovalview/<int:pk>',WccApprovalView.as_view(),name='wccapprovalview'),
    path('wccapprovaltrack/<int:pk>',WccApprovalTrack.as_view(),name='wccapprovaltrack'),
    path('wccpdfview/<int:pk>',views.WccPDFView.as_view(),name='wccpdfview'),
    path('checkwccapprovalprocess',views.CheckWccApprovalProcess.as_view(),name='checkwccapprovalprocess'),
    path('wccassignuser/<int:pk>',WccAssignUsers.as_view(),name='wccassignuser'),
    path('getallwcc' ,get_wcc_details, name="getallwcc" ),
    path('wccqueryhistory/<int:pk>',WccQueryHistory.as_view(),name='wccqueryhistory'),
    path('closewccquery/<int:pk>',views.CloseWccQuery,name='closewccquery'),


    
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)