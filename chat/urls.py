from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()                   
router.register(r'users', views.UserViewSet, 'user')

app_name = 'chat'
urlpatterns = [
    path('api/', include(router.urls)),
]