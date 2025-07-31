from django.contrib import admin
from.models import ContractMaster, Amendment
from import_export.admin import ImportExportModelAdmin
from .resources import MyModelResource
from notifications.models import Notification
from custom_auth.models import User
# Register your models here.
# admin.site.register(ContractMaster)
# admin.site.register(Amendment)

# @admin.register(ContractMaster)
# class MyModelAdmin(ImportExportModelAdmin):
#     resource_class = MyModelResource

# admin.site.unregister(Notification)

# from django.apps import apps

# Get all models in your app
# models = apps.get_models()
# app = apps.get_app_config('projects')
# # app1 = apps.get_app_config('chat')
# # app2 = apps.get_app_config('credit_note')
# # app3 = app.models | app1.models | app2.models
# for model_name, model in app.items():
#     if model not in admin.site._registry:
#         admin.site.register(model,ImportExportModelAdmin)
# admin.site.register(User,ImportExportModelAdmin)
# Register all models with ImportExportModelAdmin
# for model in models:
#     if model not in admin.site._registry:
#         admin.site.register(model, ImportExportModelAdmin)