from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'cost_code'
 
urlpatterns = [
    path('costcodemasterlist',views.listCostCodeMaster.as_view(),name='costcodemasterlist'),
    path('costcodetypelist/<int:pk>',views.listCostCodeType.as_view(),name='costcodetypelist'),
    path('createcostcodetype/<str:level_id>/',views.CreateCostCodeType.as_view(),name='createcostcodetype'),
    path('costcodelist',views.listCostCode.as_view(),name='costcodelist'),
    path('generate_cost_code',views.GenerateCostCode.as_view(),name='generate_cost_code'),
    path('createcostcode',views.CreateCostCodeMaster.as_view(),name='createcostcode'),
    path('costcodetypeedit/<int:pk>',views.editCostCodeType.as_view(),name='costcodetypeedit'),
    path('checkcostcodetype',views.CheckCostCodetype.as_view(),name='checkcostcodetype'),
    path('checkcostcomponent',views.CheckCostComponent.as_view(),name='checkcostcomponent'),
    path('checkcostcodenumber',views.CheckCostcodeNumber.as_view(),name='CheckCostcodeNumber'),
    path('costcodetypedownloadtemplate/<int:pk>',views.CreateCostCompxl.as_view(),name='costcodetypedownloadtemplate'),
    path('importcostcodecomponent',views.ImportCostCodeType.as_view(),name='importcostcodecomponent'),
    path('listcostcodevendor',views.listCostCodeVendor.as_view(),name='listcostcodevendor'),
    path('createcostcodevendor',views.CreateCostCodeVendor.as_view(),name='createcostcodevendor'),
    path('getlevel2_costcode',views.getlevel2_costcode,name='getlevel2_costcode'),
    path('editcostcode/<int:order>/<int:maincode>',views.EditCostCode.as_view(),name='editcostcode'),
    path('deletecostcode/<int:order>/<int:maincode>',views.DeleteCostCode.as_view(),name='deletecostcode'),
    path('getvendorcostcode',views.GetVendorCostCode.as_view(),name='getvendorcostcode'),
    path('vendorcostcodeview/<str:vendor>',views.CostCodeVendorView.as_view(),name='vendorcostcodeview'),
    path('check_costcode_exists',views.check_costcode_exists,name='check_costcode_exists'),
    path('check_costcode',views.check_costcode,name='check_costcode'),
    path('level1costcode',views.level1costcode,name='level1costcode'),
    path('importcostcode',views.ImportCostCode.as_view(),name='importcostcode'),
    path('downloadcostcode_template',views.downloadcostcode_template,name='downloadcostcode_template'),
    path('exportcostcode',views.ExportCostCode.as_view(),name='exportcostcode'),
    path('generatecostcode_excel',views.Generatecostcode_excel.as_view(),name='generatecostcode_excel'),
    path('selectcategory',views.SelectCodeCategory.as_view(),name='selectcodecategory'),
    path('editcostcodemaster',views.Editcostcodemaster.as_view(),name='editcostcodemaster'),
    path('getmaxval/',views.getmaxvalue.as_view(),name='getmaxvalue'),
    path('deletevendorcostcode/',views.deletevendorcostcode.as_view(),name="deletevendorcostcode"),
    path('costcodevendorpdf/',views.Generatecostcodevendor_excel.as_view(),name='costcodevendorpdf'),
    path('importcostcodegenerate/',views.ImportCostCodeGenerateType.as_view(),name='ImportCostCodeGenerateType'),
    path('importcostcodegenerateone/',views.ImportCostCodeStepOne.as_view(),name='importcostcodegenerateone'),
    path('getlevelbyid',views.GetLevelbyId.as_view(),name="getlevelbyid"),
    path('getcosttype',views.DuplicateCostTypeCheck.as_view(),name="getcosttype"),
    path('getmasterid',views.GetMasterId.as_view(),name='getmasterid'),
    path('getcostcodevalues',views.GetCostCodeValues.as_view(),name='getcostcodevalues'),
    path('getgeneratecostcode',views.GetCodeGenerate.as_view(),name='getgeneratecostcode'),
    path('costcodevendor/<str:vendor>',views.GenerateVendorPdf.as_view(),name='generatevendorpdf'),
    path('deletemaster/',views.DeleteMaster.as_view(),name="deletemaster"),
    path('getcosttypevalues',views.GetCostTypeValue.as_view(),name="getcosttypevalues"),
    path('validatecclevel/',views.validatecclevel.as_view(),name='validate-costcode-level'),
    path('createcostcoderangetype/<str:level_id>/<int:id>/',views.CreateCostCodeRangeType.as_view(),name='createcostcoderangetype'),
    path('validatecostcoderange/',views.validatecostcoderange.as_view(),name='validatecostcoderange'),
    path('generatevendorreport/<int:pk>',views.generateVendorReport,name='generateVendorReport'),
    path('displaycost_code',views.Displaycostcode.as_view(),name='displaycost_code'),
    path('getcost_code/',views.getcost_code,name='getcost_code'),
    path('add_sequence/',views.Addsequence.as_view(),name='add_sequence'),
    path('check_sequence_exist/',views.check_sequence_exist,name='check_sequence_exist'),
    path('getcomponent/',views.getcomponent,name='getcomponent'),
    path('update_costcode_status/',views.update_costcode_status,name='update_costcode_status'),
    path('getvendor_costcode/',views.getvendor_costcode,name='getvendor_costcode'),
    path('getvendorcostcode_bycontract/<int:pk>',views.getvendorcostcode_bycontract,name='getvendorcostcode_bycontract'),


    

]