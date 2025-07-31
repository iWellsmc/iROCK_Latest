

# Create your models here.
from unittest.util import _MAX_LENGTH
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
class Fileupload(models.Model):
    id= models.AutoField(primary_key=True)
    chats=models.CharField(max_length=255,blank=True ,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    senderr=models.CharField(max_length=255,blank=True ,null=True)
    document = models.FileField(upload_to='documents',blank=True ,null=True)

class Chatroom(models.Model):
    id= models.AutoField(primary_key=True)
    type=models.CharField(max_length=255,blank=True ,null=True)
    name=models.CharField(max_length=255,blank=True ,null=True)
    company_id=models.IntegerField(blank=True ,null=True)

class ChatMembers(models.Model):
    id= models.AutoField(primary_key=True)
    chatroom=models.ForeignKey('chat.Chatroom',on_delete=models.CASCADE,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    # date_joined=models.DateTimeField(auto_now_add=True)
    group_owner=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

class Message(models.Model):
    id= models.AutoField(primary_key=True)
    chats=models.TextField(blank=True,null=True)
    timestamp = models.CharField(max_length=255)
    chatroom=models.ForeignKey('chat.Chatroom',on_delete=models.CASCADE,blank=True, null=True)
    file = models.CharField(max_length=455,blank=True, null=True)
    user=models.ForeignKey("custom_auth.User",on_delete=models.CASCADE,blank=True, null=True)
    uid=models.CharField(max_length=455,blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    chat_member_ids = models.CharField(max_length=100,blank=True,null=True)

class Notify_chat(models.Model):
    id=id= models.AutoField(primary_key=True)
    sender_id=models.IntegerField(blank=True)
    receiver_id=models.IntegerField(blank=True)
    sender_name=models.CharField(max_length=255,blank=True ,null=True)
    receiver_name=models.CharField(max_length=255,blank=True ,null=True)
    read=models.IntegerField(blank=True,null=True)
    unread=models.IntegerField(blank=True,null=True)
    verb=models.CharField(max_length=255,blank=True ,null=True)
    discription=models.TextField(blank=True,null=True)
    roomid=models.IntegerField(blank=True,null=True)
    readerstatus = models.CharField(max_length=255, blank=True, null=True)
