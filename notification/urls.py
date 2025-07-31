from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'notification'

urlpatterns = [

    # path('signup/', views.SignupView.as_view(), name='signup'),  
  

]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
