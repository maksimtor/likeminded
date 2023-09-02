import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import CustomUser as User
from .models import Chat
from chat.tools.searchAlgorithm import waiting_for_invite, search_to_invite
from django.contrib.auth.models import User as RealUser
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness, AcceptanceCalculator, LikenessCalculator
import time
import threading

class ChatSearchConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        user = User.objects.get(pk=int(self.room_name))
        if (user.user == None):
            user.delete()
        else:
            user.status='Stopped'
            user.save()
        self.send(text_data=json.dumps({
            'message': '',
            'name': '',
            'type': 'exit'
        }))
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'exit_message'
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def find_room(self, user_id):
        print("Start search for user " + str(user_id))
        user = User.objects.filter(pk=int(user_id)).prefetch_related('ignored_users').prefetch_related('usersIgnoredBy').get()
        user.status = 'Searching'
        user.save()
        print (user.name + " starts waiting for invite")
        waiting_for_invite(self, user, 10)
        print (user.name + " starts searching users")
        search_to_invite(self, user)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']

        t = threading.Thread(target=self.find_room,args=[self.room_name])
        t.setDaemon(True)
        t.start()

        self.threadToStop = t

    def chat_message(self, event):
        message = event['message']
        name = event['name']

        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'name': name
        }))

    def exit_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'exit_message'
        }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        chats = Chat.objects.filter(id=self.room_name).delete()
        self.send(text_data=json.dumps({
            'message': '',
            'name': '',
            'type': 'exit'
        }))
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'exit_message'
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']

        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name
                }
            )

    def chat_message(self, event):
        message = event['message']
        name = event['name']

        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'name': name
        }))

    def exit_message(self, event):
        self.send(text_data=json.dumps({
            'type': 'exit_message'
        }))