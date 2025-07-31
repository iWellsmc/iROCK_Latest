from django.contrib import admin
from .models import UserDepartment,UserGroup
# Register your models here.
admin.site.register(UserDepartment)
admin.site.register(UserGroup)