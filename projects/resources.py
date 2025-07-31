from import_export import resources
from .models import ContractMaster

class MyModelResource(resources.ModelResource):
    class Meta:
        model = ContractMaster
        fields = '__all__'
