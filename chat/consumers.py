import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import CustomUser as User
from .models import Chat
from django.contrib.auth.models import User as RealUser
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness, AcceptanceCalculator, LikenessCalculator
import time
import threading

class ChatSearchConsumer(WebsocketConsumer):
    def connect(self):
        # print("Hi")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Delete room from db
        # chats = Chat.objects.filter(id=self.room_name).delete()
        print("Deleting custom user " + self.room_name)
        user = User.objects.get(pk=int(self.room_name))
        if (user.user == None):
            print("Deleted")
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
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def find_room(self, user_id):
        print("Start search for user " + str(user_id))
        user = User.objects.get(pk=int(user_id))
        user.status = 'Searching'
        user.save()
        print (user.name + "Start waiting for ")
        for i in range (0,10):
            print(i)
            time.sleep(1)
            if User.objects.get(pk=user.pk).status == 'Invited':
                print ("User " + user.name + " is invited to " + str(User.objects.get(pk=user.pk).room_to_join))
                self.send(text_data=json.dumps({
                    'type': 'chat_message',
                    'message': User.objects.get(pk=user.pk).room_to_join,
                    'name': 'name'
                }))
                return 1
            if User.objects.get(pk=user.pk).status == 'Stopped':
                return 1

        while User.objects.get(pk=user.pk).status == 'Searching':
            print(user.name + "Start searching")
            searching_users = User.objects.filter(status="Searching")
            best_user = None
            best_score = 0
            for target_user in searching_users:
                main_accepts_target = AcceptanceCalculator(main_user=user, target_user=target_user)
                target_accepts_main = AcceptanceCalculator(main_user=target_user, target_user=user)
                users_new_match = main_accepts_target.users_match() and target_accepts_main.users_match()
                print("Listen!")
                print(main_accepts_target.users_match())
                print(target_accepts_main.users_match())
                users_old_match = calcAcceptance(mainUser=user, targetUser=target_user) == 1 and calcAcceptance(mainUser=target_user, targetUser=user) == 1
                if (users_new_match and user.id != target_user.id and target_user not in user.ignored_users.all() and target_user not in user.usersIgnoredBy.all()):
                    l1 = calcLikeness(mainUser=user, targetUser=target_user)
                    l2 = calcLikeness(mainUser=target_user, targetUser=user)
                    result = (l1+l2)/2
                    if result>best_score:
                        best_score = result
                        best_user = target_user.pk
                if User.objects.get(pk=user.pk).status == 'Invited':
                    print ("User " + user.name + " is invited to " + str(User.objects.get(pk=user.pk).room_to_join))
                    self.send(text_data=json.dumps({
                        'type': 'chat_message',
                        'message': User.objects.get(pk=user.pk).room_to_join,
                        'name': 'name'
                    }))
                    return 1
                if User.objects.get(pk=user.pk).status == 'Stopped':
                    return 1
            print("Finish searching")
            if best_score > 0 and User.objects.get(pk=best_user).status == "Searching":
                print("Getting to the room")
                chat = Chat()
                chat.save()
                User.objects.get(pk=best_user).room_to_join = chat.id
                User.objects.get(pk=best_user).status = "Invited"
                for_sure = User.objects.get(pk=best_user)
                for_sure.room_to_join = chat.id
                for_sure.status = "Invited"
                for_sure.save()
                myself = User.objects.get(pk=user.pk)
                myself.status="Inactive"
                myself.save()
                User.objects.get(pk=user.pk).status = "Inactive"
                print ("User " + str(user.name) + " created chat " + str(chat.id))
                self.send(text_data=json.dumps({
                    'type': 'chat_message',
                    'message': chat.id,
                    'name': 'name'
                }))
                return 1

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']

        t = threading.Thread(target=self.find_room,args=[self.room_name])
        t.setDaemon(True)
        t.start()

        self.threadToStop = t

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'name': name
        }))

    def exit_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'exit_message'
        }))



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # print("Hi")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        # for i in range(0,5):
        #     time.sleep(1)
        # self.send(text_data=json.dumps({
        #     'type': 'chat_message',
        #     'message': 'You are connected hmm',
        #     'name': 'name'
        # }))

    def disconnect(self, close_code):
        # Delete room from db
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
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
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
            )        # Send message to room group

    def chat_message(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'name': name
        }))

    def exit_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'exit_message'
        }))