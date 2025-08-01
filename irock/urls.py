"""irock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
from custom_auth import views

handler404 = 'custom_auth.views.error_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('custom_auth.urls')),
    path('projects/', include('projects.urls')),
    # path('projects/', include('projects.urls')),
    path('notification/', include(notifications.urls, namespace='notifications')),
    path('invoice/', include('invoice.urls')),
    path('chat/', include('chat.urls')),
    path('credit/', include('credit_note.urls')),
    path('invoiceguard/', include('InvoiceGuard.urls')),
    path('finance/',include('finance.urls')),
    path('cost_code/',include('cost_code.urls')),
    path('wcc/',include('wcc.urls')),
    path('projectflow/', include('projectflow.urls')),
    path('invoiceview/', include('invoiceview.urls')),
    path('dashboard/', include('dashboard.urls')),



]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

