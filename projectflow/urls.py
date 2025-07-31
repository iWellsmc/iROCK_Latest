from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'projectflow'
 
urlpatterns = [
    path('createprocessflow/<int:pk>',views.createProcessflow.as_view(),name='createprocessflow'),
    path('createflowlevel/<int:pk>',views.createflowlevel.as_view(),name='createflowlevel'),
    path('editflowlevel/<int:pk>',views.editflowlevel.as_view(),name='editflowlevel'),
    path('getprocess_byflow',views.getprocess_byflow,name="getprocess_byflow"),
    path('getmodule_byprocess',views.getmodule_byprocess,name="getmodule_byprocess"),
    path('getroles_and_projectusers',views.getroles_and_projectusers,name="getroles_and_projectusers"),
    path('checkprojectflow_level',views.checkprojectflow_level,name="checkprojectflow_level"),
    path('delete_level',views.delete_level,name="delete_level"),
    path('projectinvoiceflowview/<int:pk>',views.ProjectInvoiceFlowView.as_view(),name='projectinvoiceflowview'),
    path('get_signatories',views.get_signatories,name='get_signatories')

]