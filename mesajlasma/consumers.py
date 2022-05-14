import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.dispatch import receiver

from profil.models import Kullanici

from .models import Mesaj,MesajKanali
from django.contrib.auth.models import User
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'mesajlar_%s' %self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
         )
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']
        receiver_user = data['receiver_user']

        await self.save_message(user,self.room_group_name,message,receiver_user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {  
                'type':'chat_message',
                'message':message,
                'user':user,
                'receiver_user':receiver_user

             }
        )
    async def chat_message(self,event):
        message = event['message']
        user = event['user']
        receiver_user = event['receiver_user']

        await self.send(text_data = json.dumps({
            'message':message,
            'user':user,
            'receiver_user':receiver_user
        }))
    
    @sync_to_async
    def save_message(self,user,room,message,receiver_user):
        sender_user = User.objects.get(username=user)
        sender_user = Kullanici.objects.get(user = sender_user.id)
        receiver_user = User.objects.get(username = receiver_user)
        receiver_user = Kullanici.objects.get(user = receiver_user.id)
        mesaj_kanali = Mesaj.objects.filter(room = room)
        if mesaj_kanali.exists():
            mesajkanali= None          
        else:
           mesajkanali =  MesajKanali.objects.create(sender_user=sender_user,room=room,receiver_user = receiver_user)
        Mesaj.objects.create(sender_user=sender_user,room=room,mesaj=message,receiver_user = receiver_user)

        
