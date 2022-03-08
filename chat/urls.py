from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()                   
router.register(r'users', views.UserView, 'user')
router.register(r'chats', views.ChatView, 'chat')

app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /chat/5/
    # path('<int:chat_id>/', views.chat_room, name='chat_room'),
    # path('start_search/', views.startSearching, name='start_search'),
    # path('check_search/', views.checkRoom, name='check_search'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_real_user/', views.create_real_user, name='create_real_user'),
    path('validate_user/', views.validate_user_does_not_exists, name='validate_user'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('get_user_chats/', views.get_user_chats, name='get_user_chats'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/', include(router.urls)),
]
