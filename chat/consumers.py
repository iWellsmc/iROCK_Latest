import json
# from trace import Trace
# from urllib import request

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.views import message, room

from .models import Chatroom, Message
from custom_auth.models import *

# from django.http import JsonResponse
# from asgiref.sync import async_to_sync, sync_to_async

from.views import create_message
# from django.db.models import Q

# from notifications.signals import notify

from chat.models import *
# import calendar
# import time

import datetime
import pytz

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self,roomid,msgs,pk_id,files,sender,uid,group_chatmember):
        print(f'consumer chat {group_chatmember}')
        # self.user = self.scope['user']
        if (Message.objects.filter(user=sender,uid=uid).exists()):
            # print('record already exits')
            msg=Message.objects.filter(user=sender,uid=uid).first()
        else:
            splitval=pk_id.split(',')
            json_dumps=json.dumps(splitval)
            # current_GMT = time.gmtime()
            # print('current_GMT',current_GMT)
            # time_stamp = calendar.timegm(current_GMT)
            # print("Current timestamp:", time_stamp)
            utc_timezone = pytz.utc
            utc_time = datetime.datetime.now(utc_timezone)
            # print(utc_time.strftime('%Y-%m-%d %H:%M:%S'))
            time_stamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
            msg = create_message(msgs,json_dumps,uid,sender,roomid,time_stamp,group_chatmember)
            receiverid=ChatMembers.objects.filter(chatroom_id=roomid).exclude(user_id=sender).values_list('user_id',flat=True).last()
            # print('receiverid',receiverid)
            recivername=User.objects.filter(id=receiverid).values('name').last()
            receivername=recivername['name']
            sendername=User.objects.filter(id=sender).values('name').last()
            sendername=sendername['name']
            # print('roomid-for check',roomid)
            receivr_id=receiverid
           
            read=0
            unread=0
            verb_msg='new message'+sendername
            checktype=Chatroom.objects.filter(id=roomid).first()
            # print('checktype',checktype.type)
            if(checktype.type == 'single'):
                notifi=Notify_chat.objects.create(sender_id=sender, receiver_id=receivr_id,sender_name=sendername,receiver_name=receivername,read=read,unread=unread,verb=verb_msg,discription=msgs)
                # print('notifi',notifi)
                # print('record created')
            else:
                # print('elseelse',roomid)
                get_gropu_members = ChatMembers.objects.filter(chatroom=roomid,is_active=True).values('user_id')
                # print(f"ORM DATA {get_gropu_members}")
                for i in get_gropu_members:
                    # if(i != sender):
                    #     notifi=Notify_chat.objects.create(sender_id=sender, receiver_id=i,sender_name=sendername,receiver_name=receivername,read=read,unread=unread,verb=verb_msg,discription=msgs)
                    #     print('notifi',notifi)
                    #     print('record created')
                    # print(f"{i['user_id']}")
                    # print(type(i['user_id']))
                    if int(sender) != int(i['user_id']):
                        notifi=Notify_chat.objects.create(sender_id=sender, receiver_id=receivr_id,sender_name=sendername,receiver_name=receivername,read=read,unread=unread,verb=verb_msg,discription=msgs,roomid=roomid,readerstatus=i['user_id'])
                        # print('notifi-grp created',notifi)
                # print('record created grp')

            
        return msg

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        # print('receiver-workig')
        # print('text',text_data)
        self.user = self.scope['user']
        currentuser=self.user
        # print('reciver',currentuser.id)
        text_data_json = json.loads(text_data)
        # print('abc',text_data_json)
        message = text_data_json['message']
        files=text_data_json['file']
        pk_id=text_data_json['ids']
        sender=text_data_json['sender']
        uid=text_data_json['uid']
        roomid=text_data_json['roomid']
        group_chatmember = text_data_json['group_chatmember']
        await self.channel_layer.group_send(self.room_group_name,{
            'type': 'chat_message',
            'message': message,
            'files' : files,
            'ids':pk_id,
            'currentuser':currentuser.id,
            'sender':sender,
            'uid':uid,
            'roomid':roomid,
            'q':'1',
            'group_chatmember':group_chatmember

  })
   
    
   
    async def chat_message(self, event):
        # print('testing')
        # print('eve',event)
       
        message = event['message']
        file=event['files']
        pk_id=event['ids']

        sender=event['sender']
        uid=event['uid']
        
        roomid=event['roomid']
        group_chatmember = event['group_chatmember']
        # print('jai hind',event)
        # print('jai hind1',roomid)

        if (file == None):
            file=''
        else:
            file=file
        if (pk_id == None):
            pk_id = ''
        else:
            pk_id = pk_id
        # print('filesa',file)

        

        getmsg=await self.create_chat(roomid,message,pk_id,file,sender,uid,group_chatmember)
        
        await self.send(text_data=json.dumps({
        'type': 'websocket.send',
            'message': message,
            'file' : file,
            'ids':pk_id,
            'sender': sender,
            'uid':uid,
            'msguserid':getmsg.user_id,
            'roomid':roomid,
            'group_chatmember':group_chatmember
        }))