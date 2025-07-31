from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'invoiceview'
 
urlpatterns = [
    path('calendarview',views.Calendarview.as_view(), name='calendarview'),
    path('listview',views.Listview.as_view(), name='listview'),
    path('listview_date',views.Listview_date.as_view(), name='listview_date'),


]