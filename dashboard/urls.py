from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static #import this
from django.contrib.auth.decorators import login_required



app_name = 'dashboard'
urlpatterns = [
    path('dashboard/',views.Dashboard.as_view(),name='dashboard'),
    path('getcountry_wise_project/',views.getcountry_wise_project,name='getcountry_wise_project'),
    path('getinvoicesummarychart_byvendor/',views.getinvoicesummarychart_byvendor,name='getinvoicesummarychart_byvendor'),
    path('getunpaid_overdueinvoices/',views.getunpaid_overdueinvoices,name='getunpaid_overdueinvoices'),
    path('filtervendor_dashboard/',views.filtervendor_dashboard,name='filtervendor_dashboard'),
    path('dash_country_viewas/',views.dash_country_viewas,name='dash_country_viewas'),  
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)