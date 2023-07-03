from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()                   
router.register(r'users', views.UserView, 'user')

app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /chat/5/
    # path('<int:chat_id>/', views.chat_room, name='chat_room'),
    # path('start_search/', views.startSearching, name='start_search'),
    # path('check_search/', views.checkRoom, name='check_search'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_real_user/', views.create_real_user, name='create_real_user'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),
    path('validate_user/', views.validate_user_does_not_exists, name='validate_user'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('ignore_user/', views.ignore_user, name = 'ignore_user'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('upload_profile_photo/', views.upload_profile_photo, name='upload_profile_photo'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/', include(router.urls)),
]