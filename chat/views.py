import ast
from tabnanny import check
from django.http import JsonResponse
from django.shortcuts import render,redirect
from InvoiceGuard.models.role_right import RoleRight
from chat.models import *
import mimetypes
from django.http import HttpResponse
import json
from custom_auth.models import *
from django.db.models import Count
from notifications.signals import notify
from notifications.models import Notification
import csv
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.files.storage import FileSystemStorage
from projectflow.models.flow import ProjectFlowModuleUsers, ProjectFlowModules, ProjectFlowlevel

from projects.models import ContractMasterVendor,ProjectUser,ContractMaster

from .forms import FileUploadForm
from django.db.models import Q
# Import mimetypes module
import mimetypes
# import os module
import os
import re
from django.views.decorators.clickjacking import xframe_options_exempt

from django.template.loader import render_to_string
from itertools import chain,groupby
from operator import attrgetter

def index(request):

    # # chatdata=Message.object.all();
    # print(chatdata)
    return render(request, 'chat/index.html', {})
@xframe_options_exempt
def room(request, room_name):
   
    # print('working',room_name)
    grouped_objects = {}
    request.session['backurl'] = request.META.get('HTTP_REFERER')
    lasturl=request.session['backurl'] 
    form = FileUploadForm()
    sender=request.user.id
    roles_id = User.objects.get(id=sender)
    lastchats=Message.objects.filter(chatroom_id=room_name)[0:10]
    if(request.user.roles.id==4):
        get_all_vendors=User.objects.filter(company_id=request.company.id,status=1,cin_number=request.user.cin_number).exclude(id=request.user.id)
        a= User.objects.filter(company_id=request.company.id,status=1).exclude(roles_id=4)
        userlists = list(chain(a, get_all_vendors))
    else:
        #use for project wise user 
        userlists= User.objects.filter(company_id=request.company.id,status=1).exclude(id=request.user.id,name__iexact='')
    if (request.user.roles_id==4):
        get_all_vendors=list(User.objects.filter(company_id=request.company.id,status=1,cin_number=request.user.cin_number).exclude(id=request.user.id).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary')) 
        # users=list(User.objects.filter(company_id=request.company.id,status=1).exclude(roles_id=4).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary'))  
        # userlistdata = list(chain(users, get_all_vendors))
        getvendordetails=ContractMasterVendor.objects.getvendor_byvin(request.user.cin_number,request.company)
        all_contracts=ContractMaster.objects.filter(contractvendor_id=getvendordetails.id,status=1).values_list('projects_id',flat=True).distinct()
        get_roles=RoleRight.objects.filter_by_right_slug(request.company,'communicate-with-vendor').values_list('role_id',flat=True)
        rights_based_user_list=[]
        for project_data in all_contracts:
            get_project_level=ProjectFlowlevel.objects.getprojectflowlevel_by_project_id(project_data)
            for level in get_project_level:
                project_flow_modules=ProjectFlowModules.objects.filter(projectflow_level_id=level.id,status=0,project_id=project_data,role_id__in=get_roles).values_list('id',flat=True)
                users_list=list(ProjectFlowModuleUsers.objects.filter(status=0,ProjectFlowModules_id__in=project_flow_modules).values_list('user__user_id',flat=True))
                rights_based_user_list.extend(users_list)
        remove_duplicate_users=list(set(rights_based_user_list))
        # print('rights_based_user_list',rights_based_user_list)
        users=list(User.objects.filter(id__in=remove_duplicate_users).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary','user_department_id','user_department__department'))
        userlistdata = list(chain(get_all_vendors,users))
        userlistdata = [dict(item, **{'type':'single'}) for item in userlistdata]
    else:
        get_projects=ProjectUser.objects.getprojectuser_byuserid(request.user.id)
        project_ids_list=get_projects.values_list('project_id',flat=True)
        get_all_projects_user=ProjectUser.objects.getuser_byproject_ids(project_ids_list).exclude(user_id=request.user.id).values_list('user_id',flat=True).distinct()
        if (request.user.roles_id == 2):
            userlistdata=list(User.objects.filter(company_id=request.company.id,status=1).exclude(id=request.user.id).exclude(roles_id=4).exclude(roles_id=None).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary','user_department_id','user_department__department'))
            bank_users_query=list(User.objects.filter(company_id=request.company.id,status=1,roles_id=None).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary','user_department_id','user_department__department'))
            bank_users_list=[{**item, "user_department__department": "Bank User"} for item in bank_users_query]
            userlistdata.extend(bank_users_list)

        elif (request.user.roles_id == 3):
            userlistdata=list(User.objects.filter(id__in=get_all_projects_user).exclude(roles_id=3).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary','user_department_id','user_department__department'))
            userlistdata.extend(list(User.objects.filter(company_id=request.company.id,status=1,roles_id=2).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary','user_department_id','user_department__department')))
            for user_data in userlistdata:
                if user_data.get('user_department__department') == None:
                    user_data['user_department__department']="Client Administrator"
                    break

        userlistdata = [dict(item, **{'type':'single'}) for item in userlistdata]
        # filtered_list = [item for item in userlistdata if item.get('user_department__department') is not None]
        # print('filtered_list',filtered_list)
        # userlistdata.sort(key=lambda x: x.get('user_department__department'))
        try:
            userlistdata.sort(key=lambda x: x.get('user_department__department'))
        except:
            userlistdata.sort(key=lambda x: x.get('id'))
        for key, group in groupby(userlistdata, key=lambda x: x.get('user_department__department')):
            grouped_objects[key] = list(group)
            ## Check above code
        vendors_list=list(User.objects.filter(company_id=request.company.id,status=1,roles_id=4).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary'))
        vendors_list = [dict(item, **{'type':'single'}) for item in vendors_list]
        if (request.user.roles_id == 4 and len(vendors_list) > 0):
            grouped_objects['Vendors']=vendors_list
        elif (request.user.roles_id == 3):
            get_pfmusers=ProjectFlowModuleUsers.objects.get_data_user_ids(get_projects.values_list('id',flat=True))
            get_role_ids=ProjectFlowModules.objects.get_data_ids(get_pfmusers.values_list('ProjectFlowModules_id',flat=True))
            get_communicate_rights=RoleRight.objects.filter_by_role_ids(get_role_ids.values_list('role_id',flat=True),"communicate-with-vendor")
            if (len(vendors_list) > 0 and get_communicate_rights.count() > 0):
                grouped_objects['Vendors']=vendors_list
    
        # userlistdata=list(User.objects.filter(company_id=request.company.id,status=1).exclude(id=request.user.id).values('name','id','lastname','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary'))
    grouplist=list(Chatroom.objects.filter(type="group").values_list('id',flat=True))
    # print('userlist',userlist)

    userlistdata = [dict(item, **{'type':'single'}) for item in userlistdata]
    # print("asd",userlistdata)
    # if Chatroom.objects.filter(chatroom_id=room_name,type="single").exists():
    #     receivernames=ChatMembers.objects.filter(chatroom_id=room_name).exclude(user_id=sender).first()
    # else:
    receivernames=ChatMembers.objects.filter(chatroom_id=room_name).exclude(user_id=sender).values_list('user_id',flat=True)
    showusername=User.objects.filter(id__in=receivernames)
    allgrouplist=[]
    for i in grouplist:
        group=ChatMembers.objects.filter(user_id=request.user.id,chatroom_id=i).first()
        if (group != None):
            allgrouplist.append({'name':group.chatroom.name,'id':i,'type':group.chatroom.type})

    userlistdata.extend(allgrouplist)
    # remove dict if type is single and email is empty
    userlistdata = [i for i in userlistdata if not (i['type'] == 'single' and i['name'] == '')]
    current_user= request.user.id
    # getlast_msger=Message.objects.filter(user_id=current_user).order_by('chatroom_id')
    getlast_msger=Message.objects.order_by('-id').values('chatroom_id')
    latest_msg=[]
    for i in getlast_msger:
        # print('i',i['chatroom_id'])
        both=ChatMembers.objects.filter(chatroom_id=i['chatroom_id'],user_id__status=1).filter(user_id=current_user).first()
        # print('both',both.chatroom.id)
        if (both != None):
            if both.chatroom.id not in latest_msg:
                latest_msg.append(both.chatroom.id)
        # check=both[i]['chatroom_id']
        # if i['chatroom_id'] not in latest_msg:
        #     latest_msg.append(i['chatroom_id'])

    # print('latest_msg',latest_msg)
    filterusers=[]
    for j in latest_msg:
        chatroom=Chatroom.objects.filter(id=j).first()
        if( chatroom.type == 'single'):
            stackname=ChatMembers.objects.filter(chatroom_id=j,user_id__status=1).exclude(user_id=current_user).first()
            # print('stackname',stackname)
            user_id=request.user.id
            # print('user_id',user_id)
            if stackname!= None:
                getnotify=Notify_chat.objects.filter(receiver_id=user_id,sender_id=stackname.user.id,read=0,roomid=None)
                # print('getnotify',getnotify)
                # getnotifymsg=Notify_chat.objects.filter(receiver_id=user_id).order_by('-id').valures()
                filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'lastname':stackname.user.lastname,'type':'single','count':getnotify.count()})  
        else:
            grpnotify=Notify_chat.objects.filter(roomid=chatroom.id,read=0,readerstatus=request.user.id)
            filterusers.append({'id':chatroom.id,'name':chatroom.name,'type':'group','count':grpnotify.count()})  
    getmembers=[]
    userlist=[]
    filtermembers=[]
    for group in allgrouplist:
        # print(group['id'])
        # print(type(room_name))
        groupids=str(group['id'])
        if(groupids == room_name):
            # print('inloop')
            groupdetails=ChatMembers.objects.filter(chatroom_id=room_name).values('user_id','chatroom_id')
            # # print('room_name',groupdetails)
            for i  in groupdetails:
                # print(i['user_id'])
                groupmembrs=User.objects.filter(id=i['user_id']).first()
                if (groupmembrs !=None):
                    # print('groupmembrs',groupmembrs.id)
                    userlist.append(groupmembrs.id)
                    filtermembers.append({'name':groupmembrs.name,'id':groupmembrs.id,'status':1})
                    getmembers.append({'name':groupmembrs.name,'id':groupmembrs.id,'roomname':room_name,'lastname':groupmembrs.lastname})
            get=list(User.objects.filter(status=1,company_id=request.user.company.id).exclude(id__in=userlist).values('id','name'))
            newlist=[a.update({"status":0}) for a in get]
            filtermembers.extend(get)
            # print('b',filtermembers)
            # print('get',newlist)
    # 
               
                   

    getgrpname=Chatroom.objects.filter(id=room_name).values('name','type').first()
    # grpnotify=Notify_chat.objects.filter(roomid=room_name)


  
    
    return render(request, 'chat/chatroom.html', {
        'room_name': room_name,
        'form':form,
        'sender':sender, #
        'roles_id':roles_id,
        # 'lastchat':lastchats, #
        'userlist':userlists, #4
        #'grouplist':allgrouplist, #3
        # 'showusername':showusername, 
        # 'lasturl':lasturl,
        'userlistdata':userlistdata, #2
        'filterusers':filterusers, #
        # 'person_notify':data
        'getmembers':filtermembers, #1
        # 'getgrpname':getgrpname, 
        'grouped_objects':grouped_objects
    })


def file_upload_ajax(request):
    # print('file',request)
    if request.method == 'POST':
        data={'id':'1','file':'dsgsdg'}
        # form = FileUploadForm(request.POST, request.FILES)
        multiplefile=request.FILES.getlist('document')
        for file in multiplefile:
           Fileupload.objects.create(document=file)  

        if (multiplefile):
            count=len(multiplefile)
            fileref=Fileupload.objects.all().order_by('-id')[:count]
            attach=[]
            for i in  fileref:
                attach.append({'id':i.id,'file':i.document.name})
            data=attach            
        return JsonResponse({'data':data})
    else:
        return JsonResponse({'error': True, 'errors': 'form.errors'})

# restoring the previous file with json response
def file_upload_ajax(request):
    # print('in file uplaod')
    # print('file',request)
    if request.method == 'POST':
        data={'id':'1','file':'dsgsdg'}
        # form = FileUploadForm(request.POST, request.FILES)
        multiplefile=request.FILES.getlist('document')
        for file in multiplefile:
           Fileupload.objects.create(document=file)  

        if (multiplefile):
            count=len(multiplefile)
            # print(count)
            fileref=Fileupload.objects.all().order_by('-id')[:count]
            attach=[]
            for i in  fileref:
                attach.append({'id':i.id,'file':i.document.name})
            # return JsonResponse(fileref)
            data=attach
            # print(data)
            
        return JsonResponse({'data':data})
    else:
        return JsonResponse({'error': True, 'errors': 'form.errors'})

def download(request,fileid):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print('bf',BASE_DIR)

    get_filename=Fileupload.objects.filter(id=fileid).first()
    filename = get_filename.document
    # print('filename',filename.path)
    filepath = filename.path
    # return HttpResponse('download error')
    # print('fileparth',filepath)
    
    path = open(filepath, 'rb')
    #  open(file_location,encoding='utf-8') as csvfile:
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # print(response)
    return response
    # return filename.url


   
    # get_filename=Fileupload.objects.filter(id=fileid).first()
    # filename = get_filename.document
    # print('filename',filename)

    # mime_type, _ = mimetypes.guess_type(filepath)
    # Define the full file path
    # # filepath = '/opt/lampp/htdocs/irockmsg/'+str(filename)
    # # print('filname',filepath)
    # # Open the file for reading content
    # path = open(filename, 'r')
    # with open(filename, 'rb') as file:
    #     print(chardet.detect(file.read()))
    # # Return the response value
    # return 'response'
    
def download2(request,fileid):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'icons8-add-user-male-48.png'
    # Define the full file path
    filepath = BASE_DIR + '/media/documents/' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


def message(request):
    # print('messing is working')
    # print('form',request.POST)
    userlist= User.objects.filter(company_id=request.company.id,status=1)
    # print('userlist',userlist)
    grouplist=list(Chatroom.objects.filter(type="group").values_list('id',flat=True))
    # print(grouplist)
    # print('session',request.META.get('HTTP_REFERER'))
    request.session['backurl'] = request.META.get('HTTP_REFERER')
    lasturl=request.session['backurl']
    # print('backurl',lasturl)
    allgrouplist=[]
    for i in grouplist:
        group=ChatMembers.objects.filter(user_id=request.user.id,chatroom_id=i).first()
        if (group != None):
            allgrouplist.append({'groupname':group.chatroom.name,'groupid':i})
    # print('allgrouplist',allgrouplist)
    # currentuser=User.objects.filter(id=request.user.id)
    # print('current',currentuser.id)
 
    current_company=Companies.objects.filter(id=request.company.id)
    # print('cin',current_company[0].cin_number)
    # if (request.POST):
    #     print('d',request.user.id)   
    # a=User.objects.filter(company_id=request.company.id).exclude(id=request.user.id) 
    # print('a',a)
    return render(request, 'chat/message.html', {'userlist':userlist,'current_user':request.user.id,'current_company':current_company,'groupname':allgrouplist,'lasturl':lasturl})




def createroom(request):
    # print('request',request.GET.get('type'))
    # type=request.GET.get('type')
    groupname=request.GET.get('groupname',None)
    # print('grp',groupname)
    senderid=request.GET.get('sender_id',None)
    receiverid=request.GET.get('receiver_id',None)
    # room=Chatroom.objects.filter(Q(sender_id=senderid) | Q(sender_id=receiverid) and Q(receiver_id=senderid) | Q(receiver_id=receiverid)).first()
    # SELECT chatroom_id,COUNT(user_id) as total FROM `chat_chatmembers` WHERE user_id=1 OR user_id=2 GROUP BY chatroom_id HAVING total=2;

    if(groupname != None):
        # print('empty')
        convertreceivers=ast.literal_eval(receiverid)
        convertreceivers.append(request.user.id)
        convertreceivers = list(map(int, convertreceivers))
        # print(convertreceivers)
        if (Chatroom.objects.filter(name__iexact=groupname,company_id=request.company.id).exists()):
            return JsonResponse({'roomid':'exists'})
        else:
            createchatroom=Chatroom.objects.create(name=groupname,type='group',company_id=request.company.id)
            roomid=createchatroom.id
            creategroupdata=[]
            for i in convertreceivers:
                if i == request.user.id:
                    creategroupdata.append(ChatMembers(chatroom_id=roomid,user_id=i,group_owner=True))
                else:
                    creategroupdata.append(ChatMembers(user_id=i,chatroom_id=roomid))
            ChatMembers.objects.bulk_create(creategroupdata)
            return JsonResponse({'roomid':roomid})
    else:
        # print('skjdlfksdlf')
        senderid=request.user.id
        # print(senderid,receiverid)
        q=list(ChatMembers.objects.values('chatroom_id').filter(Q(user_id=senderid) | Q(user_id=receiverid)).annotate(total=Count('chatroom_id')).filter(total=2))
        # print('sadsa',q)
        # print('getroom',q[0]['chatroom_id'])
        # print('len',len(q))
        datalist=[x['chatroom_id'] for x in q]
        singlelist=Chatroom.objects.filter(id__in=datalist,type='single').values_list('id',flat=True)
        # print("datalist",datalist)
        if (len(singlelist) > 0):
            
            roomid=singlelist[0]
            # totalvalue=singlelist[0]['total']
            # if (totalvalue == 2):
            #     print('exists')
                # roomid=singlelist[0]['chatroom_id']
            # else:
            #     print('create')
            #     createchatroom=Chatroom.objects.create(type="single")
            #     roomid=createchatroom.id
            #     create_chatmember=ChatMembers.objects.create(chatroom_id=roomid,user_id=senderid)
            #     create_chatmembers=ChatMembers.objects.create(chatroom_id=roomid,user_id=receiverid)
        else:
            # print('create 2')
            createchatroom=Chatroom.objects.create(name="single",type="single")
            roomid=createchatroom.id
            create_chatmember=ChatMembers.objects.create(chatroom_id=roomid,user_id=senderid)
            create_chatmembers=ChatMembers.objects.create(chatroom_id=roomid,user_id=receiverid)
        return JsonResponse({'roomid':roomid})


def creategroupchatting(request):
    
    response = HttpResponse(request)



def userserarching(request):
    # print('hgdhfhg')
    sortvalue=request.GET.get('value')
    # print('sortvalue',sortvalue)
   
    # userlistdata=list(User.objects.filter(company_id=request.company.id,status=1).exclude(id=request.user.id).values('name','id'))
    # grouplist=list(Chatroom.objects.filter(type="group").values_list('id',flat=True))
   
    # print("asdds",userlistdata)
   
    # # receivernames=ChatMembers.objects.filter(chatroom_id=room_name).exclude(user_id=sender).values_list('user_id',flat=True)

    # allgrouplist=[]
    # for i in grouplist:
    #     group=ChatMembers.objects.filter(user_id=request.user.id,chatroom_id=i).first()
    #     if (group != None):
    #         allgrouplist.append({'name':group.chatroom.name,'id':i})
    
    # userlistdata.extend(allgrouplist)
    # print(userlistdata)
    # sortlist=[]
    # # # values = [i['name'] for i in userlistdata]
    # # # print('values',values)
    # print(sortvalue)
    # for sort in userlistdata:
    #     regex=re.compile(sortvalue,re.IGNORECASE)
    #     # print(regex)
          
    #     # searching contains value
    #     # print(sort['name'])
    #     if(regex.search(sort['name']) == None):
    #         print('no value')
            
    #     else:
    #         # print(sort['name'])
    #         sortlist.append(sort)
    #         print('sortlist',sortlist)
    #     # if (sort['name'].startswith(regex)):
    #     #     print('no value')
    #     #     sortlist.append(sort)
            

    # print('sort',sortlist)
    # return JsonResponse({'userlistdata':sortlist})
    current_user= request.user.id
    getlast_msger=Message.objects.filter(user_id=current_user).order_by('-id').values('chatroom_id')
    # print(getlast_msger)

    latest_msg=[]
    for i in getlast_msger:
        # print(i['chatroom_id'] )
        if i['chatroom_id'] not in latest_msg:
            latest_msg.append(i['chatroom_id'])

    # print('latest_msg',latest_msg)
    filterusers=[]
    for j in latest_msg:
        chatroom=Chatroom.objects.filter(id=j).first()
        if( chatroom.type == 'single'):
            stackname=ChatMembers.objects.filter(chatroom_id=j).exclude(user_id=current_user).first()
            # print('stackname',stackname)
            lastname="" if stackname.user.lastname == None else stackname.user.lastname
            filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'lastname':lastname,'type':'single'})  
        else:
            filterusers.append({'id':chatroom.id,'name':chatroom.name,'type':'group'})  
    if (sortvalue != ''):
        regex=re.compile(sortvalue,re.IGNORECASE)
        sortlist=[]
        for val in filterusers:
            if(regex.search(val['name']) != None):
                sortlist.append(val)
        data={'data':sortlist}
    else:
        data={'data':filterusers}
    return JsonResponse(data)




# def root_to_chat(request):
#     print('root_to_chat safsdffsgg')
#     print('sessionsss',request.META.get('HTTP_REFERER'))
#     request.session['backurl'] = request.META.get('HTTP_REFERER')

#     return redirect('chat:message')

def chatnotification(request):
    # print('chatnotification')
    user_id=request.GET.get('id')
    # receiver_id = request.GET.get('receiver_id')
    # 
    getnotify=Notify_chat.objects.filter(read=0,readerstatus=request.user.id)
    # get room id
    # Chatroom.objects.filter(id__in=getnotify.values_list('chatroom_id',flat=True)).values_list('id',flat=True)
    # print(f"Group notifi count {getnotify.count()}")
    getgrpnotify=ChatMembers.objects.filter(user_id=user_id).values('user_id')
    # print('getnotifyy',getgrpnotify)
    # getsendermsg=Notify_chat.objects.filter(receiver_id=user_id,read=0).order_by('-id').values()
    getnotifymsg = Notify_chat.objects.filter(receiver_id=user_id).order_by('-id').values()
    # print(f"Receiver ID {receiver_id}")
    individualnotify=Notify_chat.objects.filter(receiver_id=request.user.id,read=0,roomid=None,readerstatus=None)
    
    # grpnotify=Notify_chat.objects.filter(roomid=chatroom.id,read=0,readerstatus=request.user.id)
    # print(f"Individual notifi count {individualnotify.count()} getnotifymsg {getnotify.count()}")
    data={'count':individualnotify.count()+getnotify.count(),'msgdetails':list(getnotifymsg)}
    # print('data',data)
    return JsonResponse(data)
    # return JsonResponse({'data':data})

def updatenotificaton(request):
    # print('request')
    # print('gfdjghfhgchjghjghjg')
    user_id=request.GET.get('id')
    # print('indexchatread',user_id)
    readed = Notify_chat.objects.filter(receiver_id=user_id).update(read=1)
    # print('readed',readed)
    # getnotifymsg=Notify_chat.objects.filter(receiver_id=user_id).order_by('-id').values()
    # data={'count':getnotify.count(),'msgdetails':list(getnotifymsg)}
    return JsonResponse({'updated':'updated'})


def showlastestmsg(request):
    current_user= request.GET.get('userid')
    # print(current_user)
    # getlast_msger=Message.objects.filter(user_id=current_user).order_by('chatroom_id')
    # getlast_msger=Message.objects.filter(user_id=current_user).order_by('-id').values('chatroom_id')
    # print(getlast_msger)
    
    # latest_msg=[]
    # for i in getlast_msger:
    #     # print(i['chatroom_id'] )
    #     if i['chatroom_id'] not in latest_msg:
    #         latest_msg.append(i['chatroom_id'])
    getlast_msger=Message.objects.order_by('-id').values('chatroom_id')
    
    # print('getlast_msger',getlast_msger)

    latest_msg=[]
    for i in getlast_msger:
        # print('i',i['chatroom_id'])
        both=ChatMembers.objects.filter(chatroom_id=i['chatroom_id']).filter(user_id=current_user).first()
        # print('both',both.chatroom.id)
        if (both != None):
            if both.chatroom.id not in latest_msg:
                latest_msg.append(both.chatroom.id)
        # check=both[i]['chatroom_id']
        # if i['chatroom_id'] not in latest_msg:
        #     latest_msg.append(i['chatroom_id'])


    # print('latest_msg',latest_msg)
    filterusers=[]
    for j in latest_msg:
        chatroom=Chatroom.objects.filter(id=j).first()
        if( chatroom.type == 'single'):
            stackname=ChatMembers.objects.filter(chatroom_id=j).exclude(user_id=current_user).first()
            # print(stackname)
            user_id=request.user.id
            # print('user_id',user_id)
            # getnotify=Notify_chat.objects.filter(receiver_id=user_id,sender_id=stackname.user.id,read=0)
            # print('getnotify',getnotify)
            getnotify=Notify_chat.objects.filter(receiver_id=user_id,sender_id=stackname.user.id,read=0,roomid=None)
            # getnotifymsg=Notify_chat.objects.filter(receiver_id=user_id).order_by('-id').valures()
            # print()
            filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'type':'single','count':getnotify.count()})  
            # filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'type':'single'})  
        else:
            grpnotify=Notify_chat.objects.filter(roomid=chatroom.id,read=0,readerstatus=request.user.id)
            filterusers.append({'id':chatroom.id,'name':chatroom.name,'type':'group','count':grpnotify.count()})  
    #  print('stackname',k['user_id'])

    #         filterusers.append(k['user_id'])

    # print('filterusers',filterusers)
    return JsonResponse({'data':filterusers})




def messageview_status(request):
    # print(request.GET.get('receiver_id'))
    senderid=request.GET.get('receiver_id')
    updatenotify=Notify_chat.objects.filter(sender_id=senderid).update(read=1)
    # print('updatenotify',updatenotify)
    return JsonResponse({'data1':'data2'})




def grp_delete(request):
    # print('delete grp')
    roomid=request.GET.get('id')
    type=request.GET.get('type')
    # print(type)
    # print(roomid)

    Chatroom.objects.filter(id=roomid,type=type).delete()


    return JsonResponse({'data':'data'})



def groupchat_edit(request):
    # print('delete grp')
    grpmembrs=request.GET.get('group_members')
    geteditroomid=request.GET.get('roomid')
    convertreceivers=ast.literal_eval(grpmembrs)
    # convertreceivers = list(map(, convertreceivers))
    # print('convertreceivers',convertreceivers)
    # privousgrouplist=ChatMembers.objects.filter(chatroom_id=geteditroomid).values_list('user_id',flat=True)
    # print('privousgrouplist',privousgrouplist)
    # for inlist in privousgrouplist:
    #     if str(inlist) in convertreceivers:
    #         print('1')
    #     else:
    #         print(2)
    convertreceivers.append(request.user.id)
    new_list=[]
    for i in convertreceivers:
        val=str(i).replace(',','')
        new_list.append(val)
        members=ChatMembers.objects.filter(chatroom_id=geteditroomid,user_id=val).first()
        # print("members",members)
        if (members==None):
            ChatMembers.objects.create(chatroom_id=geteditroomid,user_id=i)
        else:
            ChatMembers.objects.filter(chatroom_id=geteditroomid,user_id=val).update(is_active=True)
    data = ChatMembers.objects.filter(chatroom_id=geteditroomid).exclude(user__id__in=convertreceivers)
    # print(f"chatmembers before delete {data.id}")
    for i in data:
        # print(f"chatmembers id {i.chatroom_id} user_id {i.user_id}")
        # print(f"chatmembers id {i.chatroom_id} user_id {i.user_id}")
    # delete notify chat
        Notify_chat.objects.filter(read=0,receiver_id=i.user_id,roomid=i.chatroom_id).delete()
    data.update(is_active=False)
    #  list(ChatMembers.objects.filter(chatroom_id=1,is_active=True,chatroom__type='group').values_list('user_id',flat=True))
    # delete_members = data.delete()
    return JsonResponse({'data':'data'})





def removeattachementdfile(request):

    
    getattache_id=request.GET.get('id')


    Fileupload.objects.get(id=getattache_id).delete()

    return JsonResponse({'data':'data'})



def groupmessageview_status(request):
    # print(request.GET.get('value'))
    # updatenotify=request.GET.get('value')
    updatenotify=request.GET['value']
    # print(f'updatenotify{updatenotify}')
    notifi=Notify_chat.objects.filter(roomid=updatenotify,readerstatus=request.user.id).update(read=1)
    
    return JsonResponse({'data':'updatedd'})

def update_notify_message(request):
    current_user= request.user.id
    getlast_msger=Message.objects.order_by('-id').values('chatroom_id')
    latest_msg=[]
    for i in getlast_msger:
        both=ChatMembers.objects.filter(chatroom_id=i['chatroom_id']).filter(user_id=current_user).first()
        if (both != None):
            if both.chatroom.id not in latest_msg:
                latest_msg.append(both.chatroom.id)
    filterusers=[]
    for j in latest_msg:
        chatroom=Chatroom.objects.filter(id=j).first()
        if( chatroom.type == 'single'):
            stackname=ChatMembers.objects.filter(chatroom_id=j).exclude(user_id=current_user).first()
            user_id=request.user.id
            getnotify=Notify_chat.objects.filter(receiver_id=user_id,sender_id=stackname.user.id,read=0,roomid=None)
            filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'lastname':stackname.user.lastname,'type':'single','count':getnotify.count()})  
        else:
            grpnotify=Notify_chat.objects.filter(roomid=chatroom.id,read=0,readerstatus=request.user.id)
            filterusers.append({'id':chatroom.id,'name':chatroom.name,'type':'group','count':grpnotify.count()})  
    return JsonResponse({'data':filterusers})

def read_message(request):
    # print('a')
    # return JsonResponse({'read_message':request.GET.get('roomid')})    
    current_roomid = request.GET.get('roomid')

    get_room_type = Chatroom.objects.filter(id=int(current_roomid)).values('type')

    print(f'get_room_type: {get_room_type}')
    
    return JsonResponse({'data':list(get_room_type)})

#######################################################################################################################################
# new controller
#######################################################################################################################################
def baseview(request):
    return render(request,'chat/boilerplate.html')
def recentchat_members(request):
    current_user= request.user.id
    getlast_msger=Message.objects.order_by('-id').values('chatroom_id')
    latest_msg=[]
    for i in getlast_msger:
        both=ChatMembers.objects.filter(chatroom_id=i['chatroom_id']).filter(user_id=current_user).first()
        if (both != None):
            if both.chatroom.id not in latest_msg:
                latest_msg.append(both.chatroom.id)
    filterusers=[]
    for j in latest_msg:
        chatroom=Chatroom.objects.filter(id=j).first()
        if( chatroom.type == 'single'):
            stackname=ChatMembers.objects.filter(chatroom_id=j).exclude(user_id=current_user).first()
            user_id=request.user.id
            getnotify=Notify_chat.objects.filter(receiver_id=user_id,sender_id=stackname.user.id,read=0,roomid=None)
            filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'lastname':stackname.user.lastname,'type':'single','count':getnotify.count()})  
        else:
            grpnotify=Notify_chat.objects.filter(roomid=chatroom.id,read=0,readerstatus=request.user.id)
            filterusers.append({'id':chatroom.id,'name':chatroom.name,'type':'group','count':grpnotify.count()})
    return JsonResponse({'data':filterusers})
def recent_chat(request):
    current_user = request.user.id
    # get_recent_chat = Chatroom.objects.filter(Q(chatmembers__user_id=current_user) | Q(chatmembers__user_id=current_user)).distinct()
    # get_recent_chat = get_recent_chat.order_by('-id').values('id','name','type')
    # return JsonResponse({'data':list(get_recent_chat)})
    getlast_msger=Message.objects.order_by('-id').values('chatroom_id')
    latest_msg=[]
    for i in getlast_msger:
        both=ChatMembers.objects.filter(chatroom_id=i['chatroom_id']).filter(user_id=current_user).first()
        if (both != None):
            if both.chatroom.id not in latest_msg:
                latest_msg.append(both.chatroom.id)
    filterusers=[]
    for j in latest_msg:
        chatroom=Chatroom.objects.filter(id=j).first()
        if( chatroom.type == 'single'):
            stackname=ChatMembers.objects.filter(chatroom_id=j).exclude(user_id=current_user).first()
            user_id=request.user.id
            getnotify=Notify_chat.objects.filter(receiver_id=user_id,sender_id=stackname.user.id,read=0,roomid=None)
            filterusers.append({'id':stackname.user.id,'name':stackname.user.name,'lastname':stackname.user.lastname,'type':'single','count':getnotify.count()})  
        else:
            grpnotify=Notify_chat.objects.filter(roomid=chatroom.id,read=0,readerstatus=request.user.id)
            filterusers.append({'id':chatroom.id,'name':chatroom.name,'type':'group','count':grpnotify.count()})
    return JsonResponse({'data':filterusers})
    
def get_chatmessages_by_room(request):
    current_room_id = request.GET.get('room_id')
    typeofroom = request.GET.get('type')
    # print(f'current_room_id from Middleware: {current_room_id}')
    user_id = request.user.id
    start = request.GET.get('start', None)
    rowperpage = request.GET.get('rowperpage', None)
    # print(f'start: {start} rowperpage: {rowperpage}')
    all_messages=[]
    # get room type
    if typeofroom == 'single':
        # print('single')
        current_room_id = userid_to_roomid(user_id,current_room_id,request.company.id)
        # print(f'current_room_id from Method: {current_room_id}')
    room_type = Chatroom.objects.filter(id=current_room_id).first().type
    # print(f'room_type: {room_type}')
    total_messages = Message.objects.filter(chatroom_id=int(current_room_id)).count()
    # print(f'total_messages: {total_messages}')
    if start is None and rowperpage is None:
        # print('a')
        if room_type == 'group':
            group_owner_id = ChatMembers.objects.filter(chatroom_id=int(current_room_id),user=request.user.id).values('group_owner','id').first()
            if (group_owner_id['group_owner'] is True):
                group_owner = True
            else:
                group_owner = False
            # print(f'group_owner: {group_owner}')
            get_joined_date = ChatMembers.objects.filter(chatroom_id=current_room_id,user_id=user_id,user_id__status=1).first()
            is_active = get_joined_date.is_active
            joined_date = get_joined_date.date_joined
            # get messages greater than joined date
            get_chat_messagesids = Message.objects.filter(chatroom_id=current_room_id,date_created__gte=joined_date,chat_member_ids__contains=group_owner_id['id']).order_by('-id','date_created')[:10]
        else:
            group_owner = False
            is_active = True
            get_chat_messagesids=Message.objects.filter(chatroom_id=current_room_id).order_by('-id')[:10]
        for i in get_chat_messagesids:
            user_data=User.objects.filter(id=i.user_id).first()
            # get file name
            get_file=i.file
            convert_array=ast.literal_eval(get_file)
            # print(f'convert_array: {convert_array}')    
            slist = list(filter(None, convert_array))
            file_data = Fileupload.objects.filter(id__in=slist).values('id','document')
            all_messages.append({'id':user_data.id,'name':user_data.name,'lastname':user_data.lastname,'chat':i.chats,'created_at':i.timestamp,'file_data':list(file_data),'role_id':user_data.roles_id}) 
        # print(f'abs: {list(all_messages)}')   
        receivernames = ChatMembers.objects.filter(chatroom_id=int(current_room_id),is_active=True).exclude(user_id=user_id).values_list('user_id',flat=True)
        chat_memberid = list(ChatMembers.objects.filter(chatroom_id=current_room_id,is_active=True,chatroom__type='group').values_list('id',flat=True))
        # print(f'chat_memberid {chat_memberid}')    
        showusername = [{**change,'designation_role': (ContractMasterVendor.objects.filter(vin=change['cin_number']).values_list('vendor_name', flat=True).first() if change['roles_id'] == 4 else 'Client Administrator')} if change['roles_id'] in [2, 4] else change for change in list(User.objects.filter(id__in=receivernames).values('id', 'name', 'lastname', 'designation_role', 'roles_id', 'cin_number'))]
        getgrpname = Chatroom.objects.filter(id=int(current_room_id)).values('name','type').first()
    else:
        group_owner = False
        is_active = False
        # print(f'start: {start} rowperpage: {rowperpage}')
        if room_type == 'group':
            get_joined_date = ChatMembers.objects.filter(chatroom_id=current_room_id,user_id=user_id).first()
            joined_date = get_joined_date.date_joined
            get_chat_messagesids = Message.objects.filter(chatroom_id=current_room_id,date_created__gte=joined_date,chat_member_ids__contains=get_joined_date.id).order_by('-id','date_created')[int(start):int(start)+int(rowperpage)]
        else:
            get_chat_messagesids=Message.objects.filter(chatroom_id=current_room_id).order_by('-id')[int(start):int(start)+int(rowperpage)]
        for i in get_chat_messagesids:
            user_data=User.objects.filter(id=i.user_id).first()
            # get file name
            get_file=i.file
            convert_array=ast.literal_eval(get_file)
            # print(f'convert_array: {convert_array}')    
            slist = list(filter(None, convert_array))
            file_data = Fileupload.objects.filter(id__in=slist).values('id','document')
            all_messages.append({'id':user_data.id,'name':user_data.name,'lastname':user_data.lastname,'chat':i.chats,'created_at':i.timestamp,'file_data':list(file_data)}) 
        # print(f'abs: {list(all_messages)}')      
        showusername = []
        getgrpname = []
        chat_memberid = []
    return JsonResponse({'user_id':user_id,'total_messages':total_messages,'showusername':showusername,'getgrpname':getgrpname,'data':all_messages,'room_type':room_type,'current_room_id':current_room_id,'group_owner':group_owner,'is_active':is_active,'chat_memberid':chat_memberid}) 

def get_chatmessages_by_room_pagination(request):
    current_room_id = request.GET.get('room_id')
    # print(f'current_room_id: {current_room_id}')
    user_id = request.user.id
    # pagination of data 10 records per page
    page = request.GET.get('page', 1)
    paginator = Paginator(Message.objects.filter(chatroom_id=current_room_id).order_by('-id').values(), 10)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    # get all messages with pagination
    get_chat_messages=list(messages)
    # print(f'get_chat_messages: {get_chat_messages}')
    return JsonResponse({'data':list(get_chat_messages),'user_id':user_id})

def get_group_members(request):
    current_room_id = request.GET.get('room_id')
    receivernames = list(ChatMembers.objects.filter(chatroom_id=int(current_room_id),is_active=True,user_id__status=1).values_list('user_id',flat=True))
    user_id=request.user.id
    receivernames.remove(user_id)
    showusername = list(User.objects.filter(id__in=receivernames).values('id','name','lastname','status','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary'))
    # get all active users exluding group members
    receivernames.append(user_id)
    for data in User.objects.filter(status=1,company_id=request.company.id).exclude(id__in=receivernames).values('id','name','lastname','status','roles_id','cin_number','designation_role','contactpersonstatus','is_primary','is_secondary'):
        data['status']=0
        showusername.append(data)
    # showusername.append(list(User.objects.filter(status=1,company_id=request.company.id).exclude(id__in=receivernames).values('id','name','lastname','status')))
    # print(f'showusername12345: {showusername}')
    showusername = [i for i in showusername if not (i['roles_id'] == 4 and i['name'] == '')]
    for i in showusername:
        if i['roles_id'] == 4:
            i['designation_role'] = ContractMasterVendor.objects.filter(vin=i['cin_number']).first().vendor_name
            if i['contactpersonstatus'] == 1 and i['is_primary'] == 1:
                i['vendor_role'] = 'Contact Person/Primary Personnel'
            elif i['contactpersonstatus'] == 1 and i['is_secondary'] == 1:
                i['vendor_role'] = 'Contact Person/Secondary Personnel'
            elif i['is_primary'] == 1:
                i['vendor_role'] = 'Primary Personnel'
            elif i['is_secondary'] == 1:
                i['vendor_role'] = 'Secondary Personnel'
            elif i['contactpersonstatus'] == 1:
                i['vendor_role'] = 'Contact Person'
    return JsonResponse({'data':list(showusername)})

def get_chatroom_by_recent_chat(request):
    user_id = request.user.id
    # get all recent chat
    get_recent_chat = Chatroom.objects.filter(Q(user_id=user_id) | Q(chatmembers__user_id=user_id)).distinct().values('id','name','type','created_at','user_id')
    # print(f'get_recent_chat: {get_recent_chat}')
    return JsonResponse({'data':list(get_recent_chat)})

# if chat is single user id to room id
def userid_to_roomid(senderid,receiverid,company_id):
    q=list(ChatMembers.objects.values('chatroom_id').filter(Q(user_id=senderid) | Q(user_id=receiverid)).annotate(total=Count('chatroom_id')).filter(total=2))
    datalist=[x['chatroom_id'] for x in q]
    singlelist=Chatroom.objects.filter(id__in=datalist,type='single').values_list('id',flat=True)
    if (len(singlelist) > 0):            
        roomid=singlelist[0]
    else:
        createchatroom=Chatroom.objects.create(name="single",type="single",company_id=company_id)
        roomid=createchatroom.id
        print(f'senderid: {senderid} receiverid: {receiverid}')
        ChatMembers.objects.create(chatroom_id=roomid,user_id=senderid)
        ChatMembers.objects.create(chatroom_id=roomid,user_id=receiverid)
    return roomid

def get_grouplist(request):
    grouplist=list(Chatroom.objects.filter(type="group").values_list('id',flat=True))
    allgrouplist=[]
    for i in grouplist:
        group=ChatMembers.objects.filter(user_id=request.user.id,chatroom_id=i).first()
        if (group != None):
            allgrouplist.append({'name':group.chatroom.name,'id':i,'type':group.chatroom.type,'is_active':group.is_active})
    # print(f'allgrouplist: {allgrouplist}')
    return JsonResponse({'data':allgrouplist})

def get_username(request):
    current_room_id = request.GET.get('room_id')
    sender_id = request.GET.get('sender_id')
    room_type = Chatroom.objects.filter(id=current_room_id).first().type
    user_name = list(User.objects.filter(id=sender_id).values('name','lastname'))
    # print(f'method: get_username user_name: {user_name} room_type: {room_type}')
    return JsonResponse({'data':user_name,'room_type':room_type})

def create_message(msgs,json_dumps,uid,sender,roomid,time_stamp,group_chatmember):
    # chat_memberid = list(ChatMembers.objects.filter(chatroom_id=roomid,is_active=True,chatroom__type='group').values_list('id',flat=True))
    msg=Message.objects.create(chats=msgs,file=json_dumps,uid=uid,user_id=sender,chatroom_id=roomid,timestamp=time_stamp,chat_member_ids=group_chatmember)
    return msg