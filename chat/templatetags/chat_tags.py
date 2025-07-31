from django import template
from projects.models import ContractMasterVendor,UserRights,Q
register = template.Library()

@register.simple_tag
def get_vendorname(cin_number):
    return ContractMasterVendor.objects.filter(vin=cin_number).values_list('vendor_name', flat=True).first()

@register.simple_tag
def check_create_edit_delete(userid,module):
    print('userid',userid)
    if UserRights.objects.filter(user_id=userid,module_id=module).filter(Q(create=1) | Q(delete=1) | Q(edit=1)):
        return 1
    else:
        return 0
    
