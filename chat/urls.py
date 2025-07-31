# chat/urls.py
from django.urls import path
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views 

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('file_upload_ajax', views.file_upload_ajax, name='file_upload_ajax'),
    path('download/<int:fileid>', views.download, name='download'), 
    path('message', views.message, name='message'), 
    path('createroom', views.createroom, name='createroom'), 
    path('userserarching', views.userserarching, name='userserarching'), 
    path('chatnotification', views.chatnotification, name='chatnotification'), 
    path('showlastestmsg', views.showlastestmsg, name='showlastestmsg'), 
    path('messageview_status', views.messageview_status, name='messageview_status'), 
    # path('indexchatread', views.indexchatread, name='indexchatread'), 
    path('updatenotificaton', views.updatenotificaton, name='updatenotificaton'), 
    path('grp_delete', views.grp_delete, name='grp_delete'), 
    path('groupchat_edit', views.groupchat_edit, name='groupchat_edit'), 
    path('removeattachementdfile', views.removeattachementdfile, name='removeattachementdfile'), 
    path('groupmessageview_status', views.groupmessageview_status, name='groupmessageview_status'), 
    path('update_notify', views.update_notify_message, name='update_notify'),
    path('read_message', views.read_message, name='read_message'),
#####################################################################################
    path('base', views.baseview, name='baseview'),
    path('recentchat_members', views.recentchat_members, name='recentchat_members'),
    path('recent_chat', views.recent_chat, name='recent_chat'), 
    path('get_chatmessages_by_room_id', views.get_chatmessages_by_room, name='get_chatmessages_by_room'),
    path('get_chatmessages_by_room_pagination', views.get_chatmessages_by_room_pagination, name='get_chatmessages_by_room_pagination'),
    path('get_group_members', views.get_group_members, name='get_group_members'),
    path('get_grouplist', views.get_grouplist, name='get_grouplist'),
    path('get_username', views.get_username, name='get_username'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)