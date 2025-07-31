from django.shortcuts import render
from django.views.generic import View,DeleteView
from projectflow.models import *
from projects.models import *
from InvoiceGuard.models import *
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.core import serializers
import json
from projects.helpers import create_user_log

# Create your views here.
class createflowlevel(View):
    def get(self,request,pk):
        project = Projectcreation.objects.select_related('projectname','flow').get(company=request.company,id=pk)
        # print(f"project {project}")
        data={}
        if(project.flow_level=='clusters'):
            data['clusters']=ProjectCluster.objects.filter(project_id=pk)
        elif(project.flow_level=='discipline'):
            data['discipline']=list(ProjectDevelopmentSubType.objects.filter_by_project(pk,1).values('discipline_subtype__discipline_subtype','project_discipline__project_discipline','id','project_discipline__cluster__clustersubname__cluster_subname'))
            # data['discipline']=ProjectDevelopmentSubType.objects.filter(project_id=pk).select_related('discipline_subtype')
        else:
            # data['well']=WellSub.objects.filter(project_id=pk)
            well_data_list=[]
            get_discipline=list(ProjectWellName.objects.filter_by_project(pk,1).values('welltype__discipline_type__discipline_subtype__discipline_subtype','welltype__discipline_type_id','welltype__discipline_type__project_discipline__project_discipline','welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname'))
            new_list=[dict(t) for t in {tuple(d.items()) for d in reversed(get_discipline)}]
            for discipline in new_list:
                project_discipline=""
                if discipline['welltype__discipline_type__project_discipline__project_discipline'] == "1":
                    project_discipline="Green Field Development"
                elif discipline['welltype__discipline_type__project_discipline__project_discipline'] == "2":
                    project_discipline="Brown Field Development"    
                else:
                    project_discipline="Others"
            #     data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
            #     get_well_type=ProjectWellType.objects.get_by_discipline(pk,discipline['welltype__discipline_type_id'],1)
            #     well_data=list(ProjectWellName.objects.filter_by_well_type(pk,get_well_type.id,1).values('wellname__well_subname','id'))
            #     data_obj.update({'well_datas':well_data})
            #     well_data_list.append(data_obj)
            # data['well']=well_data_list
                data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
                get_well_type=ProjectWellType.objects.filter_by_discipline(pk,discipline['welltype__discipline_type_id'],1)
                well_array=[]
                for well_type in get_well_type:
                    well_data=list(ProjectWellName.objects.filter_by_well_type(pk,well_type.id,1).values('wellname__well_subname','id'))
                    well_array.extend(well_data)
                data_obj['well_datas']=well_array
                well_data_list.append(data_obj)
            data['well']=well_data_list
        return render(request,'createlevel.html',{'project':project,'leveltypes':data})

    def post(self,request,pk):
        level_ids=request.POST.getlist('level_type_id')
        wellbased_type_id=request.POST.getlist('wellbased_type_id')
        project_name = request.POST.get('project_name_user_log')
        print(f"post data {request.POST}")
        project = Projectcreation.objects.select_related('projectname','flow').get(company=request.company,id=pk)
        if (project.flow_level == "well"):
            process=FlowProcess.objects.getprocess_byflow(project.flow_id)
            for level in wellbased_type_id:
                for process_data in process:
                    no_of_stations=request.POST.get('wellbased_type_stations_'+str(level)+'_'+str(process_data['id']))
                    if(no_of_stations):
                        # print('well daya',pk,level,no_of_stations,process_data['id'],request.company,project.flow_level,project.flow.id)
                        projectflow_level=ProjectFlowlevel.objects.createprojectflowlevelwellbased(pk,level,no_of_stations,process_data['id'],request.company,project.flow_level,project.flow.id)

                        for i in range(0,int(no_of_stations)):
                            module_id=request.POST.get('wellbased_type_module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                            no_of_users=request.POST.get('wellbased_type_nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                            role_id=request.POST.get('wellbased_type_role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                            project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,projectflow_level,role_id)
                            # print(no_of_users,request.company,module_id,pk,role_id)
                            module_users=request.POST.getlist('wellbased_type_moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                            for user in module_users:
                                # print(request.company,user,pk)
                                ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,projectflow_level)
                                

        process=FlowProcess.objects.getprocess_byflow(project.flow_id)
        for level in level_ids:
            for process_data in process:
                no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
                if(no_of_stations):
                    # print(pk,level,no_of_stations,process_data['id'],request.company,project.flow_level,project.flow.id)
                    projectflow_level=ProjectFlowlevel.objects.createprojectflowlevel(pk,level,no_of_stations,process_data['id'],request.company,project.flow_level,project.flow.id)

                    for i in range(0,int(no_of_stations)):
                        module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                        no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                        if no_of_users:
                            no_of_users=no_of_users
                        else:
                            no_of_users=None
                        role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                        project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,projectflow_level,role_id)
                        print(f'project_flow_modules {project_flow_modules}')
                        # print(no_of_users,request.company,module_id,pk,role_id)
                        module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                        for user in module_users:
                            # print(request.company,user,pk)
                            ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,projectflow_level)
      
        usercreate = request.user.roles_id
        create_user_log(request,project_name,' Invoice Approval Workflow','Create','Invoice Approval Workflow Created',usercreate)        
                          

        return redirect('projects:projectinvoiceflow')  

class editflowlevel(View):
    def get(self,request,pk):
        project = Projectcreation.objects.select_related('projectname','flow').get(company=request.company,id=pk)
        flow_process=FlowProcess.objects.getprocess_byflow(project.flow_id)
        data={}
        if(project.flow_level=='clusters'):
            data['clusters']=ProjectCluster.objects.filter(project_id=pk)
        elif(project.flow_level=='discipline'):
            data['discipline']=list(ProjectDevelopmentSubType.objects.filter_by_project(pk,1).values('discipline_subtype__discipline_subtype','project_discipline__project_discipline','id','project_discipline__cluster__clustersubname__cluster_subname'))
            # data['discipline']=ProjectDevelopmentSubType.objects.filter(project_id=pk).select_related('discipline_subtype')
        else:
            # data['well']=WellSub.objects.filter(project_id=pk)
            well_data_list=[]
            get_discipline=list(ProjectWellName.objects.filter_by_project(pk,1).values('welltype__discipline_type__discipline_subtype__discipline_subtype','welltype__discipline_type_id','welltype__discipline_type__project_discipline__project_discipline','welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname'))
            new_list=[dict(t) for t in {tuple(d.items()) for d in reversed(get_discipline)}]
            for discipline in new_list:
                project_discipline=""
                if discipline['welltype__discipline_type__project_discipline__project_discipline'] == "1":
                    project_discipline="Green Field Development"
                elif discipline['welltype__discipline_type__project_discipline__project_discipline'] == "2":
                    project_discipline="Brown Field Development"    
                else:
                    project_discipline="Others"
                data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
                get_well_type=ProjectWellType.objects.filter_by_discipline(pk,discipline['welltype__discipline_type_id'],1)
                well_array=[]
                for well_type in get_well_type:
                    well_data=list(ProjectWellName.objects.filter_by_well_type(pk,well_type.id,1).values('wellname__well_subname','id'))
                    well_array.extend(well_data)
                data_obj['well_datas']=well_array
                well_data_list.append(data_obj)
            data['well']=well_data_list
            #     data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
            #     get_well_type=ProjectWellType.objects.get_by_discipline(pk,discipline['welltype__discipline_type_id'],1)
            #     well_data=list(ProjectWellName.objects.filter_by_well_type(pk,get_well_type.id,1).values('wellname__well_subname','id'))
            #     data_obj.update({'well_datas':well_data})
            #     well_data_list.append(data_obj)
            # data['well']=well_data_list
        return render(request,'editlevel.html',{'project':project,'leveltypes':data,'flow_process':flow_process,'project_id':pk,'company':request.company})
       
    def post(self,request,pk):
        level_ids=request.POST.getlist('level_type_id')
        wellbased_type_id=request.POST.getlist('wellbased_type_id')
        project = Projectcreation.objects.select_related('projectname','flow').get(company=request.company,id=pk)
        process=FlowProcess.objects.getprocess_byflow(project.flow_id)
        if (project.flow_level == "well"):    
            print('req',request.POST)
            project_level_wellbased_list=[]
            for level in wellbased_type_id:
                getprojectflow_level=ProjectFlowlevel.objects.filterprojectflow_bylevelwellbased(level,project.flow_level,request.company,pk,project.flow.id)
                if (getprojectflow_level.count() > 0):
                    print('yes')
                    for flow_level in getprojectflow_level:
                        project_level_wellbased_list.append(flow_level.id)
                        for process_data in process:
                            no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
                            check_data=ProjectFlowlevel.objects.filter_id_process_wellbased(flow_level.id,process_data['id']).first()
                            if (check_data):
                                print('check_data',check_data)
                                print(flow_level.id,process_data['id'],no_of_stations)
                                ProjectFlowlevel.objects.updateprojectlevel_by_level_wellbased_id(flow_level.id,process_data['id'],no_of_stations)
                                level_based_project_module_list=[]
                                for i in range(0,int(no_of_stations)):
                                    module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i),None)
                                    projectflowmodule_id=request.POST.get('projectflowmodule_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                                    no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                                    if not no_of_users:
                                        no_of_users=None
                                    role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                                    if (projectflowmodule_id):
                                        level_based_project_module_list.append(projectflowmodule_id)
                                        print('exsist pfm')
                                        projectmodules=ProjectFlowModules.objects.update_projectflowmodules(flow_level.id,projectflowmodule_id,module_id,no_of_users,role_id)
                                        module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                                        print('users',module_users)
                                        users_list=[]
                                        for user in module_users:
                                            getprojectflowusers=ProjectFlowModuleUsers.objects.getflowusers_by_user_module(projectflowmodule_id,user,flow_level)
                                            if(getprojectflowusers==None):
                                                print('new usrr',user)
                                                get_project_modules=ProjectFlowModules.objects.get_project_flowmodule(flow_level.id,projectflowmodule_id)
                                                create_new_user=ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(get_project_modules,request.company,user,pk,flow_level)
                                                users_list.append(create_new_user.id)
                                            else:
                                                print('old usrr',user)
                                                ProjectFlowModuleUsers.objects.update_user_status(projectflowmodule_id,user,flow_level)
                                                users_list.append(getprojectflowusers.id)
                                        ProjectFlowModuleUsers.objects.remove_users_status(projectflowmodule_id,flow_level,users_list)
                                    else:
                                        print('new pfm')
                                        project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,flow_level,role_id)
                                        level_based_project_module_list.append(project_flow_modules.id)
                                        module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                                        for user in module_users:
                                            ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,flow_level)
                                ProjectFlowModules.objects.remove_modules_status(flow_level,level_based_project_module_list)
                                ProjectFlowModuleUsers.objects.remove_users_flowlevel(flow_level.id,level_based_project_module_list)
                else:
                    print('new pfl',level)
                    for process_data in process:
                        no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
                        if(no_of_stations):
                            projectflow_level=ProjectFlowlevel.objects.createprojectflowlevelwellbased(pk,level,no_of_stations,process_data['id'],request.company,project.flow_level,project.flow.id)
                            project_level_wellbased_list.append(projectflow_level.id)
                            for i in range(0,int(no_of_stations)):
                                module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                                no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                                role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                                project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,projectflow_level,role_id)
                                module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                                for user in module_users:
                                    ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,projectflow_level)
            ProjectFlowlevel.objects.remove_level_wellbased_status(request.company,pk,project_level_wellbased_list,project.flow.id)

        project_level_list=[]
        for level in level_ids:
            getprojectflow_level=ProjectFlowlevel.objects.filterprojectflow_bylevel(level,project.flow_level,request.company,pk,project.flow.id)
            if (getprojectflow_level.count() > 0):
                #append getprojectflow_level ids
                for flow_level in getprojectflow_level:
                    project_level_list.append(flow_level.id)
                    for process_data in process:
                        no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
                        check_data=ProjectFlowlevel.objects.filter_id_process(flow_level.id,process_data['id']).first()
                        if (check_data):
                            print(flow_level.id,process_data['id'],no_of_stations)
                            ProjectFlowlevel.objects.updateprojectlevel_by_levelid(flow_level.id,process_data['id'],no_of_stations)
                            project_module_list=[]
                            for i in range(0,int(no_of_stations)):
                                module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i),None)
                                projectflowmodule_id=request.POST.get('projectflowmodule_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                                no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                                if not no_of_users:
                                    no_of_users=None
                                role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                                if (projectflowmodule_id):
                                    project_module_list.append(projectflowmodule_id)
                                    # print('exsist pfm')
                                    projectmodules=ProjectFlowModules.objects.update_projectflowmodules(flow_level.id,projectflowmodule_id,module_id,no_of_users,role_id)
                                    module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                                    # print('users',module_users)
                                    users_list=[]
                                    for user in module_users:
                                        getprojectflowusers=ProjectFlowModuleUsers.objects.getflowusers_by_user_module(projectflowmodule_id,user,flow_level)
                                        if(getprojectflowusers==None):
                                            get_project_modules=ProjectFlowModules.objects.get_project_flowmodule(flow_level.id,int(projectflowmodule_id))
                                            create_new_user=ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(get_project_modules,request.company,user,pk,flow_level)
                                            users_list.append(create_new_user.id)
                                        else:
                                            print('old usrr',user)
                                            ProjectFlowModuleUsers.objects.update_user_status(projectflowmodule_id,user,flow_level)
                                            users_list.append(getprojectflowusers.id)
                                    ProjectFlowModuleUsers.objects.remove_users_status(projectflowmodule_id,flow_level,users_list)
                                else:
                                    print('new pfm')
                                    project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,flow_level,role_id)
                                    project_module_list.append(project_flow_modules.id)
                                    module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                                    for user in module_users:
                                        ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,flow_level)
                            ProjectFlowModules.objects.remove_modules_status(flow_level,project_module_list)
                            ProjectFlowModuleUsers.objects.remove_users_flowlevel(flow_level.id,project_module_list)
            else:
                print('new pfl',level)
                # project_level_list.append(level)
                for process_data in process:
                    no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
                    if(no_of_stations):
                        projectflow_level=ProjectFlowlevel.objects.createprojectflowlevel(pk,level,no_of_stations,process_data['id'],request.company,project.flow_level,project.flow.id)
                        project_level_list.append(projectflow_level.id)
                        for i in range(0,int(no_of_stations)):
                            module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                            no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i),None)
                            role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                            project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,projectflow_level,role_id)
                            module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                            for user in module_users:
                                ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,projectflow_level)
        ProjectFlowlevel.objects.remove_level_status(request.company,pk,project_level_list,project.flow.id)
            # if(getprojectflow_level==None):
                # print('new',level)
            #     for process_data in process:
            #         no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
            #         if(no_of_stations):
            #             projectflow_level=ProjectFlowlevel.objects.createprojectflowlevel(pk,level,no_of_stations,process_data['id'],request.company,project.flow_level)
            #             for i in range(1,int(no_of_stations)+1):
            #                 module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
            #                 no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
            #                 role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
            #                 project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,projectflow_level,role_id)
            #                 module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
            #                 for user in module_users:
            #                     ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,projectflow_level)
            # else:
                # print(f"post {request.POST}")
                # print(f"old {level}")
                # for process_data in process:
                #     no_of_stations=request.POST.get('stations_'+str(level)+'_'+str(process_data['id']))
                #     if(no_of_stations):
                #         print('ns',no_of_stations,process_data['process_id'])
                #         print(ProjectFlowlevel.objects.filter(id=level_id,process_id=process_data))
                        # projectflow_level=ProjectFlowlevel.objects.updateprojectlevel_by_levelid(getprojectflow_level.id,no_of_stations)
                        # for i in range(0,int(no_of_stations)):
                        #     module_id=request.POST.get('module_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                        #     projectflowmodule_id=request.POST.get('projectflowmodule_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(i))
                        #     no_of_users=request.POST.get('nouser_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                        #     role_id=request.POST.get('role_id_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                        #     projectmodules=ProjectFlowModules.objects.getprojectmodules_by_level_module_role(getprojectflow_level.id,module_id,role_id)
                        #     if(projectflowmodule_id):
                        #         project_flow_modules=ProjectFlowModules.objects.updateprojectflowmodules(no_of_users,module_id,role_id,projectflowmodule_id)
                        #         module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                        #         for user in module_users:
                        #             getprojectflowusers=ProjectFlowModuleUsers.objects.getflowusers_by_user_module(projectmodules.id,user,projectflow_level)
                        #             if(getprojectflowusers==None):
                        #                 ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(projectmodules,request.company,user,pk,getprojectflow_level)
                        #     else:
                        #         project_flow_modules=ProjectFlowModules.objects.createprojectflowmodules(no_of_users,request.company,module_id,pk,getprojectflow_level,role_id)
                        #         module_users=request.POST.getlist('moduleusers_'+str(level)+'_'+str(process_data['id'])+'_'+str(module_id)+'_'+str(i))
                        #         for user in module_users:
                        #             ProjectFlowModuleUsers.objects.createProjectFlowModuleUsers(project_flow_modules,request.company,user,pk,getprojectflow_level)
        return redirect('projects:projectinvoiceflow')  
        

class createProcessflow(View):
    def get(self,request,pk):
        project = Projectcreation.objects.select_related('projectname').get(company=request.company,id=pk)
        flows=Flow.objects.getallflows(request.company)
        return render(request,'createflow.html',{'project':project,'flows':flows})

    def post(self,request,pk):
        print('re',request.POST)
        bank_user=request.POST.get('bank_user',0)
        Projectcreation.objects.filter(id=pk).update(flow_id=request.POST['flow_id'],flow_level=request.POST['flow_level'],invoice_bank_user=1)
        checkflowlevel_byproject=ProjectFlowlevel.objects.getprojectflowlevel_by_project_id(pk)
        ProjectFlowlevel.objects.update_flow_level_name(pk,request.POST['flow_level'])
        print(f"checkflowlevel_byproject {checkflowlevel_byproject.count()}")
        if(request.POST['submit_type'] == '0'):
            return redirect('projects:projectinvoiceflow') 
        else:
            if(checkflowlevel_byproject.count() > 0):
                return redirect('projectflow:editflowlevel',pk=pk)
            else:
                return redirect('projectflow:createflowlevel',pk=pk)

def getprocess_byflow(request):
    flow_id=request.GET['flow_id']
    process=FlowProcess.objects.getprocess_byflow(flow_id)
    process_data=list(process)
    return JsonResponse({'process':process_data})

def getmodule_byprocess(request):
    process_id=request.GET['process_id']
    modules=ProcessModule.objects.getmodule_byprocess(process_id)
    modules_data=list(modules)
    return JsonResponse({'modules':modules_data})

def getroles_and_projectusers(request):
    project_id=request.GET['project_id']
    module_id=request.GET['module_id']
    roles=Role.objects.filter_by_module_id(module_id,request.company)
    projectusers=ProjectUser.objects.getuser_byproject(project_id)
    roles_data=list(roles)
    projectusers_data=list(projectusers)
    data={
        'roles_data':serializers.serialize('json', roles_data),
        'projectusers_data':projectusers_data
    }
    return JsonResponse(data, safe=False)

def get_signatories(request):
    project_id=request.GET['project_id']
    module_id=request.GET['module_id']
    projectname=request.GET['projectname']
    roles=Role.objects.filter_by_module_id(module_id,request.company)
    get_project_signatories=SignatoriesSettings.objects.filter_by_project(projectname,request.company.id,2,1)
    print('juhabkj',get_project_signatories)
    if (get_project_signatories.count() > 0):
        print('asdfd')
        filtered_ids=get_project_signatories.values_list('id',flat=True)
    else:
        get_project_signatories=SignatoriesSettings.objects.filter_by_project(None,request.company.id,1,1)
        filtered_ids=get_project_signatories.values_list('id',flat=True)
    users_list=list(SignatoriesUsers.objects.filter_by_signatoryIds(filtered_ids).select_related('user').annotate(user__id=F('signatory__currency__currency_symbol')).values('id','user__name','user__lastname','user__designation_role','signatory__currency__currency_symbol'))
    # print('users_list',users_list)
    # print('get_project_signatories',SignatoriesUsers.objects.select_related('user').annotate(user__id=F('user__id')).values('id','user__name','user__lastname','user__designation_role'))
    #  users_list.values_list('user',flat=True)
    # projectusers=ProjectUser.objects.getuser_byproject(project_id)
    roles_data=list(roles)
    # projectusers_data=list(projectusers)
    data={
        'roles_data':serializers.serialize('json', roles_data),
        'users_list':users_list,
        # 'projectusers_data':projectusers_data
    }
    return JsonResponse(data, safe=False)

def checkprojectflow_level(request):
    level_id=request.GET['level_id']
    level_type=request.GET['level_type']
    project_id=request.GET['project_id']
    process_id=request.GET['process_id']
    get_process=request.GET['get_process']
    projectflow_level=ProjectFlowlevel.objects.getprojectflow_bylevel(level_id,level_type,request.company,project_id,get_process)
    if(projectflow_level):
        project_flowlevel_dict = serializers.serialize('python', [projectflow_level])[0]['fields']
        json_data = json.dumps(project_flowlevel_dict)
    else:
        json_data = ''
    modules=ProcessModule.objects.getmodule_byprocess(process_id)
    modules_data=list(modules)
    if(projectflow_level):
        status=True
    else:
        status=False
    data={
        'projectflow_level':json_data,
        'status':status,
        'modules':modules_data
    }
    return JsonResponse(data, safe=False)

def delete_level(request):
    level_id=request.GET['level_id']
    level_type=request.GET['level_type']
    project_id=request.GET['project_id']
    # getprojectflow_level=ProjectFlowlevel.objects.getprojectflow_bylevel(level_id,level_type,request.company,project_id)
    # ProjectFlowModuleUsers.objects.deleteprojectflowusers_by_levelid(getprojectflow_level.id,request.company,project_id)
    # ProjectFlowModules.objects.deleteprojectmodules_by_levelid(getprojectflow_level.id,request.company,project_id)
    # ProjectFlowlevel.objects.deleteprojectlevel_by_levelid(getprojectflow_level.id,request.company,project_id)
    return JsonResponse(True, safe=False)

class ProjectInvoiceFlowView(View):
    def get(self,request,pk):
        project = Projectcreation.objects.select_related('projectname','flow').get(company=request.company,id=pk)
        flow_process=FlowProcess.objects.getprocess_byflow(project.flow_id)
        data={}
        if(project.flow_level=='clusters'):
            data['clusters']=ProjectCluster.objects.filter(project_id=pk)
        elif(project.flow_level=='discipline'):
            data['discipline']=list(ProjectDevelopmentSubType.objects.filter_by_project(pk,1).values('discipline_subtype__discipline_subtype','project_discipline__project_discipline','id','project_discipline__cluster__clustersubname__cluster_subname'))
            # data['discipline']=ProjectDevelopmentSubType.objects.filter(project_id=pk).select_related('discipline_subtype')
        else:
            # data['well']=WellSub.objects.filter(project_id=pk)
            well_data_list=[]
            get_discipline=list(ProjectWellName.objects.filter_by_project(pk,1).values('welltype__discipline_type__discipline_subtype__discipline_subtype','welltype__discipline_type_id','welltype__discipline_type__project_discipline__project_discipline','welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname'))
            new_list=[dict(t) for t in {tuple(d.items()) for d in reversed(get_discipline)}]
            for discipline in new_list:
                project_discipline=""
                if discipline['welltype__discipline_type__project_discipline__project_discipline'] == "1":
                    project_discipline="Green Field Development"
                elif discipline['welltype__discipline_type__project_discipline__project_discipline'] == "2":
                    project_discipline="Brown Field Development"    
                else:
                    project_discipline="Others"
            #     data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
            #     get_well_type=ProjectWellType.objects.get_by_discipline(pk,discipline['welltype__discipline_type_id'],1)
            #     well_data=list(ProjectWellName.objects.filter_by_well_type(pk,get_well_type.id,1).values('wellname__well_subname','id'))
            #     data_obj.update({'well_datas':well_data})
            #     well_data_list.append(data_obj)
            # data['well']=well_data_list
                data_obj={'discipline_name':discipline['welltype__discipline_type__discipline_subtype__discipline_subtype'],'discipline_id':discipline['welltype__discipline_type_id'],'project_discipline':project_discipline,'cluster':discipline['welltype__discipline_type__project_discipline__cluster__clustersubname__cluster_subname']}
                get_well_type=ProjectWellType.objects.filter_by_discipline(pk,discipline['welltype__discipline_type_id'],1)
                well_array=[]
                for well_type in get_well_type:
                    well_data=list(ProjectWellName.objects.filter_by_well_type(pk,well_type.id,1).values('wellname__well_subname','id'))
                    well_array.extend(well_data)
                data_obj['well_datas']=well_array
                well_data_list.append(data_obj)
            data['well']=well_data_list
        return render(request,'flowview.html',{'project':project,'leveltypes':data,'flow_process':flow_process,'project_id':pk,'company':request.company})
       








