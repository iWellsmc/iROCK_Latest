from django.db import models
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class CostCodeSubManager(models.Manager):
    def create_costcode_sub(self,cost_code,order,cost_type_id,costcode_main_id,company,costcodepreview=None,costcode_master_id=None):
        return self.create(cost_code=cost_code,order=order,company=company,cost_type_id=cost_type_id,costcode_main_id=costcode_main_id,costcode_preview=costcodepreview,costcode_master_id=costcode_master_id)
    def getgroup_costcode_sub(self,main_costcode):
        return self.filter(costcode_main_id=main_costcode.id,status=1).values('order').annotate(total=Count('order'))
    def getallcostcodesub_order(self,main_costcode,order):
        return self.select_related('cost_type','costcode_master').filter(costcode_main_id=main_costcode,order=order)
    def getcostcodesub_order_index(self,order,maincostcode_id,index):
        return self.filter(costcode_main_id=maincostcode_id,order=order)[index]
    def getcostcodesub_with_components_order_index(self,order,maincostcode_id,index):
        return self.select_related('cost_type').filter(costcode_main_id=maincostcode_id,order=order)[index]
    def getcostcodesub_codecode(self,costcode,company):
        return self.filter(costcode_preview=costcode,status=1,company=company)
    def update_costcode_sub(self,id,cost_type_id,costcode,costcodepreview,maincode):
        return self.filter(id=id,costcode_main_id=maincode).update(cost_type_id=cost_type_id,cost_code=costcode,costcode_preview=costcodepreview)
    def deletecostcode(self,maincode,order,status):
        return self.filter(costcode_main_id=maincode,order=order).update(status=status)  
    def deletecostcodemain(self,maincode):
        return self.filter(id=maincode).update(status=0)
    def getlastcostcodesub(self,maincode):
        return self.filter(costcode_main_id=maincode).order_by('-id').first()
    def checkcostcodetypeexists(self,costtypeid,company,component_name):
        return self.select_related('cost_type').filter(cost_type_id=costtypeid,company=company,status=1,cost_type__component_name=component_name)
    
    def get_by_main_id(self,order,main_id,status):
        return self.filter(order=order,costcode_main_id=main_id,status=status).first()
    
    def get_by_company_main_id(self,main_id,order,company):
        return self.filter(costcode_main_id=main_id,order=order,company_id=company).last()
    
    def get_by_company(self,status,company):
        return self.filter(status=status,company_id=company)
    
    def getallcode_by_masterid(self,company_id,costcode_master_id):
        return self.filter(status=1,company_id=company_id,costcode_master_id=costcode_master_id)
    
    def getallcode_by_masterid_mainid(self,company_id,costcode_master_id,costcode_main_id):
        return self.filter(status=1,company_id=company_id,costcode_master_id=costcode_master_id,costcode_main_id=costcode_main_id)
    
    def getallsubcode_bymainids(self,main_id):
        # main_id_string = ', '.join(str(id) for id in main_ids)
        return self.filter(status=1,costcode_main_id=main_id)
    
    def getcostcodemain_byorder(self,order,company_id,costcode_main_id):
        return self.filter(order=order,company_id=company_id,costcode_main_id=costcode_main_id).select_related('costcode_main')
    
    def getcostcodemain_byorder_costcodemain(self,order,company_id,costcode_main_id):
        return self.filter(order=order,company_id=company_id,costcode_main_id=costcode_main_id).select_related('costcode_main')

    def getcostcodesub_by_master_order(self,order,company,costcode_master_id,costcode_main_id):
        try:
            return self.get(company=company,order=order,costcode_master_id=costcode_master_id,costcode_main_id=costcode_main_id)
        except ObjectDoesNotExist:
            return ""
    
    def getlastorder(self,company_id):
        return self.filter(company_id=company_id).last()
    
    def updatecostcode_preview_byorder(self,order,costcode_main_id,costcode_preview):
        return self.filter(order=order,costcode_main_id=costcode_main_id).update(costcode_preview=costcode_preview)
    
    def check_nextcode_available(self,company_id,costcode_master_id,costcode_main_id,costcode):
        return self.filter(status=1,company_id=company_id,costcode_master_id=costcode_master_id,costcode_main_id=costcode_main_id,cost_code=costcode)
        
    
    def getcostcodesub_by_limit_offset(self,offset,limit,company_id,search_value):
        return self.select_related('cost_type').filter(Q(company_id=company_id) & Q(cost_type__component_name__icontains=search_value)).values('order','costcode_main_id').distinct()[offset:offset+limit]
    
    def getcostcodesub_total(self,company_id,search_value):
        return self.select_related('cost_type').filter(Q(company_id=company_id) & Q(cost_type__component_name__icontains=search_value)).values('order','costcode_main_id').distinct()
    
    def getcostcodesub_by_limit_offset_costcodemain(self,offset,limit,company_id,search_value,allcostcode):
        return self.select_related('cost_type').filter(Q(company_id=company_id) & Q(status=1) & (Q(cost_type__component_name__icontains=search_value) | Q(costcode_main__level1_discipline__name__icontains=search_value) | Q(costcode_main__level1_developmenttype__development_type__icontains=search_value) | Q(costcode_main__level2_discipline__discipline_subtype__icontains=search_value)) & Q(costcode_main_id__in=allcostcode)).values('order','costcode_main_id').distinct()[offset:offset+limit]
    
    def getcostcodesub_by_total_costcodemain(self,company_id,search_value,allcostcode):
        return self.select_related('cost_type').filter(Q(company_id=company_id) & Q(status=1) & (Q(cost_type__component_name__icontains=search_value) | Q(costcode_main__level1_discipline__name__icontains=search_value) | Q(costcode_main__level1_developmenttype__development_type__icontains=search_value) | Q(costcode_main__level2_discipline__discipline_subtype__icontains=search_value)) & Q(costcode_main_id__in=allcostcode)).values('order','costcode_main_id').distinct()
    
    def getcostcodesub_component_details(self,id):
        return self.select_related('cost_type').get(id=id)
    
    def getcostcodesub_by_costtype_id(self,cost_type_id,company_id,costcode_main_id):
        return self.filter(cost_type_id=cost_type_id,company_id=company_id,status=1,costcode_main_id=costcode_main_id)

    def getprevious_costcode(self,costcode_sub_id,order):
        return self.filter(order=order,id__lt=costcode_sub_id).order_by('-id').first()

    def getnext_costcode(self,costcode_sub_id,order):
        return self.filter(order=order,id__gt=costcode_sub_id).order_by('-id').first()



class CostCodeSub(models.Model):
    id = models.AutoField(primary_key=True)
    costcode_main=models.ForeignKey('CostCodeMain',on_delete=models.CASCADE,blank=True,null=True)
    cost_type=models.ForeignKey('CostCodeType',on_delete=models.CASCADE,blank=True,null=True)
    cost_code=models.CharField(max_length=25,verbose_name="Cost Code", blank=True, null=True)
    order=models.IntegerField(blank=True, null=True)
    status=models.BooleanField(blank=True, null=True,default=1)
    company=models.ForeignKey("custom_auth.Companies",on_delete=models.CASCADE,blank=True, null=True)
    costcode_preview=models.CharField(max_length=100,verbose_name="Cost Code Preview", blank=True, null=True)
    costcode_master=models.ForeignKey('CostCodeMaster',on_delete=models.CASCADE,blank=True,null=True)

    objects=CostCodeSubManager()
