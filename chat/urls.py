from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()                   
#router.register(r'users', views.UserView, 'user')

app_name = 'chat'
urlpatterns = [
    path('create_user/', views.UserView.as_view(), name='create_user'),
    path('create_real_user/', views.UserView.as_view(), name='create_real_user'),
    path('validate_user/', views.ValidateUserRegistration.as_view(), name='validate_user'),
    path('validate_login/', views.ValidateLogin.as_view(), name='validate_login'),
    path('get_user_profile/<int:user_id>/', views.UserView.as_view(), name='get_user_profile'),
    path('ignore_user/', views.IgnoreUser.as_view(), name = 'ignore_user'),
    path('update_profile/', views.UserView.as_view(), name='update_profile'),
    path('upload_profile_photo/', views.ProfilePhoto.as_view(), name='upload_profile_photo'),
    path('api/', include(router.urls)),
]