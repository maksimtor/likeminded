import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, SearchingInstance, CustomUser as User, ChatRoom, Message
from django.contrib.auth.models import User as RealUser
from chat.tools.prefAlgorithm import calcAcceptance, calcLikeness
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
                if (calcAcceptance(mainUser=user, targetUser=target_user) == 1 and calcAcceptance(mainUser=target_user, targetUser=user) == 1 and user.id != target_user.id and target_user not in user.friends.all() and target_user not in user.ignoredUsers.all() and target_user not in user.usersIgnoredBy.all()):
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

        if (text_data_json['type'] == 'possible_unblind'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'possible_unblind',
                    'message': message,
                    'name': name
                }
            )

        elif (text_data_json['type'] == 'unblind_request'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'unblind_request',
                    'message': message,
                    'name': name
                }
            )

        elif (text_data_json['type'] == 'approve_request'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'approve_request',
                    'message': message,
                    'name': name
                }
            )

        else :
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name
                }
            )
        # Send message to room group

    # Receive message from room group
    def possible_unblind(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'possible_unblind',
            'message': message,
            'name': name
        }))

    def approve_request(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'approve_request',
            'message': message,
            'name': name
        }))

    def unblind_request(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'unblind_request',
            'message': message,
            'name': name
        }))
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


class FriendChatConsumer(WebsocketConsumer):
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
        chats = Chat.objects.filter(id=self.room_name).delete()
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        m_type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']

        if (m_type == 'open_chat'):
            chat_room = ChatRoom.objects.get(id=self.room_name)
            messages = chat_room.messages.order_by('timestamp').all()[:10]
            for message in messages:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'restore_chat',
                        'message': message.message,
                        'name': message.user.username,
                        'read': message.read,
                        'idd': message.user.profile.id,
                    }
                )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_restored'
                }
        )
        elif (m_type == 'messages_read'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'messages_read',
                    'message': message,
                    'name': name
                }
            )
        else:
            # save message
            chat_room = ChatRoom.objects.get(id=self.room_name)
            chat_message = Message.objects.create(message=message, user=User.objects.get(id=name).user)
            chat_room.messages.add(chat_message)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name': name
                }
            )

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
    def restore_chat(self, event):
        message = event['message']
        name = event['name']
        read = event['read']
        idd = event['idd']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'restore_chat',
            'message': message,
            'name': name,
            'read': read,
            'id': idd,
        }))

    def messages_read(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'messages_read',
            'message': message,
            'name': name
        }))
    def exit_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'exit_message'
        }))
    def chat_restored(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_restored'
        }))
