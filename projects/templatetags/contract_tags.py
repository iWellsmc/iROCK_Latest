from django import template
from projects.models import VendorContractPriceTable
register = template.Library()

@register.simple_tag
def checkpricetable_exist_by_contract_id(contract_id,amendment_addendum_id=None):
    print(f"contract_id {contract_id}")
    price_table=VendorContractPriceTable.objects.checkpricetable_exists_by_contractid(contract_id,amendment_addendum_id)
    return price_table.count()


