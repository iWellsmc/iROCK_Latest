from django.contrib import admin
from.models import *
# Register your models here.


class SignatoryUserInline(admin.TabularInline):
    model = SignatoriesUsers

class SignatoryAdmin(admin.ModelAdmin):
    inlines = [SignatoryUserInline]
admin.site.register(SignatoriesSettings, SignatoryAdmin)
admin.site.register(Module)
admin.site.register(Role)
admin.site.register(Right)
admin.site.register(RoleRight)
admin.site.register(Process)
admin.site.register(ProcessModule)
admin.site.register(Flow)
admin.site.register(FlowProcess)
# admin.site.register(SignatoriesSettings)
# admin.site.register(SignatoriesUsers)